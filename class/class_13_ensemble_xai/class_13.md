---
title: "Class 13"
subtitle: "Ensemble Detection and Explainable AI"
author: "Constantine Macris"
date: "2026"
titlepage: true
titlepage-color: "1E3A5F"
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "FFFFFF"
titlepage-rule-height: 2
book: true
classoption: oneside
code-block-font-size: \scriptsize
description: |
    Combining detection methods and making decisions interpretable
---

# Class 13 -- Ensemble Detection and Explainable AI

## Learning Outcomes

- Combine multiple detection methods into ensemble systems
- Implement voting and weighted combination strategies
- Apply explainable AI techniques to maritime IDS
- Generate human-interpretable alert explanations
- Evaluate ensemble system performance

## Definitions

- **Ensemble** -- Combination of multiple models/methods
- **Voting** -- Decision based on majority agreement
- **Stacking** -- Using model outputs as inputs to meta-model
- **XAI** -- Explainable Artificial Intelligence
- **SHAP** -- SHapley Additive exPlanations
- **LIME** -- Local Interpretable Model-agnostic Explanations

## Reading Assignment

- Literature Review: Section 4.3 (Ensemble Methods)
- Literature Review: Section 7 (Interpretability)
- Survey papers on XAI for security applications

## Why Ensemble Detection?

### No Single Perfect Detector

| Method | Catches | Misses |
|--------|---------|--------|
| Frequency | Rate anomalies | Content changes |
| Entropy | Distribution shifts | Rate-matched attacks |
| ML (SVM) | Boundary violations | Novel patterns |
| LSTM | Sequence anomalies | Single-message attacks |
| Fingerprint | Impersonation | Legitimate new devices |

### Ensemble Benefits

1. **Complementary strengths**: Cover each other's weaknesses
2. **Reduced false positives**: Multiple confirmation required
3. **Reduced false negatives**: Multiple detection chances
4. **Robustness**: Harder for attacker to evade all methods
5. **Confidence**: Agreement increases trust in alerts

<!--
Instructor Notes:

Key principle: Defense in depth

Just as we layer physical security:
- Locks + alarms + cameras + guards

We layer detection methods:
- Frequency + entropy + ML + fingerprinting

An attack must evade ALL layers to succeed undetected.
-->

## Ensemble Architectures

### Voting Ensemble

Simple majority or unanimous voting:

```python
class VotingEnsemble:
    def __init__(self, detectors, strategy='majority'):
        """
        Voting-based ensemble detector

        Args:
            detectors: List of detector instances
            strategy: 'majority', 'unanimous', or 'any'
        """
        self.detectors = detectors
        self.strategy = strategy

    def predict(self, features, can_id, timestamp):
        """
        Get ensemble prediction

        Returns:
            is_anomaly: Ensemble decision
            votes: Individual detector votes
            details: Detection details from each
        """
        votes = []
        details = []

        for detector in self.detectors:
            try:
                is_anomaly, detail = detector.predict(features, can_id, timestamp)
                votes.append(1 if is_anomaly else 0)
                details.append({
                    'detector': detector.__class__.__name__,
                    'vote': is_anomaly,
                    'detail': detail
                })
            except Exception as e:
                # Handle detector failures gracefully
                votes.append(0)
                details.append({
                    'detector': detector.__class__.__name__,
                    'vote': None,
                    'error': str(e)
                })

        # Apply strategy
        if self.strategy == 'majority':
            is_anomaly = sum(votes) > len(votes) / 2
        elif self.strategy == 'unanimous':
            is_anomaly = all(v == 1 for v in votes)
        elif self.strategy == 'any':
            is_anomaly = any(v == 1 for v in votes)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

        return is_anomaly, votes, details

    def get_confidence(self, votes):
        """Calculate confidence from vote distribution"""
        agreement = max(sum(votes), len(votes) - sum(votes))
        return agreement / len(votes)
```

### Weighted Voting

Weight detectors by their historical accuracy:

```python
class WeightedEnsemble:
    def __init__(self, detectors, weights=None):
        """
        Weighted voting ensemble

        Args:
            detectors: List of detector instances
            weights: List of weights (default: equal weights)
        """
        self.detectors = detectors
        if weights is None:
            weights = [1.0 / len(detectors)] * len(detectors)
        self.weights = np.array(weights)
        self.weights = self.weights / self.weights.sum()  # Normalize

    def predict(self, features, can_id, timestamp, threshold=0.5):
        """
        Get weighted ensemble prediction

        Returns:
            is_anomaly: True if weighted score > threshold
            score: Weighted anomaly score [0, 1]
            contributions: Per-detector contribution
        """
        scores = []
        contributions = []

        for i, detector in enumerate(self.detectors):
            is_anomaly, detail = detector.predict(features, can_id, timestamp)
            score = 1.0 if is_anomaly else 0.0

            # Some detectors provide continuous scores
            if detail and 'score' in detail:
                score = detail['score']

            scores.append(score)
            contributions.append({
                'detector': detector.__class__.__name__,
                'raw_score': score,
                'weight': self.weights[i],
                'contribution': score * self.weights[i]
            })

        # Weighted combination
        ensemble_score = np.dot(scores, self.weights)
        is_anomaly = ensemble_score > threshold

        return is_anomaly, ensemble_score, contributions

    def update_weights(self, feedback):
        """
        Update weights based on detection feedback

        Args:
            feedback: List of (detector_idx, was_correct) tuples
        """
        # Simple weight update rule
        for idx, was_correct in feedback:
            if was_correct:
                self.weights[idx] *= 1.1  # Increase weight
            else:
                self.weights[idx] *= 0.9  # Decrease weight

        # Renormalize
        self.weights = self.weights / self.weights.sum()
```

### Stacking Ensemble

Use meta-learner to combine detector outputs:

```python
from sklearn.linear_model import LogisticRegression

class StackingEnsemble:
    def __init__(self, base_detectors, meta_model=None):
        """
        Stacking ensemble with meta-learner

        Args:
            base_detectors: List of base detector instances
            meta_model: Model to combine base predictions (default: LogisticRegression)
        """
        self.base_detectors = base_detectors
        self.meta_model = meta_model or LogisticRegression()
        self.is_trained = False

    def get_base_predictions(self, samples):
        """Get predictions from all base detectors"""
        base_preds = []

        for sample in samples:
            features, can_id, timestamp = sample
            sample_preds = []

            for detector in self.base_detectors:
                is_anomaly, detail = detector.predict(features, can_id, timestamp)
                # Get continuous score if available
                if detail and 'score' in detail:
                    sample_preds.append(detail['score'])
                else:
                    sample_preds.append(1.0 if is_anomaly else 0.0)

            base_preds.append(sample_preds)

        return np.array(base_preds)

    def train_meta_model(self, samples, labels):
        """
        Train meta-model on labeled data

        Args:
            samples: List of (features, can_id, timestamp) tuples
            labels: Binary labels (0=normal, 1=attack)
        """
        # Get base predictions
        X_meta = self.get_base_predictions(samples)

        # Train meta-model
        self.meta_model.fit(X_meta, labels)
        self.is_trained = True

        # Return training metrics
        train_preds = self.meta_model.predict(X_meta)
        accuracy = np.mean(train_preds == labels)

        return {'accuracy': accuracy}

    def predict(self, features, can_id, timestamp):
        """Get stacked ensemble prediction"""
        if not self.is_trained:
            raise ValueError("Meta-model not trained")

        # Get base predictions
        sample = [(features, can_id, timestamp)]
        X_meta = self.get_base_predictions(sample)

        # Meta-model prediction
        prediction = self.meta_model.predict(X_meta)[0]
        probability = self.meta_model.predict_proba(X_meta)[0]

        return bool(prediction), {
            'probability': probability[1],
            'base_scores': X_meta[0].tolist()
        }
```

<!--
Instructor Notes:

Ensemble comparison:
- Voting: Simple, no training needed
- Weighted: Adapts to detector performance
- Stacking: Most powerful, needs labeled data

For maritime IDS:
- Start with voting (easy deployment)
- Add weights based on operational experience
- Use stacking if labeled attack data available

Key: Base detectors should be diverse!
Similar detectors don't add much value.
-->

## Building the Maritime Ensemble

### Recommended Architecture

```python
class MaritimeIDSEnsemble:
    def __init__(self, baseline_path, fingerprint_path):
        """
        Production maritime IDS ensemble

        Combines:
        1. Frequency-based detection
        2. Entropy-based detection
        3. ML anomaly detection (SVM)
        4. Device fingerprinting
        """
        # Initialize detectors
        self.frequency_detector = self._init_frequency(baseline_path)
        self.entropy_detector = self._init_entropy(baseline_path)
        self.ml_detector = self._init_ml(baseline_path)
        self.fingerprint_detector = self._init_fingerprint(fingerprint_path)

        # Ensemble weights (tuned for maritime)
        self.weights = {
            'frequency': 0.25,
            'entropy': 0.20,
            'ml': 0.25,
            'fingerprint': 0.30  # High weight for physical detection
        }

        # Alert thresholds
        self.alert_threshold = 0.5
        self.critical_threshold = 0.8

    def process_message(self, can_id, data, timestamp):
        """
        Process message through ensemble

        Returns:
            alert_level: 'normal', 'warning', 'critical'
            score: Ensemble anomaly score
            explanation: Human-readable explanation
        """
        # Get individual predictions
        freq_result = self.frequency_detector.check_message(can_id, timestamp)
        entropy_result = self.entropy_detector.check_message(can_id, timestamp)
        ml_result = self.ml_detector.predict(can_id, data, timestamp)
        fp_result = self.fingerprint_detector.verify(can_id, timestamp)

        # Calculate weighted score
        score = (
            self.weights['frequency'] * freq_result['score'] +
            self.weights['entropy'] * entropy_result['score'] +
            self.weights['ml'] * ml_result['score'] +
            self.weights['fingerprint'] * fp_result['score']
        )

        # Determine alert level
        if score >= self.critical_threshold:
            alert_level = 'critical'
        elif score >= self.alert_threshold:
            alert_level = 'warning'
        else:
            alert_level = 'normal'

        # Generate explanation
        explanation = self._generate_explanation(
            freq_result, entropy_result, ml_result, fp_result, score
        )

        return {
            'alert_level': alert_level,
            'score': score,
            'explanation': explanation,
            'details': {
                'frequency': freq_result,
                'entropy': entropy_result,
                'ml': ml_result,
                'fingerprint': fp_result
            }
        }
```

## Explainable AI (XAI)

### Why Explainability Matters

1. **Trust**: Operators need to understand alerts
2. **Validation**: Verify detector is working correctly
3. **Debugging**: Find and fix false positives
4. **Compliance**: Regulations may require explanations
5. **Learning**: Improve security understanding

### Alert Explanation Generator

```python
class AlertExplainer:
    def __init__(self):
        self.explanation_templates = {
            'frequency_high': "Message rate for PGN {pgn} from device {sa} is {rate:.1f} Hz, "
                             "which is {deviation:.1f}x higher than baseline ({baseline:.1f} Hz).",
            'frequency_low': "Message rate for PGN {pgn} from device {sa} dropped to {rate:.1f} Hz, "
                            "which is {deviation:.1f}x lower than baseline ({baseline:.1f} Hz).",
            'entropy_drop': "Network traffic diversity dropped significantly. "
                           "Entropy: {entropy:.2f} bits (baseline: {baseline:.2f} bits). "
                           "This may indicate a denial-of-service attack.",
            'entropy_rise': "New message types detected. Entropy: {entropy:.2f} bits "
                           "(baseline: {baseline:.2f} bits). "
                           "Possible message injection or new device.",
            'ml_anomaly': "Machine learning model detected anomalous pattern. "
                         "Anomaly score: {score:.3f} (threshold: {threshold:.3f}). "
                         "Top contributing features: {features}.",
            'fingerprint_mismatch': "Device {sa} clock signature does not match enrollment. "
                                   "Expected skew: {expected:.1f} ppm, "
                                   "observed: {observed:.1f} ppm. "
                                   "Possible device impersonation.",
            'multiple_detectors': "Multiple detection methods triggered: {methods}. "
                                  "High confidence attack detection."
        }

    def explain(self, detection_results):
        """
        Generate human-readable explanation for detection

        Args:
            detection_results: Output from ensemble detector

        Returns:
            explanation: Human-readable string
            technical_details: Detailed technical information
        """
        explanations = []
        triggered_methods = []

        # Frequency explanation
        freq = detection_results['details']['frequency']
        if freq.get('triggered'):
            triggered_methods.append('Frequency Monitor')
            if freq['type'] == 'HIGH_RATE':
                explanations.append(self.explanation_templates['frequency_high'].format(
                    pgn=freq['pgn'],
                    sa=freq['sa'],
                    rate=freq['rate'],
                    deviation=freq['rate'] / freq['baseline'],
                    baseline=freq['baseline']
                ))
            else:
                explanations.append(self.explanation_templates['frequency_low'].format(
                    pgn=freq['pgn'],
                    sa=freq['sa'],
                    rate=freq['rate'],
                    deviation=freq['baseline'] / max(freq['rate'], 0.001),
                    baseline=freq['baseline']
                ))

        # Entropy explanation
        entropy = detection_results['details']['entropy']
        if entropy.get('triggered'):
            triggered_methods.append('Entropy Analyzer')
            if entropy['type'] == 'LOW_ENTROPY':
                explanations.append(self.explanation_templates['entropy_drop'].format(
                    entropy=entropy['value'],
                    baseline=entropy['baseline']
                ))
            else:
                explanations.append(self.explanation_templates['entropy_rise'].format(
                    entropy=entropy['value'],
                    baseline=entropy['baseline']
                ))

        # ML explanation
        ml = detection_results['details']['ml']
        if ml.get('triggered'):
            triggered_methods.append('ML Anomaly Detector')
            top_features = self._get_top_features(ml)
            explanations.append(self.explanation_templates['ml_anomaly'].format(
                score=ml['score'],
                threshold=ml['threshold'],
                features=', '.join(top_features)
            ))

        # Fingerprint explanation
        fp = detection_results['details']['fingerprint']
        if fp.get('triggered'):
            triggered_methods.append('Device Fingerprint')
            explanations.append(self.explanation_templates['fingerprint_mismatch'].format(
                sa=fp['sa'],
                expected=fp['expected_skew'],
                observed=fp['observed_skew']
            ))

        # Summary if multiple triggered
        if len(triggered_methods) > 1:
            explanations.insert(0, self.explanation_templates['multiple_detectors'].format(
                methods=', '.join(triggered_methods)
            ))

        return '\n'.join(explanations), detection_results['details']

    def _get_top_features(self, ml_result, top_n=3):
        """Get top contributing features from ML result"""
        if 'feature_importance' in ml_result:
            sorted_features = sorted(
                ml_result['feature_importance'].items(),
                key=lambda x: abs(x[1]),
                reverse=True
            )
            return [f"{name}: {value:.3f}" for name, value in sorted_features[:top_n]]
        return ['(feature importance not available)']
```

<!--
Instructor Notes:

XAI is crucial for operational IDS:

Without explanation:
"ALERT: Anomaly detected at 14:32:45"
Operator: "What? Why? Is it real?"

With explanation:
"ALERT: Device 36 (GPS) clock signature mismatch.
Expected +23 ppm, observed -8 ppm.
Possible spoofing attack on navigation."
Operator: "I'll verify GPS position visually."

Clear explanations enable:
1. Faster triage
2. Appropriate response
3. Fewer ignored alerts
4. Better security posture
-->

## SHAP Values for ML Explanation

### What are SHAP Values?

SHAP (SHapley Additive exPlanations) attributes prediction to each feature:
- Positive SHAP: Feature increases anomaly score
- Negative SHAP: Feature decreases anomaly score
- Magnitude: Importance of feature for this prediction

```python
import shap

class SHAPExplainer:
    def __init__(self, model, feature_names):
        """
        SHAP-based model explainer

        Args:
            model: Trained ML model
            feature_names: List of feature names
        """
        self.model = model
        self.feature_names = feature_names
        self.explainer = None

    def fit_explainer(self, background_data):
        """
        Fit SHAP explainer with background data

        Args:
            background_data: Sample of normal traffic features
        """
        # Use KernelExplainer for model-agnostic explanation
        self.explainer = shap.KernelExplainer(
            self.model.predict_proba,
            shap.sample(background_data, 100)
        )

    def explain_prediction(self, features):
        """
        Explain single prediction

        Returns:
            explanation: Dict with feature contributions
        """
        if self.explainer is None:
            raise ValueError("Explainer not fitted")

        # Calculate SHAP values
        shap_values = self.explainer.shap_values(features.reshape(1, -1))

        # For binary classification, use class 1 (anomaly) values
        if isinstance(shap_values, list):
            shap_values = shap_values[1][0]
        else:
            shap_values = shap_values[0]

        # Create explanation
        explanation = {}
        for name, value in zip(self.feature_names, shap_values):
            explanation[name] = {
                'shap_value': float(value),
                'direction': 'increases anomaly' if value > 0 else 'decreases anomaly',
                'importance': abs(value)
            }

        # Sort by importance
        sorted_features = sorted(
            explanation.items(),
            key=lambda x: x[1]['importance'],
            reverse=True
        )

        return {
            'feature_contributions': dict(sorted_features),
            'base_value': float(self.explainer.expected_value[1]),
            'prediction_value': float(sum(shap_values) + self.explainer.expected_value[1])
        }

    def generate_text_explanation(self, shap_explanation, top_n=5):
        """Generate human-readable explanation from SHAP values"""
        contributions = shap_explanation['feature_contributions']
        top_features = list(contributions.items())[:top_n]

        lines = ["ML model explanation:"]
        lines.append(f"Base anomaly probability: {shap_explanation['base_value']:.2%}")
        lines.append(f"Final anomaly probability: {shap_explanation['prediction_value']:.2%}")
        lines.append("")
        lines.append("Top contributing factors:")

        for name, info in top_features:
            direction = "↑" if info['shap_value'] > 0 else "↓"
            lines.append(f"  {direction} {name}: {info['shap_value']:+.3f} ({info['direction']})")

        return '\n'.join(lines)
```

## Alert Management

### Alert Prioritization

```python
class AlertManager:
    def __init__(self):
        self.active_alerts = []
        self.alert_history = []
        self.suppression_rules = {}

    def process_alert(self, alert):
        """
        Process new alert with prioritization and deduplication

        Returns:
            action: 'notify', 'suppress', 'escalate'
            priority: 1 (highest) to 5 (lowest)
        """
        # Calculate priority based on multiple factors
        priority = self._calculate_priority(alert)

        # Check for suppression (duplicate or known false positive)
        if self._should_suppress(alert):
            return 'suppress', priority

        # Check for escalation (critical or multiple triggers)
        if self._should_escalate(alert):
            return 'escalate', 1  # Highest priority

        # Add to active alerts
        self.active_alerts.append(alert)

        return 'notify', priority

    def _calculate_priority(self, alert):
        """Calculate alert priority (1-5)"""
        score = alert['score']

        # Base priority on score
        if score >= 0.9:
            priority = 1
        elif score >= 0.7:
            priority = 2
        elif score >= 0.5:
            priority = 3
        elif score >= 0.3:
            priority = 4
        else:
            priority = 5

        # Adjust based on affected systems
        if self._affects_navigation(alert):
            priority = max(1, priority - 1)

        if self._affects_propulsion(alert):
            priority = max(1, priority - 1)

        return priority

    def _should_suppress(self, alert):
        """Check if alert should be suppressed"""
        # Check time-based suppression (same alert within 60 seconds)
        for active in self.active_alerts:
            if self._is_duplicate(alert, active):
                if alert['timestamp'] - active['timestamp'] < 60:
                    return True

        # Check manual suppression rules
        key = (alert.get('pgn'), alert.get('sa'))
        if key in self.suppression_rules:
            return True

        return False

    def generate_alert_report(self):
        """Generate summary report of active alerts"""
        if not self.active_alerts:
            return "No active alerts."

        report_lines = [
            f"Active Alerts: {len(self.active_alerts)}",
            "=" * 40
        ]

        # Group by alert level
        critical = [a for a in self.active_alerts if a['alert_level'] == 'critical']
        warning = [a for a in self.active_alerts if a['alert_level'] == 'warning']

        if critical:
            report_lines.append(f"\nCRITICAL ({len(critical)}):")
            for alert in critical[:5]:  # Top 5
                report_lines.append(f"  - {alert['explanation'][:80]}...")

        if warning:
            report_lines.append(f"\nWARNING ({len(warning)}):")
            for alert in warning[:5]:
                report_lines.append(f"  - {alert['explanation'][:80]}...")

        return '\n'.join(report_lines)
```

## Lab Preview: Week 13

In Lab 13, you will:

1. Build ensemble detector with all methods
2. Compare voting strategies
3. Implement alert explanation generator
4. Apply SHAP to ML detector
5. Evaluate ensemble performance
6. Design operator dashboard mockup

**Deliverable**: Functional ensemble IDS with explanations

## Homework

### Required

1. **Read**: Literature Review Sections 4.3 and 7
2. **Implement**: Voting ensemble with at least 3 detectors
3. **Write**: Explanation templates for 5 attack scenarios

### Suggested

- Research: LIME vs SHAP comparison
- Explore: scikit-learn VotingClassifier
- Consider: How would you explain alerts to non-technical crew?

## Discussion Questions

1. How do you choose weights for weighted voting?
2. When is stacking better than simple voting?
3. Why is explainability harder for deep learning?
4. Should alerts always include technical details?

## References

- [SHAP Documentation]
- [Ensemble Learning Methods]
- [XAI for Cybersecurity]

[SHAP Documentation]:https://shap.readthedocs.io
[Ensemble Learning Methods]:https://scikit-learn.org/stable/modules/ensemble.html
[XAI for Cybersecurity]:https://arxiv.org/abs/2011.04573

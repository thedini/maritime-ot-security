---
title: "Lab 13"
subtitle: "Ensemble Detection and Explainability"
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
    Building an ensemble IDS with explainable alerts
---

# Lab 13 -- Ensemble Detection and Explainability

## Lab Overview

**Duration**: 2 hours
**Prerequisites**: Labs 09-12 completed, Class 13 material reviewed
**Materials Required**:
- All detector implementations from Labs 09-12
- Test captures (normal and attack)
- Python 3.x

## Objectives

By the end of this lab, you will:

1. Combine multiple detection methods
2. Implement voting and weighted strategies
3. Generate human-readable alert explanations
4. Evaluate ensemble performance
5. Build operator-friendly output

## Part 1: Integrate Detection Methods (30 minutes)

### 1.1 Load All Detectors

```python
#!/usr/bin/env python3
"""
ensemble_ids.py - Combined intrusion detection system
"""
import numpy as np
from collections import defaultdict
import json

# Import your detector implementations
from frequency_ids import FrequencyDetector, FrequencyBaseline
from entropy_ids import EntropyDetector, EntropyBaseline
from ml_detection import SVMDetector, FeatureExtractor
from fingerprint import ImpersonationDetector, FingerprintDatabase

class EnsembleIDS:
    def __init__(self, config):
        """
        Ensemble IDS combining multiple detection methods

        Args:
            config: Dict with paths to baselines, models, etc.
        """
        self.config = config
        self.detectors = {}
        self.weights = config.get('weights', {})

        # Initialize detectors
        self._init_frequency_detector()
        self._init_entropy_detector()
        self._init_ml_detector()
        self._init_fingerprint_detector()

        # Alert management
        self.alerts = []
        self.message_count = 0

        # Feature extractor for ML
        self.feature_extractor = FeatureExtractor(window_size=100)
        self.message_buffer = []

        print(f"Ensemble IDS initialized with {len(self.detectors)} detectors")

    def _init_frequency_detector(self):
        """Initialize frequency-based detector"""
        try:
            baseline = FrequencyBaseline(self.config['frequency_baseline'])
            self.detectors['frequency'] = FrequencyDetector(
                baseline,
                threshold_sigma=self.config.get('frequency_threshold', 3)
            )
            self.weights.setdefault('frequency', 0.25)
            print("  ✓ Frequency detector loaded")
        except Exception as e:
            print(f"  ✗ Frequency detector failed: {e}")

    def _init_entropy_detector(self):
        """Initialize entropy-based detector"""
        try:
            baseline = EntropyBaseline()
            baseline.load(self.config['entropy_baseline'])
            self.detectors['entropy'] = EntropyDetector(
                baseline,
                window_size=100,
                threshold_sigma=self.config.get('entropy_threshold', 3)
            )
            self.weights.setdefault('entropy', 0.20)
            print("  ✓ Entropy detector loaded")
        except Exception as e:
            print(f"  ✗ Entropy detector failed: {e}")

    def _init_ml_detector(self):
        """Initialize ML-based detector"""
        try:
            self.detectors['ml'] = SVMDetector()
            self.detectors['ml'].load(self.config['ml_model'])
            self.weights.setdefault('ml', 0.25)
            print("  ✓ ML detector loaded")
        except Exception as e:
            print(f"  ✗ ML detector failed: {e}")

    def _init_fingerprint_detector(self):
        """Initialize fingerprint-based detector"""
        try:
            db = FingerprintDatabase()
            db.load(self.config['fingerprint_db'])
            self.detectors['fingerprint'] = ImpersonationDetector(
                db,
                tolerance_ppm=self.config.get('fingerprint_tolerance', 10)
            )
            self.weights.setdefault('fingerprint', 0.30)
            print("  ✓ Fingerprint detector loaded")
        except Exception as e:
            print(f"  ✗ Fingerprint detector failed: {e}")

    def process_message(self, can_id, data, timestamp):
        """
        Process message through all detectors

        Returns:
            alert: Ensemble alert if triggered, None otherwise
        """
        self.message_count += 1

        # Update message buffer for ML
        self.message_buffer.append({
            'can_id': can_id,
            'data': data,
            'timestamp': timestamp
        })
        if len(self.message_buffer) > 200:
            self.message_buffer = self.message_buffer[-200:]

        # Get individual detector results
        results = {}

        # Frequency
        if 'frequency' in self.detectors:
            is_anom, detail = self.detectors['frequency'].process_message(
                can_id, timestamp
            )
            results['frequency'] = {
                'triggered': is_anom,
                'score': 1.0 if is_anom else 0.0,
                'detail': detail
            }

        # Entropy
        if 'entropy' in self.detectors:
            alerts = self.detectors['entropy'].process_message(
                can_id, data, timestamp
            )
            results['entropy'] = {
                'triggered': len(alerts) > 0,
                'score': 1.0 if alerts else 0.0,
                'detail': alerts[0] if alerts else None
            }

        # ML (batch processing)
        if 'ml' in self.detectors and len(self.message_buffer) >= 100:
            if self.message_count % 50 == 0:  # Check every 50 messages
                features = self.feature_extractor.extract(self.message_buffer)
                if features is not None:
                    preds, scores = self.detectors['ml'].predict(features)
                    results['ml'] = {
                        'triggered': preds[0] == -1,
                        'score': -scores[0] if scores[0] < 0 else 0,
                        'detail': {'decision_score': scores[0]}
                    }

        # Fingerprint
        if 'fingerprint' in self.detectors:
            alert = self.detectors['fingerprint'].process_message(
                can_id, timestamp
            )
            results['fingerprint'] = {
                'triggered': alert is not None,
                'score': 1.0 if alert else 0.0,
                'detail': alert
            }

        # Calculate ensemble score
        ensemble_score = self._calculate_ensemble_score(results)

        # Generate alert if threshold exceeded
        if ensemble_score >= self.config.get('alert_threshold', 0.5):
            return self._create_alert(can_id, timestamp, ensemble_score, results)

        return None

    def _calculate_ensemble_score(self, results):
        """Calculate weighted ensemble score"""
        total_score = 0
        total_weight = 0

        for detector, result in results.items():
            if detector in self.weights:
                weight = self.weights[detector]
                score = result.get('score', 0)
                total_score += weight * score
                total_weight += weight

        return total_score / total_weight if total_weight > 0 else 0

    def _create_alert(self, can_id, timestamp, score, results):
        """Create ensemble alert"""
        pgn = (can_id >> 8) & 0x3FFFF
        sa = can_id & 0xFF

        # Identify triggered detectors
        triggered = [k for k, v in results.items() if v.get('triggered')]

        alert = {
            'timestamp': timestamp,
            'can_id': can_id,
            'pgn': pgn,
            'source_addr': sa,
            'ensemble_score': score,
            'triggered_detectors': triggered,
            'detector_results': results,
            'severity': self._calculate_severity(score, len(triggered))
        }

        self.alerts.append(alert)
        return alert

    def _calculate_severity(self, score, num_triggered):
        """Calculate alert severity"""
        if score >= 0.9 or num_triggered >= 3:
            return 'CRITICAL'
        elif score >= 0.7 or num_triggered >= 2:
            return 'HIGH'
        elif score >= 0.5:
            return 'MEDIUM'
        else:
            return 'LOW'
```

### 1.2 Configure Ensemble

Create configuration file:

```python
config = {
    'frequency_baseline': 'baseline.json',
    'entropy_baseline': 'entropy_baseline.json',
    'ml_model': 'svm_model.joblib',
    'fingerprint_db': 'fingerprint_db.json',
    'weights': {
        'frequency': 0.25,
        'entropy': 0.20,
        'ml': 0.25,
        'fingerprint': 0.30
    },
    'frequency_threshold': 3,
    'entropy_threshold': 3,
    'fingerprint_tolerance': 10,
    'alert_threshold': 0.5
}

# Save config
with open('ensemble_config.json', 'w') as f:
    json.dump(config, f, indent=2)
```

### 1.3 Initialize and Test

```python
# Load configuration
with open('ensemble_config.json') as f:
    config = json.load(f)

# Create ensemble
ensemble = EnsembleIDS(config)

# Quick test
print(f"\nEnsemble ready with weights:")
for det, weight in ensemble.weights.items():
    print(f"  {det}: {weight:.2f}")
```

## Part 2: Implement Alert Explainer (25 minutes)

### 2.1 Build Explanation Generator

```python
class AlertExplainer:
    def __init__(self):
        """
        Generate human-readable explanations for alerts
        """
        self.templates = {
            'frequency_high': (
                "Message rate for PGN {pgn} from device {sa} is abnormally high. "
                "Observed rate: {observed:.1f} Hz (expected: {expected:.1f} Hz). "
                "This may indicate a spoofing or denial-of-service attack."
            ),
            'frequency_low': (
                "Message rate for PGN {pgn} from device {sa} has dropped. "
                "Observed rate: {observed:.1f} Hz (expected: {expected:.1f} Hz). "
                "Device may be offline or compromised."
            ),
            'entropy_low': (
                "Network traffic diversity has decreased significantly. "
                "Current entropy: {value:.2f} bits (baseline: {baseline:.2f} bits). "
                "This typically indicates a denial-of-service attack where "
                "one message type is flooding the network."
            ),
            'entropy_high': (
                "Network traffic shows unusual diversity. "
                "Current entropy: {value:.2f} bits (baseline: {baseline:.2f} bits). "
                "New devices or message types may have been introduced."
            ),
            'ml_anomaly': (
                "Machine learning model detected anomalous traffic pattern. "
                "Anomaly score: {score:.3f}. "
                "The current traffic deviates from learned normal behavior."
            ),
            'fingerprint_mismatch': (
                "Device {sa} ({device_name}) does not match its enrolled fingerprint. "
                "Expected clock skew: {expected:.1f} ppm, observed: {observed:.1f} ppm. "
                "POSSIBLE DEVICE IMPERSONATION ATTACK. "
                "An attacker may be spoofing messages from this device."
            ),
            'multiple_detectors': (
                "HIGH CONFIDENCE ALERT: Multiple detection methods triggered simultaneously. "
                "Detectors: {detectors}. "
                "This strongly indicates a real attack rather than a false positive."
            )
        }

    def explain(self, alert):
        """
        Generate explanation for alert

        Args:
            alert: Alert dict from EnsembleIDS

        Returns:
            explanation: Human-readable string
        """
        explanations = []
        results = alert.get('detector_results', {})

        # Check each detector
        if results.get('frequency', {}).get('triggered'):
            detail = results['frequency'].get('detail', {})
            if detail:
                template = 'frequency_high' if detail.get('type') == 'HIGH_RATE' else 'frequency_low'
                explanations.append(self.templates[template].format(
                    pgn=alert.get('pgn', 'unknown'),
                    sa=alert.get('source_addr', 'unknown'),
                    observed=1.0 / detail.get('interval', 1),
                    expected=1.0 / detail.get('expected_interval', 0.1)
                ))

        if results.get('entropy', {}).get('triggered'):
            detail = results['entropy'].get('detail', {})
            if detail:
                template = 'entropy_low' if detail.get('type') == 'LOW_ENTROPY' else 'entropy_high'
                explanations.append(self.templates[template].format(
                    value=detail.get('value', 0),
                    baseline=detail.get('baseline_mean', 0)
                ))

        if results.get('ml', {}).get('triggered'):
            detail = results['ml'].get('detail', {})
            explanations.append(self.templates['ml_anomaly'].format(
                score=detail.get('decision_score', 0)
            ))

        if results.get('fingerprint', {}).get('triggered'):
            detail = results['fingerprint'].get('detail', {})
            if detail:
                explanations.append(self.templates['fingerprint_mismatch'].format(
                    sa=alert.get('source_addr', 'unknown'),
                    device_name=detail.get('device_name', 'Unknown'),
                    expected=detail.get('expected_skew', 0),
                    observed=detail.get('observed_skew', 0)
                ))

        # Add multi-detector note if applicable
        triggered = alert.get('triggered_detectors', [])
        if len(triggered) > 1:
            explanations.insert(0, self.templates['multiple_detectors'].format(
                detectors=', '.join(triggered)
            ))

        return '\n\n'.join(explanations) if explanations else "No specific explanation available."

    def format_alert(self, alert):
        """
        Format complete alert output

        Returns:
            Formatted string for display/logging
        """
        lines = [
            "=" * 70,
            f"ALERT [{alert['severity']}] - {alert['timestamp']:.3f}",
            "=" * 70,
            f"Source Address: {alert['source_addr']}",
            f"PGN: {alert['pgn']}",
            f"Ensemble Score: {alert['ensemble_score']:.3f}",
            f"Triggered Detectors: {', '.join(alert['triggered_detectors'])}",
            "",
            "EXPLANATION:",
            "-" * 70,
            self.explain(alert),
            "=" * 70,
        ]
        return '\n'.join(lines)
```

### 2.2 Test Explainer

```python
# Create explainer
explainer = AlertExplainer()

# Process traffic and show explained alerts
ensemble = EnsembleIDS(config)

with open('attack_capture.txt') as f:
    for line in f:
        msg = parse_message(line)
        if msg:
            alert = ensemble.process_message(
                msg['can_id'], msg['data'], msg['timestamp']
            )
            if alert:
                print(explainer.format_alert(alert))
                print()
```

## Part 3: Voting Strategies (20 minutes)

### 3.1 Implement Multiple Strategies

```python
class VotingStrategy:
    """Different voting strategies for ensemble"""

    @staticmethod
    def majority(results, threshold=0.5):
        """
        Majority voting - alert if >50% detectors trigger
        """
        triggered = sum(1 for r in results.values() if r.get('triggered'))
        return triggered > len(results) * threshold

    @staticmethod
    def unanimous(results):
        """
        Unanimous voting - all detectors must trigger
        """
        return all(r.get('triggered') for r in results.values())

    @staticmethod
    def any_trigger(results):
        """
        Any voting - alert if any detector triggers
        """
        return any(r.get('triggered') for r in results.values())

    @staticmethod
    def weighted(results, weights, threshold=0.5):
        """
        Weighted voting - weighted sum exceeds threshold
        """
        total_score = 0
        total_weight = 0
        for detector, result in results.items():
            if detector in weights:
                total_score += weights[detector] * result.get('score', 0)
                total_weight += weights[detector]
        return (total_score / total_weight) >= threshold if total_weight > 0 else False

    @staticmethod
    def priority_based(results, priority_order):
        """
        Priority voting - defer to highest priority detector
        """
        for detector in priority_order:
            if detector in results:
                return results[detector].get('triggered', False)
        return False
```

### 3.2 Compare Strategies

```python
def compare_voting_strategies(ensemble, capture_file, attack_labels=None):
    """
    Compare different voting strategies

    Returns:
        Results for each strategy
    """
    strategies = {
        'majority': lambda r: VotingStrategy.majority(r, 0.5),
        'any': VotingStrategy.any_trigger,
        'weighted': lambda r: VotingStrategy.weighted(r, ensemble.weights, 0.5),
        'unanimous': VotingStrategy.unanimous,
    }

    results = {name: {'alerts': 0, 'messages': 0} for name in strategies}

    with open(capture_file) as f:
        for line in f:
            msg = parse_message(line)
            if not msg:
                continue

            # Get individual detector results
            detector_results = {}  # ... (process message through each detector)

            for name, strategy in strategies.items():
                results[name]['messages'] += 1
                if strategy(detector_results):
                    results[name]['alerts'] += 1

    print("\nVoting Strategy Comparison:")
    print("=" * 50)
    for name, r in results.items():
        rate = r['alerts'] / r['messages'] * 100 if r['messages'] > 0 else 0
        print(f"{name:15s}: {r['alerts']:5d} alerts ({rate:.2f}%)")

    return results
```

### 3.3 Strategy Selection

Based on your comparison, which strategy is best for:

| Scenario | Recommended Strategy | Rationale |
|----------|---------------------|-----------|
| High security (miss nothing) | | |
| Low false positives (fewer alerts) | | |
| Balanced | | |

## Part 4: Performance Evaluation (20 minutes)

### 4.1 Run Complete Evaluation

```python
def evaluate_ensemble(ensemble, normal_file, attack_file):
    """
    Comprehensive ensemble evaluation
    """
    # Process normal traffic
    print("Processing normal traffic...")
    ensemble.alerts = []
    normal_count = 0

    with open(normal_file) as f:
        for line in f:
            msg = parse_message(line)
            if msg:
                ensemble.process_message(msg['can_id'], msg['data'], msg['timestamp'])
                normal_count += 1

    normal_alerts = len(ensemble.alerts)

    # Process attack traffic
    print("Processing attack traffic...")
    ensemble.alerts = []
    attack_count = 0

    with open(attack_file) as f:
        for line in f:
            msg = parse_message(line)
            if msg:
                ensemble.process_message(msg['can_id'], msg['data'], msg['timestamp'])
                attack_count += 1

    attack_alerts = len(ensemble.alerts)

    # Calculate metrics
    fpr = normal_alerts / normal_count if normal_count > 0 else 0
    tpr = attack_alerts / attack_count if attack_count > 0 else 0

    # Precision/recall (simplified - assumes all attack alerts are TP)
    tp = attack_alerts
    fp = normal_alerts
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tpr
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    results = {
        'normal_messages': normal_count,
        'attack_messages': attack_count,
        'normal_alerts': normal_alerts,
        'attack_alerts': attack_alerts,
        'false_positive_rate': fpr,
        'true_positive_rate': tpr,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

    print("\nEnsemble Evaluation Results:")
    print("=" * 50)
    for key, value in results.items():
        if isinstance(value, float):
            print(f"{key:25s}: {value:.4f}")
        else:
            print(f"{key:25s}: {value}")

    return results
```

### 4.2 Record Final Metrics

| Metric | Value |
|--------|-------|
| False Positive Rate | |
| True Positive Rate | |
| Precision | |
| Recall | |
| F1 Score | |

### 4.3 Per-Detector Contribution

```python
def analyze_detector_contributions(alerts):
    """Analyze which detectors contribute most to alerts"""
    detector_counts = defaultdict(int)
    detector_alone = defaultdict(int)

    for alert in alerts:
        triggered = alert['triggered_detectors']
        for det in triggered:
            detector_counts[det] += 1
        if len(triggered) == 1:
            detector_alone[triggered[0]] += 1

    print("\nDetector Contributions:")
    print("-" * 40)
    for det in detector_counts:
        print(f"{det:15s}: {detector_counts[det]:4d} alerts "
              f"({detector_alone[det]} alone)")
```

## Part 5: Create Dashboard Mockup (15 minutes)

### 5.1 Design Alert Dashboard Output

```python
class AlertDashboard:
    def __init__(self, ensemble):
        self.ensemble = ensemble
        self.explainer = AlertExplainer()

    def print_status(self):
        """Print current system status"""
        stats = self.ensemble.get_statistics()

        print("\n" + "=" * 70)
        print("MARITIME IDS DASHBOARD")
        print("=" * 70)
        print(f"Status: ACTIVE")
        print(f"Messages Processed: {stats.get('message_count', 0):,}")
        print(f"Active Alerts: {len(self.ensemble.alerts)}")
        print()

        # Active alerts summary
        if self.ensemble.alerts:
            critical = sum(1 for a in self.ensemble.alerts if a['severity'] == 'CRITICAL')
            high = sum(1 for a in self.ensemble.alerts if a['severity'] == 'HIGH')
            medium = sum(1 for a in self.ensemble.alerts if a['severity'] == 'MEDIUM')

            print("Alert Summary:")
            print(f"  🔴 CRITICAL: {critical}")
            print(f"  🟠 HIGH: {high}")
            print(f"  🟡 MEDIUM: {medium}")
            print()

            # Show most recent critical alert
            critical_alerts = [a for a in self.ensemble.alerts
                             if a['severity'] == 'CRITICAL']
            if critical_alerts:
                print("Most Recent Critical Alert:")
                print("-" * 40)
                print(self.explainer.explain(critical_alerts[-1]))

        print("=" * 70)

    def export_report(self, filename):
        """Export alert report to file"""
        with open(filename, 'w') as f:
            f.write("Maritime IDS Alert Report\n")
            f.write("=" * 70 + "\n\n")

            for alert in self.ensemble.alerts:
                f.write(self.explainer.format_alert(alert))
                f.write("\n\n")

        print(f"Report exported to {filename}")
```

### 5.2 Sample Output

Generate sample dashboard output for your report.

## Deliverables

Submit via course portal:

1. **ensemble_ids.py** - Complete implementation
2. **ensemble_config.json** - Configuration file
3. **Evaluation results** - Metrics table
4. **Sample alerts** - 3-5 explained alerts
5. **Lab report** - Analysis and recommendations

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Ensemble integration working | 25 |
| Alert explainer implemented | 20 |
| Voting strategies compared | 15 |
| Performance evaluation complete | 25 |
| Dashboard output quality | 15 |
| **Total** | **100** |

## Next Lab Preview

Lab 14 is the Capstone:
- Red team/blue team exercise
- Final system evaluation
- Presentation preparation
- Course wrap-up

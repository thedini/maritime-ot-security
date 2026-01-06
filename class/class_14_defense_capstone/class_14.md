---
title: "Class 14"
subtitle: "Defense Architecture and Capstone Review"
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
    Comprehensive defense architecture and final capstone review
---

# Class 14 -- Defense Architecture and Capstone Review

## Learning Outcomes

- Design comprehensive maritime IDS architecture
- Implement defense-in-depth for NMEA 2000 networks
- Conduct red team/blue team exercises
- Evaluate detection system effectiveness
- Present final capstone findings

## Session Structure

1. **Defense Architecture** (30 min) - Building a complete IDS
2. **Red Team Exercise** (45 min) - Students attack, system defends
3. **Blue Team Analysis** (30 min) - Analyze detection results
4. **Capstone Presentations** (45 min) - Student project reviews

## Comprehensive Defense Architecture

### Defense-in-Depth Model

```
┌─────────────────────────────────────────────────────────────┐
│                    MARITIME IDS ARCHITECTURE                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 5: Operator Interface                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Dashboard │ Alerts │ Reports │ Controls │ XAI      │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│  Layer 4: Alert Management                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Prioritization │ Correlation │ Suppression │ Log   │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│  Layer 3: Ensemble Detection                                 │
│  ┌──────────┬──────────┬──────────┬──────────┐             │
│  │ Frequency│ Entropy  │ ML/LSTM  │ Device   │             │
│  │ Monitor  │ Analyzer │ Detector │ Fingerprint│            │
│  └──────────┴──────────┴──────────┴──────────┘             │
│                           │                                  │
│  Layer 2: Data Processing                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Parser │ Feature Extract │ Baseline │ Normalize    │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│  Layer 1: Data Collection                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  CAN Interface │ Buffer │ Timestamp │ Store         │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│  ═══════════════ NMEA 2000 Bus ════════════════════════     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Complete IDS Implementation

```python
#!/usr/bin/env python3
"""
Maritime IDS - Complete Defense System
Production-ready implementation combining all detection methods
"""

import time
import json
import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import threading
import queue

# Detection modules (from previous weeks)
from frequency_detector import FrequencyDetector
from entropy_detector import EntropyDetector
from ml_detector import MLAnomalyDetector
from fingerprint_detector import FingerprintDetector
from alert_explainer import AlertExplainer

@dataclass
class Alert:
    timestamp: float
    severity: str  # 'critical', 'high', 'medium', 'low'
    source_addr: int
    pgn: int
    detection_type: str
    score: float
    explanation: str
    raw_data: dict

class MaritimeIDS:
    def __init__(self, config_path: str):
        """
        Initialize complete Maritime IDS

        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()

        # Initialize detectors
        self.logger.info("Initializing detection modules...")
        self.frequency_detector = FrequencyDetector(
            self.config['baseline_path'],
            threshold_sigma=self.config.get('frequency_threshold', 3)
        )
        self.entropy_detector = EntropyDetector(
            window_size=self.config.get('entropy_window', 100),
            baseline_path=self.config['baseline_path']
        )
        self.ml_detector = MLAnomalyDetector(
            model_path=self.config['model_path']
        )
        self.fingerprint_detector = FingerprintDetector(
            fingerprint_path=self.config['fingerprint_path']
        )

        # Alert management
        self.explainer = AlertExplainer()
        self.alert_queue = queue.Queue()
        self.active_alerts = []
        self.alert_history = []

        # Statistics
        self.stats = {
            'messages_processed': 0,
            'alerts_generated': 0,
            'alerts_by_type': defaultdict(int),
            'start_time': time.time()
        }

        # Ensemble weights
        self.weights = self.config.get('ensemble_weights', {
            'frequency': 0.25,
            'entropy': 0.20,
            'ml': 0.25,
            'fingerprint': 0.30
        })

        self.logger.info("Maritime IDS initialized successfully")

    def process_message(self, can_id: int, data: bytes, timestamp: float) -> Optional[Alert]:
        """
        Process single CAN message through all detection layers

        Returns:
            Alert if anomaly detected, None otherwise
        """
        self.stats['messages_processed'] += 1

        # Extract metadata
        pgn = (can_id >> 8) & 0x3FFFF
        sa = can_id & 0xFF

        # Layer 2: Data Processing
        features = self._extract_features(can_id, data, timestamp)

        # Layer 3: Run all detectors
        results = {
            'frequency': self.frequency_detector.check(can_id, timestamp),
            'entropy': self.entropy_detector.check(can_id, timestamp),
            'ml': self.ml_detector.predict(features),
            'fingerprint': self.fingerprint_detector.verify(sa, timestamp)
        }

        # Calculate ensemble score
        ensemble_score = self._calculate_ensemble_score(results)

        # Generate alert if threshold exceeded
        if ensemble_score >= self.config.get('alert_threshold', 0.5):
            alert = self._create_alert(
                timestamp, sa, pgn, ensemble_score, results
            )
            self._handle_alert(alert)
            return alert

        return None

    def _calculate_ensemble_score(self, results: dict) -> float:
        """Calculate weighted ensemble anomaly score"""
        score = 0.0
        for detector, result in results.items():
            if result and 'score' in result:
                score += self.weights.get(detector, 0.25) * result['score']
        return score

    def _create_alert(self, timestamp: float, sa: int, pgn: int,
                      score: float, results: dict) -> Alert:
        """Create alert with explanation"""
        # Determine severity
        if score >= 0.9:
            severity = 'critical'
        elif score >= 0.7:
            severity = 'high'
        elif score >= 0.5:
            severity = 'medium'
        else:
            severity = 'low'

        # Identify primary detection type
        triggered = [k for k, v in results.items() if v and v.get('triggered')]
        detection_type = '+'.join(triggered) if triggered else 'ensemble'

        # Generate explanation
        explanation = self.explainer.explain(results, sa, pgn, score)

        return Alert(
            timestamp=timestamp,
            severity=severity,
            source_addr=sa,
            pgn=pgn,
            detection_type=detection_type,
            score=score,
            explanation=explanation,
            raw_data=results
        )

    def _handle_alert(self, alert: Alert):
        """Handle generated alert"""
        self.stats['alerts_generated'] += 1
        self.stats['alerts_by_type'][alert.detection_type] += 1

        # Add to queues
        self.alert_queue.put(alert)
        self.active_alerts.append(alert)

        # Trim active alerts (keep last 100)
        if len(self.active_alerts) > 100:
            self.active_alerts = self.active_alerts[-100:]

        # Log alert
        self.logger.warning(
            f"ALERT [{alert.severity.upper()}]: SA={alert.source_addr}, "
            f"PGN={alert.pgn}, Score={alert.score:.3f}, "
            f"Type={alert.detection_type}"
        )

    def get_stats(self) -> dict:
        """Get IDS statistics"""
        runtime = time.time() - self.stats['start_time']
        return {
            **self.stats,
            'runtime_seconds': runtime,
            'messages_per_second': self.stats['messages_processed'] / max(runtime, 1),
            'alert_rate': self.stats['alerts_generated'] / max(self.stats['messages_processed'], 1)
        }

    def get_alert_summary(self) -> str:
        """Generate alert summary report"""
        stats = self.get_stats()

        lines = [
            "=" * 50,
            "MARITIME IDS ALERT SUMMARY",
            "=" * 50,
            f"Runtime: {stats['runtime_seconds']:.1f} seconds",
            f"Messages Processed: {stats['messages_processed']:,}",
            f"Processing Rate: {stats['messages_per_second']:.1f} msg/sec",
            f"Total Alerts: {stats['alerts_generated']}",
            f"Alert Rate: {stats['alert_rate']*100:.3f}%",
            "",
            "Alerts by Detection Type:"
        ]

        for dtype, count in sorted(stats['alerts_by_type'].items()):
            lines.append(f"  {dtype}: {count}")

        if self.active_alerts:
            lines.append("")
            lines.append("Recent Critical/High Alerts:")
            critical_high = [a for a in self.active_alerts
                           if a.severity in ('critical', 'high')]
            for alert in critical_high[-5:]:
                lines.append(f"  [{alert.severity}] SA={alert.source_addr}: "
                           f"{alert.explanation[:60]}...")

        lines.append("=" * 50)
        return '\n'.join(lines)
```

<!--
Instructor Notes:

This is the culmination of the course.
Students should recognize each component from previous weeks.

Key design decisions:
1. Modular - each detector independent
2. Configurable - weights, thresholds in config
3. Observable - statistics, logging
4. Explainable - human-readable alerts

Production deployment considerations:
- Run in separate process
- Database backend for alerts
- Web interface for operators
- SIEM integration
-->

## Network Architecture Recommendations

### Placement Options

```
Option A: Inline Monitor
─────────────────────────────
  ┌─────────┐    ┌─────────┐    ┌─────────┐
  │  GPS    │────│   IDS   │────│ Chart   │
  └─────────┘    │ (inline)│    │ Plotter │
                 └─────────┘

Option B: Passive Tap
─────────────────────────────
  ┌─────────┐    ┌─────────┐
  │  GPS    │────│ Chart   │
  └─────────┘    │ Plotter │
       │         └─────────┘
       │ (tap)
  ┌─────────┐
  │   IDS   │
  │(passive)│
  └─────────┘

Option C: Gateway Integration
─────────────────────────────
  ┌─────────┐    ┌─────────────────┐    ┌─────────┐
  │  GPS    │────│  IDS Gateway    │────│ Chart   │
  └─────────┘    │  (filter/alert) │    │ Plotter │
                 └─────────────────┘
```

### Recommendation

**Option B (Passive Tap)** for most deployments:
- No single point of failure
- Doesn't add latency
- Can't accidentally block traffic
- Easier to deploy/maintain

**Option C (Gateway)** for high-security:
- Can actively block attacks
- More complex deployment
- Requires careful configuration
- Potential availability impact

## Red Team Exercise

### Exercise Objectives

Students will:
1. Execute attacks from Weeks 5-7
2. Attempt to evade detection from Weeks 9-12
3. Document successful/failed attack attempts
4. Analyze which detection methods caught attacks

### Attack Scenarios

| Scenario | Attack | Detection Expected |
|----------|--------|-------------------|
| 1 | DoS flood (priority 0) | Frequency + Entropy |
| 2 | Position spoof (naive) | Frequency (2x rate) |
| 3 | Position spoof (rate-matched) | Fingerprint |
| 4 | Replay attack | LSTM + Entropy |
| 5 | Engine false alarm | ML + Fingerprint |
| 6 | Stealthy drift | Ensemble (weak signal) |

### Red Team Scorecard

```markdown
# Red Team Exercise Scorecard

## Team: _______________

### Attack Results

| Scenario | Attack Executed | Detected? | By Which Method? | Evasion Attempt |
|----------|----------------|-----------|------------------|-----------------|
| 1 | DoS | Y/N | | |
| 2 | Position (naive) | Y/N | | |
| 3 | Position (smart) | Y/N | | |
| 4 | Replay | Y/N | | |
| 5 | Engine spoof | Y/N | | |
| 6 | Stealthy drift | Y/N | | |

### Evasion Techniques Tried
- [ ] Rate matching
- [ ] Gradual value changes
- [ ] Using existing device SA
- [ ] Timing synchronization
- [ ] Other: _______________

### Detection Gaps Found
1.
2.
3.

### Recommendations for Blue Team
1.
2.
3.
```

<!--
Instructor Notes:

Red team exercise structure:
1. Divide class into red/blue teams
2. Red teams get 30 minutes to plan attacks
3. Execute attacks against IDS
4. Blue team monitors and documents
5. Swap roles and repeat
6. Debrief and discuss

Key learning: Even with good detection,
sophisticated attacks may succeed partially.
Defense is about raising the bar, not perfection.
-->

## Blue Team Analysis

### Detection Analysis Framework

```python
class DetectionAnalyzer:
    def __init__(self, ids_instance):
        self.ids = ids_instance
        self.attack_log = []
        self.detection_log = []

    def log_attack(self, attack_type: str, start_time: float,
                   end_time: float, parameters: dict):
        """Log attack for correlation with detections"""
        self.attack_log.append({
            'type': attack_type,
            'start': start_time,
            'end': end_time,
            'parameters': parameters
        })

    def correlate_detections(self):
        """Correlate attacks with detections"""
        results = []

        for attack in self.attack_log:
            # Find detections during attack window
            detections = [
                alert for alert in self.ids.alert_history
                if attack['start'] <= alert.timestamp <= attack['end']
            ]

            results.append({
                'attack': attack,
                'detected': len(detections) > 0,
                'detection_count': len(detections),
                'first_detection_delay': (
                    detections[0].timestamp - attack['start']
                    if detections else None
                ),
                'detection_types': list(set(d.detection_type for d in detections)),
                'max_score': max([d.score for d in detections], default=0)
            })

        return results

    def calculate_metrics(self, correlation_results: list):
        """Calculate detection metrics"""
        total_attacks = len(correlation_results)
        detected = sum(1 for r in correlation_results if r['detected'])
        missed = total_attacks - detected

        # Get false positives (detections outside attack windows)
        attack_times = set()
        for attack in self.attack_log:
            for t in range(int(attack['start']), int(attack['end']) + 1):
                attack_times.add(t)

        false_positives = sum(
            1 for alert in self.ids.alert_history
            if int(alert.timestamp) not in attack_times
        )

        return {
            'total_attacks': total_attacks,
            'detected': detected,
            'missed': missed,
            'detection_rate': detected / max(total_attacks, 1),
            'false_positives': false_positives,
            'mean_detection_delay': sum(
                r['first_detection_delay'] for r in correlation_results
                if r['first_detection_delay'] is not None
            ) / max(detected, 1)
        }

    def generate_report(self, correlation_results: list):
        """Generate analysis report"""
        metrics = self.calculate_metrics(correlation_results)

        report = [
            "=" * 60,
            "BLUE TEAM DETECTION ANALYSIS",
            "=" * 60,
            "",
            "OVERALL METRICS:",
            f"  Detection Rate: {metrics['detection_rate']:.1%}",
            f"  Attacks Detected: {metrics['detected']}/{metrics['total_attacks']}",
            f"  Attacks Missed: {metrics['missed']}",
            f"  False Positives: {metrics['false_positives']}",
            f"  Mean Detection Delay: {metrics['mean_detection_delay']:.2f}s",
            "",
            "PER-ATTACK ANALYSIS:",
            "-" * 60
        ]

        for result in correlation_results:
            status = "✓ DETECTED" if result['detected'] else "✗ MISSED"
            report.append(f"\n{result['attack']['type']}:")
            report.append(f"  Status: {status}")
            if result['detected']:
                report.append(f"  Detection Methods: {', '.join(result['detection_types'])}")
                report.append(f"  Detection Delay: {result['first_detection_delay']:.2f}s")
                report.append(f"  Max Score: {result['max_score']:.3f}")
            else:
                report.append(f"  Attack Parameters: {result['attack']['parameters']}")
                report.append("  Recommendation: Review detection thresholds")

        report.append("\n" + "=" * 60)
        return '\n'.join(report)
```

## Capstone Project Guidelines

### Project Requirements

1. **Implementation** (40%)
   - Working IDS with at least 3 detection methods
   - Ensemble combination logic
   - Alert generation with explanations

2. **Evaluation** (30%)
   - Test against 5+ attack types
   - Calculate detection metrics
   - Analyze false positive rate

3. **Documentation** (20%)
   - Architecture diagram
   - Configuration guide
   - Performance analysis

4. **Presentation** (10%)
   - 10-minute presentation
   - Live demo (optional)
   - Q&A response

### Presentation Structure

```markdown
# Capstone Presentation Outline

## 1. Introduction (1 min)
- Team members
- Project scope

## 2. Architecture (2 min)
- Detection methods used
- Ensemble strategy
- Key design decisions

## 3. Implementation (3 min)
- Technical challenges
- Solutions developed
- Code highlights

## 4. Evaluation (3 min)
- Test methodology
- Results summary
- Detection metrics

## 5. Conclusions (1 min)
- What works well
- Limitations
- Future improvements
```

<!--
Instructor Notes:

Capstone grading rubric:

Implementation (40 points):
- Multiple detection methods: 15
- Ensemble logic: 10
- Alert quality: 10
- Code quality: 5

Evaluation (30 points):
- Test methodology: 10
- Results analysis: 15
- Metrics calculation: 5

Documentation (20 points):
- Architecture clarity: 10
- Completeness: 5
- Reproducibility: 5

Presentation (10 points):
- Clarity: 5
- Demo (if applicable): 3
- Q&A: 2
-->

## Course Summary

### What We Learned

| Module | Topics | Skills Gained |
|--------|--------|---------------|
| 1 (Weeks 1-3) | CAN/NMEA 2000, Hardware | Protocol understanding, OpenBridge |
| 2 (Weeks 4-7) | Attacks | Recon, spoofing, DoS, replay |
| 3 (Weeks 9-13) | Detection | Frequency, entropy, ML, fingerprinting |
| Final | Integration | Ensemble IDS, XAI, defense arch |

### Key Takeaways

1. **CAN/NMEA 2000 is inherently vulnerable**
   - No authentication
   - Broadcast by design
   - Spoofing is trivial

2. **Defense requires depth**
   - No single method catches everything
   - Ensemble approaches are essential
   - Combine statistical, ML, and physical

3. **Explainability matters**
   - Operators need to understand alerts
   - Trust comes from transparency
   - XAI enables effective response

4. **Maritime context is unique**
   - Safety-critical environment
   - Limited connectivity at sea
   - Regulatory considerations

### Future Directions

- **NMEA 2000 Security Extensions** - Authentication proposals
- **AI/ML Advances** - Deep learning for anomaly detection
- **Autonomous Vessels** - Increased attack surface
- **Regulation** - IMO cyber security guidelines
- **Industry Collaboration** - Threat intelligence sharing

## Final Exam Information

### Format

- **Part A**: Written (40%) - Theory, analysis questions
- **Part B**: Practical (40%) - Detection implementation
- **Part C**: Capstone (20%) - Project presentation

### Topics Covered

All topics from Weeks 1-13:
- CAN bus protocol
- NMEA 2000 structure
- Attack techniques
- Detection methods
- Ensemble systems
- XAI concepts

### Allowed Materials

- One page (double-sided) notes
- PGN reference sheet (provided)
- Calculator

## Course Feedback

Please complete the course evaluation:
- [Evaluation link to be provided]

Your feedback helps improve future offerings.

## References

- [IMO Maritime Cyber Risk Management]
- [NIST Cybersecurity Framework]
- [Maritime Transportation System ICS-CERT]

[IMO Maritime Cyber Risk Management]:https://www.imo.org/en/OurWork/Security/Pages/Cyber-security.aspx
[NIST Cybersecurity Framework]:https://www.nist.gov/cyberframework
[Maritime Transportation System ICS-CERT]:https://www.cisa.gov/maritime-transportation-system

---

## Acknowledgments

This course was developed with support from:
- University of Rhode Island
- [Additional sponsors/collaborators]

Special thanks to all guest speakers and industry partners who contributed to this course.

---

**Thank you for your participation in this course!**

For questions or continued collaboration:
- Email: [instructor email]
- GitHub: [course repository]

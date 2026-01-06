---
title: "Lab 09"
subtitle: "Frequency-Based Intrusion Detection"
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
    Building and testing a frequency-based intrusion detection system
---

# Lab 09 -- Frequency-Based Intrusion Detection

## Lab Overview

**Duration**: 2 hours
**Prerequisites**: Labs 05, 08 completed, Class 09 material reviewed
**Materials Required**:
- Baseline from Lab 05
- Python 3.x with statistics library
- Access to test network

## Objectives

By the end of this lab, you will:

1. Build comprehensive frequency baseline
2. Implement real-time frequency detector
3. Test against simulated attacks
4. Calculate detection metrics (precision, recall)
5. Tune detection thresholds

## Part 1: Build Frequency Baseline (30 minutes)

### 1.1 Load Lab 05 Baseline

```python
#!/usr/bin/env python3
"""
frequency_ids.py - Frequency-based IDS
"""
import json
import statistics
from collections import defaultdict
import time

class FrequencyBaseline:
    def __init__(self, baseline_file=None):
        self.baselines = {}

        if baseline_file:
            self.load(baseline_file)

    def load(self, filename):
        """Load baseline from JSON file"""
        with open(filename) as f:
            data = json.load(f)

        # Convert string keys to tuples
        for key, stats in data.items():
            pgn, sa = map(int, key.split('_'))
            self.baselines[(pgn, sa)] = stats

        print(f"Loaded baseline for {len(self.baselines)} (PGN, SA) pairs")

    def get_stats(self, pgn, sa):
        """Get baseline stats for specific (PGN, SA)"""
        return self.baselines.get((pgn, sa))

    def print_summary(self):
        """Print baseline summary"""
        print("\nFrequency Baseline Summary")
        print("=" * 60)
        for (pgn, sa), stats in sorted(self.baselines.items()):
            print(f"PGN {pgn:6d} SA {sa:3d}: "
                  f"{stats['frequency_hz']:6.2f} Hz "
                  f"(±{stats['std_interval']*1000:.1f}ms)")

# Load your baseline
baseline = FrequencyBaseline('baseline.json')
baseline.print_summary()
```

### 1.2 Verify Baseline Coverage

Ensure baseline covers critical PGNs:

```python
critical_pgns = [
    (127250, 'Heading'),
    (129025, 'Position'),
    (129026, 'COG/SOG'),
    (130306, 'Wind'),
    (127488, 'Engine'),
]

print("\nCritical PGN Coverage:")
for pgn, name in critical_pgns:
    covered = any(p == pgn for (p, _) in baseline.baselines.keys())
    status = "✓" if covered else "✗"
    print(f"  {status} PGN {pgn} ({name})")
```

### 1.3 Extend Baseline if Needed

If missing critical PGNs, capture more data:

```bash
# Capture additional traffic
python network_capture.py -p /dev/ttyACM0 -d 600 -o extended_capture.txt

# Rebuild baseline
python frequency_profile.py extended_capture.txt extended_baseline.json
```

## Part 2: Implement Frequency Detector (30 minutes)

### 2.1 Build Real-Time Detector

```python
class FrequencyDetector:
    def __init__(self, baseline, threshold_sigma=3):
        """
        Frequency-based anomaly detector

        Args:
            baseline: FrequencyBaseline instance
            threshold_sigma: Standard deviations for alert threshold
        """
        self.baseline = baseline
        self.k = threshold_sigma

        # Track last message time per (PGN, SA)
        self.last_seen = {}
        self.interval_history = defaultdict(list)

        # Alert tracking
        self.alerts = []
        self.message_count = 0

    def process_message(self, can_id, timestamp):
        """
        Process message and check for frequency anomaly

        Returns:
            is_anomaly: True if anomaly detected
            alert: Alert dict if anomaly, None otherwise
        """
        self.message_count += 1

        # Extract PGN and SA
        pgn = (can_id >> 8) & 0x3FFFF
        sa = can_id & 0xFF
        key = (pgn, sa)

        # Get baseline stats
        stats = self.baseline.get_stats(pgn, sa)

        # Skip if no baseline
        if stats is None:
            self.last_seen[key] = timestamp
            return False, None

        # Skip first message (no interval yet)
        if key not in self.last_seen:
            self.last_seen[key] = timestamp
            return False, None

        # Calculate interval
        interval = timestamp - self.last_seen[key]
        self.last_seen[key] = timestamp

        # Ignore unreasonable intervals (> 10 seconds)
        if interval > 10:
            return False, None

        # Get expected interval and threshold
        expected = stats['mean_interval']
        std = stats.get('std_interval', expected * 0.1)

        # Calculate bounds
        lower = expected - (self.k * std)
        upper = expected + (self.k * std)

        # Check for anomaly
        if interval < lower:
            # Messages too fast
            alert = self._create_alert(
                'HIGH_RATE', pgn, sa, interval, expected, std, timestamp
            )
            return True, alert

        elif interval > upper:
            # Messages too slow
            alert = self._create_alert(
                'LOW_RATE', pgn, sa, interval, expected, std, timestamp
            )
            return True, alert

        return False, None

    def _create_alert(self, alert_type, pgn, sa, interval, expected, std, timestamp):
        """Create alert structure"""
        deviation = (interval - expected) / std if std > 0 else 0

        alert = {
            'type': alert_type,
            'pgn': pgn,
            'source_addr': sa,
            'timestamp': timestamp,
            'interval': interval,
            'expected_interval': expected,
            'deviation_sigma': deviation,
            'severity': self._calculate_severity(abs(deviation))
        }

        self.alerts.append(alert)
        return alert

    def _calculate_severity(self, deviation_sigma):
        """Calculate alert severity based on deviation"""
        if deviation_sigma > 10:
            return 'CRITICAL'
        elif deviation_sigma > 5:
            return 'HIGH'
        elif deviation_sigma > 3:
            return 'MEDIUM'
        else:
            return 'LOW'

    def get_statistics(self):
        """Get detector statistics"""
        return {
            'messages_processed': self.message_count,
            'alerts_generated': len(self.alerts),
            'alert_rate': len(self.alerts) / max(self.message_count, 1),
            'alerts_by_type': self._count_by_type()
        }

    def _count_by_type(self):
        """Count alerts by type"""
        counts = defaultdict(int)
        for alert in self.alerts:
            counts[alert['type']] += 1
        return dict(counts)
```

### 2.2 Create Processing Loop

```python
def run_detector(capture_file, baseline_file, threshold_sigma=3):
    """
    Run detector on capture file

    Args:
        capture_file: Path to captured traffic
        baseline_file: Path to baseline JSON
        threshold_sigma: Detection threshold

    Returns:
        Detector with results
    """
    # Initialize
    baseline = FrequencyBaseline(baseline_file)
    detector = FrequencyDetector(baseline, threshold_sigma)

    # Process capture
    print(f"Processing {capture_file}...")

    with open(capture_file) as f:
        for line in f:
            # Parse line (adjust for your format)
            # Expected: timestamp can_id data
            parts = line.strip().split()
            if len(parts) < 2:
                continue

            try:
                timestamp = float(parts[0].strip('()'))
                can_id = int(parts[1], 16)
            except (ValueError, IndexError):
                continue

            # Process
            is_anomaly, alert = detector.process_message(can_id, timestamp)

            if is_anomaly:
                print(f"ALERT: {alert['type']} - PGN {alert['pgn']} SA {alert['source_addr']} "
                      f"(deviation: {alert['deviation_sigma']:.1f}σ)")

    # Print summary
    stats = detector.get_statistics()
    print(f"\n{'='*50}")
    print(f"Detection Complete")
    print(f"Messages: {stats['messages_processed']}")
    print(f"Alerts: {stats['alerts_generated']}")
    print(f"Alert rate: {stats['alert_rate']*100:.3f}%")
    print(f"By type: {stats['alerts_by_type']}")

    return detector
```

## Part 3: Test Against Attacks (30 minutes)

### 3.1 Test Against Normal Traffic

First, verify low false positive rate on normal data:

```python
# Test on normal traffic
detector = run_detector('normal_capture.txt', 'baseline.json', threshold_sigma=3)

# Record results
normal_alerts = detector.get_statistics()['alerts_generated']
normal_messages = detector.get_statistics()['messages_processed']
false_positive_rate = normal_alerts / normal_messages
print(f"False positive rate: {false_positive_rate*100:.3f}%")
```

**Normal Traffic Results:**
- Messages processed: _______
- Alerts generated: _______
- False positive rate: _______ %

### 3.2 Test Against DoS Attack

Create attack capture or use from Lab 08:

```python
# Test on DoS attack capture
detector = run_detector('dos_attack_capture.txt', 'baseline.json', threshold_sigma=3)
```

**DoS Attack Results:**
- Messages processed: _______
- Alerts generated: _______
- Attack messages sent: _______
- Detection rate: _______ %

### 3.3 Test Against Spoofing Attack

Test with spoofing capture (2x rate):

```python
# Naive spoofing doubles message rate
detector = run_detector('spoofing_capture.txt', 'baseline.json', threshold_sigma=3)
```

**Spoofing Results:**
- Detected as HIGH_RATE? YES / NO
- Time to first detection: _______ seconds

### 3.4 Test Against Rate-Matched Spoofing

Challenge: Does detector catch rate-matched attack?

```python
# Smart spoofing matches baseline rate
detector = run_detector('smart_spoofing_capture.txt', 'baseline.json', threshold_sigma=3)
```

**Rate-Matched Results:**
- Detected? YES / NO
- Why or why not? _________________

## Part 4: Threshold Tuning (20 minutes)

### 4.1 Test Multiple Thresholds

```python
def evaluate_thresholds(normal_capture, attack_capture, baseline_file):
    """
    Evaluate detector at different thresholds

    Returns:
        Results for each threshold value
    """
    results = {}

    for k in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
        # Test on normal traffic
        baseline = FrequencyBaseline(baseline_file)
        normal_detector = FrequencyDetector(baseline, threshold_sigma=k)

        # Process normal
        # ... (process file)

        normal_fp = normal_detector.get_statistics()['alerts_generated']

        # Test on attack traffic
        attack_detector = FrequencyDetector(baseline, threshold_sigma=k)

        # Process attack
        # ... (process file)

        attack_tp = attack_detector.get_statistics()['alerts_generated']

        results[k] = {
            'false_positives': normal_fp,
            'true_positives': attack_tp,
            'threshold': k
        }

    return results

results = evaluate_thresholds('normal.txt', 'attack.txt', 'baseline.json')

print("\nThreshold Analysis:")
print(f"{'k':>5} | {'FP':>6} | {'TP':>6} | {'Notes'}")
print("-" * 40)
for k, r in sorted(results.items()):
    print(f"{k:5.1f} | {r['false_positives']:6d} | {r['true_positives']:6d} |")
```

### 4.2 Select Optimal Threshold

Based on your results, select threshold:

| Criterion | Value |
|-----------|-------|
| Lowest FP with >90% TP | k = ___ |
| Balanced FP/TP | k = ___ |
| Recommended for production | k = ___ |

### 4.3 ROC Curve Visualization

```python
import matplotlib.pyplot as plt

def plot_threshold_performance(results, total_normal, total_attack):
    """Plot ROC-like curve for threshold selection"""
    k_values = sorted(results.keys())

    # Calculate rates
    fpr = [results[k]['false_positives'] / total_normal for k in k_values]
    tpr = [results[k]['true_positives'] / total_attack for k in k_values]

    # Plot
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, 'b-o', linewidth=2)

    # Annotate points
    for i, k in enumerate(k_values):
        plt.annotate(f'k={k}', (fpr[i], tpr[i]), textcoords="offset points",
                    xytext=(5, 5))

    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate (Detection Rate)')
    plt.title('Frequency Detector Threshold Analysis')
    plt.grid(True)
    plt.savefig('threshold_analysis.png')
    plt.show()
```

## Part 5: Performance Metrics (10 minutes)

### 5.1 Calculate Final Metrics

With your chosen threshold:

```python
def calculate_metrics(detector, attack_labels):
    """
    Calculate detection metrics

    Args:
        detector: Detector with alerts
        attack_labels: Dict of {timestamp: True/False} indicating attacks
    """
    # Match alerts to labels
    tp = 0  # True positives
    fp = 0  # False positives

    for alert in detector.alerts:
        ts = alert['timestamp']
        # Check if this was during an attack (simplification)
        if is_attack_time(ts, attack_labels):
            tp += 1
        else:
            fp += 1

    # Calculate metrics
    total_attacks = sum(attack_labels.values())
    fn = total_attacks - tp  # Attacks we missed
    tn = len(attack_labels) - total_attacks - fp

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        'true_positives': tp,
        'false_positives': fp,
        'false_negatives': fn,
        'true_negatives': tn,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }
```

### 5.2 Record Final Results

| Metric | Value |
|--------|-------|
| Threshold (k) | |
| True Positives | |
| False Positives | |
| False Negatives | |
| Precision | |
| Recall | |
| F1 Score | |

## Deliverables

Submit via course portal:

1. **baseline.json** - Complete frequency baseline
2. **frequency_ids.py** - Your detector implementation
3. **threshold_analysis.png** - ROC curve plot
4. **Lab report** - Including all metrics tables

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Baseline complete and accurate | 20 |
| Detector implementation working | 25 |
| Attack detection tested | 20 |
| Threshold analysis complete | 20 |
| Metrics calculated correctly | 15 |
| **Total** | **100** |

## Next Lab Preview

In Lab 10, you will:
- Implement entropy-based detection
- Compare to frequency method
- Build multi-method detector
- Evaluate combined performance

---
title: "Class 09"
subtitle: "Frequency-Based Anomaly Detection"
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
    Detecting attacks through message frequency analysis
---

# Class 09 -- Frequency-Based Anomaly Detection

## Learning Outcomes

- Understand frequency as an attack indicator
- Build baseline frequency profiles
- Implement statistical anomaly detection
- Tune detection thresholds
- Evaluate detector performance

## Definitions

- **Baseline** -- Normal behavior profile for comparison
- **Anomaly** -- Deviation from expected behavior
- **False Positive** -- Incorrect alert (normal flagged as attack)
- **False Negative** -- Missed attack (attack flagged as normal)
- **Detection Rate** -- Percentage of attacks correctly identified
- **Standard Deviation** -- Statistical measure of variability

## Reading Assignment

- Literature Review: Section 4.1.1 (Frequency-Based Detection)
- Statistical anomaly detection fundamentals
- Time-series analysis basics

## Why Frequency Detection?

### The Insight

Every legitimate device transmits at a predictable rate:

| Device | PGN | Expected Rate |
|--------|-----|---------------|
| GPS | 129025 | 10 Hz ± 0.1 Hz |
| Compass | 127250 | 10 Hz ± 0.1 Hz |
| Wind | 130306 | 1 Hz ± 0.05 Hz |
| Engine | 127488 | 10 Hz ± 0.1 Hz |
| Engine | 127489 | 0.5 Hz ± 0.05 Hz |

### Attack Signatures

| Attack | Frequency Signature |
|--------|---------------------|
| DoS Flood | Rate >> baseline |
| Spoofing (naive) | Rate > baseline (2x) |
| Spoofing (smart) | Rate = baseline (hard to detect) |
| Device failure | Rate = 0 |
| Intermittent attack | Rate variance >> baseline |

<!--
Instructor Notes:

Frequency-based detection is the "low-hanging fruit":
- Easy to implement
- Low computational cost
- Catches unsophisticated attacks

Limitations:
- Smart attackers match baseline rate
- Doesn't detect content anomalies
- Requires stable baseline

This is Week 4 reconnaissance applied defensively!
We profiled the network - now we monitor for changes.
-->

## Statistical Background

### Mean and Standard Deviation

```python
import statistics

def calculate_baseline(intervals):
    """
    Calculate baseline statistics from message intervals

    Args:
        intervals: List of time intervals between messages

    Returns:
        mean, std_dev, frequency
    """
    if len(intervals) < 2:
        return None, None, None

    mean_interval = statistics.mean(intervals)
    std_interval = statistics.stdev(intervals)
    frequency = 1.0 / mean_interval if mean_interval > 0 else 0

    return mean_interval, std_interval, frequency
```

### Normal Distribution

For normally distributed data:
- 68% of values within 1σ of mean
- 95% of values within 2σ of mean
- 99.7% of values within 3σ of mean

**Detection threshold**: Alert if value > mean + k×σ

Typical k values:
- k = 2: Sensitive (more false positives)
- k = 3: Balanced
- k = 4: Conservative (fewer false positives)

## Building a Frequency Baseline

### Data Collection

```python
#!/usr/bin/env python3
"""
Frequency Baseline Builder for Maritime IDS
"""
from collections import defaultdict
import statistics
import time

class FrequencyBaseline:
    def __init__(self):
        self.message_times = defaultdict(list)  # (pgn, sa) -> [timestamps]
        self.baselines = {}  # (pgn, sa) -> {mean, std, freq}

    def record_message(self, can_id, timestamp):
        """Record message timestamp for baseline building"""
        pgn = (can_id >> 8) & 0x3FFFF
        sa = can_id & 0xFF
        key = (pgn, sa)

        self.message_times[key].append(timestamp)

    def build_baseline(self, min_samples=100):
        """Build baseline from recorded messages"""
        for key, timestamps in self.message_times.items():
            if len(timestamps) < min_samples:
                continue

            # Calculate intervals
            intervals = []
            for i in range(1, len(timestamps)):
                interval = timestamps[i] - timestamps[i-1]
                if 0 < interval < 10:  # Filter outliers
                    intervals.append(interval)

            if len(intervals) < min_samples - 1:
                continue

            # Calculate statistics
            mean_interval = statistics.mean(intervals)
            std_interval = statistics.stdev(intervals)
            frequency = 1.0 / mean_interval

            self.baselines[key] = {
                'mean_interval': mean_interval,
                'std_interval': std_interval,
                'frequency': frequency,
                'sample_count': len(intervals)
            }

        return self.baselines

    def save_baseline(self, filename):
        """Save baseline to file"""
        import json
        # Convert tuple keys to strings for JSON
        serializable = {
            f"{pgn}_{sa}": stats
            for (pgn, sa), stats in self.baselines.items()
        }
        with open(filename, 'w') as f:
            json.dump(serializable, f, indent=2)

    def load_baseline(self, filename):
        """Load baseline from file"""
        import json
        with open(filename) as f:
            data = json.load(f)
        # Convert string keys back to tuples
        self.baselines = {
            tuple(map(int, key.split('_'))): stats
            for key, stats in data.items()
        }
```

<!--
Instructor Notes:

Baseline building process:
1. Capture traffic during NORMAL operation
2. Calculate mean and std for each (PGN, SA) pair
3. Store baseline for detection

Critical questions:
- How long to capture? (30+ minutes recommended)
- What is "normal"? (No attacks, typical operation)
- How often to update? (Weekly, or after configuration changes)

Lab will collect baseline from OpenPlotter network.
-->

## Implementing Frequency Detector

### Basic Rate Monitor

```python
class FrequencyDetector:
    def __init__(self, baseline, threshold_sigma=3):
        """
        Initialize frequency-based anomaly detector

        Args:
            baseline: FrequencyBaseline instance with loaded baselines
            threshold_sigma: Number of standard deviations for alert
        """
        self.baseline = baseline.baselines
        self.k = threshold_sigma

        # Real-time tracking
        self.last_seen = {}  # (pgn, sa) -> last timestamp
        self.alerts = []

    def check_message(self, can_id, timestamp):
        """
        Check if message timing is anomalous

        Returns:
            (is_anomaly, alert_info)
        """
        pgn = (can_id >> 8) & 0x3FFFF
        sa = can_id & 0xFF
        key = (pgn, sa)

        # Skip if no baseline
        if key not in self.baseline:
            self.last_seen[key] = timestamp
            return False, None

        # Skip first message
        if key not in self.last_seen:
            self.last_seen[key] = timestamp
            return False, None

        # Calculate interval
        interval = timestamp - self.last_seen[key]
        self.last_seen[key] = timestamp

        # Get baseline stats
        stats = self.baseline[key]
        expected = stats['mean_interval']
        std = stats['std_interval']

        # Check for anomaly
        lower_bound = expected - (self.k * std)
        upper_bound = expected + (self.k * std)

        if interval < lower_bound:
            # Messages too fast
            alert = {
                'type': 'HIGH_RATE',
                'pgn': pgn,
                'sa': sa,
                'interval': interval,
                'expected': expected,
                'bound': lower_bound,
                'deviation': (expected - interval) / std
            }
            self.alerts.append(alert)
            return True, alert

        elif interval > upper_bound:
            # Messages too slow (possible device issue)
            alert = {
                'type': 'LOW_RATE',
                'pgn': pgn,
                'sa': sa,
                'interval': interval,
                'expected': expected,
                'bound': upper_bound,
                'deviation': (interval - expected) / std
            }
            self.alerts.append(alert)
            return True, alert

        return False, None
```

### Window-Based Rate Detection

```python
class WindowRateDetector:
    def __init__(self, baseline, window_sec=1.0, threshold_sigma=3):
        """
        Window-based rate detector

        Counts messages per window instead of checking intervals
        """
        self.baseline = baseline.baselines
        self.k = threshold_sigma
        self.window_sec = window_sec

        # Per-key tracking
        self.window_counts = defaultdict(int)
        self.window_start = {}

    def check_message(self, can_id, timestamp):
        """Check message rate in sliding window"""
        pgn = (can_id >> 8) & 0x3FFFF
        sa = can_id & 0xFF
        key = (pgn, sa)

        # Initialize window
        if key not in self.window_start:
            self.window_start[key] = timestamp
            self.window_counts[key] = 1
            return False, None

        # Check if window complete
        window_elapsed = timestamp - self.window_start[key]
        self.window_counts[key] += 1

        if window_elapsed >= self.window_sec:
            # Window complete - check rate
            rate = self.window_counts[key] / window_elapsed

            # Get expected rate
            if key in self.baseline:
                expected_rate = self.baseline[key]['frequency']
                # Estimate std of rate from interval std
                rate_std = expected_rate * (
                    self.baseline[key]['std_interval'] /
                    self.baseline[key]['mean_interval']
                )

                # Check bounds
                lower = expected_rate - (self.k * rate_std)
                upper = expected_rate + (self.k * rate_std)

                # Reset window
                self.window_start[key] = timestamp
                self.window_counts[key] = 0

                if rate < lower or rate > upper:
                    return True, {
                        'type': 'RATE_ANOMALY',
                        'pgn': pgn,
                        'sa': sa,
                        'rate': rate,
                        'expected': expected_rate,
                        'bounds': (lower, upper)
                    }

            # Reset window
            self.window_start[key] = timestamp
            self.window_counts[key] = 0

        return False, None
```

<!--
Instructor Notes:

Two approaches:
1. Interval-based: Check each message timing
2. Window-based: Count messages per time window

Interval-based:
- More precise
- Catches single anomalies
- More computationally intensive

Window-based:
- Smooths out jitter
- Better for rate flooding
- Less sensitive to single delays

In practice, use both or window-based for efficiency.
-->

## Detection Threshold Tuning

### The Trade-off

```
Higher k (threshold):
├── Fewer false positives
├── More false negatives
└── Misses subtle attacks

Lower k (threshold):
├── More false positives
├── Fewer false negatives
└── Catches subtle attacks
```

### Threshold Selection

```python
def evaluate_threshold(detector, test_data, labels, k_values):
    """
    Evaluate detector at different thresholds

    Args:
        detector: FrequencyDetector instance
        test_data: List of (can_id, timestamp) tuples
        labels: List of True (attack) / False (normal)
        k_values: List of k values to test

    Returns:
        Results for each k value
    """
    results = {}

    for k in k_values:
        detector.k = k
        detector.alerts = []

        # Reset detector state
        detector.last_seen = {}

        # Process test data
        predictions = []
        for (can_id, ts), label in zip(test_data, labels):
            is_anomaly, _ = detector.check_message(can_id, ts)
            predictions.append(is_anomaly)

        # Calculate metrics
        tp = sum(1 for p, l in zip(predictions, labels) if p and l)
        fp = sum(1 for p, l in zip(predictions, labels) if p and not l)
        tn = sum(1 for p, l in zip(predictions, labels) if not p and not l)
        fn = sum(1 for p, l in zip(predictions, labels) if not p and l)

        results[k] = {
            'true_positive': tp,
            'false_positive': fp,
            'true_negative': tn,
            'false_negative': fn,
            'precision': tp / (tp + fp) if (tp + fp) > 0 else 0,
            'recall': tp / (tp + fn) if (tp + fn) > 0 else 0,
            'accuracy': (tp + tn) / len(labels)
        }

    return results
```

### ROC Curve Analysis

```python
import matplotlib.pyplot as plt

def plot_roc_curve(results):
    """Plot ROC curve from threshold evaluation"""
    k_values = sorted(results.keys())

    # Calculate TPR and FPR
    tpr = []  # True Positive Rate (Recall)
    fpr = []  # False Positive Rate

    for k in k_values:
        r = results[k]
        tpr.append(r['recall'])
        fpr.append(r['false_positive'] / (r['false_positive'] + r['true_negative'])
                   if (r['false_positive'] + r['true_negative']) > 0 else 0)

    # Plot
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, 'b-', linewidth=2)
    plt.plot([0, 1], [0, 1], 'r--')  # Random classifier line

    # Annotate k values
    for i, k in enumerate(k_values):
        plt.annotate(f'k={k}', (fpr[i], tpr[i]))

    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate (Recall)')
    plt.title('ROC Curve - Frequency Detector')
    plt.grid(True)
    plt.savefig('roc_curve.png')
    plt.close()
```

<!--
Instructor Notes:

ROC curve interpretation:
- Upper left corner = best (high TPR, low FPR)
- Diagonal line = random guessing
- Area Under Curve (AUC) = overall performance

For maritime IDS:
- Safety critical = prioritize recall (catch all attacks)
- Accept more false positives
- Human validation of alerts

Typical recommendation: k=3 as starting point,
then tune based on operational feedback.
-->

## Multi-PGN Correlation

### Detecting Smart Attackers

Smart attackers match baseline rate for target PGN.
But they may create anomalies elsewhere:

```python
class CorrelatedDetector:
    def __init__(self, baseline, threshold_sigma=3):
        self.baseline = baseline.baselines
        self.k = threshold_sigma
        self.device_rates = defaultdict(list)  # sa -> [recent rates]

    def check_device_correlation(self, sa, window_sec=10):
        """
        Check if device's PGN rates are internally consistent

        A device should have consistent relative rates between PGNs
        """
        # Get all PGNs for this device
        device_pgns = [
            (pgn, src) for (pgn, src) in self.baseline.keys()
            if src == sa
        ]

        if len(device_pgns) < 2:
            return False, None

        # Calculate current rate ratios vs baseline ratios
        current_ratios = []
        baseline_ratios = []

        for i, (pgn1, _) in enumerate(device_pgns):
            for pgn2, _ in device_pgns[i+1:]:
                # Get baseline ratio
                baseline_ratio = (
                    self.baseline[(pgn1, sa)]['frequency'] /
                    self.baseline[(pgn2, sa)]['frequency']
                )
                baseline_ratios.append(baseline_ratio)

                # Get current ratio (from recent rates)
                # ... implementation ...

        # Compare ratios - significant deviation indicates attack
        return False, None
```

### Example: GPS vs Heading Correlation

Normal relationship:
- PGN 129025 (Position): 10 Hz
- PGN 127250 (Heading): 10 Hz
- Ratio: 1.0

If attacker spoofs position at 10 Hz:
- Position: 20 Hz total (legitimate + spoofed)
- Heading: 10 Hz (unchanged)
- Ratio: 2.0 → Anomaly!

## Real-Time Implementation

### Efficient Processing

```python
class EfficientFrequencyMonitor:
    def __init__(self, baseline_file):
        """Production-ready frequency monitor"""
        # Load baseline
        self.baseline = self._load_baseline(baseline_file)

        # Fixed-size sliding windows for efficiency
        self.window_size = 100  # messages
        self.windows = {}

        # Alert rate limiting
        self.alert_cooldown = {}
        self.cooldown_seconds = 60

    def process_message(self, can_id, timestamp):
        """Process message with O(1) complexity"""
        pgn = (can_id >> 8) & 0x3FFFF
        sa = can_id & 0xFF
        key = (pgn, sa)

        # Skip unknown PGNs
        if key not in self.baseline:
            return None

        # Update sliding window (circular buffer)
        if key not in self.windows:
            self.windows[key] = {
                'timestamps': [0.0] * self.window_size,
                'index': 0,
                'full': False
            }

        w = self.windows[key]
        w['timestamps'][w['index']] = timestamp
        w['index'] = (w['index'] + 1) % self.window_size
        if w['index'] == 0:
            w['full'] = True

        # Only check when window full
        if not w['full']:
            return None

        # Calculate rate from window
        oldest_idx = w['index']
        newest_idx = (w['index'] - 1) % self.window_size
        duration = w['timestamps'][newest_idx] - w['timestamps'][oldest_idx]

        if duration <= 0:
            return None

        rate = self.window_size / duration

        # Check against baseline
        expected = self.baseline[key]['frequency']
        threshold = self.baseline[key]['threshold']

        if abs(rate - expected) > threshold:
            # Check cooldown
            if self._check_cooldown(key, timestamp):
                return {
                    'timestamp': timestamp,
                    'pgn': pgn,
                    'sa': sa,
                    'rate': rate,
                    'expected': expected,
                    'severity': self._calculate_severity(rate, expected, threshold)
                }

        return None

    def _check_cooldown(self, key, timestamp):
        """Rate limit alerts per (pgn, sa)"""
        if key in self.alert_cooldown:
            if timestamp - self.alert_cooldown[key] < self.cooldown_seconds:
                return False
        self.alert_cooldown[key] = timestamp
        return True

    def _calculate_severity(self, rate, expected, threshold):
        """Calculate alert severity"""
        deviation = abs(rate - expected) / threshold
        if deviation > 5:
            return 'CRITICAL'
        elif deviation > 3:
            return 'HIGH'
        elif deviation > 2:
            return 'MEDIUM'
        else:
            return 'LOW'
```

<!--
Instructor Notes:

Production considerations:
1. Memory: Fixed-size windows, not growing lists
2. CPU: O(1) per message, circular buffer
3. Alert fatigue: Cooldown prevents flooding
4. Severity levels: Help prioritize response

Performance targets:
- 10,000 messages/second on commodity hardware
- <1ms latency per check
- <100MB memory for 1000 PGN/SA combinations
-->

## Lab Preview: Week 9

In Lab 09, you will:

1. Collect baseline from test network (30 minutes)
2. Implement FrequencyDetector class
3. Test against simulated attacks:
   - 2x rate spoofing
   - DoS flooding
   - Smart rate-matched spoofing
4. Calculate detection metrics
5. Tune threshold for optimal performance

**Evaluation**: ROC curve, precision, recall

## Homework

### Required

1. **Read**: Literature Review Section 4.1.1 completely
2. **Implement**: Basic frequency detector with configurable k
3. **Analyze**: What attacks does frequency detection miss?

### Suggested

- Research: CUSUM algorithm for change detection
- Explore: scikit-learn anomaly detection
- Consider: How would you detect gradual rate changes?

## Discussion Questions

1. Why is frequency detection effective against unsophisticated attackers?
2. How could an attacker evade frequency-based detection?
3. What is the impact of network jitter on detection accuracy?
4. Should frequency thresholds be static or adaptive?

## References

- [Statistical Process Control]
- [Time Series Anomaly Detection]
- [Maritime IDS Research]

[Statistical Process Control]:https://en.wikipedia.org/wiki/Statistical_process_control
[Time Series Anomaly Detection]:https://www.sciencedirect.com
[Maritime IDS Research]:https://www.sciencedirect.com

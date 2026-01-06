---
title: "Lab 10"
subtitle: "Entropy-Based Intrusion Detection"
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
    Implementing entropy analysis for CAN bus attack detection
---

# Lab 10 -- Entropy-Based Intrusion Detection

## Lab Overview

**Duration**: 2 hours
**Prerequisites**: Labs 05, 09 completed, Class 10 material reviewed
**Materials Required**:
- Baseline from Lab 05
- Python 3.x with math library
- Attack captures from Labs 06-08

## Objectives

By the end of this lab, you will:

1. Calculate Shannon entropy for CAN traffic
2. Build entropy baseline from normal traffic
3. Implement sliding window entropy detector
4. Compare detection to frequency-based method
5. Analyze complementary detection capabilities

## Part 1: Entropy Calculation (25 minutes)

### 1.1 Implement Shannon Entropy

```python
#!/usr/bin/env python3
"""
entropy_ids.py - Entropy-based IDS
"""
import math
from collections import Counter

def shannon_entropy(values):
    """
    Calculate Shannon entropy of value distribution

    Args:
        values: List of values (CAN IDs, bytes, etc.)

    Returns:
        Entropy in bits
    """
    if not values:
        return 0.0

    # Count occurrences
    counter = Counter(values)
    total = len(values)

    # Calculate entropy
    entropy = 0.0
    for count in counter.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)

    return entropy

def normalized_entropy(values, max_unique=None):
    """
    Calculate normalized entropy (0-1 range)

    Args:
        values: List of values
        max_unique: Maximum possible unique values

    Returns:
        Normalized entropy (0 = single value, 1 = uniform distribution)
    """
    if not values:
        return 0.0

    raw_entropy = shannon_entropy(values)

    if max_unique is None:
        max_unique = len(set(values))

    if max_unique <= 1:
        return 0.0

    max_entropy = math.log2(max_unique)
    return raw_entropy / max_entropy if max_entropy > 0 else 0.0
```

### 1.2 Test Entropy Calculation

Verify your implementation:

```python
# Test cases
test_cases = [
    ([1, 1, 1, 1], "All same"),          # Entropy = 0
    ([1, 2], "Two values, equal"),        # Entropy = 1.0
    ([1, 1, 1, 2], "Biased"),            # Entropy < 1.0
    ([1, 2, 3, 4], "Four values, equal"), # Entropy = 2.0
]

print("Entropy Test Cases:")
print("=" * 50)
for values, description in test_cases:
    h = shannon_entropy(values)
    h_norm = normalized_entropy(values)
    print(f"{description:25s}: H={h:.3f} bits, H_norm={h_norm:.3f}")
```

**Expected results:**
- All same: H = 0.000 bits
- Two equal: H = 1.000 bits
- Four equal: H = 2.000 bits

### 1.3 Calculate Traffic Entropy Types

Implement entropy for different traffic aspects:

```python
def calculate_can_id_entropy(messages, window_size=100):
    """Calculate entropy of CAN IDs in window"""
    can_ids = [msg['can_id'] for msg in messages[-window_size:]]
    return shannon_entropy(can_ids)

def calculate_pgn_entropy(messages, window_size=100):
    """Calculate entropy of PGNs in window"""
    pgns = [(msg['can_id'] >> 8) & 0x3FFFF for msg in messages[-window_size:]]
    return shannon_entropy(pgns)

def calculate_sa_entropy(messages, window_size=100):
    """Calculate entropy of Source Addresses in window"""
    sas = [msg['can_id'] & 0xFF for msg in messages[-window_size:]]
    return shannon_entropy(sas)

def calculate_data_entropy(messages, window_size=100):
    """Calculate entropy of data bytes"""
    all_bytes = []
    for msg in messages[-window_size:]:
        all_bytes.extend(msg['data'])
    return shannon_entropy(all_bytes)
```

## Part 2: Build Entropy Baseline (25 minutes)

### 2.1 Calculate Baseline Entropy

```python
class EntropyBaseline:
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.baselines = {
            'can_id': {'values': [], 'mean': 0, 'std': 0},
            'pgn': {'values': [], 'mean': 0, 'std': 0},
            'sa': {'values': [], 'mean': 0, 'std': 0},
            'data': {'values': [], 'mean': 0, 'std': 0}
        }

    def add_sample(self, messages):
        """Add entropy sample from message window"""
        if len(messages) < self.window_size:
            return

        self.baselines['can_id']['values'].append(
            calculate_can_id_entropy(messages, self.window_size))
        self.baselines['pgn']['values'].append(
            calculate_pgn_entropy(messages, self.window_size))
        self.baselines['sa']['values'].append(
            calculate_sa_entropy(messages, self.window_size))
        self.baselines['data']['values'].append(
            calculate_data_entropy(messages, self.window_size))

    def calculate_stats(self):
        """Calculate baseline statistics"""
        import statistics

        for key in self.baselines:
            values = self.baselines[key]['values']
            if len(values) > 1:
                self.baselines[key]['mean'] = statistics.mean(values)
                self.baselines[key]['std'] = statistics.stdev(values)
            elif len(values) == 1:
                self.baselines[key]['mean'] = values[0]
                self.baselines[key]['std'] = values[0] * 0.1  # Estimate

    def save(self, filename):
        """Save baseline to JSON"""
        import json
        # Remove raw values, keep only stats
        output = {}
        for key, stats in self.baselines.items():
            output[key] = {
                'mean': stats['mean'],
                'std': stats['std'],
                'sample_count': len(stats['values'])
            }
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)

    def load(self, filename):
        """Load baseline from JSON"""
        import json
        with open(filename) as f:
            data = json.load(f)
        for key, stats in data.items():
            if key in self.baselines:
                self.baselines[key]['mean'] = stats['mean']
                self.baselines[key]['std'] = stats['std']
```

### 2.2 Build Baseline from Capture

```python
def build_entropy_baseline(capture_file, window_size=100, step_size=50):
    """
    Build entropy baseline from capture file

    Args:
        capture_file: Path to normal traffic capture
        window_size: Entropy window size
        step_size: Slide step between windows

    Returns:
        EntropyBaseline instance
    """
    baseline = EntropyBaseline(window_size)
    messages = []

    print(f"Building entropy baseline from {capture_file}")
    print(f"Window size: {window_size}, Step: {step_size}")

    with open(capture_file) as f:
        for line in f:
            # Parse message (adjust for your format)
            msg = parse_message(line)
            if msg:
                messages.append(msg)

                # Add sample when we have enough messages
                if len(messages) >= window_size and len(messages) % step_size == 0:
                    baseline.add_sample(messages)

    baseline.calculate_stats()

    print(f"\nBaseline Statistics:")
    for key, stats in baseline.baselines.items():
        print(f"  {key:10s}: mean={stats['mean']:.3f}, std={stats['std']:.3f}")

    return baseline

# Build baseline
baseline = build_entropy_baseline('normal_capture.txt')
baseline.save('entropy_baseline.json')
```

### 2.3 Record Baseline Values

| Entropy Type | Mean | Std Dev | Samples |
|--------------|------|---------|---------|
| CAN ID | | | |
| PGN | | | |
| Source Address | | | |
| Data Bytes | | | |

## Part 3: Implement Entropy Detector (30 minutes)

### 3.1 Build Real-Time Detector

```python
class EntropyDetector:
    def __init__(self, baseline, window_size=100, threshold_sigma=3):
        """
        Entropy-based anomaly detector

        Args:
            baseline: EntropyBaseline instance
            window_size: Sliding window size
            threshold_sigma: Detection threshold in standard deviations
        """
        self.baseline = baseline.baselines
        self.window_size = window_size
        self.k = threshold_sigma

        # Message buffer
        self.messages = []

        # Alert tracking
        self.alerts = []
        self.message_count = 0

    def process_message(self, can_id, data, timestamp):
        """
        Process message and check entropy anomaly

        Returns:
            alerts: List of triggered alerts (may be empty)
        """
        self.message_count += 1

        # Add to buffer
        self.messages.append({
            'can_id': can_id,
            'data': data,
            'timestamp': timestamp
        })

        # Maintain window
        if len(self.messages) > self.window_size * 2:
            self.messages = self.messages[-self.window_size * 2:]

        # Check only when window full
        if len(self.messages) < self.window_size:
            return []

        # Check every window_size/4 messages
        if self.message_count % (self.window_size // 4) != 0:
            return []

        return self._check_entropy(timestamp)

    def _check_entropy(self, timestamp):
        """Check all entropy types against baseline"""
        alerts = []

        # Calculate current entropies
        current = {
            'can_id': calculate_can_id_entropy(self.messages, self.window_size),
            'pgn': calculate_pgn_entropy(self.messages, self.window_size),
            'sa': calculate_sa_entropy(self.messages, self.window_size),
            'data': calculate_data_entropy(self.messages, self.window_size)
        }

        # Check each against baseline
        for key, value in current.items():
            stats = self.baseline.get(key, {})
            mean = stats.get('mean', value)
            std = stats.get('std', 0.1)

            # Calculate deviation
            deviation = (value - mean) / std if std > 0 else 0

            # Check threshold
            if abs(deviation) > self.k:
                alert_type = 'LOW_ENTROPY' if deviation < 0 else 'HIGH_ENTROPY'
                alert = {
                    'type': alert_type,
                    'entropy_type': key,
                    'timestamp': timestamp,
                    'value': value,
                    'baseline_mean': mean,
                    'baseline_std': std,
                    'deviation_sigma': deviation,
                    'severity': self._severity(abs(deviation))
                }
                alerts.append(alert)
                self.alerts.append(alert)

        return alerts

    def _severity(self, deviation):
        if deviation > 10:
            return 'CRITICAL'
        elif deviation > 5:
            return 'HIGH'
        else:
            return 'MEDIUM'

    def get_statistics(self):
        """Get detection statistics"""
        by_type = {}
        for alert in self.alerts:
            key = f"{alert['type']}_{alert['entropy_type']}"
            by_type[key] = by_type.get(key, 0) + 1

        return {
            'messages_processed': self.message_count,
            'alerts_generated': len(self.alerts),
            'alerts_by_type': by_type
        }
```

### 3.2 Test Detector on Normal Traffic

```python
# Load baseline and create detector
baseline = EntropyBaseline(window_size=100)
baseline.load('entropy_baseline.json')

detector = EntropyDetector(baseline, window_size=100, threshold_sigma=3)

# Process normal traffic
with open('normal_capture.txt') as f:
    for line in f:
        msg = parse_message(line)
        if msg:
            alerts = detector.process_message(
                msg['can_id'], msg['data'], msg['timestamp']
            )
            for alert in alerts:
                print(f"Alert: {alert['type']} ({alert['entropy_type']})")

stats = detector.get_statistics()
print(f"\nNormal traffic: {stats['alerts_generated']} alerts")
```

## Part 4: Test Against Attacks (25 minutes)

### 4.1 Test Against DoS Attack

```python
# Reset detector
detector = EntropyDetector(baseline, window_size=100, threshold_sigma=3)

# Process DoS capture
print("Testing DoS attack...")
with open('dos_attack_capture.txt') as f:
    for line in f:
        msg = parse_message(line)
        if msg:
            alerts = detector.process_message(
                msg['can_id'], msg['data'], msg['timestamp']
            )
            for alert in alerts:
                print(f"  {alert['type']}: {alert['entropy_type']} "
                      f"({alert['deviation_sigma']:.1f}σ)")

stats = detector.get_statistics()
print(f"DoS detection: {stats['alerts_by_type']}")
```

**Expected DoS signature:**
- LOW_ENTROPY for CAN ID (flooding single ID)
- LOW_ENTROPY for PGN (single PGN dominates)

**Record results:**
- Entropy drop detected? YES / NO
- Alert type(s): _________________
- Detection delay: _______ messages

### 4.2 Test Against Spoofing Attack

```python
# Process spoofing capture
detector = EntropyDetector(baseline, window_size=100, threshold_sigma=3)

print("Testing spoofing attack...")
# ... process spoofing capture
```

**Spoofing signature:**
- May see HIGH_ENTROPY (new values)
- Or NO change if well-crafted

**Results:**
- Entropy change detected? YES / NO
- Alert type: _________________

### 4.3 Test Against Replay Attack

```python
# Process replay capture
detector = EntropyDetector(baseline, window_size=100, threshold_sigma=3)

print("Testing replay attack...")
# ... process replay capture
```

**Replay signature:**
- May see LOW_ENTROPY in data (repeated values)
- Or lower variance in entropy over time

**Results:**
- Entropy change detected? YES / NO
- Data entropy affected? YES / NO

### 4.4 Results Summary

| Attack | CAN ID Entropy | PGN Entropy | Data Entropy | Detected? |
|--------|----------------|-------------|--------------|-----------|
| DoS | ↓ / ↑ / = | ↓ / ↑ / = | ↓ / ↑ / = | |
| Spoofing | ↓ / ↑ / = | ↓ / ↑ / = | ↓ / ↑ / = | |
| Replay | ↓ / ↑ / = | ↓ / ↑ / = | ↓ / ↑ / = | |

## Part 5: Compare to Frequency Detection (15 minutes)

### 5.1 Run Both Detectors

```python
def compare_detectors(capture_file, freq_baseline, entropy_baseline):
    """Compare frequency and entropy detectors"""

    from frequency_ids import FrequencyDetector, FrequencyBaseline

    # Initialize both
    freq_detector = FrequencyDetector(freq_baseline, threshold_sigma=3)
    ent_detector = EntropyDetector(entropy_baseline, window_size=100, threshold_sigma=3)

    freq_alerts = []
    ent_alerts = []

    with open(capture_file) as f:
        for line in f:
            msg = parse_message(line)
            if msg:
                # Frequency detection
                is_anom, alert = freq_detector.process_message(
                    msg['can_id'], msg['timestamp']
                )
                if is_anom:
                    freq_alerts.append(alert)

                # Entropy detection
                alerts = ent_detector.process_message(
                    msg['can_id'], msg['data'], msg['timestamp']
                )
                ent_alerts.extend(alerts)

    return {
        'frequency': len(freq_alerts),
        'entropy': len(ent_alerts),
        'both': len(set(a['timestamp'] for a in freq_alerts) &
                    set(a['timestamp'] for a in ent_alerts))
    }
```

### 5.2 Comparison Results

| Attack | Frequency Detects | Entropy Detects | Both Detect |
|--------|-------------------|-----------------|-------------|
| DoS | | | |
| Spoofing (naive) | | | |
| Spoofing (smart) | | | |
| Replay | | | |

### 5.3 Analysis Questions

1. Which attacks does entropy catch that frequency misses?
2. Which attacks does frequency catch that entropy misses?
3. Why is combining both methods beneficial?

## Deliverables

Submit via course portal:

1. **entropy_ids.py** - Your implementation
2. **entropy_baseline.json** - Baseline data
3. **Comparison table** - Frequency vs Entropy results
4. **Lab report** - Including analysis

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Entropy correctly implemented | 20 |
| Baseline built and saved | 20 |
| Detector working | 20 |
| Attack detection tested | 25 |
| Comparison analysis | 15 |
| **Total** | **100** |

## Next Lab Preview

In Lab 11, you will:
- Implement ML-based detection
- Train SVM and Random Forest models
- Build LSTM autoencoder
- Compare all detection methods

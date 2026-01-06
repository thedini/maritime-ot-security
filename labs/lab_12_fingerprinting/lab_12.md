---
title: "Lab 12"
subtitle: "Device Fingerprinting"
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
    Implementing clock skew analysis for device identification
---

# Lab 12 -- Device Fingerprinting

## Lab Overview

**Duration**: 2 hours
**Prerequisites**: Labs 09-11 completed, Class 12 material reviewed
**Materials Required**:
- Extended capture (10+ minutes) from test network
- Python 3.x with scipy
- Multiple active devices on test network

## Objectives

By the end of this lab, you will:

1. Understand clock skew measurement
2. Calculate device fingerprints from timing data
3. Build fingerprint enrollment database
4. Detect device impersonation
5. Evaluate fingerprint accuracy

## Part 1: Clock Skew Analysis (30 minutes)

### 1.1 Understand Clock Skew

Each device has a crystal oscillator with unique characteristics:
- Nominal frequency: 16.000 MHz (or 8.000 MHz)
- Actual frequency: 16.000800 MHz (example)
- Skew: +50 ppm (parts per million)

This skew manifests in message timing.

### 1.2 Implement Clock Skew Calculator

```python
#!/usr/bin/env python3
"""
fingerprint.py - Device fingerprinting via clock skew
"""
import numpy as np
from scipy import stats
from collections import defaultdict
import json

class ClockSkewAnalyzer:
    def __init__(self):
        """
        Analyze clock skew for each device (Source Address)
        """
        self.device_data = defaultdict(lambda: {
            'timestamps': [],
            'intervals': [],
            'pgns': set()
        })

    def add_message(self, source_addr, pgn, timestamp):
        """
        Record message for clock skew analysis

        Args:
            source_addr: Device source address
            pgn: Parameter Group Number
            timestamp: Message arrival time (reference clock)
        """
        data = self.device_data[source_addr]
        data['pgns'].add(pgn)

        if data['timestamps']:
            interval = timestamp - data['timestamps'][-1]
            if 0 < interval < 10:  # Filter outliers
                data['intervals'].append(interval)

        data['timestamps'].append(timestamp)

    def calculate_skew(self, source_addr, expected_interval=0.1, min_samples=100):
        """
        Calculate clock skew for device

        The key insight: if device sends at 10 Hz but its clock is fast,
        messages arrive slightly faster than expected from our reference.

        Args:
            source_addr: Device to analyze
            expected_interval: Expected message interval (e.g., 0.1s for 10Hz)
            min_samples: Minimum samples needed

        Returns:
            skew_ppm: Clock skew in parts per million
            confidence: R-squared of linear fit
            stats: Additional statistics
        """
        data = self.device_data.get(source_addr)
        if data is None or len(data['intervals']) < min_samples:
            return None, None, None

        intervals = np.array(data['intervals'])

        # Calculate mean interval
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)

        # Skew = (observed - expected) / expected
        # Positive skew = device clock is fast (messages arrive faster)
        skew = (mean_interval - expected_interval) / expected_interval
        skew_ppm = skew * 1e6

        # Linear regression for confidence
        # If timing is consistent, R^2 will be high
        x = np.arange(len(intervals))
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            x, np.cumsum(intervals)
        )
        confidence = r_value ** 2

        return skew_ppm, confidence, {
            'mean_interval': mean_interval,
            'std_interval': std_interval,
            'sample_count': len(intervals),
            'pgn_count': len(data['pgns'])
        }

    def analyze_all_devices(self, expected_intervals=None):
        """
        Analyze all devices in capture

        Args:
            expected_intervals: Dict of SA -> expected interval
                               If None, uses median interval

        Returns:
            Dict of fingerprints per device
        """
        results = {}

        for sa in self.device_data.keys():
            # Determine expected interval
            if expected_intervals and sa in expected_intervals:
                expected = expected_intervals[sa]
            else:
                # Use median of observed intervals
                intervals = self.device_data[sa]['intervals']
                if len(intervals) < 10:
                    continue
                expected = np.median(intervals)

            skew, confidence, stats = self.calculate_skew(
                sa, expected_interval=expected, min_samples=50
            )

            if skew is not None:
                results[sa] = {
                    'skew_ppm': skew,
                    'confidence': confidence,
                    **stats
                }

        return results
```

### 1.3 Process Capture File

```python
def analyze_capture(capture_file):
    """Analyze capture for device fingerprints"""
    analyzer = ClockSkewAnalyzer()

    print(f"Processing {capture_file}...")
    message_count = 0

    with open(capture_file) as f:
        for line in f:
            msg = parse_message(line)  # Use your parser
            if msg:
                sa = msg['can_id'] & 0xFF
                pgn = (msg['can_id'] >> 8) & 0x3FFFF
                analyzer.add_message(sa, pgn, msg['timestamp'])
                message_count += 1

    print(f"Processed {message_count} messages")
    print(f"Found {len(analyzer.device_data)} devices")

    # Analyze
    results = analyzer.analyze_all_devices()

    print("\nDevice Fingerprints:")
    print("=" * 70)
    print(f"{'SA':>4} | {'Skew (ppm)':>12} | {'Confidence':>10} | {'Samples':>8} | PGNs")
    print("-" * 70)

    for sa in sorted(results.keys()):
        fp = results[sa]
        print(f"{sa:4d} | {fp['skew_ppm']:12.2f} | {fp['confidence']:10.4f} | "
              f"{fp['sample_count']:8d} | {fp['pgn_count']}")

    return results

# Analyze your capture
fingerprints = analyze_capture('extended_capture.txt')
```

### 1.4 Record Device Fingerprints

| SA | Skew (ppm) | Confidence | Interval Mean | Samples |
|----|------------|------------|---------------|---------|
| | | | | |
| | | | | |
| | | | | |

## Part 2: Build Fingerprint Database (25 minutes)

### 2.1 Implement Fingerprint Database

```python
class FingerprintDatabase:
    def __init__(self):
        """
        Database of enrolled device fingerprints
        """
        self.fingerprints = {}

    def enroll(self, source_addr, fingerprint, device_name=None, notes=None):
        """
        Enroll device in database

        Args:
            source_addr: Device source address
            fingerprint: Dict from ClockSkewAnalyzer
            device_name: Human-readable name
            notes: Additional notes
        """
        import time

        self.fingerprints[source_addr] = {
            **fingerprint,
            'device_name': device_name or f"Device_{source_addr}",
            'notes': notes,
            'enrolled': time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'active'
        }

        print(f"Enrolled SA {source_addr}: {device_name}")
        print(f"  Skew: {fingerprint['skew_ppm']:.2f} ppm")
        print(f"  Confidence: {fingerprint['confidence']:.4f}")

    def verify(self, source_addr, current_fingerprint, tolerance_ppm=10):
        """
        Verify device matches enrolled fingerprint

        Args:
            source_addr: Device to verify
            current_fingerprint: Current calculated fingerprint
            tolerance_ppm: Maximum allowed skew difference

        Returns:
            match: True if device matches
            confidence: Match confidence score
            details: Comparison details
        """
        enrolled = self.fingerprints.get(source_addr)

        if enrolled is None:
            return None, 0, {'error': 'Device not enrolled'}

        # Calculate skew difference
        enrolled_skew = enrolled['skew_ppm']
        current_skew = current_fingerprint['skew_ppm']
        skew_diff = abs(enrolled_skew - current_skew)

        # Match if within tolerance
        match = skew_diff <= tolerance_ppm

        # Confidence based on how close the match is
        confidence = max(0, 1 - (skew_diff / tolerance_ppm)) if tolerance_ppm > 0 else 0

        details = {
            'enrolled_skew': enrolled_skew,
            'current_skew': current_skew,
            'skew_difference': skew_diff,
            'tolerance': tolerance_ppm,
            'enrolled_date': enrolled['enrolled']
        }

        return match, confidence, details

    def save(self, filename):
        """Save database to JSON"""
        with open(filename, 'w') as f:
            json.dump(self.fingerprints, f, indent=2)
        print(f"Saved {len(self.fingerprints)} fingerprints to {filename}")

    def load(self, filename):
        """Load database from JSON"""
        with open(filename) as f:
            self.fingerprints = json.load(f)
        # Convert string keys to int
        self.fingerprints = {int(k): v for k, v in self.fingerprints.items()}
        print(f"Loaded {len(self.fingerprints)} fingerprints from {filename}")
```

### 2.2 Enroll Devices

```python
# Create database and enroll devices
db = FingerprintDatabase()

# Enroll each device from fingerprints
device_names = {
    36: "GPS Unit",
    42: "Wind Sensor",
    24: "Autopilot",
    # Add your devices
}

for sa, fp in fingerprints.items():
    name = device_names.get(sa, f"Unknown_{sa}")
    db.enroll(sa, fp, device_name=name)

# Save database
db.save('fingerprint_db.json')
```

### 2.3 Enrollment Report

Create enrollment report:

```markdown
# Device Fingerprint Enrollment Report

## Enrollment Date: ___________
## Capture Duration: ___ minutes
## Devices Enrolled: ___

### Device Inventory

| SA | Name | Skew (ppm) | Confidence | Status |
|----|------|------------|------------|--------|
| | | | | |
| | | | | |
```

## Part 3: Impersonation Detection (30 minutes)

### 3.1 Build Impersonation Detector

```python
class ImpersonationDetector:
    def __init__(self, fingerprint_db, tolerance_ppm=10, window_size=100):
        """
        Detect device impersonation via fingerprint mismatch

        Args:
            fingerprint_db: FingerprintDatabase instance
            tolerance_ppm: Match tolerance
            window_size: Messages needed for verification
        """
        self.db = fingerprint_db
        self.tolerance = tolerance_ppm
        self.window_size = window_size

        # Per-device message buffers
        self.device_buffers = defaultdict(lambda: {
            'timestamps': [],
            'intervals': []
        })

        # Alerts
        self.alerts = []

    def process_message(self, can_id, timestamp):
        """
        Process message and check fingerprint

        Returns:
            alert: Alert dict if impersonation detected, None otherwise
        """
        sa = can_id & 0xFF

        # Update buffer
        buf = self.device_buffers[sa]
        if buf['timestamps']:
            interval = timestamp - buf['timestamps'][-1]
            if 0 < interval < 10:
                buf['intervals'].append(interval)
        buf['timestamps'].append(timestamp)

        # Maintain window
        if len(buf['intervals']) > self.window_size * 2:
            buf['intervals'] = buf['intervals'][-self.window_size:]
            buf['timestamps'] = buf['timestamps'][-self.window_size:]

        # Check periodically when we have enough data
        if len(buf['intervals']) >= self.window_size:
            if len(buf['intervals']) % (self.window_size // 2) == 0:
                return self._verify_device(sa, timestamp)

        return None

    def _verify_device(self, sa, timestamp):
        """Verify device fingerprint"""
        buf = self.device_buffers[sa]
        intervals = np.array(buf['intervals'][-self.window_size:])

        # Calculate current fingerprint
        mean_interval = np.mean(intervals)
        expected = np.median(intervals)  # Use median as expected
        skew = (mean_interval - expected) / expected * 1e6

        current_fp = {'skew_ppm': skew}

        # Verify against database
        match, confidence, details = self.db.verify(sa, current_fp, self.tolerance)

        if match is None:
            # Unknown device - could be alert too
            return None

        if not match:
            alert = {
                'type': 'IMPERSONATION',
                'timestamp': timestamp,
                'source_addr': sa,
                'device_name': self.db.fingerprints[sa].get('device_name'),
                'expected_skew': details['enrolled_skew'],
                'observed_skew': details['current_skew'],
                'difference': details['skew_difference'],
                'tolerance': self.tolerance
            }
            self.alerts.append(alert)
            return alert

        return None
```

### 3.2 Test Normal Operation

```python
# Load fingerprint database
db = FingerprintDatabase()
db.load('fingerprint_db.json')

# Create detector
detector = ImpersonationDetector(db, tolerance_ppm=10, window_size=100)

# Process normal traffic
print("Testing on normal traffic...")
normal_alerts = 0

with open('normal_capture.txt') as f:
    for line in f:
        msg = parse_message(line)
        if msg:
            alert = detector.process_message(msg['can_id'], msg['timestamp'])
            if alert:
                normal_alerts += 1
                print(f"  Alert: {alert['source_addr']} - {alert['type']}")

print(f"Normal traffic: {normal_alerts} alerts (false positives)")
```

**Normal Traffic Results:**
- Messages processed: _______
- False positives: _______

### 3.3 Simulate Impersonation Attack

```python
# Simulate impersonation by injecting messages with different timing
def simulate_impersonation(capture_file, target_sa, fake_interval_offset=0.001):
    """
    Simulate impersonation by slightly altering timing

    A different device will have different clock skew
    """
    detector = ImpersonationDetector(db, tolerance_ppm=10)
    alerts = []

    with open(capture_file) as f:
        for line in f:
            msg = parse_message(line)
            if msg:
                # Inject fake messages for target SA
                if (msg['can_id'] & 0xFF) == target_sa:
                    # Add offset to simulate different clock
                    fake_ts = msg['timestamp'] + fake_interval_offset
                    alert = detector.process_message(msg['can_id'], fake_ts)
                    if alert:
                        alerts.append(alert)

    return alerts

# Test impersonation of GPS (SA 36)
target_sa = 36  # Change to your GPS SA
alerts = simulate_impersonation('normal_capture.txt', target_sa, 0.002)
print(f"Impersonation detected: {len(alerts)} alerts")
```

### 3.4 Impersonation Detection Results

| Scenario | Timing Offset | Detected? | Alert Count |
|----------|---------------|-----------|-------------|
| +0.1ms | | | |
| +1ms | | | |
| +2ms | | | |
| +5ms | | | |

## Part 4: Tolerance Tuning (15 minutes)

### 4.1 Test Multiple Tolerances

```python
def evaluate_tolerance(db, normal_file, attack_file, tolerances):
    """Evaluate detection at different tolerances"""
    results = {}

    for tol in tolerances:
        # Normal traffic
        detector = ImpersonationDetector(db, tolerance_ppm=tol)
        normal_fp = 0
        # ... process normal file

        # Attack traffic (simulated)
        attack_tp = 0
        # ... process attack file

        results[tol] = {
            'tolerance': tol,
            'false_positives': normal_fp,
            'true_positives': attack_tp
        }

    return results

tolerances = [5, 10, 15, 20, 25, 30]
results = evaluate_tolerance(db, 'normal.txt', 'attack.txt', tolerances)

print("\nTolerance Analysis:")
for tol, r in sorted(results.items()):
    print(f"Tolerance {tol:2d} ppm: FP={r['false_positives']:3d}, "
          f"TP={r['true_positives']:3d}")
```

### 4.2 Select Optimal Tolerance

Based on results, select tolerance:

- Recommended tolerance: _______ ppm
- Rationale: _________________

## Part 5: Documentation (10 minutes)

### 5.1 Fingerprint Database Report

```markdown
# Device Fingerprint Database

## Summary
- Total devices enrolled: ___
- Capture date: ___
- Capture duration: ___

## Device Details

### Device 1: [Name]
- Source Address: ___
- Clock Skew: ___ ppm
- Confidence: ___
- Primary PGNs: ___

### Device 2: [Name]
...
```

### 5.2 Detection Performance

| Metric | Value |
|--------|-------|
| False positive rate | |
| True positive rate | |
| Optimal tolerance | |
| Detection delay (messages) | |

## Deliverables

Submit via course portal:

1. **fingerprint.py** - Implementation
2. **fingerprint_db.json** - Enrolled devices
3. **Analysis report** - Tolerance tuning results
4. **Lab report** - Including fingerprint database

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Clock skew calculation correct | 25 |
| Database enrollment working | 20 |
| Impersonation detection working | 25 |
| Tolerance analysis complete | 15 |
| Documentation quality | 15 |
| **Total** | **100** |

## Challenge Question

Can you impersonate a device without being detected?

What would you need to know/control?

## Next Lab Preview

In Lab 13, you will:
- Build ensemble IDS combining all methods
- Implement explainable alerts
- Evaluate combined system
- Prepare for capstone

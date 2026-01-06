---
title: "Class 12"
subtitle: "Device Fingerprinting and Authentication"
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
    Identifying devices through clock skew and behavioral fingerprinting
---

# Class 12 -- Device Fingerprinting and Authentication

## Learning Outcomes

- Understand device fingerprinting principles
- Implement clock skew analysis for device identification
- Build behavioral fingerprints from message patterns
- Detect device impersonation attacks
- Evaluate fingerprinting accuracy and limitations

## Definitions

- **Fingerprint** -- Unique characteristics identifying a device
- **Clock Skew** -- Drift in device's internal clock relative to reference
- **Behavioral Fingerprint** -- Pattern of messages/timing unique to device
- **Impersonation** -- Attacker pretending to be legitimate device
- **Spoofing** -- Sending messages with false source address

## Reading Assignment

- Literature Review: Section 5 (Device Fingerprinting)
- Literature Review: Section 6.5 (Clock Skew Detection)
- Research papers on CAN bus device fingerprinting

## Why Device Fingerprinting?

### The Problem

CAN bus has no authentication:
- Any device can claim any Source Address
- Messages appear legitimate regardless of source
- Spoofing is trivially easy

### The Solution

Every physical device has unique characteristics:
- Clock frequency drift
- Message timing patterns
- Voltage characteristics
- Behavioral sequences

**Even if attacker spoofs Source Address, they can't spoof physics!**

<!--
Instructor Notes:

This is one of the most powerful detection techniques.
It works because:
1. Every crystal oscillator is slightly different
2. Processing delays are hardware-specific
3. Analog characteristics vary

No software changes can make one device
perfectly mimic another's physical timing.

Analogy: Like voice recognition - you can
imitate what someone says, but not exactly how.
-->

## Clock Skew Fundamentals

### What is Clock Skew?

Every device has an internal clock:
- Based on crystal oscillator
- Nominally 8/16 MHz (for CAN controllers)
- Actually slightly off (±50 ppm typical)

Skew = (actual frequency - nominal frequency) / nominal frequency

Example:
- Nominal: 16.000000 MHz
- Actual: 16.000800 MHz
- Skew: +50 ppm (50 parts per million)

### Why Skew is Unique

Manufacturing variations cause:
- Crystal cut angle differences
- Temperature sensitivity differences
- Aging characteristics

Two devices from same batch may have:
- Device A: +23 ppm
- Device B: -17 ppm

**Measurable and consistent over time!**

### Measuring Clock Skew

```python
import numpy as np
from scipy import stats

class ClockSkewAnalyzer:
    def __init__(self, reference_time='system'):
        """
        Clock skew analyzer for device fingerprinting

        Args:
            reference_time: 'system' uses local clock as reference
        """
        self.reference_time = reference_time
        self.device_timestamps = {}  # sa -> [(local_ts, msg_count)]

    def record_message(self, source_addr, local_timestamp, message_count=None):
        """
        Record message timestamp for skew analysis

        Args:
            source_addr: Device source address
            local_timestamp: Local system timestamp (reference)
            message_count: Sequence number if available
        """
        if source_addr not in self.device_timestamps:
            self.device_timestamps[source_addr] = []

        self.device_timestamps[source_addr].append({
            'local_ts': local_timestamp,
            'msg_count': message_count or len(self.device_timestamps[source_addr])
        })

    def calculate_skew(self, source_addr, min_samples=100):
        """
        Calculate clock skew for device

        Returns:
            skew_ppm: Clock skew in parts per million
            confidence: R-squared value of linear fit
        """
        if source_addr not in self.device_timestamps:
            return None, None

        samples = self.device_timestamps[source_addr]
        if len(samples) < min_samples:
            return None, None

        # Extract timestamps and message counts
        local_times = np.array([s['local_ts'] for s in samples])
        msg_counts = np.array([s['msg_count'] for s in samples])

        # Normalize to start from 0
        local_times = local_times - local_times[0]

        # Linear regression: local_time = slope * msg_count + intercept
        # Slope represents average interval from device's perspective
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            msg_counts, local_times
        )

        # Expected interval (e.g., 100ms for 10 Hz)
        expected_interval = 0.1  # seconds

        # Calculate skew
        # If device clock is fast, messages arrive earlier than expected
        # skew = (actual_interval - expected_interval) / expected_interval
        skew = (slope - expected_interval) / expected_interval
        skew_ppm = skew * 1e6

        confidence = r_value ** 2

        return skew_ppm, confidence
```

<!--
Instructor Notes:

Clock skew measurement:
1. Record arrival times of periodic messages
2. Assume device sends at constant rate (10 Hz)
3. Linear regression finds actual rate
4. Difference from expected = skew

Key insight: We're measuring the device's clock
through its message timing, not directly.

Important: Need many samples (100+) for accuracy.
Short-term jitter averages out over time.
-->

## Building Device Fingerprints

### Fingerprint Components

| Component | Measurement | Uniqueness |
|-----------|-------------|------------|
| Clock skew | ppm from expected | High |
| Interval mean | Average message period | Medium |
| Interval std | Timing jitter | Medium |
| Message order | Sequence patterns | Low-Medium |
| PGN set | Which messages sent | Low |

### Comprehensive Fingerprint

```python
class DeviceFingerprint:
    def __init__(self, source_addr):
        self.source_addr = source_addr
        self.timestamps = []
        self.pgns = set()
        self.intervals = []
        self.message_count = 0

        # Fingerprint components
        self.clock_skew = None
        self.skew_confidence = None
        self.interval_mean = None
        self.interval_std = None
        self.pgn_pattern = None

    def add_message(self, timestamp, pgn):
        """Add message to fingerprint calculation"""
        self.pgns.add(pgn)
        self.message_count += 1

        if self.timestamps:
            interval = timestamp - self.timestamps[-1]
            if 0 < interval < 1:  # Filter outliers
                self.intervals.append(interval)

        self.timestamps.append(timestamp)

    def calculate_fingerprint(self, min_samples=500):
        """Calculate complete device fingerprint"""
        if len(self.intervals) < min_samples:
            return None

        # Clock skew (simplified - uses interval deviation)
        expected_interval = np.median(self.intervals)
        self.interval_mean = np.mean(self.intervals)
        self.interval_std = np.std(self.intervals)

        # Skew from expected
        self.clock_skew = (self.interval_mean - expected_interval) / expected_interval * 1e6

        # Confidence based on consistency
        cv = self.interval_std / self.interval_mean  # Coefficient of variation
        self.skew_confidence = max(0, 1 - cv * 10)

        # PGN pattern
        self.pgn_pattern = frozenset(self.pgns)

        return {
            'source_addr': self.source_addr,
            'clock_skew_ppm': self.clock_skew,
            'confidence': self.skew_confidence,
            'interval_mean': self.interval_mean,
            'interval_std': self.interval_std,
            'pgn_count': len(self.pgns),
            'pgn_set': list(self.pgns),
            'message_count': self.message_count
        }

    def matches(self, other_fingerprint, skew_tolerance=5, interval_tolerance=0.01):
        """
        Check if another fingerprint matches this device

        Args:
            other_fingerprint: Fingerprint to compare
            skew_tolerance: Maximum skew difference (ppm)
            interval_tolerance: Maximum interval difference (seconds)

        Returns:
            match_score: 0-1 (1 = perfect match)
        """
        if self.clock_skew is None or other_fingerprint.clock_skew is None:
            return 0.0

        # Clock skew similarity
        skew_diff = abs(self.clock_skew - other_fingerprint.clock_skew)
        skew_score = max(0, 1 - skew_diff / skew_tolerance)

        # Interval similarity
        interval_diff = abs(self.interval_mean - other_fingerprint.interval_mean)
        interval_score = max(0, 1 - interval_diff / interval_tolerance)

        # PGN overlap
        pgn_overlap = len(self.pgn_pattern & other_fingerprint.pgn_pattern)
        pgn_total = len(self.pgn_pattern | other_fingerprint.pgn_pattern)
        pgn_score = pgn_overlap / pgn_total if pgn_total > 0 else 0

        # Weighted combination
        match_score = (0.5 * skew_score + 0.3 * interval_score + 0.2 * pgn_score)

        return match_score
```

### Fingerprint Database

```python
class FingerprintDatabase:
    def __init__(self):
        self.fingerprints = {}  # source_addr -> DeviceFingerprint
        self.baseline = {}  # source_addr -> baseline fingerprint data

    def learn_device(self, source_addr, messages):
        """Learn fingerprint from training messages"""
        fp = DeviceFingerprint(source_addr)

        for timestamp, pgn in messages:
            fp.add_message(timestamp, pgn)

        fingerprint_data = fp.calculate_fingerprint()
        if fingerprint_data:
            self.baseline[source_addr] = fingerprint_data
            self.fingerprints[source_addr] = fp

        return fingerprint_data

    def verify_device(self, source_addr, recent_messages):
        """Verify device matches its baseline fingerprint"""
        if source_addr not in self.baseline:
            return None, "Unknown device"

        # Build fingerprint from recent messages
        current_fp = DeviceFingerprint(source_addr)
        for timestamp, pgn in recent_messages:
            current_fp.add_message(timestamp, pgn)

        current_data = current_fp.calculate_fingerprint(min_samples=50)
        if current_data is None:
            return None, "Insufficient data"

        # Compare to baseline
        baseline_fp = self.fingerprints[source_addr]
        match_score = baseline_fp.matches(current_fp)

        return match_score, current_data
```

<!--
Instructor Notes:

Fingerprint matching considerations:
1. Clock skew is most reliable (highest weight)
2. Interval mean/std add confidence
3. PGN set is weak (easily spoofed)

Tolerance values need tuning:
- Too strict = false alarms
- Too loose = missed attacks

Temperature affects clock skew!
- May need temperature compensation
- Or wider tolerance for mobile vessels
-->

## Detecting Impersonation

### Attack Scenario

Attacker spoofs Source Address 36 (legitimate GPS):
1. Attacker uses CAN ID with SA=36
2. Messages appear to come from GPS
3. But attacker's clock skew differs!

### Impersonation Detector

```python
class ImpersonationDetector:
    def __init__(self, fingerprint_db, match_threshold=0.7):
        """
        Detect device impersonation through fingerprinting

        Args:
            fingerprint_db: FingerprintDatabase with learned devices
            match_threshold: Minimum match score to accept device
        """
        self.db = fingerprint_db
        self.threshold = match_threshold

        # Sliding windows per source address
        self.recent_messages = {}  # sa -> [(timestamp, pgn)]
        self.window_size = 100

        # Alert tracking
        self.alerts = []

    def process_message(self, can_id, timestamp):
        """Process message and check for impersonation"""
        sa = can_id & 0xFF
        pgn = (can_id >> 8) & 0x3FFFF

        # Update message window
        if sa not in self.recent_messages:
            self.recent_messages[sa] = []

        self.recent_messages[sa].append((timestamp, pgn))

        # Maintain window
        while len(self.recent_messages[sa]) > self.window_size:
            self.recent_messages[sa].pop(0)

        # Verify fingerprint periodically
        if len(self.recent_messages[sa]) >= self.window_size:
            if len(self.recent_messages[sa]) % 50 == 0:  # Check every 50 messages
                match_score, details = self.db.verify_device(
                    sa, self.recent_messages[sa]
                )

                if match_score is not None and match_score < self.threshold:
                    alert = {
                        'type': 'IMPERSONATION',
                        'source_addr': sa,
                        'match_score': match_score,
                        'expected_skew': self.db.baseline.get(sa, {}).get('clock_skew_ppm'),
                        'observed_skew': details.get('clock_skew_ppm') if details else None,
                        'timestamp': timestamp
                    }
                    self.alerts.append(alert)
                    return True, alert

        return False, None
```

### Example Detection

```
Baseline (legitimate GPS, SA=36):
  Clock skew: +23.4 ppm
  Interval mean: 0.1002 s
  Confidence: 0.95

Attack detected (spoofed SA=36):
  Clock skew: -8.7 ppm
  Interval mean: 0.0998 s
  Match score: 0.42 (< 0.7 threshold)

ALERT: Possible impersonation of device 36!
  Expected skew: +23.4 ppm
  Observed skew: -8.7 ppm
  Difference: 32.1 ppm
```

<!--
Instructor Notes:

This is a powerful detection method because:
1. Attacker can spoof any data content
2. Attacker can spoof source address
3. But attacker CANNOT spoof their hardware clock!

Even professional attackers can't defeat this without:
- Physical access to legitimate device
- Extremely precise timing control
- Knowledge of target device's exact skew

Limitation: Requires learning phase.
New devices must be enrolled before protection.
-->

## Voltage-Based Fingerprinting

### Physical Layer Analysis

CAN bus has characteristic voltages:
- CAN-H: ~3.5V (dominant), ~2.5V (recessive)
- CAN-L: ~1.5V (dominant), ~2.5V (recessive)

Device variations:
- Driver strength
- Rise/fall times
- Voltage levels

### Voltage Fingerprinting (Concept)

```python
# Note: Requires specialized hardware (oscilloscope/ADC)

class VoltageFingerprint:
    def __init__(self):
        self.voltage_samples = []

    def record_sample(self, can_h, can_l, timestamp):
        """Record voltage sample"""
        self.voltage_samples.append({
            'can_h': can_h,
            'can_l': can_l,
            'differential': can_h - can_l,
            'timestamp': timestamp
        })

    def extract_features(self):
        """Extract voltage-based features"""
        differentials = [s['differential'] for s in self.voltage_samples]

        return {
            'mean_differential': np.mean(differentials),
            'std_differential': np.std(differentials),
            'max_differential': np.max(differentials),
            'min_differential': np.min(differentials),
            # Rise/fall times would require high-speed sampling
        }
```

### Practical Limitations

| Aspect | Challenge |
|--------|-----------|
| Hardware | Need ADC/oscilloscope |
| Speed | High sample rate required |
| Environment | Voltage varies with temperature |
| Distance | Signal degrades over cable length |

**Voltage fingerprinting is powerful but requires specialized hardware.**

## Behavioral Fingerprinting

### Message Sequence Patterns

Devices often send messages in predictable order:

```python
class SequenceFingerprint:
    def __init__(self, source_addr, sequence_length=5):
        self.source_addr = source_addr
        self.sequence_length = sequence_length
        self.sequence_counts = {}  # tuple -> count
        self.recent_pgns = []

    def add_message(self, pgn):
        """Track message sequence patterns"""
        self.recent_pgns.append(pgn)

        if len(self.recent_pgns) >= self.sequence_length:
            # Record sequence
            seq = tuple(self.recent_pgns[-self.sequence_length:])
            self.sequence_counts[seq] = self.sequence_counts.get(seq, 0) + 1

            # Maintain window
            if len(self.recent_pgns) > self.sequence_length * 10:
                self.recent_pgns = self.recent_pgns[-self.sequence_length:]

    def get_common_sequences(self, top_n=10):
        """Get most common sequences"""
        sorted_seqs = sorted(
            self.sequence_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_seqs[:top_n]

    def calculate_sequence_entropy(self):
        """Calculate entropy of sequence distribution"""
        total = sum(self.sequence_counts.values())
        if total == 0:
            return 0

        entropy = 0
        for count in self.sequence_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * np.log2(p)

        return entropy
```

### Response Timing

Devices have characteristic response times:

```python
class ResponseFingerprint:
    def __init__(self):
        self.request_response_times = {}  # (request_pgn, response_pgn) -> [times]

    def record_exchange(self, request_pgn, request_time,
                        response_pgn, response_time, source_addr):
        """Record request-response timing"""
        key = (request_pgn, response_pgn, source_addr)
        delay = response_time - request_time

        if key not in self.request_response_times:
            self.request_response_times[key] = []

        self.request_response_times[key].append(delay)

    def get_response_fingerprint(self, source_addr):
        """Get response timing fingerprint for device"""
        device_timings = {}

        for (req_pgn, resp_pgn, sa), times in self.request_response_times.items():
            if sa == source_addr and len(times) >= 10:
                device_timings[(req_pgn, resp_pgn)] = {
                    'mean': np.mean(times),
                    'std': np.std(times),
                    'min': np.min(times),
                    'max': np.max(times)
                }

        return device_timings
```

<!--
Instructor Notes:

Behavioral fingerprinting:
- Easier to implement (no special hardware)
- But easier to spoof (if attacker studies patterns)

Best approach: Combine multiple methods
1. Clock skew (hard to spoof)
2. Voltage (very hard, needs hardware)
3. Behavior (easy, adds confidence)

Defense in depth principle applies!
-->

## Fingerprint Management

### Enrollment Process

```python
class FingerprintManager:
    def __init__(self, db_path='fingerprints.json'):
        self.db_path = db_path
        self.fingerprints = self._load_database()

    def enroll_device(self, source_addr, training_messages,
                      device_name=None, location=None):
        """
        Enroll new device into fingerprint database

        Args:
            source_addr: Device source address
            training_messages: List of (timestamp, pgn) tuples
            device_name: Human-readable name
            location: Physical location on vessel
        """
        # Build fingerprint
        fp = DeviceFingerprint(source_addr)
        for ts, pgn in training_messages:
            fp.add_message(ts, pgn)

        fp_data = fp.calculate_fingerprint()

        if fp_data is None:
            return False, "Insufficient training data"

        # Store with metadata
        self.fingerprints[source_addr] = {
            **fp_data,
            'device_name': device_name,
            'location': location,
            'enrolled_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'active'
        }

        self._save_database()
        return True, fp_data

    def revoke_device(self, source_addr):
        """Revoke enrolled device"""
        if source_addr in self.fingerprints:
            self.fingerprints[source_addr]['status'] = 'revoked'
            self._save_database()
            return True
        return False

    def update_fingerprint(self, source_addr, recent_messages):
        """Update fingerprint with recent data (drift compensation)"""
        if source_addr not in self.fingerprints:
            return False

        # Calculate new fingerprint
        fp = DeviceFingerprint(source_addr)
        for ts, pgn in recent_messages:
            fp.add_message(ts, pgn)

        new_data = fp.calculate_fingerprint(min_samples=50)

        if new_data:
            # Weighted average with existing (prevents sudden changes)
            old = self.fingerprints[source_addr]
            alpha = 0.1  # Learning rate

            old['clock_skew_ppm'] = (1 - alpha) * old['clock_skew_ppm'] + \
                                    alpha * new_data['clock_skew_ppm']
            old['interval_mean'] = (1 - alpha) * old['interval_mean'] + \
                                   alpha * new_data['interval_mean']
            old['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S')

            self._save_database()
            return True

        return False
```

## Lab Preview: Week 12

In Lab 12, you will:

1. Collect messages from multiple devices
2. Calculate clock skew for each device
3. Build fingerprint database
4. Simulate device impersonation attack
5. Test fingerprint-based detection
6. Evaluate accuracy and false positive rate

**Challenge**: Can you impersonate a device without detection?

## Homework

### Required

1. **Read**: Literature Review Section 5 completely
2. **Calculate**: Clock skew from sample timing data (provided)
3. **Design**: Fingerprint enrollment procedure for a vessel

### Suggested

- Research: Temperature effects on crystal oscillators
- Explore: IEEE papers on physical unclonable functions
- Consider: How would you handle device replacement?

## Discussion Questions

1. Why can't an attacker perfectly mimic another device's clock skew?
2. How should fingerprints be updated over time?
3. What happens when a device is replaced with identical model?
4. Could a sophisticated attacker defeat fingerprinting?

## References

- [CAN Bus Fingerprinting Research]
- [Clock Skew Detection Papers]
- [Physical Layer Security]

[CAN Bus Fingerprinting Research]:https://www.usenix.org/conference/usenixsecurity
[Clock Skew Detection Papers]:https://ieeexplore.ieee.org
[Physical Layer Security]:https://www.springer.com

---
title: "Class 10"
subtitle: "Entropy-Based Anomaly Detection"
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
    Using information entropy to detect CAN bus attacks
---

# Class 10 -- Entropy-Based Anomaly Detection

## Learning Outcomes

- Understand Shannon entropy and its application to network traffic
- Calculate entropy for CAN bus message streams
- Detect attacks through entropy deviation
- Compare entropy to frequency-based detection
- Implement sliding-window entropy monitoring

## Definitions

- **Entropy** -- Measure of information randomness/unpredictability
- **Shannon Entropy** -- H(X) = -Σ p(x) log₂ p(x)
- **Symbol** -- Basic unit for entropy calculation (byte, PGN, etc.)
- **Window** -- Fixed-size sample for entropy calculation
- **Information Gain** -- Change in entropy indicating new information

## Reading Assignment

- Literature Review: Section 4.1.2 (Entropy-Based Detection)
- Shannon's "A Mathematical Theory of Communication" (overview)
- Research papers on entropy-based IDS

## Why Entropy Detection?

### Intuition

Normal CAN traffic has characteristic patterns:
- Certain CAN IDs appear more often
- Data bytes have predictable distributions
- Message sequences follow patterns

Attacks disrupt these patterns:
- DoS: One ID dominates (entropy drops)
- Spoofing: New IDs appear (entropy increases then stabilizes)
- Replay: Pattern shifts (entropy changes)

### Complementary to Frequency Detection

| Detection Method | Catches | Misses |
|------------------|---------|--------|
| Frequency | Rate changes | Content changes |
| Entropy | Distribution changes | Rate-matched attacks |
| Combined | Most attacks | Sophisticated mimicry |

<!--
Instructor Notes:

Entropy detection comes from information theory.
Originally for data compression - now for security.

Key insight: Entropy measures SURPRISE.
- High entropy = unpredictable = many different values
- Low entropy = predictable = few repeated values

CAN attacks change the "surprise" level of traffic.
-->

## Shannon Entropy Fundamentals

### Mathematical Definition

For a discrete random variable X with possible values {x₁, x₂, ..., xₙ}:

```
H(X) = -Σᵢ p(xᵢ) × log₂(p(xᵢ))
```

Where:
- H(X) is entropy in bits
- p(xᵢ) is probability of value xᵢ
- log₂ is logarithm base 2

### Properties

| Property | Value | Meaning |
|----------|-------|---------|
| Minimum | 0 | Completely predictable (one value) |
| Maximum | log₂(n) | Completely random (uniform distribution) |

### Simple Example

Coin flip entropy:
- Fair coin: p(H) = p(T) = 0.5
- H = -0.5×log₂(0.5) - 0.5×log₂(0.5) = 1 bit

Biased coin (p(H) = 0.9):
- H = -0.9×log₂(0.9) - 0.1×log₂(0.1) = 0.47 bits

**Lower entropy = more predictable**

## Entropy in CAN Bus Traffic

### What to Measure?

Several entropy calculation approaches:

1. **CAN ID Entropy**: Distribution of message IDs
2. **Data Byte Entropy**: Distribution of payload bytes
3. **PGN Entropy**: Distribution of NMEA 2000 PGNs
4. **Source Address Entropy**: Distribution of senders

### CAN ID Entropy

```python
import math
from collections import Counter

def calculate_can_id_entropy(messages):
    """
    Calculate Shannon entropy of CAN IDs

    Args:
        messages: List of CAN IDs (integers)

    Returns:
        Entropy in bits
    """
    if not messages:
        return 0.0

    # Count occurrences
    counter = Counter(messages)
    total = len(messages)

    # Calculate probabilities and entropy
    entropy = 0.0
    for count in counter.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)

    return entropy

# Example
normal_traffic = [0x09F80124, 0x09F11024, 0x09F80124,
                  0x09FD0224, 0x09F80124, 0x09F11024]
print(f"Normal entropy: {calculate_can_id_entropy(normal_traffic):.2f} bits")

# DoS attack (all same ID)
dos_traffic = [0x00000000] * 100
print(f"DoS entropy: {calculate_can_id_entropy(dos_traffic):.2f} bits")
```

### Expected Output

```
Normal entropy: 1.92 bits
DoS entropy: 0.00 bits
```

<!--
Instructor Notes:

Walk through the math:
- Normal: 3 unique IDs, roughly equal distribution
- DoS: 1 unique ID, all same
- DoS entropy = 0 because p=1, log₂(1)=0

This is the core detection insight:
DoS attacks REDUCE entropy (less variety)
Spoofing may INCREASE entropy (new IDs)

But entropy can also stay same if attack matches distribution!
-->

## Implementing Entropy Detector

### Sliding Window Entropy

```python
class EntropyDetector:
    def __init__(self, window_size=100, baseline_entropy=None,
                 threshold_low=0.3, threshold_high=0.3):
        """
        Entropy-based anomaly detector

        Args:
            window_size: Number of messages in sliding window
            baseline_entropy: Expected entropy (calculated from training)
            threshold_low: Alert if entropy drops by this ratio
            threshold_high: Alert if entropy rises by this ratio
        """
        self.window_size = window_size
        self.baseline = baseline_entropy
        self.threshold_low = threshold_low
        self.threshold_high = threshold_high

        # Sliding window buffer
        self.window = []
        self.alerts = []

    def calculate_window_entropy(self):
        """Calculate entropy of current window"""
        if len(self.window) < self.window_size:
            return None

        counter = Counter(self.window)
        total = len(self.window)

        entropy = 0.0
        for count in counter.values():
            p = count / total
            entropy -= p * math.log2(p)

        return entropy

    def process_message(self, can_id, timestamp):
        """
        Process incoming message

        Returns:
            (is_anomaly, alert_info)
        """
        # Add to window
        self.window.append(can_id)

        # Maintain window size
        if len(self.window) > self.window_size:
            self.window.pop(0)

        # Skip until window full
        if len(self.window) < self.window_size:
            return False, None

        # Calculate current entropy
        current_entropy = self.calculate_window_entropy()

        # Compare to baseline
        if self.baseline is None:
            return False, None

        # Calculate deviation
        deviation = (current_entropy - self.baseline) / self.baseline

        # Check thresholds
        if deviation < -self.threshold_low:
            alert = {
                'type': 'LOW_ENTROPY',
                'timestamp': timestamp,
                'entropy': current_entropy,
                'baseline': self.baseline,
                'deviation': deviation,
                'interpretation': 'Possible DoS attack (reduced diversity)'
            }
            self.alerts.append(alert)
            return True, alert

        elif deviation > self.threshold_high:
            alert = {
                'type': 'HIGH_ENTROPY',
                'timestamp': timestamp,
                'entropy': current_entropy,
                'baseline': self.baseline,
                'deviation': deviation,
                'interpretation': 'Possible injection attack (new IDs)'
            }
            self.alerts.append(alert)
            return True, alert

        return False, None
```

### Building Entropy Baseline

```python
class EntropyBaseline:
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.entropy_samples = []

    def train(self, messages):
        """
        Build baseline from training messages

        Args:
            messages: List of (can_id, timestamp) tuples
        """
        # Calculate entropy for sliding windows
        window = []

        for can_id, _ in messages:
            window.append(can_id)

            if len(window) > self.window_size:
                window.pop(0)

            if len(window) == self.window_size:
                entropy = self._calculate_entropy(window)
                self.entropy_samples.append(entropy)

        # Calculate statistics
        if self.entropy_samples:
            self.mean = sum(self.entropy_samples) / len(self.entropy_samples)
            variance = sum((x - self.mean) ** 2 for x in self.entropy_samples)
            self.std = math.sqrt(variance / len(self.entropy_samples))

            return {
                'mean_entropy': self.mean,
                'std_entropy': self.std,
                'min_entropy': min(self.entropy_samples),
                'max_entropy': max(self.entropy_samples),
                'sample_count': len(self.entropy_samples)
            }

        return None

    def _calculate_entropy(self, window):
        counter = Counter(window)
        total = len(window)
        entropy = 0.0
        for count in counter.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy
```

<!--
Instructor Notes:

Baseline building:
1. Collect normal traffic (no attacks)
2. Slide window across traffic
3. Calculate entropy at each position
4. Record mean and std of entropy

Detection:
- If entropy drops below mean - k×std → DoS
- If entropy rises above mean + k×std → Injection

Similar to frequency, but measuring DISTRIBUTION not RATE.
-->

## Data Byte Entropy

### Beyond CAN ID

CAN ID entropy misses:
- Spoofing that uses existing IDs
- Payload manipulation

Solution: Calculate entropy of data bytes too

```python
def calculate_data_entropy(data_bytes):
    """
    Calculate entropy of CAN payload bytes

    Args:
        data_bytes: List of 8-byte payloads (as bytes or list)

    Returns:
        Entropy of byte value distribution
    """
    # Flatten all bytes
    all_bytes = []
    for payload in data_bytes:
        all_bytes.extend(payload)

    if not all_bytes:
        return 0.0

    counter = Counter(all_bytes)
    total = len(all_bytes)

    entropy = 0.0
    for count in counter.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy

# Example: Normal varied data
normal_data = [
    bytes([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0]),
    bytes([0x43, 0x21, 0x87, 0x65, 0xBA, 0xDC, 0xFE, 0x10]),
    bytes([0x00, 0xFF, 0x55, 0xAA, 0x33, 0xCC, 0x66, 0x99]),
]

# Replay attack (same data repeated)
replay_data = [bytes([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0])] * 100

print(f"Normal data entropy: {calculate_data_entropy(normal_data):.2f} bits")
print(f"Replay data entropy: {calculate_data_entropy(replay_data):.2f} bits")
```

### Per-PGN Data Entropy

Different PGNs have different expected data patterns:

```python
class PerPGNEntropyDetector:
    def __init__(self):
        self.pgn_baselines = {}  # pgn -> {mean_entropy, std_entropy}
        self.pgn_windows = defaultdict(list)

    def build_baseline(self, messages, window_size=50):
        """Build per-PGN data entropy baselines"""
        # Group messages by PGN
        pgn_data = defaultdict(list)

        for can_id, data in messages:
            pgn = (can_id >> 8) & 0x3FFFF
            pgn_data[pgn].append(data)

        # Calculate baseline for each PGN
        for pgn, payloads in pgn_data.items():
            if len(payloads) < window_size * 2:
                continue

            entropies = []
            for i in range(0, len(payloads) - window_size, window_size // 2):
                window = payloads[i:i+window_size]
                entropy = calculate_data_entropy(window)
                entropies.append(entropy)

            if entropies:
                self.pgn_baselines[pgn] = {
                    'mean': statistics.mean(entropies),
                    'std': statistics.stdev(entropies) if len(entropies) > 1 else 0.1
                }

        return self.pgn_baselines
```

## Attack Signatures in Entropy

### DoS Attack

```
Before DoS:
CAN IDs: [0x09F80124, 0x09F11024, 0x09FD0224, ...]
Entropy: ~2.5 bits

During DoS:
CAN IDs: [0x00000000, 0x00000000, 0x00000000, ...]
Entropy: 0.0 bits

Signature: Sharp entropy DROP
```

### Spoofing Attack (New ID)

```
Before Spoofing:
CAN IDs: 5 unique IDs, balanced distribution
Entropy: ~2.3 bits

During Spoofing:
CAN IDs: 5 original + 1 spoofed (at 2x rate)
Entropy: ~2.4 bits (slight increase, then stabilizes)

Signature: Entropy SHIFT (may be subtle)
```

### Replay Attack

```
Before Replay:
Data entropy varies based on real sensor changes
Entropy fluctuates: 5.0 ± 0.5 bits

During Replay:
Same data repeated, less variation
Entropy: 4.2 bits (lower, more stable)

Signature: Entropy DROPS and STABILIZES
```

<!--
Instructor Notes:

Detection summary:
- DoS: Dramatic entropy drop (easy)
- Injection: Entropy may rise (medium)
- Replay: Entropy drops, variance drops (tricky)
- Sophisticated spoof: May not change entropy (hard)

Entropy works best in combination with other methods.
It catches different attacks than frequency detection.
-->

## Normalized Entropy

### Making Entropy Comparable

Raw entropy depends on number of possible values.
Normalize to [0, 1] range:

```python
def normalized_entropy(values, max_possible_values=None):
    """
    Calculate normalized entropy (0-1 range)

    Args:
        values: List of observed values
        max_possible_values: Maximum unique values possible
                            (default: actual unique count)

    Returns:
        Normalized entropy (0 = no variety, 1 = maximum variety)
    """
    if not values:
        return 0.0

    counter = Counter(values)
    n_unique = len(counter)
    total = len(values)

    if max_possible_values is None:
        max_possible_values = n_unique

    if max_possible_values <= 1:
        return 0.0

    # Calculate raw entropy
    entropy = 0.0
    for count in counter.values():
        p = count / total
        entropy -= p * math.log2(p)

    # Normalize by maximum possible entropy
    max_entropy = math.log2(max_possible_values)

    return entropy / max_entropy if max_entropy > 0 else 0.0
```

### Application to CAN

```python
# For CAN IDs (29-bit = max 2^29 unique values)
# But typically only ~20 active IDs on vessel network

# Normalize to actual network size
active_ids = 20
current_entropy = calculate_can_id_entropy(traffic)
normalized = current_entropy / math.log2(active_ids)

# Now 0 = all same ID, 1 = perfectly balanced among 20 IDs
```

## Multi-Dimensional Entropy

### Combined Detection

```python
class MultiDimensionalEntropyDetector:
    def __init__(self, window_size=100):
        self.window_size = window_size

        # Separate windows for different features
        self.can_id_window = []
        self.sa_window = []
        self.pgn_window = []
        self.data_window = []

        # Baselines
        self.baselines = {}

    def process_message(self, can_id, data, timestamp):
        """Process message and check multiple entropy dimensions"""
        pgn = (can_id >> 8) & 0x3FFFF
        sa = can_id & 0xFF

        # Update windows
        self.can_id_window.append(can_id)
        self.sa_window.append(sa)
        self.pgn_window.append(pgn)
        self.data_window.append(data)

        # Maintain window sizes
        for window in [self.can_id_window, self.sa_window,
                       self.pgn_window, self.data_window]:
            while len(window) > self.window_size:
                window.pop(0)

        # Calculate entropies
        results = {
            'can_id_entropy': self._entropy(self.can_id_window),
            'sa_entropy': self._entropy(self.sa_window),
            'pgn_entropy': self._entropy(self.pgn_window),
            'data_entropy': calculate_data_entropy(self.data_window)
        }

        # Check against baselines
        anomalies = []
        for dim, value in results.items():
            if dim in self.baselines:
                baseline = self.baselines[dim]
                if abs(value - baseline['mean']) > 3 * baseline['std']:
                    anomalies.append({
                        'dimension': dim,
                        'value': value,
                        'baseline': baseline['mean'],
                        'deviation_sigma': (value - baseline['mean']) / baseline['std']
                    })

        return anomalies

    def _entropy(self, values):
        if len(values) < self.window_size:
            return None
        return calculate_can_id_entropy(values)
```

<!--
Instructor Notes:

Multi-dimensional entropy catches more attacks:
- CAN ID entropy catches DoS
- SA entropy catches device impersonation
- PGN entropy catches protocol anomalies
- Data entropy catches replay/manipulation

But: More dimensions = more processing
Trade-off between coverage and performance.
-->

## Performance Comparison

### Frequency vs Entropy Detection

| Criterion | Frequency | Entropy |
|-----------|-----------|---------|
| DoS Detection | Excellent | Excellent |
| Spoofing (naive) | Good | Medium |
| Spoofing (smart) | Poor | Poor |
| Replay | Poor | Good |
| Computational Cost | Low | Medium |
| Memory | Low | Medium |
| Setup Complexity | Low | Medium |

### When to Use Each

- **Frequency only**: Simple deployment, catch obvious attacks
- **Entropy only**: Focus on content/pattern attacks
- **Combined**: Best coverage, more complexity

## Lab Preview: Week 10

In Lab 10, you will:

1. Calculate CAN ID entropy baseline from test network
2. Implement sliding window entropy detector
3. Test against attack scenarios:
   - DoS (entropy drop)
   - Injection (entropy rise)
   - Replay (data entropy change)
4. Compare detection performance to frequency method
5. Implement multi-dimensional entropy

**Evaluation**: Detection rate, false positive rate

## Homework

### Required

1. **Read**: Literature Review Section 4.1.2 completely
2. **Calculate**: By hand, entropy of:
   - [A, A, A, A] (4 same symbols)
   - [A, B, A, B] (alternating)
   - [A, B, C, D] (all different)
3. **Analyze**: When would entropy detection miss an attack?

### Suggested

- Research: Conditional entropy and mutual information
- Explore: scipy.stats entropy functions
- Consider: Entropy of timing intervals (inter-arrival times)

## Discussion Questions

1. Why does DoS cause entropy to drop?
2. How could an attacker maintain entropy while injecting?
3. What is the relationship between entropy and information?
4. Should entropy thresholds be adaptive?

## References

- [Shannon Entropy]
- [Entropy-Based Network Anomaly Detection]
- [Information Theory and Security]

[Shannon Entropy]:https://en.wikipedia.org/wiki/Entropy_(information_theory)
[Entropy-Based Network Anomaly Detection]:https://ieeexplore.ieee.org
[Information Theory and Security]:https://www.sciencedirect.com

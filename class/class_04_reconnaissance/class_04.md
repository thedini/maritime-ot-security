---
title: "Class 04"
subtitle: "Reconnaissance and Network Mapping"
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
    Techniques for mapping and profiling NMEA 2000 networks
---

# Class 04 -- Reconnaissance and Network Mapping

## Learning Outcomes

- Enumerate devices on NMEA 2000 networks
- Extract device product information (PGN 126996)
- Build frequency profiles for baseline establishment
- Identify critical systems and high-value targets
- Understand attacker perspective for better defense

## Definitions

- **Reconnaissance** -- Information gathering phase of an attack
- **Passive Recon** -- Observing without transmitting
- **Active Recon** -- Sending messages to elicit responses
- **Baseline** -- Normal behavior profile for comparison
- **Fingerprinting** -- Identifying specific device characteristics

## Reading Assignment

- Literature Review: Section 4.1.1 (Frequency-Based Detection)
- Literature Review: Section 5 (Device Fingerprinting)
- NMEA 2000 Address Claim mechanism documentation

## Why Reconnaissance Matters

### Attacker Perspective

Before attacking, an adversary needs to know:
1. What devices are on the network?
2. What messages do they send?
3. How often do they communicate?
4. What are high-value targets?
5. What will detection systems notice?

### Defender Perspective

Understanding reconnaissance helps us:
1. Know what attackers can learn
2. Build accurate baselines
3. Detect unauthorized devices
4. Identify anomalous patterns
5. Design detection strategies

<!--
Instructor Notes:

Frame this as "know your enemy" - we learn attack techniques to build better defenses.

Key principle: Defenders need to think like attackers.

Ask students: "What would you want to know before attacking a vessel network?"
-->

## Passive Reconnaissance

### What Can Be Observed?

Without transmitting any messages, an attacker learns:

| Information | Source | Value to Attacker |
|-------------|--------|-------------------|
| Device count | Unique Source Addresses | Network size |
| Device types | PGNs transmitted | Target identification |
| Message rates | Timing analysis | Baseline for evasion |
| Data values | Payload decoding | Current vessel state |
| Network topology | Message patterns | Attack planning |

### Tools for Passive Recon

```bash
# Capture all traffic
candump -ta can0 > capture.txt

# Real-time monitoring
candump can0

# With our parser
cat capture.txt | python3 parser.py -s
```

<!--
Instructor Notes:

Emphasize: Passive recon is UNDETECTABLE!

There is no way to know someone is listening on CAN bus.
This is fundamental to CAN's security weakness.

Any device on the bus can read ALL traffic.
-->

## Device Enumeration

### Source Address Analysis

```python
#!/usr/bin/env python3
"""Enumerate devices by Source Address"""
from collections import defaultdict

def enumerate_devices(capture_file):
    devices = defaultdict(lambda: {
        'pgns': set(),
        'message_count': 0,
        'first_seen': None,
        'last_seen': None
    })

    with open(capture_file) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 4:
                continue

            try:
                ts = float(parts[0].strip('()'))
                can_id = int(parts[2], 16)
                sa = can_id & 0xFF
                pgn = (can_id >> 8) & 0x3FFFF

                dev = devices[sa]
                dev['pgns'].add(pgn)
                dev['message_count'] += 1
                if dev['first_seen'] is None:
                    dev['first_seen'] = ts
                dev['last_seen'] = ts
            except:
                pass

    return devices

# Usage
devices = enumerate_devices('capture.txt')
for sa, info in sorted(devices.items()):
    duration = info['last_seen'] - info['first_seen']
    rate = info['message_count'] / duration if duration > 0 else 0
    print(f"SA {sa:3d}: {info['message_count']:6d} msgs, "
          f"{len(info['pgns']):2d} PGNs, {rate:.1f} msg/s")
```

### Typical Vessel Network

| Source Address | Device Type | PGNs |
|----------------|-------------|------|
| 0-127 | Self-configurable devices | Various |
| 128-247 | Non-configurable devices | Various |
| 248-253 | Reserved | - |
| 254 | Null address | - |
| 255 | Global (broadcast dest) | - |

<!--
Instructor Notes:

Real vessel networks typically have 5-20 devices:
- GPS/chartplotter
- Autopilot
- Wind instrument
- Depth sounder
- Engine interface
- AIS transponder
- VHF radio (DSC)

Students can compare their Lab 01 results.
-->

## Product Information Extraction

### PGN 126996: Product Information

Devices broadcast their identity:

```python
def request_product_info(sa):
    """
    Request product info from specific device
    Send ISO Request (PGN 59904) for PGN 126996
    """
    # This is ACTIVE reconnaissance!
    # DA = target SA, PGN requested = 126996
    pass

def decode_product_info(data):
    """
    Decode PGN 126996 Product Information
    This is a Fast Packet message (134 bytes)
    """
    # Simplified - actual implementation needs Fast Packet handling
    result = {
        'nmea_version': struct.unpack('<H', data[0:2])[0],
        'product_code': struct.unpack('<H', data[2:4])[0],
        'model_id': data[4:36].decode('ascii').strip('\x00'),
        'sw_version': data[36:68].decode('ascii').strip('\x00'),
        'model_version': data[68:100].decode('ascii').strip('\x00'),
        'serial_number': data[100:132].decode('ascii').strip('\x00'),
    }
    return result
```

### Example Output

```
Device SA 36:
  Model: Simrad GPS500
  Software: v3.2.1
  Serial: SIM2024001234

Device SA 42:
  Model: Garmin GNX Wind
  Software: v2.1.0
  Serial: 123-45678-90
```

**Security Implications:**
- Reveals manufacturer and model
- Software version → vulnerability research
- Serial number → unique identifier

<!--
Instructor Notes:

This is powerful reconnaissance data!

Attacker can:
1. Research known vulnerabilities for specific versions
2. Find firmware update exploits
3. Identify high-value targets (autopilot, GPS)
4. Understand network composition

Demo: Show searching for CVEs related to marine electronics.
-->

## Frequency Profiling

### Why Frequency Matters

Each PGN has an expected transmission rate:

| PGN | Expected Rate | Purpose |
|-----|---------------|---------|
| 127250 | 10 Hz | Heading - needs fast updates |
| 129025 | 10 Hz | Position - rapid navigation |
| 130306 | 1 Hz | Wind - slower environmental |
| 127489 | 0.5 Hz | Engine params - low frequency |

### Building a Frequency Baseline

```python
from collections import defaultdict
import statistics

def build_frequency_baseline(capture_file, window_sec=60):
    """Build frequency baseline per PGN"""

    pgn_intervals = defaultdict(list)
    pgn_last_seen = {}

    with open(capture_file) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 4:
                continue

            try:
                ts = float(parts[0].strip('()'))
                can_id = int(parts[2], 16)
                pgn = (can_id >> 8) & 0x3FFFF
                sa = can_id & 0xFF
                key = (pgn, sa)

                if key in pgn_last_seen:
                    interval = ts - pgn_last_seen[key]
                    if interval > 0 and interval < 10:  # Filter outliers
                        pgn_intervals[key].append(interval)

                pgn_last_seen[key] = ts
            except:
                pass

    # Calculate statistics
    baseline = {}
    for key, intervals in pgn_intervals.items():
        if len(intervals) > 10:
            baseline[key] = {
                'mean_interval': statistics.mean(intervals),
                'std_interval': statistics.stdev(intervals),
                'frequency_hz': 1.0 / statistics.mean(intervals),
                'sample_count': len(intervals)
            }

    return baseline

# Usage
baseline = build_frequency_baseline('capture.txt')
for (pgn, sa), stats in sorted(baseline.items()):
    print(f"PGN {pgn:6d} SA {sa:3d}: "
          f"{stats['frequency_hz']:.2f} Hz "
          f"(±{stats['std_interval']*1000:.1f} ms)")
```

<!--
Instructor Notes:

Frequency baseline is CRITICAL for anomaly detection:
- Week 9 builds on this for frequency-based IDS
- Attackers must match baseline to avoid detection
- Deviations indicate attacks or faults

Key insight: Standard deviation tells us expected variation.
Alert if message rate deviates by more than 3 sigma.
-->

## Identifying High-Value Targets

### Critical Maritime Systems

| System | PGNs | Attack Impact |
|--------|------|---------------|
| GPS/Position | 129025, 129026 | Navigation compromise |
| Heading | 127250, 127251 | Autopilot manipulation |
| Depth | 128267 | Grounding risk |
| Engine | 127488, 127489 | Propulsion control |
| AIS | 129038, 129039 | Collision risk |
| Alarms | 126983 | Safety system bypass |

### Target Prioritization

```python
HIGH_VALUE_PGNS = {
    129025: "Position - affects navigation",
    127250: "Heading - affects autopilot",
    128267: "Depth - safety critical",
    127488: "Engine - propulsion control",
    129038: "AIS - collision avoidance",
}

def identify_targets(devices):
    """Identify high-value attack targets"""
    targets = []

    for sa, info in devices.items():
        for pgn in info['pgns']:
            if pgn in HIGH_VALUE_PGNS:
                targets.append({
                    'source_address': sa,
                    'pgn': pgn,
                    'reason': HIGH_VALUE_PGNS[pgn],
                    'message_rate': info['message_count']
                })

    return sorted(targets, key=lambda x: x['pgn'])
```

<!--
Instructor Notes:

Discuss attack scenarios:
1. Spoof GPS → vessel goes off course
2. Spoof heading → autopilot turns wrong way
3. Spoof depth → false shallow/deep readings
4. Spoof engine → false alarms or ignore real problems

Ask: "Which attack has highest safety impact?"
-->

## Active Reconnaissance

### ISO Request (PGN 59904)

Request specific PGN from device:

```python
def build_iso_request(dest_addr, requested_pgn):
    """
    Build ISO Request message
    PGN 59904 - requests device to send specific PGN
    """
    # CAN ID construction
    priority = 6
    pgn = 59904  # ISO Request PGN
    source_addr = 254  # Use null address

    can_id = (priority << 26) | (pgn << 8) | source_addr

    # Data: 3 bytes containing requested PGN (little-endian)
    data = [
        requested_pgn & 0xFF,
        (requested_pgn >> 8) & 0xFF,
        (requested_pgn >> 16) & 0xFF
    ]

    return can_id, data

# Request product info from device 36
can_id, data = build_iso_request(36, 126996)
```

### Address Claim Monitoring

Watch for new devices:

```python
def monitor_address_claims(capture_file):
    """Monitor PGN 60928 Address Claim messages"""
    claims = []

    with open(capture_file) as f:
        for line in f:
            # Parse and check for PGN 60928
            # Extract NAME (64-bit unique ID)
            # Track address changes
            pass

    return claims
```

<!--
Instructor Notes:

Active recon is DETECTABLE!

An IDS could notice:
- ISO Requests from unknown sources
- Scanning patterns (requesting from all SAs)
- Unusual request frequency

But most maritime systems have NO detection...
-->

## Reconnaissance Report Template

### Network Profile Document

```markdown
# Vessel Network Reconnaissance Report

## Executive Summary
- Devices found: X
- Critical systems: Y
- Capture duration: Z minutes

## Device Inventory

| SA | Model | Software | PGNs | Rate |
|----|-------|----------|------|------|
| 36 | GPS-500 | v3.2 | 5 | 50/s |
| 42 | Wind Sensor | v2.1 | 1 | 1/s |

## Message Frequency Baseline

| PGN | Name | Rate | StdDev |
|-----|------|------|--------|
| 127250 | Heading | 10 Hz | 2 ms |
| 129025 | Position | 10 Hz | 3 ms |

## High-Value Targets

1. GPS (SA 36) - Position data
2. Autopilot (SA 24) - Heading control

## Attack Vectors

1. Position spoofing via PGN 129025
2. Heading manipulation via PGN 127250

## Recommendations

1. Implement frequency monitoring
2. Add device allowlisting
3. Monitor for new source addresses
```

## Defense Considerations

### What Recon Reveals About Our Defenses

If an attacker can easily profile your network:
- No network segmentation
- No device authentication
- No traffic monitoring
- Predictable message patterns

### Defensive Measures

1. **Monitoring**: Detect reconnaissance scanning
2. **Allowlisting**: Alert on unknown Source Addresses
3. **Baseline Deviation**: Detect unusual request patterns
4. **Encryption**: Hide payload contents (limited support)

## Lab Preview: Week 5

In Lab 05, you will:

1. Profile the complete test network
2. Build device inventory with product info
3. Create frequency baseline for all PGNs
4. Identify high-value targets
5. Generate reconnaissance report

**Tools**: Python parser from Lab 03, OpenPlotter capture

## Homework

### Required

1. **Read**: Literature Review Section 4.1.1 and Section 5
2. **Analyze**: Your Lab 01 capture with frequency profiler
3. **Document**: List all devices and their likely functions

### Suggested

- Research: Known vulnerabilities in marine electronics
- Explore: CANboat's device database
- Consider: How would you detect recon activity?

## Discussion Questions

1. Why is passive reconnaissance undetectable on CAN?
2. How could a vessel limit information disclosure?
3. What legitimate reasons exist for ISO Requests?
4. How does frequency profiling help both attackers and defenders?

## References

- [NMEA 2000 Device Classes]
- [ISO 11783 Network Management]
- [CANboat Device Database]

[NMEA 2000 Device Classes]:https://www.nmea.org
[ISO 11783 Network Management]:https://www.iso.org/standard/57556.html
[CANboat Device Database]:https://github.com/canboat/canboat

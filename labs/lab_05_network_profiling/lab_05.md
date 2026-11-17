---
title: "Lab 05"
subtitle: "Network Profiling and Reconnaissance"
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
    Conducting network reconnaissance and building device profiles
---

# Lab 05 -- Network Profiling and Reconnaissance

## Lab Overview

**Duration**: 2 hours
**Prerequisites**: Lab 04 completed, a working NEMO board
**Materials Required**:
- NEMO board (from Lab 04) and a listen-only CAN capture interface
- Computer with Python 3.x
- Access to test NMEA 2000 network

## Objectives

By the end of this lab, you will:

1. Capture extended network traffic
2. Enumerate all devices by Source Address
3. Profile message frequencies
4. Identify critical navigation systems
5. Generate a complete network reconnaissance report

## Ethics Reminder

**IMPORTANT**: The techniques in this lab could be used to plan attacks. We learn reconnaissance to:
- Understand what attackers can discover
- Build accurate baselines for detection
- Design better defenses

All activities are conducted on **isolated test networks only**.

## Part 1: Traffic Capture (30 minutes)

NEMO displays live data but has no capture output, so recording uses a separate,
**listen-only** capture interface: for example a Raspberry Pi with a CAN HAT or a USB-CAN
adapter running SocketCAN (OpenPlotter works too). Your NEMO boards provide the traffic.

### 1.1 Set up the bench

1. Build the test network: backbone with a 120 ohm terminator at each end, your NEMO boards and any available sensors as devices, and the capture interface as one more drop.
2. Configure NEMO sensors (Lab 04, Part 4) so that at least three devices are active.
3. Bring up the capture interface at 250 kbit/s **in listen-only mode** so that it cannot transmit:

```bash
sudo ip link set can0 down
sudo ip link set can0 type can bitrate 250000 listen-only on
sudo ip link set can0 up
```

### 1.2 Record

```bash
# Capture with timestamps for 5 minutes (10-15 minutes gives a better baseline)
timeout 300 candump -ta can0 > lab05_capture.txt

# Check the message count
wc -l lab05_capture.txt
```

**Record**: number of messages captured: ____________

The scripts in this course read lines containing a timestamp, a 29-bit identifier in
hex, and the data bytes. `candump -ta` lines and the provided `datasets/` files both
work with `datasets/capture_io.py`.

### 1.3 No hardware available?

Use `datasets/normal_capture.txt` (synthetic, 5 minutes) and copy it to `lab05_capture.txt`.

<!--
Instructor Notes:

5 minutes is minimum for good frequency profiling.
10-15 minutes is better for a complete baseline.

Ensure the test network has multiple active devices
(for example three configured NEMO sensors).
Confirm the capture interface is listen-only before students connect it.
-->

## Part 2: Device Enumeration (30 minutes)

### 2.1 Parse Capture File

Create device enumeration script:

```python
#!/usr/bin/env python3
"""
device_enumerate.py - Enumerate devices from capture
"""
from collections import defaultdict
import re

def enumerate_devices(capture_file):
    """
    Enumerate all devices by Source Address

    Returns:
        dict: {sa: {'pgns': set, 'count': int, 'first': float, 'last': float}}
    """
    devices = defaultdict(lambda: {
        'pgns': set(),
        'count': 0,
        'first_seen': None,
        'last_seen': None
    })

    # Parse capture file
    with open(capture_file) as f:
        for line in f:
            # Extract timestamp and CAN ID
            # Format may vary - adjust regex as needed
            match = re.search(r'(\d+\.\d+).*?([0-9A-Fa-f]{8})', line)
            if not match:
                continue

            timestamp = float(match.group(1))
            can_id = int(match.group(2), 16)

            # Extract SA and PGN
            sa = can_id & 0xFF
            pgn = (can_id >> 8) & 0x3FFFF

            # Update device info
            dev = devices[sa]
            dev['pgns'].add(pgn)
            dev['count'] += 1
            if dev['first_seen'] is None:
                dev['first_seen'] = timestamp
            dev['last_seen'] = timestamp

    return dict(devices)

def print_device_table(devices):
    """Print device enumeration table"""
    print("\n" + "=" * 70)
    print("DEVICE ENUMERATION")
    print("=" * 70)
    print(f"{'SA':>4} | {'Messages':>10} | {'PGNs':>6} | {'Rate (msg/s)':>12} | Duration")
    print("-" * 70)

    for sa in sorted(devices.keys()):
        info = devices[sa]
        duration = info['last_seen'] - info['first_seen']
        rate = info['count'] / duration if duration > 0 else 0

        print(f"{sa:4d} | {info['count']:10d} | {len(info['pgns']):6d} | "
              f"{rate:12.1f} | {duration:.1f}s")

    print("=" * 70)
    print(f"Total devices: {len(devices)}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python device_enumerate.py <capture_file>")
        sys.exit(1)

    devices = enumerate_devices(sys.argv[1])
    print_device_table(devices)

    # List PGNs per device
    print("\nPGNs per Device:")
    for sa in sorted(devices.keys()):
        pgns = sorted(devices[sa]['pgns'])
        print(f"  SA {sa}: {pgns}")
```

### 2.2 Run Enumeration

```bash
python device_enumerate.py lab05_capture.txt
```

### 2.3 Record Findings

Complete the device inventory table:

| SA | Messages | PGNs | Rate (msg/s) | Likely Device Type |
|----|----------|------|--------------|-------------------|
| | | | | |
| | | | | |
| | | | | |

### 2.4 Identify Device Types

Based on PGNs transmitted, identify likely device types:

| PGN | Name | Device Type |
|-----|------|-------------|
| 127250 | Heading | Compass/Autopilot |
| 129025 | Position | GPS |
| 129026 | COG/SOG | GPS |
| 130306 | Wind | Wind Sensor |
| 128267 | Depth | Depth Sounder |
| 127488 | Engine Rapid | Engine Gateway |
| 127489 | Engine Dynamic | Engine Gateway |

## Part 3: Frequency Profiling (30 minutes)

### 3.1 Build Frequency Baseline

```python
#!/usr/bin/env python3
"""
frequency_profile.py - Build message frequency baseline
"""
from collections import defaultdict
import statistics
import json
import re

def build_frequency_baseline(capture_file):
    """
    Build frequency baseline for each (PGN, SA) pair

    Returns:
        dict: {(pgn, sa): {'mean_interval', 'std_interval', 'frequency', 'count'}}
    """
    # Track timestamps per (pgn, sa)
    timestamps = defaultdict(list)

    with open(capture_file) as f:
        for line in f:
            match = re.search(r'(\d+\.\d+).*?([0-9A-Fa-f]{8})', line)
            if not match:
                continue

            timestamp = float(match.group(1))
            can_id = int(match.group(2), 16)
            sa = can_id & 0xFF
            pgn = (can_id >> 8) & 0x3FFFF
            key = (pgn, sa)

            timestamps[key].append(timestamp)

    # Calculate intervals and statistics
    baseline = {}
    for key, ts_list in timestamps.items():
        if len(ts_list) < 10:  # Need minimum samples
            continue

        # Calculate intervals
        intervals = []
        for i in range(1, len(ts_list)):
            interval = ts_list[i] - ts_list[i-1]
            if 0 < interval < 10:  # Filter outliers
                intervals.append(interval)

        if len(intervals) < 5:
            continue

        # Calculate statistics
        mean_interval = statistics.mean(intervals)
        std_interval = statistics.stdev(intervals) if len(intervals) > 1 else 0
        frequency = 1.0 / mean_interval if mean_interval > 0 else 0

        baseline[key] = {
            'mean_interval': round(mean_interval, 6),
            'std_interval': round(std_interval, 6),
            'frequency_hz': round(frequency, 2),
            'sample_count': len(intervals)
        }

    return baseline

def print_frequency_table(baseline):
    """Print frequency baseline table"""
    print("\n" + "=" * 80)
    print("FREQUENCY BASELINE")
    print("=" * 80)
    print(f"{'PGN':>6} | {'SA':>4} | {'Freq (Hz)':>10} | {'Interval (ms)':>14} | "
          f"{'Std (ms)':>10} | Samples")
    print("-" * 80)

    for (pgn, sa) in sorted(baseline.keys()):
        stats = baseline[(pgn, sa)]
        print(f"{pgn:6d} | {sa:4d} | {stats['frequency_hz']:10.2f} | "
              f"{stats['mean_interval']*1000:14.2f} | "
              f"{stats['std_interval']*1000:10.2f} | {stats['sample_count']}")

    print("=" * 80)

def save_baseline(baseline, output_file):
    """Save baseline to JSON file"""
    # Convert tuple keys to strings for JSON
    serializable = {
        f"{pgn}_{sa}": stats
        for (pgn, sa), stats in baseline.items()
    }
    with open(output_file, 'w') as f:
        json.dump(serializable, f, indent=2)
    print(f"Baseline saved to {output_file}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python frequency_profile.py <capture_file> [output_json]")
        sys.exit(1)

    baseline = build_frequency_baseline(sys.argv[1])
    print_frequency_table(baseline)

    if len(sys.argv) >= 3:
        save_baseline(baseline, sys.argv[2])
    else:
        save_baseline(baseline, 'baseline.json')
```

### 3.2 Generate Baseline

```bash
python frequency_profile.py lab05_capture.txt baseline.json
```

### 3.3 Analyze Results

Complete the frequency analysis:

| PGN | Expected Rate | Observed Rate | Deviation |
|-----|---------------|---------------|-----------|
| 127250 (Heading) | 10 Hz | | |
| 129025 (Position) | 10 Hz | | |
| 130306 (Wind) | 1 Hz | | |
| 127488 (Engine) | 10 Hz | | |

**Questions to answer:**
1. Do observed rates match expected NMEA 2000 rates?
2. Which PGNs have highest variability (std deviation)?
3. Any unexpected frequencies?

## Part 4: Target Identification (15 minutes)

### 4.1 Identify Critical Systems

Create script to identify high-value targets:

```python
#!/usr/bin/env python3
"""
identify_targets.py - Identify high-value attack targets
"""

HIGH_VALUE_PGNS = {
    129025: ("Position Rapid", "Navigation", "CRITICAL"),
    127250: ("Vessel Heading", "Autopilot", "CRITICAL"),
    129026: ("COG/SOG", "Navigation", "HIGH"),
    128267: ("Depth", "Safety", "HIGH"),
    127488: ("Engine Rapid", "Propulsion", "HIGH"),
    127489: ("Engine Dynamic", "Propulsion", "HIGH"),
    127505: ("Fluid Level", "Monitoring", "MEDIUM"),
    130306: ("Wind Data", "Environment", "MEDIUM"),
}

def identify_targets(devices):
    """Identify high-value targets from device inventory"""
    targets = []

    for sa, info in devices.items():
        for pgn in info['pgns']:
            if pgn in HIGH_VALUE_PGNS:
                name, category, severity = HIGH_VALUE_PGNS[pgn]
                targets.append({
                    'source_addr': sa,
                    'pgn': pgn,
                    'name': name,
                    'category': category,
                    'severity': severity,
                    'message_count': info['count']
                })

    # Sort by severity
    severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2}
    targets.sort(key=lambda x: severity_order.get(x['severity'], 99))

    return targets

def print_target_report(targets):
    """Print target identification report"""
    print("\n" + "=" * 70)
    print("HIGH-VALUE TARGET IDENTIFICATION")
    print("=" * 70)

    for severity in ['CRITICAL', 'HIGH', 'MEDIUM']:
        severity_targets = [t for t in targets if t['severity'] == severity]
        if severity_targets:
            print(f"\n{severity} TARGETS:")
            for t in severity_targets:
                print(f"  SA {t['source_addr']:3d}: PGN {t['pgn']} - {t['name']} ({t['category']})")

    print("\n" + "=" * 70)
```

### 4.2 Prioritize Targets

Based on your analysis, rank the top 3 attack targets:

1. **Target 1**: SA ___, PGN ___, Reason: _______________
2. **Target 2**: SA ___, PGN ___, Reason: _______________
3. **Target 3**: SA ___, PGN ___, Reason: _______________

## Part 5: Reconnaissance Report (15 minutes)

### 5.1 Generate Report

Compile your findings into a professional reconnaissance report:

```markdown
# Network Reconnaissance Report

## Executive Summary
- Total devices found: ___
- Critical systems identified: ___
- Capture duration: ___ minutes
- Total messages: ___

## Network Inventory

### Device Table
[Include your device enumeration table]

### Device Identification
[Map Source Addresses to likely device types]

## Message Frequency Analysis

### Frequency Baseline
[Include frequency baseline table]

### Anomalies
[Note any unexpected frequencies]

## Critical System Analysis

### High-Value Targets
[List and prioritize targets]

### Attack Surface Assessment
[Describe potential attack vectors]

## Recommendations for Defense

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

## Appendix: Raw Data
[Reference capture file]
```

### 5.2 Defense Perspective

Based on your reconnaissance, answer:

1. What would an IDS need to monitor on this network?
2. Which baselines are most important for detection?
3. What devices should be fingerprinted?

## Deliverables

Submit via course portal:

1. **Capture file** - lab05_capture.txt
2. **Baseline JSON** - baseline.json
3. **Reconnaissance report** - PDF, 3-5 pages
4. **Scripts used** - Python files

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Complete 5+ minute capture | 20 |
| Device enumeration complete | 20 |
| Frequency baseline accurate | 20 |
| Targets correctly identified | 20 |
| Report quality and completeness | 20 |
| **Total** | **100** |

## Discussion Questions

Answer in your report:

1. What information is available through passive reconnaissance?
2. How could this information be used by an attacker?
3. How can defenders use this same information?

## Next Lab Preview

In Lab 06, you will use reconnaissance data to:
- Execute navigation spoofing attacks
- Spoof GPS position messages
- Manipulate heading data
- Observe effects on test display

**Bring your baseline.json file to Lab 06!**

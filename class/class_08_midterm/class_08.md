---
title: "Class 08"
subtitle: "Midterm Review and Practical Assessment"
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
    Midterm examination covering CAN bus fundamentals and attack techniques
---

# Class 08 -- Midterm Review and Practical Assessment

## Session Overview

This session consists of:

1. **Lecture Review** (30 minutes) - Key concepts from Weeks 1-7
2. **Written Examination** (45 minutes) - Theory and analysis
3. **Practical Assessment** (45 minutes) - Hands-on skills demonstration

## Topics Covered

### Module 1: Foundations (Weeks 1-3)

- Maritime cybersecurity landscape
- CAN bus protocol fundamentals
- NMEA 2000 message structure
- PGN encoding and decoding
- Hardware architecture (OpenBridge)

### Module 2: Reconnaissance & Attacks (Weeks 4-7)

- Network reconnaissance techniques
- Device enumeration
- Navigation spoofing
- Engine system attacks
- DoS and replay attacks

## Review: CAN Bus Protocol

### Key Concepts

| Concept | Description | Exam Relevance |
|---------|-------------|----------------|
| Arbitration | Lower ID wins bus access | Priority attacks |
| Broadcast | All nodes receive all messages | No privacy |
| No Authentication | Any node can send any ID | Spoofing |
| Error Handling | TEC/REC counters | Bus-off attacks |

### CAN Frame Structure

```
Extended CAN Frame (NMEA 2000):
┌─────────────┬─────────────┬──────────┬─────────┬─────┐
│  29-bit ID  │ RTR │ IDE │ DLC │ Data (0-8 bytes) │ CRC │
└─────────────┴─────────────┴──────────┴─────────┴─────┘
```

### NMEA 2000 ID Breakdown

```
Bits 28-26: Priority (0-7, lower = higher priority)
Bit 25:     Reserved
Bit 24:     Data Page
Bits 23-16: PDU Format (PF)
Bits 15-8:  PDU Specific (PS) / Destination
Bits 7-0:   Source Address (SA)
```

<!--
Instructor Notes:

Ensure students can:
1. Parse a hex CAN ID into components
2. Calculate PGN from CAN ID
3. Identify priority, source address
4. Explain arbitration implications

Sample exam question:
"Given CAN ID 0x09F80124, identify:
 - Priority
 - PGN
 - Source Address"
-->

## Review: PGN Structure

### PGN Calculation

For PDU Format < 240 (PDU1 - destination specific):
```
PGN = Data Page × 0x10000 + PDU Format × 0x100
```

For PDU Format ≥ 240 (PDU2 - broadcast):
```
PGN = Data Page × 0x10000 + PDU Format × 0x100 + PDU Specific
```

### Critical PGNs

| PGN | Name | Data | Attack Impact |
|-----|------|------|---------------|
| 127250 | Vessel Heading | Heading, deviation | Autopilot manipulation |
| 129025 | Position Rapid | Lat/Lon | Navigation compromise |
| 129026 | COG/SOG Rapid | Course, speed | Route calculation |
| 127488 | Engine Rapid | RPM, boost | Engine monitoring |
| 127489 | Engine Dynamic | Oil, temp | Safety alarms |
| 127505 | Fluid Level | Tank levels | Fuel management |
| 130306 | Wind Data | Speed, angle | Sailing calculations |

<!--
Instructor Notes:

Students should memorize key PGNs:
- Position: 129025
- Heading: 127250
- Engine: 127488, 127489
- Wind: 130306

Exam will include matching PGNs to functions
and identifying which PGNs enable which attacks.
-->

## Review: Reconnaissance

### Passive vs. Active Reconnaissance

| Aspect | Passive | Active |
|--------|---------|--------|
| Traffic generated | None | Requests sent |
| Detection risk | None | Possible |
| Information gathered | Limited | Detailed |
| Example | Monitor traffic | ISO Request |

### Device Enumeration

```python
# Key code pattern for enumeration
def enumerate_devices(capture):
    devices = {}
    for frame in capture:
        sa = frame.can_id & 0xFF
        pgn = (frame.can_id >> 8) & 0x3FFFF
        if sa not in devices:
            devices[sa] = {'pgns': set(), 'count': 0}
        devices[sa]['pgns'].add(pgn)
        devices[sa]['count'] += 1
    return devices
```

### Frequency Profiling

- Each PGN has expected transmission rate
- Position/Heading: 10 Hz
- Engine: 0.5-10 Hz
- Environment: 1 Hz
- Deviation from baseline indicates anomaly

## Review: Spoofing Attacks

### Position Spoofing (PGN 129025)

```
Byte 0-3: Latitude (1e-7 degrees, signed int32)
Byte 4-7: Longitude (1e-7 degrees, signed int32)
```

**Conversion**: `raw_value = decimal_degrees / 1e-7`

### Heading Spoofing (PGN 127250)

```
Byte 0: SID
Byte 1-2: Heading (radians × 10000)
Byte 3-4: Deviation
Byte 5-6: Variation
Byte 7: Reference
```

**Conversion**: `raw_value = radians × 10000`

### Attack Timing

- Match legitimate message rate
- Gradual changes less detectable
- Consider physical constraints

<!--
Instructor Notes:

Practical exam may require:
1. Calculate raw position values
2. Build spoofed heading message
3. Determine correct transmission rate

Sample calculation:
Position 41.5°N, 71.4°W
Lat_raw = 41.5 / 1e-7 = 415,000,000
Lon_raw = -71.4 / 1e-7 = -714,000,000
-->

## Review: Engine Attacks

### PGN 127488 (Engine Rapid)

| Byte | Field | Resolution |
|------|-------|------------|
| 0 | Instance | - |
| 1-2 | RPM | 0.25 RPM/bit |
| 3-4 | Boost | hPa |
| 5 | Tilt | 0.4%/bit |

### PGN 127489 (Engine Dynamic)

| Field | Resolution | Range |
|-------|------------|-------|
| Oil Pressure | hPa | 0-655 bar |
| Oil Temp | 0.1 K | -273-6280°C |
| Coolant Temp | 0.01 K | -273-655°C |

### Attack Scenarios

1. **Alarm suppression**: Fake normal values
2. **False alarm**: Trigger unnecessary shutdown
3. **Damage induction**: Hide actual problems

## Review: DoS and Replay

### DoS Attack Types

| Type | Method | Detection |
|------|--------|-----------|
| Flood | Max rate transmission | Rate spike |
| Priority | Use ID 0x0 | Priority monitor |
| Error injection | Force bus-off | Error frames |

### Replay Attack Steps

1. Record legitimate traffic
2. Store with timestamps
3. Replay at appropriate time
4. Messages appear legitimate

### Hybrid Attacks

- DoS + Spoof: Block legitimate, inject fake
- Replay + Modify: Change specific fields

## Sample Exam Questions

### Theory Questions

1. Explain why CAN bus arbitration creates a security vulnerability.

2. A vessel's chart plotter shows position 41.5000°N, 71.3500°W.
   An attacker wants to spoof a position 1 nautical mile north.
   Calculate the new latitude and the raw value for PGN 129025.

3. Compare passive and active reconnaissance. What can be learned
   from each, and what are the risks?

4. Describe a scenario where engine parameter spoofing could
   cause physical damage to a vessel.

### Practical Questions

5. Given the following CAN frame, decode it:
   ```
   CAN ID: 09F80124
   Data: F0 7E D7 18 47 A4 BB D5
   ```

   a) What is the PGN?
   b) What is the source address?
   c) What type of message is this?
   d) Decode the payload values.

6. Write Python code to detect a DoS attack based on message rate.

7. Design a replay attack that would make a vessel appear stationary
   while actually moving. What messages would you record and replay?

<!--
Instructor Notes:

Grading rubric for practical questions:

Question 5 (15 points):
- PGN identification: 3 points
- SA identification: 3 points
- Message type: 3 points
- Payload decode: 6 points

Question 6 (15 points):
- Rate calculation: 5 points
- Threshold logic: 5 points
- Alert mechanism: 5 points

Question 7 (20 points):
- PGN selection: 5 points
- Recording strategy: 5 points
- Replay timing: 5 points
- Detection evasion: 5 points
-->

## Practical Assessment

### Part 1: Network Analysis (15 minutes)

Given a capture file:
1. Enumerate all devices by source address
2. Identify critical navigation devices
3. Build frequency profile for position PGN

### Part 2: Attack Construction (15 minutes)

Using OpenBridge:
1. Construct a spoofed position message
2. Calculate appropriate values
3. Inject at correct rate
4. Verify on test display

### Part 3: Detection Implementation (15 minutes)

Write code to:
1. Detect unusual message rates
2. Alert on position jumps > 0.1 nm
3. Track device availability

## Study Checklist

### Must Know (Exam Essential)

- [ ] CAN frame structure and fields
- [ ] NMEA 2000 CAN ID breakdown
- [ ] PGN calculation from CAN ID
- [ ] Position, heading raw value conversion
- [ ] Key PGN numbers and their functions
- [ ] Arbitration vulnerability
- [ ] DoS attack mechanisms
- [ ] Replay attack steps

### Should Know (Comprehensive Understanding)

- [ ] Fast Packet protocol
- [ ] ISO Request mechanism
- [ ] Address claim process
- [ ] Engine parameter PGN structures
- [ ] Error injection details
- [ ] Detection methods

### Nice to Know (Advanced)

- [ ] Clock skew fingerprinting concepts
- [ ] Multi-frame message assembly
- [ ] Proprietary PGN ranges
- [ ] Gateway attack surfaces

## Next Module Preview

### Module 3: Detection (Weeks 9-13)

- Week 9: Frequency-Based Detection
- Week 10: Entropy-Based Detection
- Week 11: Machine Learning Approaches
- Week 12: Device Fingerprinting
- Week 13: Ensemble Detection

### Shift to Defense

From this point forward:
- Focus on **detecting** attacks we learned
- Build **intrusion detection systems**
- Apply **machine learning** to maritime data
- Create **defense architectures**

<!--
Instructor Notes:

Midterm Assessment Structure:

Time: 90 minutes total
- Written: 45 minutes (50 points)
- Practical: 45 minutes (50 points)

Written Section:
- Multiple choice: 10 questions × 2 points = 20 points
- Short answer: 4 questions × 5 points = 20 points
- Analysis: 1 question × 10 points = 10 points

Practical Section:
- Part 1: 15 points
- Part 2: 20 points
- Part 3: 15 points

Passing: 70/100

Materials allowed:
- One page (double-sided) handwritten notes
- Calculator
- PGN reference sheet (provided)
-->

## Homework

### Required

1. **Complete** practice problems set (distributed separately)
2. **Review** all lab reports from Weeks 1-7
3. **Prepare** one-page note sheet for exam

### Study Resources

- Lecture slides and recordings
- Lab documentation
- Literature review sections 2-4
- PGN reference tables

## Office Hours

Additional office hours available before midterm:
- [Schedule to be announced]
- Review sessions available upon request

## References

- All previous week references
- [PGN Quick Reference Card]
- [CAN Protocol Summary]

[PGN Quick Reference Card]:https://www.nmea.org
[CAN Protocol Summary]:https://www.bosch-semiconductors.com

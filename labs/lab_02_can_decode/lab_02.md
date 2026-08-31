---
title: "Lab 02"
author: "Constantine Macris"
date: "2026"
subject: "CAN Frame Analysis"
subtitle: "Decoding at the Bit Level"
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

# Lab 02: CAN Frame Analysis

## Learning Outcomes

- Decode CAN frames from raw captures
- Convert between hexadecimal and binary representations
- Extract CAN ID fields manually
- Understand arbitration by analyzing timing
- Identify error conditions in captures

## Definitions

- **Hex** -- Hexadecimal (base-16) number representation
- **Binary** -- Base-2 number representation
- **Arbitration** -- Process of determining which message transmits first
- **Bit stuffing** -- Insertion of opposite bits to maintain synchronization

## Infrastructure Required

- Captured CAN data from Lab 01 (or provided capture file)
- Python 3.x environment
- Calculator (hex/binary conversion) or online converter
- Optional: Logic analyzer with CAN decode

<!--
Instructor Notes:

PRE-LAB SETUP:
1. Ensure students have capture from Lab 01
2. Provide backup capture file if needed
3. Have hex/binary conversion reference ready
4. Logic analyzer demo if available

Expected duration: 2 hours

This lab builds understanding before we write code in Lab 03.
-->

## Background

In this lab, you will analyze CAN frames at the bit level. Before we can build decoders and detection systems, we need to understand exactly how data is represented on the bus. You'll convert between number formats, extract fields by hand, and verify your understanding with Python.

## Part 1: Number System Review

### Hexadecimal to Binary Conversion

Each hex digit = 4 binary bits (nibble)

| Hex | Binary | Decimal |
|-----|--------|---------|
| 0 | 0000 | 0 |
| 1 | 0001 | 1 |
| 2 | 0010 | 2 |
| 3 | 0011 | 3 |
| 4 | 0100 | 4 |
| 5 | 0101 | 5 |
| 6 | 0110 | 6 |
| 7 | 0111 | 7 |
| 8 | 1000 | 8 |
| 9 | 1001 | 9 |
| A | 1010 | 10 |
| B | 1011 | 11 |
| C | 1100 | 12 |
| D | 1101 | 13 |
| E | 1110 | 14 |
| F | 1111 | 15 |

### Exercise 1.1: Convert Hex to Binary

Convert these CAN IDs to binary (show your work):

1. `0x205` = _________________ (12 bits for standard CAN)
2. `0x7DF` = _________________
3. `0x09F80205` = _________________ (29 bits for extended)

<!--
Instructor Notes:

Answers:
1. 0x205 = 0010 0000 0101 = 001000000101
2. 0x7DF = 0111 1101 1111 = 011111011111
3. 0x09F80205 = 00001 00111111 10000000 00100 00000101
   (padded to 29 bits)

Walk through conversion process on board.
-->

### Exercise 1.2: Convert Binary to Hex

Convert these binary values to hexadecimal:

1. `10110100` = 0x____
2. `11111111` = 0x____
3. `0001100110100010` = 0x____

## Part 2: Extended CAN ID Breakdown

### The 29-bit Extended ID

For NMEA 2000, we use 29-bit extended CAN IDs.

```
Bit Position:  28-26  25  24  23-16   15-8    7-0
Field:         PRI    R   DP   PF      PS      SA
```

### Exercise 2.1: Field Extraction

Given CAN ID `0x09F80205`, extract each field:

**Step 1: Convert to binary (29 bits)**
```
0x09F80205 = 00001 001 1111 1000 0000 0010 0000 0101
```

**Step 2: Group by field**
```
  Priority   R  DP    PF         PS         SA
  000       0  1    00111111   10000000   00100001   00000101
   ↓        ↓  ↓       ↓          ↓          ↓
```

Wait - that doesn't align properly. Let me show you the correct way:

**Correct alignment (29 bits total):**
```
Hex:     0    9    F    8    0    2    0    5
Binary: 0000 1001 1111 1000 0000 0010 0000 0101
        └─┬─┘└─┬─┘└───────┬──────┘└────┬────┘└────┬───┘
          │    │          │            │          │
         pad  PRI+DP     PF          PS         SA
```

**Actual field extraction:**
```python
can_id = 0x09F80205

priority    = (can_id >> 26) & 0x7     # bits 28-26
reserved    = (can_id >> 25) & 0x1     # bit 25
data_page   = (can_id >> 24) & 0x1     # bit 24
pdu_format  = (can_id >> 16) & 0xFF    # bits 23-16
pdu_specific= (can_id >> 8) & 0xFF     # bits 15-8
source_addr = can_id & 0xFF            # bits 7-0

# Result:
# priority = 2
# reserved = 0
# data_page = 0
# pdu_format = 248 (0xF8)
# pdu_specific = 2
# source_addr = 5
```

**Your turn:** Extract fields from `0x19F51324`

| Field | Hex | Decimal |
|-------|-----|---------|
| Priority | ___ | ___ |
| Reserved | ___ | ___ |
| Data Page | ___ | ___ |
| PDU Format | ___ | ___ |
| PDU Specific | ___ | ___ |
| Source Address | ___ | ___ |

**Question 1:** What is the calculated PGN for CAN ID `0x19F51324`?

<!--
Instructor Notes:

Answer for 0x19F51324:
- priority = 6
- reserved = 0
- data_page = 1
- pdu_format = 245 (0xF5)
- pdu_specific = 19 (0x13)
- source_addr = 36 (0x24)

PGN calculation:
- PF = 245 >= 240, so PDU2 format
- PGN = (1 << 16) | (245 << 8) | 19 = 129299

This is PGN 129299: GNSS Control Status
-->

## Part 3: Analyzing Real Captures

### Exercise 3.1: Manual Decode

Take 10 lines from your Lab 01 capture (or use provided file).

For each line, fill in this table:

| CAN ID (hex) | Priority | PGN | SA | Description |
|--------------|----------|-----|----|----|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

Use the PGN reference guide to look up descriptions.

### Exercise 3.2: Python Verification

Write a Python script to verify your manual calculations:

```python
#!/usr/bin/env python3
"""Verify manual CAN ID decoding"""

def decode_can_id(can_id_hex):
    """Decode extended CAN ID into NMEA 2000 fields"""
    can_id = int(can_id_hex, 16)

    priority = (can_id >> 26) & 0x7
    data_page = (can_id >> 24) & 0x1
    pdu_format = (can_id >> 16) & 0xFF
    pdu_specific = (can_id >> 8) & 0xFF
    source_addr = can_id & 0xFF

    # Calculate PGN
    if pdu_format < 240:
        pgn = (data_page << 16) | (pdu_format << 8)
        dest_addr = pdu_specific
    else:
        pgn = (data_page << 16) | (pdu_format << 8) | pdu_specific
        dest_addr = 255  # Broadcast

    return {
        'can_id': can_id_hex,
        'priority': priority,
        'data_page': data_page,
        'pdu_format': pdu_format,
        'pdu_specific': pdu_specific,
        'source_addr': source_addr,
        'pgn': pgn
    }

# Test with your values
test_ids = [
    "09F80205",
    "19F51324",
    # Add more from your capture
]

for can_id in test_ids:
    result = decode_can_id(can_id)
    print(f"CAN ID: {result['can_id']}")
    print(f"  Priority: {result['priority']}")
    print(f"  PGN: {result['pgn']}")
    print(f"  Source Address: {result['source_addr']}")
    print()
```

**Deliverable:** Screenshot showing your script output matching your manual calculations.

## Part 4: Data Field Analysis

### CAN Data Bytes

Each CAN frame carries 0-8 bytes of data. For NMEA 2000, always 8 bytes.

Example:
```
can0  09F80205   [8]  FF FC 02 7C 22 00 FF FF
                      ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑
                      0  1  2  3  4  5  6  7
```

### Byte Order (Endianness)

NMEA 2000 uses **little-endian** for multi-byte values:

```
Bytes: 7C 22
Little-endian: 0x227C = 8828 decimal
Big-endian: 0x7C22 = 31778 decimal (WRONG for NMEA 2000)
```

### Exercise 4.1: Parse Wind Data (PGN 130306)

Wind Data format:
```
Byte 0: SID (Sequence ID)
Byte 1-2: Wind Speed (0.01 m/s resolution)
Byte 3-4: Wind Angle (0.0001 radians)
Byte 5: Reference (0=True, 1=Magnetic, 2=Apparent, 3=True Boat)
Byte 6-7: Reserved
```

Given data: `01 64 00 10 27 02 FF FF`

Decode the wind data:

1. SID = Byte 0 = ____
2. Wind Speed raw = Bytes 1-2 (little-endian) = ____
3. Wind Speed (m/s) = raw × 0.01 = ____
4. Wind Speed (knots) = m/s × 1.944 = ____
5. Wind Angle raw = Bytes 3-4 (little-endian) = ____
6. Wind Angle (radians) = raw × 0.0001 = ____
7. Wind Angle (degrees) = radians × 180/π = ____
8. Reference = Byte 5 = ____

**Question 2:** In human terms, what wind condition does this represent?

<!--
Instructor Notes:

Answer:
1. SID = 0x01 = 1
2. Wind Speed raw = 0x0064 = 100
3. Wind Speed (m/s) = 100 × 0.01 = 1.0 m/s
4. Wind Speed (knots) = 1.0 × 1.944 = 1.94 knots
5. Wind Angle raw = 0x2710 = 10000
6. Wind Angle (radians) = 10000 × 0.0001 = 1.0 rad
7. Wind Angle (degrees) = 1.0 × 57.3 = 57.3°
8. Reference = 0x02 = Apparent

Answer: "1.9 knots of apparent wind at 57 degrees off the bow"
-->

### Exercise 4.2: Parse Position (PGN 129025)

Position Rapid Update format:
```
Byte 0-3: Latitude (1e-7 degrees, signed)
Byte 4-7: Longitude (1e-7 degrees, signed)
```

Given data: `A0 68 B3 18 C0 8B 88 D5`

Decode:

```python
import struct

data = bytes.fromhex("A0 68 B3 18 C0 8B 88 D5".replace(" ", ""))

# Signed 32-bit integers, little-endian
lat_raw = struct.unpack('<i', data[0:4])[0]
lon_raw = struct.unpack('<i', data[4:8])[0]

lat = lat_raw * 1e-7
lon = lon_raw * 1e-7

print(f"Latitude: {lat:.6f}°")
print(f"Longitude: {lon:.6f}°")
```

**Question 3:** Where is this vessel located? (Name the nearest city/body of water)

## Part 5: Arbitration Analysis

### Priority and Arbitration

Lower CAN ID = Higher priority = Wins arbitration

### Exercise 5.1: Determine Winners

If these messages try to transmit simultaneously, which wins?

| Message A | Message B | Winner |
|-----------|-----------|--------|
| 0x09F80205 | 0x19F51324 | ____ |
| 0x0DF11224 | 0x0DF11236 | ____ |
| 0x01F01305 | 0x09F80205 | ____ |

**Question 4:** Why does the winning message win? (Explain in terms of bits)

### Exercise 5.2: Attack Implications

An attacker wants to flood the bus with highest-priority messages.

1. What CAN ID should they use? ____
2. What priority value does this represent? ____
3. How would this affect legitimate traffic? ____

## Part 6: Error Detection

### CRC Verification

CAN includes a 15-bit CRC for error detection. The Teensy's FlexCAN controller handles this automatically, but let's understand it.

### Exercise 6.1: Identifying Errors

In real traffic, errors can appear as:
- Missing messages (dropped)
- Error frames (6 dominant bits)
- Incorrect CRC (rejected by receiver)

Review your capture file. Do you see any anomalies?

```bash
# Look for patterns that might indicate errors
cat capture_lab01.txt | awk '{print $3}' | sort | uniq -c | sort -n | head -20
```

**Question 5:** Are there any CAN IDs that appear unusually few times? What might cause this?

## Part 7: Write a Complete Decoder

### Exercise 7.1: Integration

Combine everything into a decoder that processes a capture file:

```python
#!/usr/bin/env python3
"""Complete CAN frame decoder"""
import sys

PGN_NAMES = {
    127250: "Vessel Heading",
    127251: "Rate of Turn",
    129025: "Position Rapid Update",
    129026: "COG & SOG Rapid Update",
    130306: "Wind Data",
    127488: "Engine Parameters Rapid",
    127505: "Fluid Level",
    # Add more as needed
}

def decode_frame(line):
    """Decode a single candump line"""
    parts = line.strip().split()
    if len(parts) < 4:
        return None

    try:
        # Extract timestamp if present
        if parts[0].startswith('('):
            timestamp = parts[0].strip('()')
            interface = parts[1]
            can_id_hex = parts[2]
            data_start = 4
        else:
            timestamp = None
            interface = parts[0]
            can_id_hex = parts[1]
            data_start = 3

        can_id = int(can_id_hex, 16)

        # Decode CAN ID
        priority = (can_id >> 26) & 0x7
        data_page = (can_id >> 24) & 0x1
        pdu_format = (can_id >> 16) & 0xFF
        pdu_specific = (can_id >> 8) & 0xFF
        source_addr = can_id & 0xFF

        if pdu_format < 240:
            pgn = (data_page << 16) | (pdu_format << 8)
        else:
            pgn = (data_page << 16) | (pdu_format << 8) | pdu_specific

        # Get data bytes
        data_hex = parts[data_start:]
        data = bytes.fromhex(''.join(data_hex))

        return {
            'timestamp': timestamp,
            'can_id': can_id_hex,
            'priority': priority,
            'pgn': pgn,
            'pgn_name': PGN_NAMES.get(pgn, "Unknown"),
            'source_addr': source_addr,
            'data': data
        }
    except Exception as e:
        return None

def main():
    for line in sys.stdin:
        frame = decode_frame(line)
        if frame:
            print(f"[{frame['timestamp']}] PGN {frame['pgn']:6d} ({frame['pgn_name']:25s}) "
                  f"SA:{frame['source_addr']:3d} Data: {frame['data'].hex()}")

if __name__ == "__main__":
    main()
```

Run it:
```bash
cat capture_lab01.txt | python3 decoder.py | head -50
```

**Deliverable:** Modified decoder with at least 10 PGN names filled in.

## Lab Deliverables

Submit the following:

1. **Exercise worksheets** with completed calculations (Parts 1-2)
2. **Decode table** from Exercise 3.1 (10 messages)
3. **Python script** (decoder.py) with 10+ PGN names
4. **Answers** to Questions 1-5
5. **Screenshot** showing decoder output

## Critical Questions

1. How do you convert a hex digit to binary?
2. What determines which message wins arbitration?
3. Why does NMEA 2000 use little-endian byte order?
4. How is the PGN calculated differently for PDU1 vs PDU2?
5. What attack could exploit CAN arbitration?

## Closing Thoughts

You've now decoded CAN frames at the bit level. This foundational understanding is critical for:

- Building decoders that parse real messages
- Understanding how spoofing attacks work
- Implementing detection algorithms
- Debugging when things go wrong

In Lab 03, we'll build a complete PGN parser with field-level decoding.

## References

- [CAN Specification 2.0]
- [NMEA 2000 PGN Database]
- [Hex/Binary Converter]

[CAN Specification 2.0]:https://www.bosch-semiconductors.com/media/ubk_semiconductors/pdf_1/canliteratur/can2spec.pdf
[NMEA 2000 PGN Database]:https://github.com/canboat/canboat/blob/master/analyzer/pgns.json
[Hex/Binary Converter]:https://www.rapidtables.com/convert/number/hex-to-binary.html

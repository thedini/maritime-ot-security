---
title: "Class 02"
subtitle: "NMEA 2000 Protocol and PGN Structure"
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
    NMEA 2000 higher-layer protocol and Parameter Group Numbers
---

# Class 02 -- NMEA 2000 Protocol and PGN Structure

## Learning Outcomes

- Decode NMEA 2000 PGN headers from CAN IDs
- Parse navigation, engine, and environmental messages
- Understand device addressing and NAME assignment
- Identify Product Information (PGN 126996)

## Definitions

- **NMEA** -- National Marine Electronics Association
- **PGN** -- Parameter Group Number
- **PDU** -- Protocol Data Unit
- **SA** -- Source Address
- **DA** -- Destination Address
- **NAME** -- 64-bit unique device identifier
- **Fast Packet** -- Multi-frame message protocol

## Reading Assignment

- Literature Review: Section 2.3 (NMEA 2000 and Maritime CAN)
- IEC 61162-3 overview (provided excerpt)
- NMEA 2000 PGN quick reference guide

## NMEA Standards Family

| Standard | Physical Layer | Data Rate | Description |
|----------|---------------|-----------|-------------|
| NMEA 0183 | RS-422 serial | 4800 baud | Legacy, ASCII-based |
| NMEA 2000 | CAN 2.0B | 250 kbps | Modern, binary |
| NMEA OneNet | Ethernet | 100 Mbps+ | Emerging standard |

**This course focuses on NMEA 2000 (CAN-based)**

<!--
Instructor Notes:

Historical context:
- NMEA 0183 from 1983, still widely used
- NMEA 2000 from 2001, based on SAE J1939
- NMEA OneNet announced 2020, Ethernet-based

Many vessels have BOTH 0183 and 2000 networks with gateways.

Ask: "Why would a vessel still use NMEA 0183?"
(Legacy equipment, simpler, cheaper sensors)
-->

## NMEA 2000 vs SAE J1939

NMEA 2000 is built on J1939 (truck/bus standard):

| Aspect | SAE J1939 | NMEA 2000 |
|--------|-----------|-----------|
| Industry | Automotive/Trucking | Marine |
| Physical | CAN 2.0B | CAN 2.0B |
| Bitrate | 250 kbps | 250 kbps |
| Connector | Deutsch | DeviceNet (micro) |
| PGN Range | 0-65535 | Subset + marine-specific |
| Message Types | Engine, transmission | Navigation, environment |

**Same protocol, different application domain!**

## CAN ID to PGN Decoding

### 29-bit Extended CAN ID Structure

```
 28  26 25 24 23        16 15         8 7          0
┌────┬──┬──┬──┬───────────┬────────────┬────────────┐
│ P  │R │DP│  │    PF     │    PS      │     SA     │
│ 3  │1 │1 │  │    8      │    8       │     8      │
└────┴──┴──┴──┴───────────┴────────────┴────────────┘
  │   │  │        │            │             │
  │   │  │        │            │             └── Source Address
  │   │  │        │            └── PDU Specific (Group Extension or DA)
  │   │  │        └── PDU Format
  │   │  └── Data Page
  │   └── Reserved (always 0)
  └── Priority (0-7, lower = higher priority)
```

<!--
Instructor Notes:

Draw this on the board and walk through each field.

Key insight: The PGN is NOT simply bits 8-25!
The calculation depends on PDU Format value.

This is where students often get confused - spend time here.
-->

## PGN Calculation Rules

The PGN calculation depends on the **PDU Format (PF)** value:

### If PF < 240 (0xF0): PDU1 Format (Peer-to-Peer)

```
PGN = (DP << 16) | (PF << 8)
PS field = Destination Address
```

### If PF >= 240 (0xF0): PDU2 Format (Broadcast)

```
PGN = (DP << 16) | (PF << 8) | PS
PS field = Group Extension (part of PGN)
```

**Most NMEA 2000 messages are PDU2 (broadcast)**

## Example: Decoding CAN ID 0x09F80205

```python
can_id = 0x09F80205

# Extract fields
priority = (can_id >> 26) & 0x7      # Bits 26-28
reserved = (can_id >> 25) & 0x1       # Bit 25 (always 0)
data_page = (can_id >> 24) & 0x1      # Bit 24
pdu_format = (can_id >> 16) & 0xFF    # Bits 16-23
pdu_specific = (can_id >> 8) & 0xFF   # Bits 8-15
source_addr = can_id & 0xFF           # Bits 0-7

print(f"Priority: {priority}")        # 2
print(f"Data Page: {data_page}")      # 0
print(f"PDU Format: {pdu_format}")    # 248 (0xF8)
print(f"PDU Specific: {pdu_specific}")# 2
print(f"Source Address: {source_addr}")# 5

# Calculate PGN (PF >= 240, so PDU2)
pgn = (data_page << 16) | (pdu_format << 8) | pdu_specific
print(f"PGN: {pgn}")                  # 63490 (0xF802)
```

<!--
Instructor Notes:

Work through this example step by step.

Have students calculate by hand before showing Python.

Quiz question: "What is the PGN for CAN ID 0x0DF11324?"
Answer:
- PF = 0xF1 = 241 >= 240, so PDU2
- PGN = (0 << 16) | (241 << 8) | 19 = 61715
-->

## Common NMEA 2000 PGNs

### Navigation PGNs

| PGN | Name | Update Rate | Description |
|-----|------|-------------|-------------|
| 127250 | Vessel Heading | 10 Hz | Heading sensor value |
| 127251 | Rate of Turn | 10 Hz | Rate of turn |
| 129025 | Position Rapid Update | 10 Hz | Latitude/Longitude |
| 129026 | COG & SOG Rapid Update | 10 Hz | Course and speed over ground |
| 129029 | GNSS Position Data | 1 Hz | Full GNSS position |
| 129539 | GNSS DOPs | 1 Hz | Dilution of precision |
| 129540 | GNSS Satellites in View | 1 Hz | Satellite information |

<!--
Instructor Notes:

These are the most common navigation PGNs.

Key point: "Rapid Update" PGNs are high-frequency (10 Hz)
They are prime targets for spoofing attacks!

Week 6 lab will spoof 129025 and 127250.
-->

### Engine PGNs

| PGN | Name | Update Rate | Description |
|-----|------|-------------|-------------|
| 127488 | Engine Parameters Rapid | 10 Hz | RPM, tilt, trim |
| 127489 | Engine Parameters Dynamic | 0.5 Hz | Temp, pressure, hours |
| 127493 | Transmission Parameters | 10 Hz | Gear, oil pressure |
| 127497 | Trip Parameters Engine | 1 Hz | Fuel rate, economy |
| 127505 | Fluid Level | 2.5 Hz | Tank levels |

### Environmental PGNs

| PGN | Name | Update Rate | Description |
|-----|------|-------------|-------------|
| 130306 | Wind Data | 1 Hz | Wind speed and angle |
| 130310 | Environmental Parameters | 0.5 Hz | Water temp, pressure |
| 130311 | Environmental Parameters | 0.5 Hz | Humidity, temp |
| 130312 | Temperature | 0.5 Hz | Various temp sources |
| 128267 | Water Depth | 10 Hz | Depth below transducer |

## PGN Data Field Structure

Each PGN has a defined data structure. Example: **PGN 127250 (Vessel Heading)**

```
Byte 0:    SID (Sequence ID)
Byte 1-2:  Heading (radians × 10000, unsigned)
Byte 3-4:  Deviation (radians × 10000, signed)
Byte 5-6:  Variation (radians × 10000, signed)
Byte 7:    Reference (2 bits: 0=True, 1=Magnetic, 2=Error)
           Reserved (6 bits)
```

### Decoding Example

```python
# Raw data: FF 7C 22 00 00 00 00 FC
data = bytes([0xFF, 0x7C, 0x22, 0x00, 0x00, 0x00, 0x00, 0xFC])

sid = data[0]  # 0xFF = 255 (not available)
heading_raw = data[1] | (data[2] << 8)  # 0x227C = 8828
heading_rad = heading_raw * 0.0001  # 0.8828 radians
heading_deg = heading_rad * 180 / 3.14159  # ~50.6 degrees

reference = data[7] & 0x03  # 0 = True North

print(f"Heading: {heading_deg:.1f}° {['True','Magnetic','Error'][reference]}")
```

<!--
Instructor Notes:

Walk through the byte-by-byte decoding.

Key points:
- Multi-byte values are little-endian
- Resolution/scaling varies by field
- 0xFF or 0xFFFF often means "not available"

Lab 03 will have students build a full PGN decoder.
-->

## Fast Packet Protocol

Some PGNs exceed 8 bytes and use **Fast Packet**:

- First frame: Sequence counter + total bytes + data start
- Subsequent frames: Sequence counter + continuation data
- Up to 223 bytes total (32 frames)

### Fast Packet PGNs

| PGN | Name | Size | Frames |
|-----|------|------|--------|
| 126996 | Product Information | 134 bytes | 17 |
| 129029 | GNSS Position Data | 43 bytes | 6 |
| 129038 | AIS Class A Position | 27 bytes | 4 |
| 129794 | AIS Class A Static | 76 bytes | 10 |

<!--
Instructor Notes:

Fast Packet is more complex to decode.

Show the frame structure:
Frame 0: [Seq:5][Total:8][Data0-5]
Frame 1: [Seq:5][Data6-12]
...

The sequence counter (bits 5-7) identifies the message group.
The frame counter (bits 0-4) orders frames within a message.
-->

## Device Addressing

### Source Address (SA)

- 8-bit value (0-255)
- Assigned dynamically via Address Claim
- Some addresses reserved (e.g., 254 = Null, 255 = Global)

### NAME (64-bit Unique Identifier)

Every NMEA 2000 device has a unique NAME:

```
Bits 0-20:   Identity Number (unique per manufacturer)
Bits 21-31:  Manufacturer Code (assigned by NMEA)
Bits 32-34:  Device Instance (lower 3 bits)
Bits 35-39:  Device Instance (upper 5 bits)
Bits 40-47:  Device Function
Bits 48-54:  Device Class
Bits 55:     Reserved
Bits 56-58:  System Instance
Bits 59-60:  Industry Group (4 = Marine)
Bits 61-63:  Self-Configurable Address (1 = yes)
```

### Address Claim (PGN 60928)

When a device joins the network:

1. Device broadcasts its NAME on PGN 60928
2. If address conflict, lower NAME value wins
3. Loser must claim different address
4. All devices monitor for conflicts

<!--
Instructor Notes:

Address claim is important for understanding device identity.

Security implication:
- Attacker can claim any address!
- Can impersonate legitimate devices
- No authentication of NAME

Quiz: "What Industry Group value indicates marine?" (4)
-->

## Product Information (PGN 126996)

Devices broadcast their identity:

```
Field               Size    Description
NMEA 2000 Version   2 bytes Protocol version
Product Code        2 bytes Manufacturer product ID
Model ID            32 bytes ASCII string
Software Version    32 bytes ASCII string
Model Version       32 bytes ASCII string
Model Serial Code   32 bytes ASCII string
Certification Level 1 byte  NMEA certification
Load Equivalency    1 byte  Network load units
```

**This is reconnaissance gold!**

<!--
Instructor Notes:

PGN 126996 reveals:
- Device manufacturer
- Model number
- Software version
- Serial number

Attacker uses this to:
- Identify vulnerable firmware versions
- Target specific device types
- Understand network composition

Lab 01 captured this data!
-->

## Building a PGN Decoder

### Step 1: Parse CAN ID

```python
def parse_can_id(can_id):
    priority = (can_id >> 26) & 0x7
    data_page = (can_id >> 24) & 0x1
    pdu_format = (can_id >> 16) & 0xFF
    pdu_specific = (can_id >> 8) & 0xFF
    source_addr = can_id & 0xFF

    if pdu_format < 240:
        pgn = (data_page << 16) | (pdu_format << 8)
        dest_addr = pdu_specific
    else:
        pgn = (data_page << 16) | (pdu_format << 8) | pdu_specific
        dest_addr = 255  # Broadcast

    return {
        'priority': priority,
        'pgn': pgn,
        'source': source_addr,
        'destination': dest_addr
    }
```

### Step 2: Decode Data Fields

```python
PGN_DECODERS = {
    127250: decode_vessel_heading,
    129025: decode_position_rapid,
    130306: decode_wind_data,
    # ... more decoders
}

def decode_message(can_id, data):
    header = parse_can_id(can_id)
    pgn = header['pgn']

    if pgn in PGN_DECODERS:
        header['fields'] = PGN_DECODERS[pgn](data)
    else:
        header['fields'] = {'raw': data.hex()}

    return header
```

## Security Implications

### No Message Authentication

- Any device can send any PGN
- Source Address easily spoofed
- NAME can be fabricated

### No Encryption

- All data visible on bus
- Position, speed, heading exposed
- Fuel levels, engine status visible

### Predictable Timing

- Update rates are standardized
- Attacker can anticipate messages
- Easy to inject between legitimate messages

<!--
Instructor Notes:

Emphasize these vulnerabilities:
1. Anyone with $10 adapter can read all traffic
2. Anyone can inject any message
3. No way for receivers to verify authenticity

This is WHY we need anomaly detection!
-->

## Lab Preview: Week 3

In Lab 03, you will:

1. Build a complete PGN parser in Python
2. Decode navigation PGNs (position, heading, COG/SOG)
3. Decode engine PGNs (RPM, temperature)
4. Handle Fast Packet messages
5. Create human-readable output

**Tools**: Python, captured traffic from Lab 01

## Homework

### Required

1. **Read**: Literature Review Section 2.3
2. **Practice**: Decode these CAN IDs to PGNs:
   - 0x09F11205
   - 0x0DF80136
   - 0x19F51324
3. **Calculate**: What heading (degrees) is represented by raw value 0x4E20?

### Suggested

- Read: NMEA 2000 PGN reference guide (provided)
- Watch: "NMEA 2000 Explained" (YouTube - Actisense)
- Explore: CANboat project on GitHub

## Discussion Questions

1. Why does NMEA 2000 use broadcast messages instead of addressed?
2. How would you detect a device impersonating another via Address Claim?
3. What information in PGN 126996 would help an attacker?
4. Why are "Rapid Update" PGNs sent at 10 Hz?

## References

- [NMEA 2000 Overview]
- [SAE J1939 Standard]
- [CANboat PGN Database]
- [Actisense NMEA Reader]

[NMEA 2000 Overview]:https://www.nmea.org/content/STANDARDS/NMEA_2000
[SAE J1939 Standard]:https://www.sae.org/standards/content/j1939_201710/
[CANboat PGN Database]:https://github.com/canboat/canboat
[Actisense NMEA Reader]:https://actisense.com/acti_software/nmea-reader/

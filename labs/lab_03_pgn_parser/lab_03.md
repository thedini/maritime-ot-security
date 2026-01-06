---
title: "Lab 03"
author: "Constantine Macris"
date: "2026"
subject: "PGN Parser Development"
subtitle: "Building a Complete NMEA 2000 Decoder"
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

# Lab 03: PGN Parser Development

## Learning Outcomes

- Build a complete PGN parser in Python
- Decode navigation PGNs (position, heading, COG/SOG)
- Decode engine and environmental PGNs
- Handle multi-byte values with correct byte order
- Create human-readable output for vessel monitoring

## Definitions

- **Parser** -- Software that interprets structured data
- **Resolution** -- Smallest change representable in a value
- **Scaling** -- Converting raw values to engineering units
- **Sentinel** -- Special value indicating data not available

## Infrastructure Required

- Python 3.x environment
- Captured CAN data from Lab 01
- PGN reference documentation
- Text editor or IDE

<!--
Instructor Notes:

PRE-LAB SETUP:
1. Ensure students have capture file ready
2. Provide PGN field definitions document
3. Have working solution available for demo
4. Test Python environment

Expected duration: 2-3 hours

This lab builds a tool they'll use throughout the course.
-->

## Background

In this lab, you'll build a comprehensive PGN parser that converts raw NMEA 2000 messages into human-readable data. This is the foundation for monitoring systems, anomaly detection, and understanding vessel network traffic.

## Part 1: Project Structure

### Create Project Directory

```bash
mkdir -p ~/nmea2000_parser
cd ~/nmea2000_parser
```

### File Structure

```
nmea2000_parser/
├── parser.py         # Main parser module
├── pgn_defs.py       # PGN definitions
├── utils.py          # Utility functions
├── test_parser.py    # Unit tests
└── analyze.py        # Analysis script
```

## Part 2: Utility Functions

### Create `utils.py`

```python
#!/usr/bin/env python3
"""Utility functions for NMEA 2000 parsing"""
import struct
import math

def hex_to_bytes(hex_str):
    """Convert hex string to bytes"""
    return bytes.fromhex(hex_str.replace(" ", ""))

def get_uint8(data, offset):
    """Extract unsigned 8-bit integer"""
    return data[offset]

def get_int8(data, offset):
    """Extract signed 8-bit integer"""
    return struct.unpack('b', data[offset:offset+1])[0]

def get_uint16(data, offset):
    """Extract unsigned 16-bit integer (little-endian)"""
    return struct.unpack('<H', data[offset:offset+2])[0]

def get_int16(data, offset):
    """Extract signed 16-bit integer (little-endian)"""
    return struct.unpack('<h', data[offset:offset+2])[0]

def get_uint32(data, offset):
    """Extract unsigned 32-bit integer (little-endian)"""
    return struct.unpack('<I', data[offset:offset+4])[0]

def get_int32(data, offset):
    """Extract signed 32-bit integer (little-endian)"""
    return struct.unpack('<i', data[offset:offset+4])[0]

def radians_to_degrees(rad):
    """Convert radians to degrees"""
    return rad * 180.0 / math.pi

def ms_to_knots(ms):
    """Convert m/s to knots"""
    return ms * 1.94384

def is_data_available(value, max_val):
    """Check if value indicates 'data not available'"""
    # Common sentinel values
    if value == max_val:
        return False
    if value == max_val - 1:  # Often used for "out of range"
        return False
    return True

# Reference type lookups
HEADING_REFERENCE = {
    0: "True",
    1: "Magnetic",
    2: "Error",
    3: "Null"
}

WIND_REFERENCE = {
    0: "True (ground)",
    1: "Magnetic",
    2: "Apparent",
    3: "True (boat)",
    4: "True (water)"
}

GNSS_TYPE = {
    0: "GPS",
    1: "GLONASS",
    2: "GPS+GLONASS",
    3: "GPS+SBAS",
    4: "GPS+SBAS+GLONASS",
    5: "Chayka",
    6: "Integrated",
    7: "Surveyed",
    8: "Galileo"
}
```

<!--
Instructor Notes:

These utility functions handle:
- Byte extraction with correct endianness
- Unit conversions
- Sentinel value detection

Key point: Little-endian is critical!
Many students get this wrong initially.

Demo the difference:
data = b'\x7C\x22'
little = struct.unpack('<H', data)[0]  # 8828
big = struct.unpack('>H', data)[0]     # 31778
-->

## Part 3: PGN Definitions

### Create `pgn_defs.py`

```python
#!/usr/bin/env python3
"""PGN definitions and decoders for NMEA 2000"""
from utils import *

def decode_127250_vessel_heading(data):
    """
    PGN 127250: Vessel Heading
    Rate: 10 Hz
    """
    result = {}

    # Byte 0: SID
    result['sid'] = get_uint8(data, 0)

    # Bytes 1-2: Heading (radians * 10000)
    raw_heading = get_uint16(data, 1)
    if is_data_available(raw_heading, 0xFFFF):
        heading_rad = raw_heading * 0.0001
        result['heading_deg'] = round(radians_to_degrees(heading_rad), 1)
    else:
        result['heading_deg'] = None

    # Bytes 3-4: Deviation (radians * 10000, signed)
    raw_dev = get_int16(data, 3)
    if raw_dev != 0x7FFF:
        result['deviation_deg'] = round(radians_to_degrees(raw_dev * 0.0001), 2)
    else:
        result['deviation_deg'] = None

    # Bytes 5-6: Variation (radians * 10000, signed)
    raw_var = get_int16(data, 5)
    if raw_var != 0x7FFF:
        result['variation_deg'] = round(radians_to_degrees(raw_var * 0.0001), 2)
    else:
        result['variation_deg'] = None

    # Byte 7: Reference (bits 0-1)
    ref_type = get_uint8(data, 7) & 0x03
    result['reference'] = HEADING_REFERENCE.get(ref_type, "Unknown")

    return result


def decode_129025_position_rapid(data):
    """
    PGN 129025: Position Rapid Update
    Rate: 10 Hz
    """
    result = {}

    # Bytes 0-3: Latitude (1e-7 degrees, signed)
    raw_lat = get_int32(data, 0)
    if raw_lat != 0x7FFFFFFF:
        result['latitude'] = round(raw_lat * 1e-7, 7)
    else:
        result['latitude'] = None

    # Bytes 4-7: Longitude (1e-7 degrees, signed)
    raw_lon = get_int32(data, 4)
    if raw_lon != 0x7FFFFFFF:
        result['longitude'] = round(raw_lon * 1e-7, 7)
    else:
        result['longitude'] = None

    return result


def decode_129026_cog_sog_rapid(data):
    """
    PGN 129026: COG & SOG Rapid Update
    Rate: 10 Hz
    """
    result = {}

    # Byte 0: SID
    result['sid'] = get_uint8(data, 0)

    # Byte 1: COG Reference (bits 0-1)
    ref = get_uint8(data, 1) & 0x03
    result['cog_reference'] = HEADING_REFERENCE.get(ref, "Unknown")

    # Bytes 2-3: COG (radians * 10000)
    raw_cog = get_uint16(data, 2)
    if is_data_available(raw_cog, 0xFFFF):
        result['cog_deg'] = round(radians_to_degrees(raw_cog * 0.0001), 1)
    else:
        result['cog_deg'] = None

    # Bytes 4-5: SOG (0.01 m/s)
    raw_sog = get_uint16(data, 4)
    if is_data_available(raw_sog, 0xFFFF):
        result['sog_knots'] = round(ms_to_knots(raw_sog * 0.01), 2)
    else:
        result['sog_knots'] = None

    return result


def decode_130306_wind_data(data):
    """
    PGN 130306: Wind Data
    Rate: 1 Hz
    """
    result = {}

    # Byte 0: SID
    result['sid'] = get_uint8(data, 0)

    # Bytes 1-2: Wind Speed (0.01 m/s)
    raw_speed = get_uint16(data, 1)
    if is_data_available(raw_speed, 0xFFFF):
        result['wind_speed_knots'] = round(ms_to_knots(raw_speed * 0.01), 1)
    else:
        result['wind_speed_knots'] = None

    # Bytes 3-4: Wind Angle (radians * 10000)
    raw_angle = get_uint16(data, 3)
    if is_data_available(raw_angle, 0xFFFF):
        result['wind_angle_deg'] = round(radians_to_degrees(raw_angle * 0.0001), 1)
    else:
        result['wind_angle_deg'] = None

    # Byte 5: Reference (bits 0-2)
    ref = get_uint8(data, 5) & 0x07
    result['reference'] = WIND_REFERENCE.get(ref, "Unknown")

    return result


def decode_127488_engine_rapid(data):
    """
    PGN 127488: Engine Parameters, Rapid Update
    Rate: 10 Hz
    """
    result = {}

    # Byte 0: Engine Instance
    result['instance'] = get_uint8(data, 0)

    # Bytes 1-2: Engine Speed (0.25 RPM)
    raw_rpm = get_uint16(data, 1)
    if is_data_available(raw_rpm, 0xFFFF):
        result['rpm'] = round(raw_rpm * 0.25, 0)
    else:
        result['rpm'] = None

    # Bytes 3-4: Engine Boost Pressure (100 Pa)
    raw_boost = get_uint16(data, 3)
    if is_data_available(raw_boost, 0xFFFF):
        result['boost_kpa'] = round(raw_boost * 0.1, 1)
    else:
        result['boost_kpa'] = None

    # Byte 5: Engine Tilt/Trim (%)
    raw_tilt = get_int8(data, 5)
    if raw_tilt != 0x7F:
        result['tilt_pct'] = raw_tilt
    else:
        result['tilt_pct'] = None

    return result


def decode_127505_fluid_level(data):
    """
    PGN 127505: Fluid Level
    Rate: 2.5 Hz
    """
    result = {}

    # Byte 0: Instance + Type
    instance_type = get_uint8(data, 0)
    result['instance'] = instance_type & 0x0F
    result['type'] = (instance_type >> 4) & 0x0F

    fluid_types = {
        0: "Fuel",
        1: "Water",
        2: "Gray Water",
        3: "Live Well",
        4: "Oil",
        5: "Black Water"
    }
    result['fluid_name'] = fluid_types.get(result['type'], "Unknown")

    # Bytes 1-2: Level (0.004% per bit)
    raw_level = get_uint16(data, 1)
    if is_data_available(raw_level, 0xFFFF):
        result['level_pct'] = round(raw_level * 0.004, 1)
    else:
        result['level_pct'] = None

    # Bytes 3-6: Capacity (0.1 L)
    raw_capacity = get_uint32(data, 3)
    if is_data_available(raw_capacity, 0xFFFFFFFF):
        result['capacity_liters'] = round(raw_capacity * 0.1, 1)
    else:
        result['capacity_liters'] = None

    return result


# Registry of decoders
PGN_DECODERS = {
    127250: ("Vessel Heading", decode_127250_vessel_heading),
    129025: ("Position Rapid Update", decode_129025_position_rapid),
    129026: ("COG & SOG Rapid Update", decode_129026_cog_sog_rapid),
    130306: ("Wind Data", decode_130306_wind_data),
    127488: ("Engine Parameters Rapid", decode_127488_engine_rapid),
    127505: ("Fluid Level", decode_127505_fluid_level),
}
```

<!--
Instructor Notes:

Key teaching points:

1. Resolution/scaling varies by field
   - Heading: 0.0001 rad
   - Position: 1e-7 degrees
   - Speed: 0.01 m/s

2. Sentinel values indicate "not available"
   - 0xFFFF for unsigned 16-bit
   - 0x7FFF for signed 16-bit
   - 0x7FFFFFFF for signed 32-bit

3. Bit fields within bytes
   - Reference types use only 2-3 bits
   - Must mask: value & 0x03

Students will add more decoders for homework.
-->

## Part 4: Main Parser

### Create `parser.py`

```python
#!/usr/bin/env python3
"""
NMEA 2000 Parser
Decodes CAN frames from candump output
"""
import sys
import json
from datetime import datetime
from pgn_defs import PGN_DECODERS
from utils import hex_to_bytes

class NMEA2000Parser:
    def __init__(self):
        self.message_count = 0
        self.pgn_counts = {}
        self.source_addresses = set()

    def parse_can_id(self, can_id):
        """Extract NMEA 2000 fields from 29-bit CAN ID"""
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
            'source_address': source_addr,
            'destination_address': dest_addr
        }

    def parse_line(self, line):
        """Parse a single candump line"""
        parts = line.strip().split()
        if len(parts) < 4:
            return None

        try:
            # Handle timestamp format: (1234567890.123456)
            if parts[0].startswith('('):
                timestamp_str = parts[0].strip('()')
                timestamp = float(timestamp_str)
                interface = parts[1]
                can_id_hex = parts[2]
                # Skip [8] length indicator
                data_parts = parts[4:]
            else:
                timestamp = None
                interface = parts[0]
                can_id_hex = parts[1]
                data_parts = parts[3:]

            can_id = int(can_id_hex, 16)
            header = self.parse_can_id(can_id)

            # Build data bytes
            data = hex_to_bytes(''.join(data_parts))

            # Track statistics
            self.message_count += 1
            pgn = header['pgn']
            self.pgn_counts[pgn] = self.pgn_counts.get(pgn, 0) + 1
            self.source_addresses.add(header['source_address'])

            # Decode if we have a decoder
            decoded = None
            pgn_name = "Unknown"
            if pgn in PGN_DECODERS:
                pgn_name, decoder_func = PGN_DECODERS[pgn]
                try:
                    decoded = decoder_func(data)
                except Exception as e:
                    decoded = {'error': str(e)}

            return {
                'timestamp': timestamp,
                'interface': interface,
                'can_id': can_id_hex,
                'header': header,
                'pgn_name': pgn_name,
                'data_raw': data.hex(),
                'decoded': decoded
            }

        except Exception as e:
            return {'error': str(e), 'line': line}

    def format_output(self, msg, verbose=False):
        """Format message for display"""
        if 'error' in msg and 'header' not in msg:
            return f"ERROR: {msg['error']}"

        header = msg['header']
        ts = f"[{msg['timestamp']:.6f}]" if msg['timestamp'] else ""

        basic = (f"{ts} PGN {header['pgn']:6d} ({msg['pgn_name']:25s}) "
                f"SA:{header['source_address']:3d} Pri:{header['priority']}")

        if verbose and msg['decoded']:
            decoded_str = json.dumps(msg['decoded'], indent=2)
            return f"{basic}\n{decoded_str}"
        elif msg['decoded']:
            # Single-line decoded values
            vals = []
            for k, v in msg['decoded'].items():
                if v is not None and k not in ['sid', 'instance']:
                    vals.append(f"{k}={v}")
            return f"{basic} | {', '.join(vals)}"
        else:
            return f"{basic} | raw={msg['data_raw']}"

    def get_statistics(self):
        """Return parsing statistics"""
        return {
            'total_messages': self.message_count,
            'unique_pgns': len(self.pgn_counts),
            'unique_sources': len(self.source_addresses),
            'pgn_counts': dict(sorted(self.pgn_counts.items(),
                                      key=lambda x: -x[1])),
            'source_addresses': sorted(self.source_addresses)
        }


def main():
    import argparse

    arg_parser = argparse.ArgumentParser(description='NMEA 2000 Parser')
    arg_parser.add_argument('-v', '--verbose', action='store_true',
                           help='Show detailed decoded output')
    arg_parser.add_argument('-s', '--stats', action='store_true',
                           help='Show statistics at end')
    arg_parser.add_argument('-j', '--json', action='store_true',
                           help='Output as JSON')
    arg_parser.add_argument('--filter-pgn', type=int,
                           help='Only show specific PGN')
    arg_parser.add_argument('--filter-sa', type=int,
                           help='Only show specific Source Address')
    args = arg_parser.parse_args()

    parser = NMEA2000Parser()

    for line in sys.stdin:
        msg = parser.parse_line(line)
        if msg and 'header' in msg:
            # Apply filters
            if args.filter_pgn and msg['header']['pgn'] != args.filter_pgn:
                continue
            if args.filter_sa and msg['header']['source_address'] != args.filter_sa:
                continue

            if args.json:
                print(json.dumps(msg))
            else:
                print(parser.format_output(msg, args.verbose))

    if args.stats:
        print("\n" + "="*60)
        print("STATISTICS")
        print("="*60)
        stats = parser.get_statistics()
        print(f"Total messages: {stats['total_messages']}")
        print(f"Unique PGNs: {stats['unique_pgns']}")
        print(f"Unique Sources: {stats['unique_sources']}")
        print(f"\nSource Addresses: {stats['source_addresses']}")
        print("\nTop PGNs:")
        for pgn, count in list(stats['pgn_counts'].items())[:10]:
            name = PGN_DECODERS.get(pgn, ("Unknown",))[0]
            print(f"  PGN {pgn:6d} ({name:25s}): {count:6d}")


if __name__ == "__main__":
    main()
```

<!--
Instructor Notes:

Key features of parser:
1. Handles candump timestamp format
2. Statistics tracking
3. Filtering by PGN or Source Address
4. JSON output option for integration
5. Error handling

Run demo:
cat capture.txt | python3 parser.py -s
cat capture.txt | python3 parser.py --filter-pgn 127250
cat capture.txt | python3 parser.py -v | head -50
-->

## Part 5: Testing

### Create `test_parser.py`

```python
#!/usr/bin/env python3
"""Unit tests for NMEA 2000 parser"""
import unittest
from utils import *
from pgn_defs import *
from parser import NMEA2000Parser

class TestUtils(unittest.TestCase):

    def test_get_uint16_little_endian(self):
        data = bytes([0x7C, 0x22])  # Should be 0x227C = 8828
        self.assertEqual(get_uint16(data, 0), 8828)

    def test_get_int32_negative(self):
        # -414000000 in little-endian
        data = bytes.fromhex("00 9C 4D E7")
        val = get_int32(data, 0)
        self.assertEqual(val, -414000000)

    def test_radians_to_degrees(self):
        self.assertAlmostEqual(radians_to_degrees(1.5708), 90.0, places=1)


class TestPGNDecoders(unittest.TestCase):

    def test_decode_heading(self):
        # Heading: 90 degrees magnetic
        # 90 deg = 1.5708 rad, * 10000 = 15708 = 0x3D5C
        data = bytes([0x01,  # SID
                     0x5C, 0x3D,  # Heading
                     0xFF, 0x7F,  # Deviation N/A
                     0xFF, 0x7F,  # Variation N/A
                     0x01])  # Reference = Magnetic

        result = decode_127250_vessel_heading(data)
        self.assertEqual(result['sid'], 1)
        self.assertAlmostEqual(result['heading_deg'], 90.0, places=0)
        self.assertEqual(result['reference'], "Magnetic")

    def test_decode_position(self):
        # 41.5°N, -71.4°W
        # Lat: 41.5 / 1e-7 = 415000000 = 0x18B9C4A0
        # Lon: -71.4 / 1e-7 = -714000000 = 0xD588BDC0
        data = bytes.fromhex("A0 C4 B9 18 C0 BD 88 D5")

        result = decode_129025_position_rapid(data)
        self.assertAlmostEqual(result['latitude'], 41.5, places=1)
        self.assertAlmostEqual(result['longitude'], -71.4, places=1)

    def test_decode_wind(self):
        # 15 knots apparent at 45 degrees
        # 15 kts = 7.72 m/s, / 0.01 = 772 = 0x0304
        # 45 deg = 0.785 rad, / 0.0001 = 7854 = 0x1EAE
        data = bytes([0x01,  # SID
                     0x04, 0x03,  # Speed
                     0xAE, 0x1E,  # Angle
                     0x02,  # Reference = Apparent
                     0xFF, 0xFF])

        result = decode_130306_wind_data(data)
        self.assertAlmostEqual(result['wind_speed_knots'], 15.0, places=0)
        self.assertAlmostEqual(result['wind_angle_deg'], 45.0, places=0)
        self.assertEqual(result['reference'], "Apparent")


class TestParser(unittest.TestCase):

    def test_parse_can_id(self):
        parser = NMEA2000Parser()
        result = parser.parse_can_id(0x09F80205)

        self.assertEqual(result['priority'], 2)
        self.assertEqual(result['pgn'], 63490)
        self.assertEqual(result['source_address'], 5)

    def test_parse_line(self):
        parser = NMEA2000Parser()
        line = "(1234567890.123456)  can0  09F10224   [8]  01 5C 3D 00 00 00 00 01"

        result = parser.parse_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result['header']['pgn'], 127250)


if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python3 -m pytest test_parser.py -v
# or
python3 test_parser.py
```

## Part 6: Analysis Script

### Create `analyze.py`

```python
#!/usr/bin/env python3
"""
Analyze NMEA 2000 capture for anomalies and patterns
"""
import sys
import json
from collections import defaultdict
from parser import NMEA2000Parser
from pgn_defs import PGN_DECODERS

def analyze_capture(filename):
    """Analyze a capture file for patterns"""

    parser = NMEA2000Parser()
    pgn_values = defaultdict(list)
    timestamps = []
    first_ts = None
    last_ts = None

    # Parse all messages
    with open(filename, 'r') as f:
        for line in f:
            msg = parser.parse_line(line)
            if msg and 'header' in msg:
                pgn = msg['header']['pgn']
                ts = msg['timestamp']

                if ts:
                    if first_ts is None:
                        first_ts = ts
                    last_ts = ts
                    timestamps.append(ts)

                if msg['decoded']:
                    pgn_values[pgn].append({
                        'timestamp': ts,
                        'source': msg['header']['source_address'],
                        'data': msg['decoded']
                    })

    # Calculate statistics
    duration = last_ts - first_ts if first_ts and last_ts else 0

    print("="*60)
    print("CAPTURE ANALYSIS REPORT")
    print("="*60)
    print(f"Duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
    print(f"Total messages: {parser.message_count}")
    print(f"Messages/second: {parser.message_count/duration:.1f}" if duration > 0 else "")

    # PGN frequency analysis
    print("\n" + "-"*40)
    print("PGN FREQUENCIES")
    print("-"*40)

    stats = parser.get_statistics()
    for pgn, count in list(stats['pgn_counts'].items())[:15]:
        name = PGN_DECODERS.get(pgn, ("Unknown",))[0]
        freq = count / duration * 60 if duration > 0 else 0
        print(f"PGN {pgn:6d} ({name:25s}): {count:6d} msgs, {freq:.1f}/min")

    # Device analysis
    print("\n" + "-"*40)
    print("DEVICE ANALYSIS")
    print("-"*40)

    device_pgns = defaultdict(set)
    for pgn, values in pgn_values.items():
        for v in values:
            device_pgns[v['source']].add(pgn)

    for sa in sorted(device_pgns.keys()):
        pgns = device_pgns[sa]
        print(f"\nSource Address {sa}:")
        for pgn in sorted(pgns):
            name = PGN_DECODERS.get(pgn, ("Unknown",))[0]
            print(f"  - PGN {pgn}: {name}")

    # Value analysis for key PGNs
    print("\n" + "-"*40)
    print("VALUE ANALYSIS")
    print("-"*40)

    # Heading analysis
    if 127250 in pgn_values:
        headings = [v['data'].get('heading_deg') for v in pgn_values[127250]
                   if v['data'].get('heading_deg') is not None]
        if headings:
            print(f"\nHeading (PGN 127250):")
            print(f"  Min: {min(headings):.1f}°")
            print(f"  Max: {max(headings):.1f}°")
            print(f"  Avg: {sum(headings)/len(headings):.1f}°")

    # Position analysis
    if 129025 in pgn_values:
        lats = [v['data'].get('latitude') for v in pgn_values[129025]
               if v['data'].get('latitude') is not None]
        lons = [v['data'].get('longitude') for v in pgn_values[129025]
               if v['data'].get('longitude') is not None]
        if lats and lons:
            print(f"\nPosition (PGN 129025):")
            print(f"  Lat range: {min(lats):.6f}° to {max(lats):.6f}°")
            print(f"  Lon range: {min(lons):.6f}° to {max(lons):.6f}°")

    # Wind analysis
    if 130306 in pgn_values:
        speeds = [v['data'].get('wind_speed_knots') for v in pgn_values[130306]
                 if v['data'].get('wind_speed_knots') is not None]
        if speeds:
            print(f"\nWind (PGN 130306):")
            print(f"  Min: {min(speeds):.1f} kts")
            print(f"  Max: {max(speeds):.1f} kts")
            print(f"  Avg: {sum(speeds)/len(speeds):.1f} kts")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyze.py <capture_file>")
        sys.exit(1)

    analyze_capture(sys.argv[1])
```

Run analysis:
```bash
python3 analyze.py capture_lab01.txt
```

## Part 7: Exercises

### Exercise 7.1: Add PGN Decoder

Add a decoder for **PGN 127489: Engine Parameters, Dynamic**:

```
Byte 0: Engine Instance
Bytes 1-2: Oil Pressure (100 Pa)
Bytes 3-4: Oil Temperature (0.1 K)
Bytes 5-6: Temperature (0.01 K)
Byte 7: Discrete Status 1
```

Add to `pgn_defs.py` and register in `PGN_DECODERS`.

### Exercise 7.2: Add PGN Decoder

Add a decoder for **PGN 128267: Water Depth**:

```
Byte 0: SID
Bytes 1-4: Depth (0.01 m)
Bytes 5-6: Offset (0.001 m, signed)
Byte 7: Range (10 m)
```

### Exercise 7.3: Filter Implementation

Add a time-range filter to `parser.py`:

```bash
python3 parser.py --start-time 1234567890 --end-time 1234567900
```

## Lab Deliverables

Submit the following:

1. **Complete parser package** (all .py files)
2. **Two additional PGN decoders** (Exercises 7.1 and 7.2)
3. **Analysis report** output for your Lab 01 capture
4. **Screenshot** of parser running with `--filter-pgn`
5. **Test output** showing all tests passing

## Critical Questions

1. Why must we use little-endian byte order?
2. What does a sentinel value of 0xFFFF indicate?
3. How do you extract a 2-bit field from a byte?
4. Why track statistics while parsing?
5. How would you extend this parser for Fast Packet messages?

## Closing Thoughts

You now have a working NMEA 2000 parser that can:

- Decode CAN frames to PGN information
- Parse field-level data with correct scaling
- Handle multiple message types
- Generate analysis reports

This parser is the foundation for:

- Week 5: Network reconnaissance
- Week 6-8: Attack implementation
- Week 9-12: Anomaly detection
- Week 13: Integrated IDS

Keep improving it as we add more capabilities!

## References

- [CANboat Analyzer]
- [NMEA 2000 Appendix B]
- [Python struct module]

[CANboat Analyzer]:https://github.com/canboat/canboat
[NMEA 2000 Appendix B]:https://www.nmea.org
[Python struct module]:https://docs.python.org/3/library/struct.html

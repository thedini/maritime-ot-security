# NMEA 2000 PGN Library

A standardized, open-source library of NMEA 2000 Parameter Group Number (PGN) definitions available in multiple formats for maritime cybersecurity research and development.

## Overview

This library provides comprehensive PGN definitions extracted from the NMEA 2000 specification, enhanced with data from the CANboat project and validated against real vessel traffic captures.

## Available Formats

| Format | File | Use Case |
|--------|------|----------|
| JSON | `dist/pgns.json` | Web applications, Python, JavaScript |
| YAML | `dist/pgns.yaml` | Configuration files, Kubernetes, Ansible |
| SQL | `dist/pgns.sql` | Database import (SQLite, PostgreSQL, MySQL) |
| CSV | `dist/pgns.csv` | Spreadsheets, data analysis |

## Quick Start

### Python
```python
import json

with open('dist/pgns.json') as f:
    pgns = json.load(f)

# Look up a PGN
heading = next(p for p in pgns['PGNs'] if p['PGN'] == 127250)
print(f"PGN 127250: {heading['Description']}")
```

### JavaScript
```javascript
import pgns from './dist/pgns.json';

const position = pgns.PGNs.find(p => p.PGN === 129025);
console.log(`PGN 129025: ${position.Description}`);
```

### SQL
```sql
-- Import the schema and data
.read dist/pgns.sql

-- Query navigation PGNs
SELECT pgn, description FROM pgns
WHERE category = 'Navigation';
```

## PGN Categories

| Category | PGN Range | Examples |
|----------|-----------|----------|
| ISO/Protocol | 59392-65240 | Address Claim, Transport Protocol |
| Navigation | 127250-129029 | Heading, Position, COG/SOG |
| Engine | 127488-127509 | RPM, Temperature, Fuel |
| Environmental | 130306-130316 | Wind, Depth, Water Temperature |
| Electrical | 127500-127510 | Battery, Charger Status |
| Entertainment | 130816+ | Audio, Zones, Sources |

## Schema

Each PGN entry contains:

```yaml
PGN: 127250
Id: vesselHeading
Description: Vessel Heading
Priority: 2
Category: Navigation
TransmissionInterval: 100  # milliseconds
Length: 8  # bytes
Fields:
  - Order: 1
    Id: sid
    Name: SID
    BitLength: 8
    BitOffset: 0
    FieldType: NUMBER
  - Order: 2
    Id: heading
    Name: Heading
    BitLength: 16
    BitOffset: 8
    Resolution: 0.0001  # radians
    FieldType: NUMBER
    Unit: rad
```

## Building from Source

### Prerequisites
- Python 3.8+
- PyYAML

### Generate All Formats
```bash
# Install dependencies
pip install pyyaml

# Generate distribution files
python scripts/generate.py

# Validate output
python scripts/validate.py
```

### GitHub Actions

The library automatically rebuilds on push via GitHub Actions:
- Validates JSON schema
- Generates YAML, SQL, CSV formats
- Creates release artifacts
- Publishes to GitHub Packages

## Data Sources

1. **NMEA 2000 Specification** - Official PGN definitions (proprietary)
2. **CANboat Project** - Open-source reverse-engineered definitions
3. **Field Captures** - Validated against real NMEA 2000 traffic

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Add or update PGN definitions in `src/pgns.json`
3. Run validation: `python scripts/validate.py`
4. Submit a pull request

### Adding a New PGN

```json
{
  "PGN": 130820,
  "Id": "newPgn",
  "Description": "New PGN Description",
  "Priority": 6,
  "Category": "Custom",
  "Type": "Single",
  "Complete": true,
  "Length": 8,
  "Fields": [...]
}
```

## License

This project is licensed under the MIT License.

Note: NMEA 2000 is a trademark of the National Marine Electronics Association. This project is not affiliated with or endorsed by NMEA.

## Related Projects

- [CANboat](https://github.com/canboat/canboat) - NMEA 2000 analyzer
- [SignalK](https://signalk.org/) - Open marine data format
- [NMEA2000 Library](https://github.com/ttlappalainen/NMEA2000) - Arduino library

## Citation

If you use this library in academic work, please cite:

```bibtex
@misc{nmea2000-pgn-library,
  author = {Maritime OT Security Research},
  title = {NMEA 2000 PGN Library},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/maritime-ot-security/pgn-library}
}
```

## Acknowledgments

- CANboat project for open-source PGN definitions
- Timo Lappalainen for NMEA2000 Arduino library documentation
- SignalK community for data format insights

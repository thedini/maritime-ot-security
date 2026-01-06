#!/usr/bin/env python3
"""
generate.py - Generate PGN library in multiple formats

Reads src/pgns.json and generates:
- dist/pgns.json (formatted)
- dist/pgns.yaml
- dist/pgns.sql
- dist/pgns.csv
"""

import json
import os
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None
    print("Warning: PyYAML not installed, skipping YAML generation")


def load_source():
    """Load source PGN definitions"""
    src_path = Path(__file__).parent.parent / "src" / "pgns.json"
    with open(src_path) as f:
        return json.load(f)


def generate_json(data, output_dir):
    """Generate formatted JSON output"""
    output_path = output_dir / "pgns.json"

    # Add metadata
    data["CreatedAt"] = datetime.utcnow().isoformat() + "Z"

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Generated: {output_path}")
    return output_path


def generate_yaml(data, output_dir):
    """Generate YAML output"""
    if yaml is None:
        return None

    output_path = output_dir / "pgns.yaml"

    with open(output_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Generated: {output_path}")
    return output_path


def generate_sql(data, output_dir):
    """Generate SQL schema and data"""
    output_path = output_dir / "pgns.sql"

    sql_lines = [
        "-- NMEA 2000 PGN Library SQL Schema",
        f"-- Generated: {datetime.utcnow().isoformat()}Z",
        f"-- Version: {data.get('Version', 'unknown')}",
        "",
        "-- Drop existing tables",
        "DROP TABLE IF EXISTS pgn_fields;",
        "DROP TABLE IF EXISTS pgns;",
        "DROP TABLE IF EXISTS pgn_categories;",
        "",
        "-- Categories table",
        "CREATE TABLE pgn_categories (",
        "    category_id INTEGER PRIMARY KEY,",
        "    name TEXT NOT NULL UNIQUE,",
        "    description TEXT",
        ");",
        "",
        "INSERT INTO pgn_categories (category_id, name, description) VALUES",
        "    (1, 'Protocol', 'ISO and NMEA protocol messages'),",
        "    (2, 'Navigation', 'Position, heading, speed, course'),",
        "    (3, 'Engine', 'Engine parameters and status'),",
        "    (4, 'Propulsion', 'Propulsion system data'),",
        "    (5, 'Electrical', 'Battery, charging, power'),",
        "    (6, 'Environmental', 'Wind, depth, temperature'),",
        "    (7, 'Entertainment', 'Audio and multimedia'),",
        "    (8, 'Communication', 'Radio and messaging'),",
        "    (9, 'Steering', 'Autopilot and rudder'),",
        "    (10, 'Custom', 'Manufacturer-specific'),",
        "    (11, 'Unknown', 'Unclassified');",
        "",
        "-- Main PGN table",
        "CREATE TABLE pgns (",
        "    pgn INTEGER PRIMARY KEY,",
        "    id TEXT,",
        "    description TEXT NOT NULL,",
        "    explanation TEXT,",
        "    priority INTEGER CHECK (priority BETWEEN 0 AND 7),",
        "    category_id INTEGER REFERENCES pgn_categories(category_id),",
        "    type TEXT CHECK (type IN ('Single', 'Fast', 'ISO')),",
        "    complete BOOLEAN DEFAULT FALSE,",
        "    field_count INTEGER DEFAULT 0,",
        "    length INTEGER,",
        "    transmission_interval_ms INTEGER,",
        "    transmission_irregular BOOLEAN DEFAULT FALSE",
        ");",
        "",
        "-- Fields table",
        "CREATE TABLE pgn_fields (",
        "    field_id INTEGER PRIMARY KEY AUTOINCREMENT,",
        "    pgn INTEGER REFERENCES pgns(pgn),",
        "    field_order INTEGER NOT NULL,",
        "    id TEXT,",
        "    name TEXT NOT NULL,",
        "    description TEXT,",
        "    bit_length INTEGER NOT NULL,",
        "    bit_offset INTEGER DEFAULT 0,",
        "    bit_start INTEGER DEFAULT 0,",
        "    resolution REAL DEFAULT 1.0,",
        "    offset_value REAL DEFAULT 0.0,",
        "    signed BOOLEAN DEFAULT FALSE,",
        "    range_min REAL,",
        "    range_max REAL,",
        "    unit TEXT,",
        "    field_type TEXT,",
        "    lookup_enumeration TEXT,",
        "    UNIQUE(pgn, field_order)",
        ");",
        "",
        "-- Create indexes",
        "CREATE INDEX idx_pgns_category ON pgns(category_id);",
        "CREATE INDEX idx_pgn_fields_pgn ON pgn_fields(pgn);",
        "",
        "-- Insert PGN data",
    ]

    # Category mapping
    category_map = {
        "Protocol": 1, "Navigation": 2, "Engine": 3, "Propulsion": 4,
        "Electrical": 5, "Environmental": 6, "Entertainment": 7,
        "Communication": 8, "Steering": 9, "Custom": 10, "Unknown": 11
    }

    # Insert PGNs
    for pgn in data.get("PGNs", []):
        pgn_num = pgn.get("PGN", 0)
        pgn_id = escape_sql(pgn.get("Id", ""))
        desc = escape_sql(pgn.get("Description", ""))
        explanation = escape_sql(pgn.get("Explanation", ""))
        priority = pgn.get("Priority", "NULL")
        category = category_map.get(pgn.get("Category", "Unknown"), 11)
        ptype = pgn.get("Type", "")
        complete = 1 if pgn.get("Complete", False) else 0
        field_count = pgn.get("FieldCount", 0)
        length = pgn.get("Length", "NULL")
        interval = pgn.get("TransmissionInterval", "NULL")
        irregular = 1 if pgn.get("TransmissionIrregular", False) else 0

        sql_lines.append(
            f"INSERT INTO pgns VALUES ({pgn_num}, '{pgn_id}', '{desc}', "
            f"'{explanation}', {priority}, {category}, '{ptype}', {complete}, "
            f"{field_count}, {length}, {interval}, {irregular});"
        )

        # Insert fields
        for field in pgn.get("Fields", []):
            order = field.get("Order", 0)
            fid = escape_sql(field.get("Id", ""))
            fname = escape_sql(field.get("Name", ""))
            fdesc = escape_sql(field.get("Description", ""))
            bit_length = field.get("BitLength", 0)
            bit_offset = field.get("BitOffset", 0)
            bit_start = field.get("BitStart", 0)
            resolution = field.get("Resolution", 1.0)
            offset_val = field.get("Offset", 0.0)
            signed = 1 if field.get("Signed", False) else 0
            range_min = field.get("RangeMin", "NULL")
            range_max = field.get("RangeMax", "NULL")
            unit = escape_sql(field.get("Unit", ""))
            ftype = field.get("FieldType", "")
            lookup = escape_sql(field.get("LookupEnumeration", ""))

            sql_lines.append(
                f"INSERT INTO pgn_fields (pgn, field_order, id, name, description, "
                f"bit_length, bit_offset, bit_start, resolution, offset_value, signed, "
                f"range_min, range_max, unit, field_type, lookup_enumeration) VALUES "
                f"({pgn_num}, {order}, '{fid}', '{fname}', '{fdesc}', {bit_length}, "
                f"{bit_offset}, {bit_start}, {resolution}, {offset_val}, {signed}, "
                f"{range_min}, {range_max}, '{unit}', '{ftype}', '{lookup}');"
            )

    sql_lines.append("")
    sql_lines.append("-- Useful views")
    sql_lines.append("CREATE VIEW v_navigation_pgns AS")
    sql_lines.append("SELECT * FROM pgns WHERE category_id = 2;")
    sql_lines.append("")
    sql_lines.append("CREATE VIEW v_engine_pgns AS")
    sql_lines.append("SELECT * FROM pgns WHERE category_id = 3;")
    sql_lines.append("")

    with open(output_path, "w") as f:
        f.write("\n".join(sql_lines))

    print(f"Generated: {output_path}")
    return output_path


def generate_csv(data, output_dir):
    """Generate CSV output (PGN summary only)"""
    output_path = output_dir / "pgns.csv"

    lines = ["PGN,Id,Description,Priority,Category,Type,Complete,FieldCount,Length"]

    for pgn in data.get("PGNs", []):
        row = [
            str(pgn.get("PGN", "")),
            pgn.get("Id", ""),
            escape_csv(pgn.get("Description", "")),
            str(pgn.get("Priority", "")),
            pgn.get("Category", ""),
            pgn.get("Type", ""),
            str(pgn.get("Complete", False)),
            str(pgn.get("FieldCount", 0)),
            str(pgn.get("Length", ""))
        ]
        lines.append(",".join(row))

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Generated: {output_path}")
    return output_path


def escape_sql(value):
    """Escape single quotes for SQL"""
    if value is None:
        return ""
    return str(value).replace("'", "''")


def escape_csv(value):
    """Escape and quote CSV values"""
    if value is None:
        return ""
    s = str(value)
    if "," in s or '"' in s or "\n" in s:
        return '"' + s.replace('"', '""') + '"'
    return s


def main():
    # Setup paths
    project_root = Path(__file__).parent.parent
    output_dir = project_root / "dist"
    output_dir.mkdir(exist_ok=True)

    # Load source
    print("Loading source PGN definitions...")
    data = load_source()
    print(f"Loaded {len(data.get('PGNs', []))} PGN definitions")

    # Generate all formats
    generate_json(data, output_dir)
    generate_yaml(data, output_dir)
    generate_sql(data, output_dir)
    generate_csv(data, output_dir)

    print("\nGeneration complete!")


if __name__ == "__main__":
    main()

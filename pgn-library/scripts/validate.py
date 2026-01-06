#!/usr/bin/env python3
"""
validate.py - Validate PGN library against schema

Checks:
1. JSON schema validation
2. PGN number uniqueness
3. Field bit alignment
4. Required field presence
"""

import json
import sys
from pathlib import Path

try:
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False
    print("Warning: jsonschema not installed, skipping schema validation")


def load_json(path):
    """Load JSON file"""
    with open(path) as f:
        return json.load(f)


def validate_schema(data, schema):
    """Validate data against JSON schema"""
    if not HAS_JSONSCHEMA:
        return True, []

    errors = []
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        errors.append(f"Schema validation error: {e.message}")
        if e.path:
            errors.append(f"  Path: {'.'.join(str(p) for p in e.path)}")

    return len(errors) == 0, errors


def validate_pgn_uniqueness(data):
    """Check for duplicate PGN numbers"""
    errors = []
    seen_pgns = {}

    for pgn in data.get("PGNs", []):
        pgn_num = pgn.get("PGN")
        pgn_id = pgn.get("Id", "unknown")

        if pgn_num in seen_pgns:
            # Allow duplicates if one is a fallback
            existing = seen_pgns[pgn_num]
            if pgn.get("Fallback") or existing.get("Fallback"):
                continue
            errors.append(
                f"Duplicate PGN {pgn_num}: '{pgn_id}' and '{existing.get('Id', 'unknown')}'"
            )
        else:
            seen_pgns[pgn_num] = pgn

    return len(errors) == 0, errors


def validate_field_alignment(data):
    """Check field bit offsets and lengths"""
    errors = []
    warnings = []

    for pgn in data.get("PGNs", []):
        pgn_num = pgn.get("PGN")
        fields = pgn.get("Fields", [])
        pgn_length = pgn.get("Length", 8) * 8  # Convert to bits

        expected_offset = 0
        for field in fields:
            order = field.get("Order", 0)
            bit_offset = field.get("BitOffset", 0)
            bit_length = field.get("BitLength", 0)
            name = field.get("Name", f"field{order}")

            # Check offset alignment (warning only)
            if bit_offset != expected_offset:
                warnings.append(
                    f"PGN {pgn_num} field '{name}': offset {bit_offset} != expected {expected_offset}"
                )

            # Check for overflow
            if bit_offset + bit_length > pgn_length:
                errors.append(
                    f"PGN {pgn_num} field '{name}': exceeds message length "
                    f"({bit_offset + bit_length} > {pgn_length} bits)"
                )

            expected_offset = bit_offset + bit_length

    return len(errors) == 0, errors, warnings


def validate_required_fields(data):
    """Check required fields are present"""
    errors = []

    for pgn in data.get("PGNs", []):
        pgn_num = pgn.get("PGN")

        if pgn_num is None:
            errors.append("PGN entry missing 'PGN' number")
            continue

        if not pgn.get("Description"):
            errors.append(f"PGN {pgn_num}: missing 'Description'")

    return len(errors) == 0, errors


def validate_categories(data):
    """Check category values are valid"""
    valid_categories = {
        "Protocol", "Navigation", "Engine", "Propulsion", "Electrical",
        "Environmental", "Entertainment", "Communication", "Steering",
        "Custom", "Unknown"
    }
    errors = []

    for pgn in data.get("PGNs", []):
        category = pgn.get("Category")
        if category and category not in valid_categories:
            errors.append(
                f"PGN {pgn.get('PGN')}: invalid category '{category}'"
            )

    return len(errors) == 0, errors


def main():
    project_root = Path(__file__).parent.parent
    src_path = project_root / "src" / "pgns.json"
    schema_path = project_root / "schemas" / "pgn.schema.json"

    print("=" * 60)
    print("PGN Library Validation")
    print("=" * 60)

    # Load source
    if not src_path.exists():
        print(f"ERROR: Source file not found: {src_path}")
        sys.exit(1)

    print(f"\nLoading: {src_path}")
    data = load_json(src_path)
    print(f"Found {len(data.get('PGNs', []))} PGN definitions")

    all_errors = []
    all_warnings = []

    # Schema validation
    if schema_path.exists() and HAS_JSONSCHEMA:
        print("\n1. Schema validation...")
        schema = load_json(schema_path)
        valid, errors = validate_schema(data, schema)
        if valid:
            print("   PASSED")
        else:
            print("   FAILED")
            all_errors.extend(errors)
    else:
        print("\n1. Schema validation... SKIPPED")

    # Uniqueness validation
    print("\n2. PGN uniqueness...")
    valid, errors = validate_pgn_uniqueness(data)
    if valid:
        print("   PASSED")
    else:
        print("   FAILED")
        all_errors.extend(errors)

    # Field alignment
    print("\n3. Field alignment...")
    valid, errors, warnings = validate_field_alignment(data)
    if valid:
        print("   PASSED")
    else:
        print("   FAILED")
        all_errors.extend(errors)
    all_warnings.extend(warnings)

    # Required fields
    print("\n4. Required fields...")
    valid, errors = validate_required_fields(data)
    if valid:
        print("   PASSED")
    else:
        print("   FAILED")
        all_errors.extend(errors)

    # Categories
    print("\n5. Category validation...")
    valid, errors = validate_categories(data)
    if valid:
        print("   PASSED")
    else:
        print("   FAILED")
        all_errors.extend(errors)

    # Summary
    print("\n" + "=" * 60)
    if all_errors:
        print(f"VALIDATION FAILED: {len(all_errors)} error(s)")
        print("=" * 60)
        for error in all_errors:
            print(f"  ERROR: {error}")
        sys.exit(1)
    else:
        print("VALIDATION PASSED")
        if all_warnings:
            print(f"  ({len(all_warnings)} warning(s))")
            for warning in all_warnings[:5]:  # Show first 5
                print(f"  WARNING: {warning}")
            if len(all_warnings) > 5:
                print(f"  ... and {len(all_warnings) - 5} more warnings")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
add_categories.py - Add category labels to PGN definitions

Categories are inferred from PGN ranges and descriptions.
"""

import json
import re
from pathlib import Path


# PGN category mappings
CATEGORY_RANGES = {
    # Protocol/ISO messages (59392-65535)
    (59392, 65535): "Protocol",
    # Navigation (127250-129029, 130306-130316)
    (127250, 127260): "Navigation",  # Heading, rate of turn
    (129025, 129030): "Navigation",  # Position, COG/SOG
    (130306, 130320): "Environmental",  # Wind, depth
    # Engine/Propulsion (127488-127510)
    (127488, 127510): "Engine",
    # Electrical (127500-127510)
    (127500, 127510): "Electrical",
    # Entertainment (130816+)
    (130816, 131000): "Entertainment",
}

KEYWORD_CATEGORIES = {
    "Navigation": ["heading", "position", "gps", "gnss", "waypoint", "route", "cog", "sog", "xte", "rudder", "steering"],
    "Engine": ["engine", "rpm", "temperature", "oil", "fuel", "coolant", "exhaust", "throttle"],
    "Propulsion": ["propulsion", "transmission", "gear", "shaft"],
    "Electrical": ["battery", "charger", "voltage", "current", "power", "dc", "ac", "inverter"],
    "Environmental": ["wind", "depth", "humidity", "temperature", "pressure", "water"],
    "Communication": ["radio", "dsc", "ais", "distress", "call"],
    "Steering": ["autopilot", "rudder", "helm"],
    "Entertainment": ["entertainment", "audio", "zone", "source", "volume"],
    "Protocol": ["iso", "transport", "address", "claim", "acknowledge", "request"],
}


def categorize_pgn(pgn_num, description, pgn_id=""):
    """Determine category for a PGN"""
    desc_lower = (description or "").lower()
    id_lower = (pgn_id or "").lower()

    # Check keyword matches first (more specific)
    for category, keywords in KEYWORD_CATEGORIES.items():
        for keyword in keywords:
            if keyword in desc_lower or keyword in id_lower:
                return category

    # Check PGN ranges
    for (start, end), category in CATEGORY_RANGES.items():
        if start <= pgn_num <= end:
            return category

    return "Unknown"


def add_categories(data):
    """Add category to each PGN in the data"""
    for pgn in data.get("PGNs", []):
        if "Category" not in pgn:
            pgn["Category"] = categorize_pgn(
                pgn.get("PGN", 0),
                pgn.get("Description", ""),
                pgn.get("Id", "")
            )

    return data


def main():
    src_path = Path(__file__).parent.parent / "src" / "pgns.json"

    print(f"Loading: {src_path}")
    with open(src_path) as f:
        data = json.load(f)

    print(f"Adding categories to {len(data.get('PGNs', []))} PGNs...")
    data = add_categories(data)

    # Count categories
    categories = {}
    for pgn in data.get("PGNs", []):
        cat = pgn.get("Category", "Unknown")
        categories[cat] = categories.get(cat, 0) + 1

    print("\nCategory distribution:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

    # Save back
    with open(src_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nSaved: {src_path}")


if __name__ == "__main__":
    main()

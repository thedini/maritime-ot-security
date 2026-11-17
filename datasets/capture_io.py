"""
capture_io.py - Shared parser for the course capture files.

Labs 10-13 call parse_message(line). Copy this file next to your lab scripts.
Accepts the synthetic dataset format ("<ts> <ID hex> [n] <bytes>") and the
`candump -ta` format ("(<ts>) can0  <ID>   [n]  <bytes>").
"""
import re

_LINE = re.compile(
    r"\(?(?P<ts>\d+\.\d+)\)?\s+(?:\S+\s+)?(?P<id>[0-9A-Fa-f]{8})\s+\[(?P<n>\d+)\]\s*(?P<data>(?:[0-9A-Fa-f]{2}\s*)*)")

def parse_message(line):
    """Return {'timestamp','can_id','data','pgn','source_addr'} or None."""
    m = _LINE.search(line)
    if not m:
        return None
    can_id = int(m.group("id"), 16)
    data = [int(x, 16) for x in m.group("data").split()]
    return {
        "timestamp": float(m.group("ts")),
        "can_id": can_id,
        "data": data[:int(m.group("n"))],
        "pgn": (can_id >> 8) & 0x3FFFF,
        "source_addr": can_id & 0xFF,
    }

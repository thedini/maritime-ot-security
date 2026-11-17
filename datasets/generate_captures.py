#!/usr/bin/env python3
"""
generate_captures.py - Synthetic NMEA 2000 captures for the course labs.

All data are SYNTHETIC. They are generated from a fixed seed so every student
and instructor gets identical files. They illustrate the labs' detectors; they
are not recordings of a vessel and must not be used to report detector
performance. One frame per line: timestamp, 29-bit ID (hex), length, data bytes
(the layout the lab parsers read):

    1700000000.123456 09F10D23 [8] FF 7F FB FF FF 7F FF FF

Usage:  python3 generate_captures.py [output_dir] [--aliases]
(--aliases also writes copies under the file names some labs use; see README.md)
Ground truth for each attack file is written to <name>.labels.json.
"""
import json, math, os, random, sys

SEED = 20260117
T0 = 1700000000.0

def can_id(pgn, sa, prio=2):
    return (prio << 26) | (pgn << 8) | sa

def u16(x):
    x = max(0, min(0xFFFF, int(round(x))))
    return [x & 0xFF, x >> 8]

# (name, pgn, source address, rate Hz, priority)
DEVICES = [
    ("wind",    130306, 0x23, 10, 2),
    ("heading", 127250, 0x13, 10, 2),
    ("speed",   128259, 0x1D, 1,  2),
    ("depth",   128267, 0x2C, 1,  3),
    ("pos",     129025, 0x1F, 4,  2),
    ("cogsog",  129026, 0x1F, 4,  2),
    ("engine",  127488, 0x17, 10, 2),
]

def payload(name, t, rng, sid):
    if name == "wind":
        spd = 6.0 + 1.5 * math.sin(t / 40) + rng.gauss(0, 0.15)
        ang = (0.6 + 0.2 * math.sin(t / 55) + rng.gauss(0, 0.01)) % (2 * math.pi)
        return [sid] + u16(spd * 100) + u16(ang * 10000) + [2, 0xFF, 0xFF]
    if name == "heading":
        h = (2.2 + 0.05 * math.sin(t / 90) + rng.gauss(0, 0.002)) % (2 * math.pi)
        return [sid] + u16(h * 10000) + [0xFF, 0x7F, 0xFF, 0x7F, 0xFC]
    if name == "speed":
        return [sid] + u16(300 + rng.gauss(0, 3)) + [0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    if name == "depth":
        d = 1500 + 40 * math.sin(t / 120) + rng.gauss(0, 2)
        return [sid] + u16(d) + u16(0) + [0xFF, 0xFF, 0xFF]
    if name == "pos":
        return [int((41.4892 + 1e-5 * t) * 1e7) >> s & 0xFF for s in (0, 8, 16, 24)] + \
               [int((-71.4218 + 1e-5 * t) * 1e7) >> s & 0xFF for s in (0, 8, 16, 24)]
    if name == "cogsog":
        return [sid, 0] + u16(2.2 * 10000) + u16(300 + rng.gauss(0, 3)) + [0xFF, 0xFF]
    if name == "engine":
        return [0, ] + u16(2400 * 4 + rng.gauss(0, 8)) + [0xFF, 0x7F, 0xFF, 0xFF, 0xFF]
    return [0] * 8

def normal(duration, rng, start=0.0):
    """Periodic traffic with small timing jitter; returns list of (t, id, data, device)."""
    out = []
    for name, pgn, sa, hz, prio in DEVICES:
        period = 1.0 / hz
        k = 0
        t = start + rng.uniform(0, period)
        while t < start + duration:
            out.append((t, can_id(pgn, sa, prio), payload(name, t, rng, k & 0xFF), name))
            k += 1
            t += period + rng.gauss(0, period * 0.01)
    return out

def fmt(t, cid, data):
    return "%.6f %08X [%d] %s" % (T0 + t, cid, len(data),
                                 " ".join("%02X" % b for b in data))

def write(path, frames):
    frames = sorted(frames, key=lambda f: f[0])
    with open(path, "w") as f:
        f.write("\n".join(fmt(t, cid, d) for t, cid, d, *_ in frames) + "\n")

def labels(path, kind, a, b, note):
    with open(path, "w") as f:
        json.dump({"synthetic": True, "seed": SEED, "attack": kind,
                   "attack_start_s": a, "attack_end_s": b, "note": note}, f, indent=2)

def main(out):
    os.makedirs(out, exist_ok=True)
    # normal (5 min) and extended baseline (15 min); different seeds
    write(f"{out}/normal_capture.txt", normal(300, random.Random(SEED)))
    write(f"{out}/extended_capture.txt", normal(900, random.Random(SEED + 1)))

    DUR, A, B = 120, 40, 70   # 30 s attack window

    # 1. DoS: flood of highest-priority frames
    rng = random.Random(SEED + 2)
    fr = normal(DUR, rng)
    t = A
    while t < B:
        fr.append((t, can_id(0x00000, 0x00, 0), [0] * 8, "flood"))
        t += 1 / 500.0
    write(f"{out}/dos_attack_capture.txt", fr)
    labels(f"{out}/dos_attack_capture.labels.json", "dos_flood", A, B, "500 frames/s, id 0x00000000")

    # 2. Naive spoofing: extra wind frames with wrong values, in addition to the real device
    rng = random.Random(SEED + 3)
    fr = normal(DUR, rng)
    t = A
    k = 0
    while t < B:
        fr.append((t, can_id(130306, 0x23, 2),
                   [k & 0xFF] + u16(25 * 100) + u16(1.0 * 10000) + [2, 0xFF, 0xFF], "spoof"))
        k += 1
        t += 0.05                      # 20 Hz on top of the real 10 Hz
    write(f"{out}/spoofing_capture.txt", fr)
    labels(f"{out}/spoofing_capture.labels.json", "naive_spoof", A, B,
           "false wind speed 25 m/s at 20 Hz in addition to the real sensor (rate doubles+)")

    # 3. Smart spoofing: victim silenced, attacker keeps the same ID and 10 Hz cadence
    rng = random.Random(SEED + 4)
    fr = [f for f in normal(DUR, rng) if not (f[3] == "wind" and A <= f[0] < B)]
    t = A
    k = 0
    while t < B:
        fr.append((t, can_id(130306, 0x23, 2),
                   [k & 0xFF] + u16(25 * 100) + u16(1.0 * 10000) + [2, 0xFF, 0xFF], "spoof"))
        k += 1
        t += 0.1 + rng.gauss(0, 0.001)
    write(f"{out}/smart_spoofing_capture.txt", fr)
    labels(f"{out}/smart_spoofing_capture.labels.json", "smart_spoof", A, B,
           "victim wind frames removed; false values sent at the same ID and rate. "
           "Frequency-based detectors cannot see this; content or source checks can.")

    # 4. Replay: frames from earlier in the capture retransmitted
    rng = random.Random(SEED + 5)
    fr = normal(DUR, rng)
    old = [f for f in fr if f[3] == "heading" and 5 <= f[0] < 35]
    for t, cid, d, _ in old:
        fr.append((t + 35, cid, list(d), "replay"))
    fr = [f for f in fr if not (f[3] == "heading" and A <= f[0] < B)]   # real heading suppressed
    write(f"{out}/replay_capture.txt", fr)
    labels(f"{out}/replay_capture.labels.json", "replay", A, B,
           "heading frames from t=5..35 s retransmitted at t=40..70 s; real heading suppressed")

    if "--aliases" not in sys.argv:
        return
    # optional copies using the file names individual labs expect
    for dst, src in [("lab05_capture.txt", "normal_capture.txt"),
                     ("normal.txt", "normal_capture.txt"),
                     ("attack.txt", "spoofing_capture.txt"),
                     ("attack_capture.txt", "dos_attack_capture.txt"),
                     ("capture.txt", "normal_capture.txt"),
                     ("capture_lab01.txt", "normal_capture.txt")]:
        with open(f"{out}/{src}") as s, open(f"{out}/{dst}", "w") as d:
            d.write(s.read())

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0] if args else os.path.dirname(os.path.abspath(__file__)))

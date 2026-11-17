# Course datasets (synthetic)

These captures are **synthetic**. `generate_captures.py` writes them from a fixed
seed, so every student and instructor gets identical files. They are meant to
exercise the labs' detectors. They are not recordings of a vessel, and any
detection result computed from them describes these files only.

```bash
python3 generate_captures.py            # writes the files below next to the script
python3 generate_captures.py ./out --aliases   # also writes the file names some labs use
```

| File | Content | Used by |
|------|---------|---------|
| `normal_capture.txt` | 5 min of benign periodic traffic (7 streams, 40 frames/s) | labs 5, 9–13 |
| `extended_capture.txt` | 15 min benign baseline | lab 9 |
| `dos_attack_capture.txt` | benign + 30 s flood of ID `0x00000000` at 500/s (t=40–70 s) | labs 8, 9, 13 |
| `spoofing_capture.txt` | benign + false wind values at 20 Hz on top of the real sensor | labs 9, 13 |
| `smart_spoofing_capture.txt` | real wind sensor silenced; false values at the **same ID and rate** | labs 9, 13 |
| `replay_capture.txt` | earlier heading frames replayed while the real heading is suppressed | labs 9, 13 |
| `*.labels.json` | attack type and start/end second for each attack file | lab 13 |

Some labs use other names (`lab05_capture.txt`, `normal.txt`, `attack.txt`,
`capture.txt`, `capture_lab01.txt`, `attack_capture.txt`). Run with `--aliases` or
copy the file named in the table.

Format, one frame per line: `timestamp ID [length] data bytes`
(for example `1700000000.008031 09F8021F [8] 00 00 F0 55 28 01 FF FF`).
`capture_io.py` provides `parse_message(line)`, which the labs call; it also reads
`candump -ta` lines.

## What the files teach
A rate-based detector (Lab 9) built from `normal_capture.txt` flags the DoS flood
(unknown source) and the naive spoof (rate doubles). It does **not** flag the
smart spoof or the replay, which keep the expected IDs and rates. Those need
content, source or physical-layer checks (labs 10–12). Expect a small
false-alert rate on the benign file itself.

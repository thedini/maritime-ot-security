# Readiness for sharing (CLARK.center) — status 2026-11-17

Prepared on branch `prep/clark-center-readiness`. Nothing has been pushed or submitted.
CLARK.center's submission requirements could not be read (the site renders without
static content); check them before submitting.

## Done in this branch
- `datasets/`: deterministic synthetic captures (normal, extended, DoS, naive spoof,
  smart spoof, replay) with ground-truth labels, a generator, and `capture_io.py`
  (`parse_message`, called by labs 10-13 but previously undefined).
  Verified: lab 5 enumeration and lab 9 detector run on them; naive spoof and DoS
  are flagged, smart spoof and replay are not (intended teaching point).
- Lab 9: detector alerts on an unseen (PGN, source) so a flood from a new ID is detected; prints the first 20 alerts.
- Lab 11: chronological train/test split instead of random shuffling.
- Lab 13: evaluation reports false alerts per hour, detection and delay per labeled
  attack window; no message-level F1 with "all attack alerts are true positives".
- Class 12 / lab 12: removed "unique", "can't spoof physics", "consistent over time";
  added what a fingerprinting result does and does not show.
- Class 13: ensemble benefits stated as claims to measure.
- Syllabus: three threat models, updated objectives 5, 8, 9; resource links filled.
- Removed placeholder download URLs, `[Link to be provided]`, `[Platform TBD]`; removed 7 broken image embeds.

## Still open (needs author)
1. **Licence file.** README says CC BY-SA 4.0 but the repo has no `LICENSE`. Add the canonical text.
2. **Figures.** The 6 removed diagrams (maritime trade, defense in depth, OpenBridge hardware, CAN physical, CAN arbitration, bus-off) were never created; add and re-embed if wanted.
3. **Quizzes** exist only for classes 1-2; **no answer keys** for quizzes, midterm, or lab solutions.
4. **Attack scripts** `dos_attack.py`, `replay_attack.py`, `dos_detector.py` are referenced but not provided.
5. **Hardware path.** The course uses a Teensy/OpenBridge build; the research platform is NEMO. Decide whether the course targets one or both and say so.
6. **Instructor bio / contact** and any institution-specific text.
7. **IRB** (#67) before collecting any student data or outcome claims. The course makes no learning-outcome claims.
8. Labs 10, 11 and 12 were not executed end to end; only code syntax (185 of 186 blocks parse; the one failure is a shell command in lab 8) and labs 5, 9, 13 evaluation logic were checked.
9. Offensive content (weeks 5-8): the isolation and ethics warnings are good; check CLARK's content policy for offensive-security material.

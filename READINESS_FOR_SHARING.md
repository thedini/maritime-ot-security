# Readiness for sharing (CLARK.center) — status 2026-11-17

Branch `prep/clark-center-readiness`. Nothing has been pushed or submitted.
CLARK.center's submission requirements could not be read (the site serves no static
content); check them before submitting.

## Done
- **Licence:** `LICENSE` holds the official CC BY-SA 4.0 text (README declares the same).
- **Platform:** course moved to NEMO 1.0.0 / 1.0.1 (designed by James Campbell). Class 3, lab 4,
  lab 5 capture (separate listen-only interface), README, syllabus, bill of materials,
  technology requirements, instructor guide Week 4. Only 1.0.0 is identifiable in the
  `thedini/NEMO` repo (PCB silkscreen, firmware); what 1.0.1 changes is not documented here.
- **Data:** `datasets/` deterministic synthetic captures with labels, generator, and
  `capture_io.py` (`parse_message`). Verified with lab 5 enumeration and lab 9 detector.
- **Evaluation fixes:** lab 9 (unknown-source alert), lab 11 and class 11 (chronological split),
  lab 13 (false alerts per hour and detection delay, no F1-with-all-alerts-as-TP).
- **Honesty fixes:** class/lab 12 and class 13/14 overclaims removed; ensemble benefit stated as a claim to measure.
- **Threat models:** syllabus table (TM1-TM3) and quiz questions use the framing.
- **Figures:** `images/make_figures.py` draws CAN physical layer, CAN arbitration, defense in depth (embedded in classes 0 and 1).
- **Assessments:** quizzes for classes 3-7 and 9-14 (class 1-2 existed), plus `class_08_midterm_key.md`.
  Not proofread end to end by the author; they were checked for placeholders and spot-checked.
- **Errors fixed:** class 2 / quiz 2 / lab 3 PGN decode (0x09F80205 is PGN 129026), class 10 entropy example
  (1.46 bits), class 14 `alert_history` bug, placeholders in class 8/14, lab 14, syllabus.

## Open (needs author)
1. **Labs 6-8 and parts of classes 5, 7, 8** still use the old OpenBridge serial interface and scripts
   (`ttyACM`, `dos_attack.py`, `replay_attack.py`). They need rewriting for NEMO's own demos or replacing with
   analysis exercises on the provided captures. Not done here.
2. **Class text errors:** classes 6 and 7 fixed (oil pressure units, error-counter thresholds, frame size and
   flood rate, priority-0 label, 0x00F80124 vs 0x01F80124, hybrid example reworked as a conceptual discussion).
   Still open: class 4 (address table; verify against the standard), class 9 (wind PGN rate, "OpenPlotter
   baseline"), class 8 (10 Hz vs 4 Hz in the captures, PGN snippet keeps the destination byte for PDU1 frames,
   engine pressure range).
3. **Class 13 weights:** the largest single weight is 0.30 against a 0.5 alert threshold, so no single detector can alert alone; decide if that is intended.
4. **Midterm:** class 8 prints no multiple-choice bank (the key supplies a recommended one); syllabus calls the midterm "practical" while class 8 is written plus practical.
5. **Figures not made:** maritime trade routes, NEMO hardware photo, bus-off diagram.
6. **Lab solutions** (instructor keys for labs 1-14).
7. **Instructor bio, contact, institutional text** are generic; IRB (#67) never run per the author.
8. **Content policy:** check CLARK's policy on offensive-security content for weeks 5-8.
9. **End-to-end test** to be run by the author once ready; labs 10-12 were not executed here.

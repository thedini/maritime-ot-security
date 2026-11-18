---
title: "Midterm Examination - Instructor Answer Key and Grading Guide"
subtitle: "Class 08: Midterm Review and Practical Assessment"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "midterm key"
time_limit: "90 minutes"
points: 100
passing_score: 70
---

# Midterm Answer Key and Grading Guide (Instructor Use Only)

## 1. Scoring Overview

Scoring follows the instructor notes in `class/class_08_midterm/class_08.md`. Time is 90 minutes. Passing is 70/100.

| Section | Component | Points |
|---------|-----------|--------|
| Written (45 min) | Multiple choice, 10 questions x 2 pts | 20 |
| Written | Short answer, 4 questions x 5 pts | 20 |
| Written | Analysis, 1 question x 10 pts | 10 |
| Practical (45 min) | Part 1: Network analysis | 15 |
| Practical | Part 2: Attack evidence and analysis (adapted, see Section 4) | 20 |
| Practical | Part 3: Detection implementation | 15 |
| **Total** | | **100** |

Materials allowed: one double-sided handwritten note page, calculator, PGN reference sheet.

### 1.1 Decisions made where the class file does not fully specify the exam

The class file lists the written point scheme but does not print the 10 multiple-choice questions. It also lists "Sample Exam Questions" 1-7 whose own rubric totals 50 points (15 + 15 + 20) and which overlap the practical section. This key therefore uses the following mapping. Instructors who prefer a different mapping can swap items, because every sample question is keyed below.

| Exam item | Source | Points |
|-----------|--------|--------|
| Multiple choice 1-10 | Recommended bank in Section 2.1 (written for this key from the class file's review tables) | 2 each |
| Short answer 11-14 | Sample theory questions 1-4 | 5 each |
| Analysis 15 | Sample question 5 (CAN frame decode), scaled from 15 to 10 points | 10 |
| Practical Part 3 | Includes the detection logic of sample question 6 | see Section 5 |
| Sample question 7 | Optional discussion or practice item, not scored in the 100 points | see Section 3.2 |

## 2. Written Section (50 points)

### 2.1 Multiple Choice (20 points, 2 points each)

Correct positions are varied. Award 2 points for the correct letter and 0 otherwise.

1. Which frame wins CAN arbitration when two nodes start transmitting at the same time?
   a) The one with the longer data field b) The one that started first c) The one with the lower identifier d) The one with the higher identifier
   **Answer: c.** Lower ID wins bus access, and the loser backs off without corrupting the winner. This is the arbitration row in the class review table.

2. Which PGN carries Position, Rapid Update (latitude and longitude)?
   a) 129025 b) 127250 c) 130306 d) 127488
   **Answer: a.** 129025 is position rapid. 127250 is heading, 130306 is wind and 127488 is engine rapid.

3. For PDU Format 248 (0xF8), what does the PDU Specific byte represent?
   a) A destination address b) The priority c) The source address d) A group extension that is part of the PGN
   **Answer: d.** PF of 240 or more is PDU2 (broadcast), so PS is added to the PGN. PS is a destination address only for PF below 240.

4. Which bits of the 29-bit NMEA 2000 CAN ID hold the priority?
   a) Bits 7-0 b) Bits 28-26 c) Bits 23-16 d) Bits 15-8
   **Answer: b.** Bits 28-26 hold priority (0-7, lower is higher priority). Bits 7-0 are the source address.

5. A vessel is at 41.5 degrees north. What raw value does PGN 129025 hold for this latitude (resolution 1e-7 degrees)?
   a) 4,150,000 b) 41,500,000 c) 415,000,000 d) 4,150,000,000
   **Answer: c.** raw = 41.5 / 1e-7 = 415,000,000. Option d does not fit in a signed 32-bit field.

6. Which expression gives the raw heading value for a heading of 1.0000 radians in PGN 127250?
   a) 10,000 b) 100 c) 1,000 d) 57,296
   **Answer: a.** The class gives raw = radians x 10,000, so 1.0000 rad is 10,000.

7. Which statement is true of passive reconnaissance?
   a) It sends ISO Requests b) It is easily noticed by bus monitors c) It gathers more detail than active reconnaissance d) It generates no traffic and carries no detection risk on the bus
   **Answer: d.** The class table lists traffic generated as none and detection risk as none, with more limited information than active methods.

8. Which property of CAN and NMEA 2000 most directly allows a node to send messages that claim another device's identifier?
   a) Bit stuffing b) No authentication c) The 250 kbps bitrate d) Differential signaling
   **Answer: b.** The class table says any node can send any ID. Note the question concerns a property of the protocol, not a statement that every such attempt succeeds or goes unnoticed.

9. A genuine, enrolled heading sensor keeps its own source address, normal message rate and format, but reports a false heading. Which threat model describes this?
   a) TM1: modified traffic b) TM2: substituted transmitter c) TM3: genuine device sending false values d) None of the three
   **Answer: c.** In TM3 the legitimate device itself reports the false value. Rate, ID and source checks have nothing abnormal to see.

10. Which mechanism in CAN error handling is associated with bus-off behavior?
    a) Priority bits b) Data page c) Fast Packet sequence counter d) TEC and REC error counters
    **Answer: d.** The class review table pairs error handling (TEC/REC counters) with bus-off attacks.

Position tally for Q1-10: c, a, d, b, c, a, d, b, c, d.

### 2.2 Short Answer (20 points, 5 points each)

**Question 11 (Sample theory Q1): Explain why CAN bus arbitration creates a security vulnerability.**

Correct answer: arbitration is decided bit by bit on the identifier, so the lowest identifier wins. Because priority is encoded in the most significant bits and the bus has no authentication, any node, including an unauthorized one, can present a very high priority identifier and win arbitration against legitimate traffic. The consequence is an availability problem: legitimate lower-priority messages are delayed or starved. The same weakness is why defenders watch priority values and message rates.

Full-credit answer must contain:
- Lower ID wins arbitration (1 pt)
- Priority sits in the high bits of the ID and nothing checks who may use a given priority (2 pts)
- Consequence: legitimate traffic delayed or starved, so availability is affected (1 pt)
- Link to detection (priority monitor, rate spike, or unknown source) or to the absence of authentication (1 pt)

Partial credit: 3 pts if the student states lower ID wins and gives the consequence but not the missing authentication; 2 pts for describing arbitration only; 0 for answers that describe encryption or confidentiality.

**Question 12 (Sample theory Q2): A chart plotter shows 41.5000 N, 71.3500 W. A position one nautical mile north is wanted. Calculate the new latitude and the raw value for PGN 129025.**

Correct answer: one nautical mile is one minute of latitude, which is 1/60 degree = 0.016667 degrees. New latitude = 41.5000 + 0.016667 = 41.516667 N (accept 41.5167). Raw latitude = 41.516667 / 1e-7 = 415,166,667 (the unchanged 41.5 gives 415,000,000, so the step is about 166,667 counts). Longitude is unchanged: -71.35 gives -713,500,000 as a signed 32-bit value.

Full-credit answer must contain:
- Correct nautical mile to degrees conversion: 1 nm = 1/60 degree of latitude = 1,852 m (2 pts)
- New latitude 41.5167 N (1 pt)
- Raw value of about 415,166,667, correct sign and scale (2 pts)

Partial credit: 3 pts if the conversion is right but the raw scaling is wrong or the raw longitude is given with the wrong sign; 2 pts if the student used 1 degree = 60 nm in the wrong direction but scaled correctly. Defensive link worth noting when debriefing: a jump of this size is about ten times the 0.1 nm threshold used in Practical Part 3.

**Question 13 (Sample theory Q3): Compare passive and active reconnaissance.**

Correct answer (from the class comparison table):
- Passive: sends no traffic, has no detection risk on the bus, gathers more limited information; example is monitoring traffic (source addresses, PGNs seen, message rates).
- Active: sends requests such as an ISO Request to elicit details (for example product information), gathers more detailed information, and the extra traffic can be noticed by monitoring or by rate and source checks.

Full-credit answer must contain: passive vs active definitions (1 pt); what each reveals (2 pts); the risk difference (2 pts).

Partial credit: 3 pts if the table rows are reproduced without examples; 2 pts if only one mode is explained well. Do not give credit for the claim that passive collection is "undetectable and harmless to the owner"; the credit is for stating that it generates no bus traffic.

**Question 14 (Sample theory Q4): Describe a scenario where engine parameter spoofing could cause physical damage.**

Correct answer: the class lists alarm suppression, false alarm and damage induction. A full-credit scenario: false normal values for oil pressure or coolant temperature (PGN 127489) hide a real fault from the operator and from alarms, so the engine continues to run in a damaging condition. A second acceptable scenario: false alarm values trigger an unnecessary shutdown and cause loss of propulsion at a dangerous moment.

Full-credit answer must contain:
- A concrete parameter or PGN linked to the engine (1 pt)
- The mechanism (suppressed alarm, or false alarm) (2 pts)
- The physical consequence (damage, overheating, loss of propulsion) (1 pt)
- A defensive observation such as a plausibility check, cross-check with another sensor, or detection by an ensemble (1 pt)

Do not award credit for procedural attack detail, and do not require it. A student who notes that if the false values come from the genuine engine device this is TM3, and rate and source checks would not help, should receive full credit even if the mitigation point is brief.

### 2.3 Analysis (10 points)

**Question 15 (Sample practical Q5, scaled from 15 to 10 points): Decode the CAN frame.**

```
CAN ID: 09F80124
Data:   F0 7E D7 18 47 A4 BB D5
```

a) PGN b) Source address c) Message type d) Payload values

Worked answer:
- Binary of the ID: 0000 1001 1111 1000 0000 0001 0010 0100
- Priority (bits 28-26) = 010 = 2
- Reserved (bit 25) = 0; Data Page (bit 24) = 1
- PF (bits 23-16) = 0xF8 = 248, so this is PDU2 (broadcast); PS (bits 15-8) = 0x01
- SA (bits 7-0) = 0x24 = 36
- PGN = Data Page x 0x10000 + PF x 0x100 + PS = 0x10000 + 0xF800 + 0x01 = 0x1F801 = **129025**
- Message type: Position, Rapid Update, broadcast, priority 2, from device 36
- Payload (PGN 129025: latitude int32 then longitude int32, 1e-7 degrees, little-endian):
  - Latitude bytes F0 7E D7 18 give 0x18D77EF0 = 416,775,920, which is 41.6775920 N
  - Longitude bytes 47 A4 BB D5 give 0xD5BBA447 as a signed value = -709,123,001, which is 70.9123001 W

Scoring (the class rubric of 3/3/3/6 scaled to 10: 2/2/2/4):
- PGN 129025: 2 pts. Give 1 pt for 63489 (0xF801), the common error of ignoring the Data Page bit, with the method otherwise correct.
- SA 36: 2 pts (1 pt for 0x24 without decimal conversion).
- Message type (Position Rapid, PDU2 broadcast): 2 pts (1 pt for identifying only "position" or only "broadcast").
- Payload decode: 4 pts: 1 for little-endian byte order, 1 for signed interpretation of longitude (west is negative), 1 for the 1e-7 scale, 1 for final values within 0.0001 degree. Accept 41.678 N, 70.912 W.

Common error table: reading bytes big-endian gives nonsensical coordinates; unsigned interpretation of the longitude gives about 358.58 degrees; the class snippet `(can_id >> 8) & 0x3FFFF` returns the right PGN for this PDU2 frame but would include the destination byte for PDU1 frames, so do not mark a student wrong for noticing that.

## 3. Optional Sample Items

### 3.1 Sample question 6: Write Python to detect a DoS attack based on message rate (15 pts in the class rubric)

This is covered in practical Part 3 (Section 5). If instructors score it as a written item instead, use the class rubric: rate calculation 5, threshold logic 5, alert mechanism 5.

Reference solution outline (analysis only): keep a sliding window of timestamps per CAN ID; compute messages per second; compare to a baseline built from benign traffic (for example mean plus 3 standard deviations, as the course IDS configuration does); also flag IDs never seen in the baseline and priority 0 identifiers; emit an alert with ID, observed rate and baseline.

### 3.2 Sample question 7: replay scenario (20 pts in the class rubric, not scored here)

As worded in the class file, question 7 asks students to design an attack. This key does not provide an attack design, and instructors should not require one. If the item is used for discussion or as an ungraded practice, convert it to a defensive analysis using the same four 5-point categories:

| Category | Defensive full-credit content |
|----------|-------------------------------|
| PGN selection (5) | Names the PGNs that would have to agree for a vessel to look stationary: position 129025, COG/SOG 129026, heading 127250 (and speed). Notes that they must be consistent with each other. |
| Source of the data (5) | Explains that the material would be legitimate earlier traffic, so IDs, formats and values look valid, and that nothing in the protocol authenticates it. |
| Timing (5) | Explains that matching normal message rates makes a rate-based detector blind to it (the course's `replay_capture.txt` keeps expected IDs and rates). |
| Detection (5) | Names at least two checks: repeated identical sequences or content, inconsistency with other sensors, entropy or sequence models (LSTM), source and physical-layer evidence if a different transmitter was used (TM2). Does not claim any single check is certain. |

## 4. Practical Section: Hardware Adaptation Statement

The class file's Practical Part 2 says "Using OpenBridge" to construct, inject and verify a spoofed position message. The course no longer uses a serial-attached OpenBridge board. It uses NEMO (Teensy 4.0 board by James Campbell; versions 1.0.0 and 1.0.1), which provides a sensor simulator, a live-data view and two built-in demonstrations (a denial-of-service load and impersonation of a sensor's data) on an isolated test network. NEMO has no serial capture mode, so recording uses the separate listen-only capture interface (SocketCAN with `can-utils`), and analysis uses the synthetic captures in `datasets/`.

I adapted the grading as follows, and the class file was not edited:
- Part 1 uses a synthetic capture file in place of an unspecified "capture file".
- Part 2 is reframed from "construct and inject" to "calculate, observe and verify the evidence of an impersonation or flood". Students are graded on encoding calculations and on correctly reading the evidence, not on building or transmitting frames. Any transmission is limited to NEMO's built-in demonstrations on the isolated test network under instructor supervision; capture-only students can earn full credit.
- Part 3 uses the synthetic captures and small student-made test inputs.

The datasets are synthetic (README states so). Results describe those files only and are not performance claims about a vessel. Grade on observable outcomes, not on menu paths, because NEMO 1.0.0 and 1.0.1 may differ; students should state the version they used.

## 5. Practical Section (50 points)

### Part 1: Network Analysis (15 points, 15 minutes)

Tasks: enumerate devices by source address, identify critical navigation devices, and build a frequency profile for the position PGN.

Use `datasets/normal_capture.txt` (300 s, 12,002 frames, 40 frames per second). Expected result, verified from the file:

| Source address | Hex | PGN | Meaning | Rate | CAN ID |
|---|---|---|---|---|---|
| 19 | 0x13 | 127250 | Vessel heading | 10 Hz | 09F11213 |
| 23 | 0x17 | 127488 | Engine rapid | 10 Hz | 09F20017 |
| 29 | 0x1D | 128259 | Speed | 1 Hz | 09F5031D |
| 31 | 0x1F | 129025 | Position rapid | 4 Hz | 09F8011F |
| 31 | 0x1F | 129026 | COG/SOG rapid | 4 Hz | 09F8021F |
| 35 | 0x23 | 130306 | Wind data | 10 Hz | 09FD0223 |
| 44 | 0x2C | 128267 | Water depth | 1 Hz | 0DF50B2C (priority 3) |

That is 6 source addresses and 7 message streams. SA 31 sends two PGNs. All frames use priority 2 except depth (priority 3).

Expected outcome and observable check:
- Device list shows exactly 6 source addresses with the PGNs above. A student's table can be compared with this one in under a minute.
- Critical navigation devices: SA 31 (position and COG/SOG), SA 19 (heading). Accept SA 29 (speed) and SA 44 (depth) as navigation-related; wind (SA 35) and engine (SA 23) are acceptable as "critical" only with a reason.
- Position profile: PGN 129025 from SA 31 about 4.0 Hz (1,200 frames in 300 s, interval about 250 ms with small jitter). Note: the lecture text says position and heading are 10 Hz. The synthetic file has position at 4 Hz, so mark the student against the file. A student who writes 10 Hz without computing from the capture earns no more than 2 of the 6 profile points.

Scoring (15):
- Device enumeration: 5 pts (all 6 SAs with correct PGNs 5; 5 SAs 4; 4 SAs 3; otherwise 1 per correct SA to a maximum of 2)
- Critical navigation identification with a reason: 4 pts (2 for devices, 2 for reasoning)
- Frequency profile of 129025: 6 pts (3 for rate computed from timestamps, 2 for interval or variation statistic, 1 for stating units and window used)

Partial credit: if a student's code fails to run but the table is correct from a manual or alternative method, award the table points and deduct 1 point from the profile row for the missing tooling evidence.

### Part 2: Attack Evidence and Analysis (20 points, 15 minutes, adapted)

Original task: construct a spoofed position message, calculate values, inject at the correct rate, verify on a test display.

Adapted task: (a) show the encoding calculations that a position or wind message uses; (b) from a labeled capture, determine what rate a legitimate stream should have and how the false stream differs; (c) verify the observation on NEMO's live-data view or in the capture; (d) state the threat model.

Expected outcomes:
- (a) Encoding: for 41.5 N, 71.4 W, raw latitude 415,000,000 and raw longitude -714,000,000 (class instructor note). Heading raw = radians x 10,000. Students decode a frame from the capture and show raw to engineering value (for example heading 0x7C 0x22 style little-endian conversion).
- (b) Using `spoofing_capture.txt` (labels: attack 40-70 s): PGN 130306 from SA 35 normally arrives at 10 Hz; in the window it arrives at about 30 Hz (the real 10 Hz plus about 20 Hz of false wind values at 25 m/s). Over the whole 120 s file the average rate is about 15 Hz, so an unwindowed average hides the attack; a windowed rate shows it.
- (c) Observable check: NEMO live-data view shows the device and its parsed PGN values; the capture interface log (candump with timestamps) or `capture_io.parse_message` output shows the same IDs and rates. The student should point to the time interval 40-70 s in the capture, or, for a NEMO demonstration, the interval the instructor announces.
- (d) Threat model: naive injection is TM1 (modified traffic). A smart variant that silences the real sensor and sends false values at the same ID and rate (`smart_spoofing_capture.txt`) still looks like TM1 on the bus; if a different transmitter claims the sensor's address it is TM2, which needs physical-layer evidence. A genuine device reporting false values is TM3. A rate check cannot see the smart variant; students should say so and should not claim any check is certain.

Scoring (20):
- Calculations: 6 pts (2 raw latitude, 2 raw longitude with sign, 2 correct engineering decode of one captured frame)
- Rate analysis: 6 pts (3 baseline 10 Hz, 2 observed rate in window, 1 explanation of why the whole-file average understates it)
- Verification and observable check: 5 pts (3 evidence from live-data view or capture; 2 timestamps or window identified)
- Threat model and limitation: 3 pts (2 TM1 vs TM2 vs TM3 correctly distinguished, 1 states that rate-matched variants evade a rate check)

Partial-credit guidance:
- If NEMO hardware is unavailable at the station, the capture-based route earns full credit.
- If a student's NEMO version labels or menus differ, grade the observed values, not the path.
- Award 0 for any submission that presents procedure for transmitting spoofed frames outside the instructor-supervised NEMO demonstration; refer such a submission to the instructor.

### Part 3: Detection Implementation (15 points, 15 minutes)

Tasks: detect unusual message rates, alert on position jumps greater than 0.1 nm, track device availability.

Expected outcomes by task, using `datasets/`:

1. Rate detector (5 pts). Baseline per CAN ID from `normal_capture.txt`; evaluate one-second windows.
   - `dos_attack_capture.txt` (attack 40-70 s): ID 0x00000000 appears at about 500 frames/s with priority 0 and a source never seen in the baseline; alert should begin near t = 40 s and end near t = 70 s.
   - `spoofing_capture.txt`: PGN 130306 from SA 35 at about 30 Hz versus 10 Hz in 40-70 s should alert.
   - `smart_spoofing_capture.txt` and `replay_capture.txt` keep expected IDs and rates, so a pure rate detector is expected not to alert. Students who observe and state this limitation show the intended understanding; do not penalize the missing alerts.
   - Benign file: a small number of false alerts may occur; students should report the count, ideally per hour.
   Scoring: windowed rate calculation 2, baseline-based threshold 2, alert output with ID, rate and baseline 1.

2. Position jump detector (5 pts). Decode latitude and longitude (int32, 1e-7 degrees, little-endian), compute distance between successive fixes, and alert if greater than 0.1 nm. Expected: 0.1 nm = 185.2 m = about 0.001667 degrees of latitude; longitude distance must be scaled by the cosine of latitude (about 0.75 at 41.5 degrees). None of the provided captures contains a position jump (the position stream drifts about 1e-5 degree per second), so the expected result on all five files is zero jump alerts, and a correct detector must also be shown to fire on a small student-made test input with one step larger than 0.1 nm (for example two consecutive test fixes 0.2 nm apart) and not fire on a step smaller than 0.1 nm.
   Scoring: correct decode with sign 2, correct distance calculation with units 2, threshold behavior shown on the test input 1.

3. Availability tracker (5 pts). Track last-seen time per source address (or per stream) and flag a device silent for longer than a stated multiple of its expected period (for example several periods). Expected: no outages in any provided capture; to demonstrate the logic the student removes one device's frames for a stretch from a copy of a capture (or reasons through a short hand-made list of timestamps) and shows the alert. Students should note that the smart-spoof and replay files do not produce an availability alert because frames continue to arrive under the same ID.
   Scoring: last-seen logic 2, sensible timeout tied to expected rate 2, demonstration 1.

Partial credit for all of Part 3: working logic with a wrong threshold earns two-thirds of that row; correct reasoning documented in comments or pseudocode but no running code earns up to half of the row.

## 6. Grading Rubric Summary

| Section | Points | Percentage |
|---------|--------|------------|
| Written: Multiple Choice (10 x 2) | 20 | 20% |
| Written: Short Answer (4 x 5) | 20 | 20% |
| Written: Analysis (1 x 10) | 10 | 10% |
| Practical Part 1 | 15 | 15% |
| Practical Part 2 | 20 | 20% |
| Practical Part 3 | 15 | 15% |
| **Total** | **100** | **100%** |

Passing is 70/100. A student can reach 70 in several ways; there is no separate minimum per section in the class file.

### Grade Scale

| Score | Grade |
|-------|-------|
| 90-100 | A |
| 80-89 | B |
| 70-79 | C |
| 60-69 | D |
| 0-59 | F |

## 7. Common Mistakes to Watch For

- Ignoring the Data Page bit when computing the PGN (gives 63489 instead of 129025 for Question 15)
- Reading multi-byte fields big-endian or treating the longitude as unsigned
- Reporting the lecture's 10 Hz for position instead of measuring 4 Hz in the capture
- Averaging a rate over the whole file and missing a 30-second attack window
- Expecting a rate detector to catch the smart-spoof or replay captures
- Confusing TM2 (different transmitter) with TM3 (genuine device, false values)
- Distance calculation that ignores the cosine of latitude for longitude
- Claiming any detection method is certain or that an attack cannot succeed

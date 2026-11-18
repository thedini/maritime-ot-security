---
title: "Quiz 04"
subtitle: "Reconnaissance and Network Mapping"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 04: Reconnaissance and Network Mapping

## Instructions

- Time Limit: 30 minutes
- Total Points: 100 points
- Passing Score: 70%
- Open book: No
- Collaboration: Individual work only
- Show your work for calculations

## Part 1: Multiple Choice (40 points)

**Instructions**: Circle the best answer. Each question is worth 4 points.

### Question 1

Which description fits passive reconnaissance on a CAN bus?

a) Sending requests to elicit responses from devices

b) Flooding the bus to see which devices fail

c) Physically replacing a device to study it

d) Observing traffic without transmitting any messages

---

### Question 2

Which PGN carries a device's Product Information (model, software version, serial number)?

a) 60928

b) 59904

c) 126996

d) 127250

---

### Question 3

From passive observation alone, how can an observer count the devices on a network?

a) By the number of unique source addresses seen

b) By the bus bitrate

c) By the number of termination resistors

d) By decrypting the payloads

---

### Question 4

Why is the software version in Product Information security-relevant, according to the class?

a) It sets the bus bitrate

b) It supports vulnerability research for that specific version

c) It encrypts the device serial number

d) It identifies the vessel owner

---

### Question 5

Using the class frequency table, which PGN is expected at roughly 1 Hz?

a) 127250 (heading)

b) 129025 (position)

c) Both 127250 and 129025

d) 130306 (wind)

---

### Question 6

The class instructor notes suggest raising an alert when a PGN's message rate deviates by more than what?

a) 1 sigma

b) 3 sigma

c) 10 sigma

d) Any change at all, however small

---

### Question 7

In the class table of critical maritime systems, which PGN is listed with the attack impact 'Grounding risk'?

a) 127488 (engine)

b) 129038 (AIS)

c) 128267 (depth)

d) 126983 (alarms)

---

### Question 8

A genuine, authorized depth sounder develops a fault and reports wrong depths at its normal rate from its normal source address. Which threat model does this describe, and what do an allowlist of source addresses and a frequency baseline tell you?

a) TM1 (modified traffic); both flag it immediately

b) TM2 (substituted transmitter); both flag it immediately

c) TM2 (substituted transmitter); neither is expected to flag it

d) TM3 (genuine device sending false values); neither is expected to flag it, so value-level checks are needed

---

### Question 9

Which defensive measure from the class addresses newly appearing devices on the network?

a) Allowlisting: alert on unknown source addresses

b) Lowering the bus bitrate

c) Removing both termination resistors

d) Disabling Address Claim

---

### Question 10

Which active reconnaissance activity might a monitoring system notice, according to the instructor notes?

a) Reading candump output on a capture interface

b) Passive frequency profiling

c) Reading the vessel's wiring diagram

d) ISO Requests from unknown sources, scanning patterns, or unusual request frequency

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 5 points.

### Question 11

**T / F**: Passive reconnaissance requires the observer to transmit messages on the bus.

---

### Question 12

**T / F**: PGN 126996 is a Fast Packet message, so a receiver must reassemble multiple CAN frames to read it.

---

### Question 13

**T / F**: A frequency baseline is useful only to attackers; defenders gain nothing from it.

---

### Question 14

**T / F**: Active reconnaissance generates traffic that a monitoring system could, in principle, notice.

---

### Question 15

**T / F**: The class describes real vessel networks as typically having roughly 5 to 20 devices.

---

### Question 16

**T / F**: The class presents encryption as a measure that already hides payload contents on all NMEA 2000 networks, so passive recon yields little.

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 17 (10 points)

A baseline built from a capture shows the heading PGN from one source with a mean interval of 100 ms and a standard deviation of 2 ms. (a) What update rate is this? (b) Using a 3-sigma rule, what range of intervals is treated as normal? (c) Later, the same PGN from that source address is seen arriving about every 50 ms. State whether it falls outside the range, and give two possible explanations. (d) State one limit of using frequency alone as a detector.

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

A passive capture of a test network shows a GPS, an autopilot, a depth sounder, a wind sensor and an AIS transponder. Using the class's table of critical systems, rank the three highest-value targets from an attacker's point of view and justify each by safety impact. Then state what a defender learns by seeing the same inventory.

**Answer:**

\vspace{3cm}

---

### Question 19 (10 points)

Compare passive and active reconnaissance for detectability. Then list three defensive measures from the class and, for each, name the kind of activity it helps notice or limit. Explain in one or two sentences why the class says that easy profiling of a network points to defensive gaps.

**Answer:**

\vspace{3cm}

---

## Honor Code

I certify that I have completed this quiz independently without unauthorized assistance.

**Student Name**: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Signature**: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Date**: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## Answer Key (Instructor Use Only)

### Part 1: Multiple Choice

1. **Answer: d** - Passive recon is observing without transmitting; active recon sends messages to elicit responses.

2. **Answer: c** - PGN 126996 is Product Information (manufacturer, model, software version, serial number). PGN 60928 is Address Claim, 59904 is ISO Request, 127250 is heading.

3. **Answer: a** - Device count is inferred from unique source addresses; device types are inferred from the PGNs each source transmits.

4. **Answer: b** - The class says software version feeds vulnerability research for known issues in specific versions.

5. **Answer: d** - Wind (130306) is listed at 1 Hz. Heading and position are listed at 10 Hz.

6. **Answer: b** - The instructor notes use a 3 sigma deviation as the alert threshold, using the standard deviation as the expected variation.

7. **Answer: c** - The table lists depth (128267) with grounding risk. Heading is autopilot manipulation, engine is propulsion control, AIS is collision risk, alarms are safety system bypass.

8. **Answer: d** - A genuine device sending false values is TM3. Because the device, address and rate are all normal, an allowlist and a frequency baseline are not expected to flag it; value plausibility and cross-checks against other sensors are the relevant tools.

9. **Answer: a** - Allowlisting alerts on unknown source addresses. Monitoring for new Address Claims is a related active-watch activity named in the class.

10. **Answer: d** - The instructor notes list ISO Requests from unknown sources, scanning patterns (requesting from all addresses) and unusual request frequency as things an IDS could notice, while noting most maritime systems have no detection.

---

### Part 2: True/False

11. **False** - Passive recon observes without transmitting; sending requests is active recon.

12. **True** - PGN 126996 is a Fast Packet message of about 134 bytes spread over several CAN frames.

13. **False** - Baselines support anomaly detection (Week 9 builds on them) and also help attackers understand normal behavior. Defenders use them to find deviations.

14. **True** - Active recon sends ISO Requests that a monitoring system could notice, though the class notes most maritime systems have no such detection.

15. **True** - The instructor notes say real vessel networks typically have 5-20 devices such as GPS, autopilot, wind, depth, engine interface, AIS and VHF.

16. **False** - The class lists encryption only as a defensive measure with limited support. Standard NMEA 2000 sends data in plaintext, as Class 02 taught, so observers can read it.

---

### Part 3: Short Answer

17. **Expected Answer**:
    - (a) 1 / 0.1 s = 10 Hz.
    - (b) Mean +/- 3 x 2 ms = 100 +/- 6 ms, so roughly 94 ms to 106 ms.
    - (c) 50 ms is outside that range; it corresponds to about 20 Hz, twice the baseline. Possible explanations: an additional transmitter sending the same PGN under that address, a replacement or injection attempt at a higher rate, or a device fault or misconfiguration. Alert and investigate rather than assume an attack.
    - (d) An observer that matches the baseline rate would not be flagged by frequency alone, so value checks and cross-validation against other sensors are also needed.

    **Grading**: Full credit (10 pts) for all four parts; 8 pts for one error or missing limit; 6 pts for correct math but weak interpretation; 4 pts for partial; partial credit for any correct component.

18. **Expected Answer**:
    - Depth (128267): grounding risk, safety critical.
    - Heading (127250), tied to the autopilot: autopilot manipulation; the class rates heading error among the most critical impacts. (Accept position/GPS 129025/129026, navigation compromise, in its place with justification.)
    - AIS (129038/129039): collision risk. Position, engine and alarms are also acceptable if justified from the class table (engine = propulsion control, alarms = safety system bypass).
    - Defender view: the same inventory shows what to protect and monitor first, what an unauthorized device would look like, and which devices need baselines and allowlist entries.

    **Grading**: Full credit (10 pts) for three justified targets from the table plus the defender perspective; 8 pts for targets without full justification; 6 pts for two targets; 4 pts for a list with no reasoning.

19. **Expected Answer**:
    - Passive recon does not transmit, so it produces no traffic on the bus for a monitor to see (the class stresses any device can read all traffic). Active recon sends requests (for example ISO Requests) that a monitoring system could notice, such as requests from unknown sources, scanning patterns or unusual request frequency.
    - Measures (any three): monitoring for scanning; allowlisting unknown source addresses; baseline deviation checks for unusual request patterns; encryption of payloads (limited support); network segmentation; device authentication; traffic monitoring.
    - Easy profiling points to missing segmentation, authentication, monitoring and predictable message patterns.

    **Grading**: Full credit (10 pts) for the detectability contrast, three measures with the activity each addresses, and the gap explanation; 8 pts if one element is thin; 6 pts for generic answers; 4 pts for only partial lists.

---

## Grading Rubric

| Section | Points | Percentage |
|---------|--------|------------|
| Part 1: Multiple Choice (10 questions × 4 pts) | 40 | 40% |
| Part 2: True/False (6 questions × 5 pts) | 30 | 30% |
| Part 3: Short Answer (3 questions × 10 pts) | 30 | 30% |
| **Total** | **100** | **100%** |

### Grade Scale

| Score | Grade |
|-------|-------|
| 90-100 | A |
| 80-89 | B |
| 70-79 | C |
| 60-69 | D |
| 0-59 | F |

---

## Common Mistakes to Watch For

**Question 8 (Threat models):**
- Calling a faulty or compromised genuine device TM2; a genuine device with false values is TM3
- Assuming allowlists and frequency baselines would catch TM3

**Question 17 (Baseline math):**
- Using standard deviation as the alert threshold itself rather than 3 sigma around the mean
- Converting interval to rate wrongly (rate = 1 / interval)
- Claiming frequency alone proves an attack

**Question 18 (Targets):**
- Ranking by what is most interesting instead of by safety impact
- Forgetting the defender perspective

**Question 19 (Detectability):**
- Saying active recon is invisible, or overstating that nothing can ever be detected
- Listing measures without tying each to the activity it addresses
---

## Study Tips for Next Quiz

- Practice computing rate, mean interval and a 3-sigma band from a baseline
- Memorize the frequency table and the high-value-target table
- Compare passive and active recon, including which PGNs are used
- Review PGN 126996 content and Fast Packet reassembly
- Preview Class 05 on spoofing and think about which detections work against which threat model

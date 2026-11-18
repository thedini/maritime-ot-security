---
title: "Quiz 06"
subtitle: "Engine and Propulsion System Attacks"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 06: Engine and Propulsion System Attacks

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

Why is an engine gateway an attractive device for an attacker to impersonate on an NMEA 2000 network?

a) It uses a different bitrate, so its messages cannot be monitored

b) It is the only device allowed to transmit engine PGNs under the standard

c) Other devices trust its messages and the bus provides no authentication of the sender

d) It encrypts engine data, so forged values are indistinguishable by design

---

### Question 2

Which PGN carries engine speed (RPM) and is transmitted at about 10 Hz?

a) 127489 (Engine Parameters, Dynamic)

b) 127505 (Fluid Level)

c) 127488 (Engine Parameters, Rapid Update)

d) 127508 (Battery Status)

---

### Question 3

A display shows a fuel tank nearly full when it is actually almost empty. What is the most serious consequence described in class?

a) An unnecessary fuel stop and wasted money

b) A false overheat alarm

c) Overfilling the oil system

d) Running out of fuel at sea, with possible rescue, grounding or collision

---

### Question 4

A defender sees engine RPM from one source change from idle to a very high value between two consecutive frames. Which class-taught check would flag this?

a) Rate-of-change (physical plausibility) limits

b) A check of the CAN bitrate

c) A check of the NAME industry group

d) A check of the Fast Packet sequence counter

---

### Question 5

An engine gateway with a failed or manipulated sensor reports normal oil pressure at its normal rate from its own legitimate source address, while real pressure is low. Which threat model does this match?

a) TM1: modified traffic

b) TM2: substituted transmitter

c) None; this cannot happen on a bus

d) TM3: genuine device sending false values

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 3 points.

### Question 6

**T / F**: Engine Parameters, Rapid Update (PGN 127488) is transmitted at 10 Hz.

---

### Question 7

**T / F**: A false alarm (for example a fake overheat condition) is harmless because the crew can simply ignore it.

---

### Question 8

**T / F**: NMEA 2000 authenticates the sender of engine messages, so a forged engine PGN is rejected by displays.

---

### Question 9

**T / F**: Cross-validating a fuel gauge against an independent flow measurement can reveal inconsistent fuel data.

---

### Question 10

**T / F**: Spoofing 0 RPM while the engine is running could lead the crew to try to start an already-running engine.

---

### Question 11

**T / F**: PGN 127489 (Engine Parameters, Dynamic) is a multi-frame Fast Packet message.

---

### Question 12

**T / F**: A rate-of-change limit on engine temperature is sufficient to detect every possible falsification of that value.

---

### Question 13

**T / F**: Because modern vessels often have mechanical backup indicators, a spoofed electronic display carries no safety risk.

---

### Question 14

**T / F**: Rate-of-change limits can fail to flag a falsified value that drifts slowly within physically plausible bounds.

---

### Question 15

**T / F**: Engine-attack exercises may be run on a live vessel network if the test is brief and the crew is informed.

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 16 (10 points)

Choose TWO of the following scenarios discussed in class: oil-pressure alarm suppression, a false overheat alarm, a fuel level shown as full when nearly empty, or gear-indicator confusion during docking. For each, explain the consequence for safety or cost and why the crew might trust the false reading. Then state which of your two the crew would find harder to notice, and why.

**Answer:**

\vspace{3cm}

---

### Question 17 (10 points)

A defender reviewing a capture notes: (a) engine RPM from one source changes from idle to a very high value between consecutive frames; (b) a fuel level reading rises sharply with no refueling; (c) the gear indicator shows reverse while RPM and vessel motion are consistent with forward travel. For each, name the class-taught check that flags it, and state one limitation of checks of this kind.

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

Classify each scenario as TM1, TM2 or TM3 and justify: (a) an unauthorized device on the bus transmits forged engine PGNs; (b) the genuine engine gateway, with a manipulated sensor, reports normal values from its own address. Then explain what a check on the sender cannot address, how cross-sensor validation helps, and why exercises on engine data are run only on an isolated test network.

**Answer:**

\vspace{3cm}

---

## Honor Code

I certify that I have completed this quiz independently without unauthorized assistance.

**Student Name**: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Signature**: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Date**: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## Answer Key (Instructor Use Only)

### Part 1: Multiple Choice

1. **Answer: c** - The gateway converts engine data (for example from J1939) to NMEA 2000 and is trusted by displays and plotters. With no authentication, any device able to transmit can send messages that look like the gateway's.

2. **Answer: c** - PGN 127488 carries engine speed, boost and tilt/trim at 10 Hz. PGN 127489 is the slower dynamic message (oil pressure, temperatures, hours), 127505 is fluid level and 127508 is battery status.

3. **Answer: d** - A falsely reassuring fuel level can let the vessel run out of fuel mid-voyage. An empty-when-full display causes only unnecessary refueling and cost.

4. **Answer: a** - Class lists range validation and rate-of-change limits: RPM cannot realistically go from idle to very high instantly, and temperatures change gradually.

5. **Answer: d** - The device is genuine and the address is legitimate; only the reported value is false. That is TM3. Cross-sensor validation, not sender checks, is the relevant defense.

---

### Part 2: True/False

6. **True** - Class lists PGN 127488 at 10 Hz (100 ms), carrying RPM, boost and tilt/trim.

7. **False** - False alarms can cause an unnecessary shutdown, loss of propulsion in dangerous waters, or costly inspections, and they erode trust in real alarms.

8. **False** - NMEA 2000 has no sender authentication; the class notes the gateway is trusted with no authentication, so forged messages are not rejected on that basis.

9. **True** - Class lists cross-sensor validation (fuel gauge versus flow meter) as a defense. It raises the effort needed but does not guarantee detection.

10. **True** - The class instructor notes give this example: the crew might try to start a running engine, which could damage the starter or flywheel.

11. **True** - PGN 127489 is 26 bytes long, so it is sent using Fast Packet across several CAN frames.

12. **False** - Rate-of-change limits address abrupt changes only. Class pairs them with cross-sensor validation because no single check covers every case.

13. **False** - The class notes the crew may trust the electronic display over the mechanical backup, so spoofed displays carry real risk.

14. **True** - A value moving gradually within plausible limits can stay under a rate-of-change threshold, which is why independent sensors are also useful.

15. **False** - Exercises are confined to an isolated test network. A live vessel could be put at risk, and testing without authorization is unethical.

---

### Part 3: Short Answer

16. **Expected Answer**:
    - Oil-pressure alarm suppression: a normal-looking value hides real low pressure; crew trusts the instruments; engine can seize and be destroyed.
    - False overheat alarm: crew shuts down a healthy engine; vessel loses propulsion, possibly in a shipping lane or bad weather.
    - Fuel level shown full when nearly empty: run out of fuel at sea. Gear confusion: collision risk during docking.
    - Suppression is usually harder to notice because nothing alarms until damage appears; a false alarm is noticed at once but still has a safety cost.
    - Accept any two valid scenarios from the class with correct consequences and a reasoned comparison.

    **Grading**: Full credit (10 pts) for two scenarios with correct consequences and a reasoned comparison of how noticeable each is; 8 pts for two scenarios with consequences but weak comparison; 6 pts for one scenario well explained; 4 pts for generic safety statements; partial credit for any correct point.

17. **Expected Answer**:
    - (a) Idle to very high RPM in one step: rate-of-change limit (RPM cannot change that fast). Possible falsified value or sender fault.
    - (b) Fuel level rising with no refueling: volume conservation; compare with flow meter or consumption.
    - (c) Reverse shown while RPM and motion indicate forward: engine RPM correlation with gear.
    - Response: alert the crew and verify with a physical gauge or independent sensor rather than rely on the suspect display.
    - Limit: these checks reduce risk but do not guarantee detection; a slow drift within plausible bounds may pass.

    **Grading**: Full credit (10 pts) for all three observations with the matching check and one limit; 8 pts for all three with no limit; 6 pts for two observations explained; 4 pts for naming checks without explanation; partial credit for any correct point.

18. **Expected Answer**:
    - (a) Forged messages from an unauthorized device: TM1 (modified traffic). If it claims the gateway's enrolled source address with a different transmitter, TM2 also applies.
    - (b) Genuine gateway, legitimate address and rate, false value: TM3.
    - Sender-oriented checks (address monitoring, authentication) bear on TM1/TM2 at best; they cannot address TM3 because the sender is real.
    - Cross-sensor validation helps against TM3 to the extent an independent sensor exists and is itself trustworthy.
    - Success against one threat model does not establish protection against the others.
    - Ethics: isolated test network only, because engine data affects crew safety.

    **Grading**: Full credit (10 pts) for correct classification of both scenarios, a correct statement of what sender checks cannot address, the cross-sensor point and an ethics reference; 8 pts for correct classification with minor gaps; 6 pts for classification with confused reasoning; 4 pts for naming threat models without applying them; partial credit for any correct point.

---

## Grading Rubric

| Section | Points | Percentage |
|---------|--------|------------|
| Part 1: Multiple Choice (5 questions × 4 pts) | 40 | 40% |
| Part 2: True/False (10 questions × 3 pts) | 30 | 30% |
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

**Question 1 (gateway trust):**
- Saying the gateway is secure because it uses J1939
- Missing the lack of authentication

**Question 5 (threat models):**
- Choosing TM1 because 'false data' sounds like traffic modification; the key facts are the genuine device and legitimate address
- Not recognizing that TM3 cannot be caught by sender checks

**Question 16 (safety impact):**
- Listing consequences without explaining why crews trust the instruments
- Not distinguishing a hidden alarm from a fake alarm

**Question 17 (capture checks):**
- Naming a check without linking it to the observation
- Omitting any limitation

**Question 18 (threat models and ethics):**
- Claiming cross-sensor validation always detects falsification
- Omitting the isolated-network requirement

---

## Study Tips for Next Quiz

- Review PGN 127488, 127489, 127505, 127493 and 127508 and what each reports
- Memorize the defenses listed in class: range validation, rate-of-change limits, cross-sensor validation
- Practice assigning scenarios to TM1, TM2 or TM3 and stating what each defense cannot address
- Review the safety discussion: alarm suppression versus false alarms
- Review CAN arbitration and bus-off for the next class

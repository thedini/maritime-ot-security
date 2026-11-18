---
title: "Quiz 07"
subtitle: "Denial of Service and Replay Attacks"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 07: Denial of Service and Replay Attacks

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

In CAN arbitration, which frame wins when two nodes begin transmitting at the same time?

a) The frame with the higher numeric identifier

b) The frame from the node with the lowest source address only

c) The frame with the lower identifier, because a dominant 0 bit overrides a recessive 1

d) The frame with the longer payload

---

### Question 2

Which property of NMEA 2000 explains why a replayed message is accepted by a receiver?

a) Messages are encrypted with a shared key

b) Receivers always check the sequence counter

c) Each PGN includes a timestamp that receivers verify

d) Most PGNs carry no timestamp, sequence number or authentication, so old and new frames look alike

---

### Question 3

Which observation best suggests that replayed navigation data is being injected?

a) Position and heading that contradict independent sensors, or a sudden position jump relative to a motion prediction

b) A frame with a 29-bit identifier

c) The normal 250 kbps bitrate

d) A device sending at its usual rate

---

### Question 4

What does it mean when a CAN node enters the bus-off state?

a) It has been given the highest priority

b) It has switched to a faster bitrate

c) It has been disabled from transmitting after its error counter exceeded the threshold

d) It has completed an address claim

---

### Question 5

Flooding, replay and injection of recorded frames fall under which threat model, and which threat model is NOT directly addressed by detecting them?

a) TM2 (substituted transmitter); TM1 is not addressed

b) TM1 (modified traffic); a genuine device sending false values (TM3) is not directly addressed

c) TM3 (false values); TM1 is not addressed

d) All three equally

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 3 points.

### Question 6

**T / F**: A flood of high-priority frames can starve lower-priority legitimate traffic on the bus.

---

### Question 7

**T / F**: CAN arbitration was designed primarily to authenticate message senders.

---

### Question 8

**T / F**: Of the flood variations covered in class, a full flood is the hardest to detect.

---

### Question 9

**T / F**: Device-silence (availability) monitoring can reveal that a legitimate transmitter has been blocked or disabled.

---

### Question 10

**T / F**: Timestamps and sequence numbers can help receivers detect replayed data.

---

### Question 11

**T / F**: Replaying previously recorded normal engine data during an actual fault could suppress alarms.

---

### Question 12

**T / F**: A detector that only counts frames per second is enough to catch every variation of flooding, including traffic shaped to match the normal pattern.

---

### Question 13

**T / F**: Replayed frames are valid frames, so a receiver cannot tell old from new without extra context or checks.

---

### Question 14

**T / F**: A denial of service on a vessel bus is only an inconvenience and has no safety impact.

---

### Question 15

**T / F**: For realism, flooding experiments are acceptable on a live vessel network during a low-risk period.

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 16 (10 points)

Pick THREE systems from this list: GPS/position, heading and autopilot, engine data, alarms, AIS. For each, explain the consequence if its traffic is blocked by a denial of service. Then explain why loss of navigation or control at sea is more serious than a comparable loss on a road vehicle.

**Answer:**

\vspace{3cm}

---

### Question 17 (10 points)

For each of the following, describe what a defender would expect to see in a capture or monitoring tool and name the class-taught detection indicator that applies: (a) a full flood, (b) a targeted or burst flood, (c) traffic shaped to match the normal pattern, (d) replay of recorded navigation data. Do not describe how to carry out any of them.

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

Describe two network-level and two device-level defenses covered in class, with one limitation of each. Then state which threat model these defenses address and which threat model they do not address, and why.

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

1. **Answer: c** - Lower identifier wins; a dominant 0 beats a recessive 1 and the losing node backs off. This was designed for reliability among trusted nodes, not for security.

2. **Answer: d** - The class lists no timestamps, no sequence numbers in most PGNs and no authentication, so receivers cannot distinguish old from new.

3. **Answer: a** - Class lists context mismatch (cross-sensor validation) and position jumps (Kalman filter prediction) as replay indicators. Matching rate alone shows nothing.

4. **Answer: c** - Bus-off is the error state in which a node is disabled after its error counters pass the limit. Class notes recovery can require physical access or a power cycle.

5. **Answer: b** - These behaviors are TM1. A genuine device reporting false values (TM3) produces well-formed, correctly timed traffic from its own address, which flood and replay checks do not address.

---

### Part 2: True/False

6. **True** - With a high-priority identifier an attacker wins arbitration repeatedly, so lower-priority traffic cannot get through. Class notes the bus assumes trusted nodes.

7. **False** - Arbitration is a collision-resolution mechanism designed for reliability. It does not verify sender identity.

8. **False** - The class table rates a full flood as obvious, while shaped traffic that matches the normal pattern has the lowest detectability.

9. **True** - Class lists device silence and watchdog timers under availability monitoring.

10. **True** - Class lists sequence numbers and timestamps as device-level defenses. They help only when receivers actually check them.

11. **True** - Class scenario: normal engine data replayed during a failure leaves alarms suppressed and the crew unaware.

12. **False** - Shaped traffic matches normal rates, so a pure rate counter can miss it. Class pairs rate monitoring with priority distribution, silence and error-counter monitoring.

13. **True** - Class states receivers cannot distinguish old from new; detection needs timestamps, sequence tracking, external references or cross-sensor checks.

14. **False** - Class table shows blocked GPS, heading, engine data and alarms leave the crew blind or safety systems disabled, with no way to pull over at sea.

15. **False** - Class requires an isolated test network for all such exercises. Flooding a live bus risks loss of navigation or alarms.

---

### Part 3: Short Answer

16. **Expected Answer**:
    - GPS/position blocked: navigation blind.
    - Heading blocked: autopilot may fail or hold a stale value.
    - Engine data blocked: no monitoring. Alarms blocked: safety systems disabled, faults unannounced. AIS blocked: collision risk.
    - A vessel cannot pull over; loss of navigation or control at sea can lead to grounding or collision.

    **Grading**: Full credit (10 pts) for three systems with correct consequences and the at-sea point; 8 pts for three systems without the at-sea point; 6 pts for two systems; 4 pts for generic availability statements; partial credit for any correct point.

17. **Expected Answer**:
    - (a) Full flood: legitimate traffic nearly disappears, one identifier dominates, priority distribution is abnormal; traffic spike, priority anomaly, silent devices. Obvious.
    - (b) Targeted or burst flood: specific devices or periods go quiet; needs a baseline; device-silence and rate monitoring apply.
    - (c) Shaped traffic: normal-looking rates; lowest detectability; priority, silence and context checks help but may not suffice.
    - (d) Replay: frames are valid and at normal rate; look for position jumps versus prediction, duplicate sequences, stale timestamps and mismatch with independent sensors.

    **Grading**: Full credit (10 pts) for linking at least three of the four to distinct indicators and noting that shaped traffic and replay need context beyond rate; 8 pts for three with minor gaps; 6 pts for indicators without linkage; 4 pts for rate monitoring only; partial credit for any correct point. Deduct for any attack procedure or parameters.

18. **Expected Answer**:
    - Network level: rate limiting per source, priority monitoring, allowlisting known identifiers, gateway filtering. Limits: traffic that stays within policy or matches normal patterns may pass; allowlists need maintenance.
    - Device level: sequence numbers, timestamps, watchdog timers, authentication (listed in class as future). Limits: need device support; do not stop a device that genuinely reports a wrong value.
    - Threat models: these address TM1 (modified traffic). TM2 (substituted transmitter) is examined later through fingerprinting; TM3 (genuine device, false values) is not addressed by flood or replay defenses.
    - No defense listed is claimed to be complete; layers are combined.

    **Grading**: Full credit (10 pts) for two network and two device defenses, one limit each, and a correct threat-model statement; 8 pts for defenses with one or two limits missing; 6 pts for defenses only; 4 pts for naming one category; partial credit for any correct point.

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

**Question 1 (arbitration):**
- Reversing which identifier wins
- Confusing arbitration with sender verification

**Question 5 (threat models):**
- Treating a detector for TM1 as protection against TM2 and TM3
- Not noticing that TM3 traffic is well formed and correctly timed

**Question 16 (safety impact):**
- Describing only data loss, not what it means for navigation at sea

**Question 17 (capture indicators):**
- Listing only rate for every attack
- Forgetting that replayed frames are valid frames

**Question 18 (defenses):**
- Claiming any defense is complete
- Omitting limits

---

## Study Tips for Next Quiz

- Review arbitration, dominant versus recessive bits and priority bits
- Review error counters, error passive and bus-off at a conceptual level
- Memorize the DoS and replay detection tables and their limits
- Practice stating which threat model each defense addresses and which it cannot
- Preview frequency-based detection for the next class

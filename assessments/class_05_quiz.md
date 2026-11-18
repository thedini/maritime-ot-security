---
title: "Quiz 05"
subtitle: "Navigation Spoofing Attacks"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 05: Navigation Spoofing Attacks

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

Which CAN bus weakness does the class list first as making spoofing possible?

a) Data is always fragmented

b) No authentication: any node can send any message

c) Messages are limited to 8 bytes

d) The bus runs at 250 kbps

---

### Question 2

Why does the class rate a heading error on a vessel with the autopilot engaged as Critical?

a) Chart plotters stop displaying position

b) The engine stops immediately

c) AIS is switched off

d) The autopilot compares false heading to the desired course and applies rudder correction, so the vessel can turn the wrong way

---

### Question 3

At what rate does the class say PGN 129025 (Position, Rapid Update) is normally sent?

a) 0.5 Hz

b) 1 Hz

c) 10 Hz

d) 100 Hz

---

### Question 4

According to the class table, which kind of change carries the highest detection risk?

a) Sudden jump

b) Gradual drift

c) Matching vessel motion

d) None of them

---

### Question 5

Which detection method does the class pair with 'physics violations'?

a) Clock skew fingerprinting

b) Frequency baseline comparison

c) Value delta monitoring

d) Kalman filter prediction

---

### Question 6

Which independent sources does the class suggest for cross-validating GPS?

a) Another GPS unit on the same bus only

b) Radar and visual observation

c) The vessel's wiring diagram

d) The chart plotter's own display

---

### Question 7

Which cascading effect of false position data does the class list?

a) Termination resistors fail

b) AIS transmits a false position to other vessels

c) CAN bitrate changes

d) Heading switches to true automatically

---

### Question 8

Clock skew fingerprinting is listed against 'source impersonation'. Which threat model is that, and why might it not help against a genuine device sending false values?

a) TM1; a modified frame keeps its original clock

b) TM3; false values change the clock

c) TM2; a genuine device is the legitimate transmitter, so its own timing would look normal

d) TM2; clock skew only works on 11-bit IDs

---

### Question 9

Where may the course's spoofing activities be performed?

a) Only on isolated test networks

b) On a docked vessel with the captain's permission

c) On any network after signing the ethics agreement

d) On a vessel at sea with a safety crew

---

### Question 10

A student says: 'If my spoofed position changes slowly and matches the vessel's physics, defenders cannot possibly detect it.' What is the best response?

a) Correct; physics-matched data cannot be detected

b) Correct, but only for heading

c) Incorrect; slow changes are always the easiest to detect

d) Incorrect; the class says this lowers detection risk, not to zero, and cross-validation with other sensors and source checks can still help

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 5 points.

### Question 11

**T / F**: The class states that receivers such as chart plotters verify the source of position messages.

---

### Question 12

**T / F**: The class says gradual drift has lower detection risk than a sudden jump when only value changes are monitored.

---

### Question 13

**T / F**: Sending spoofed data at the same rate as the genuine source guarantees it cannot be detected.

---

### Question 14

**T / F**: Sending messages at a rate well above the genuine source can be spotted by frequency monitoring.

---

### Question 15

**T / F**: A false position on a vessel can propagate to systems such as ECDIS and to AIS broadcasts seen by other vessels.

---

### Question 16

**T / F**: Students may test spoofing on a real vessel at the dock if the crew is informed.

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 17 (10 points)

A vessel's chart display and AIS begin to show a position that is 10 nautical miles from the true position. Using the class's cascading-effects list, describe four systems affected and the safety consequence of each. Why does one false input spread to so many systems?

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

Design layered detection for a vessel whose autopilot takes heading from the NMEA 2000 bus. Name three detection layers from the class, say what each notices, and give one limit of each. For each layer, state which threat model it is best suited to (TM1 modified traffic, TM2 substituted transmitter, TM3 genuine device sending false values) and which it is weakest against.

**Answer:**

\vspace{3cm}

---

### Question 19 (10 points)

Explain why this course requires isolated test networks and a signed ethics agreement for spoofing material. Describe two real-world harms from navigation spoofing named in the class, and give two reasons why learning these techniques is framed as defensive.

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

1. **Answer: b** - The class lists no authentication first (any node can send any message), followed by no encryption, broadcast nature and priority override.

2. **Answer: d** - Autopilot reads heading, compares it to desired course and corrects rudder, so a false heading can turn the vessel the wrong way. The class rates heading error as Critical.

3. **Answer: c** - Position Rapid Update is listed at 10 Hz (100 ms).

4. **Answer: a** - The class table: sudden jump is HIGH detection risk, gradual drift is LOW, matching vessel motion is LOWEST.

5. **Answer: d** - Physics violations are paired with Kalman filter prediction; sudden changes with value delta monitoring; wrong frequency with baseline comparison; impersonation with clock skew.

6. **Answer: b** - The class suggests cross-validating GPS with other sources such as radar and visual observation.

7. **Answer: b** - Cascading effects listed: ECDIS wrong position, AIS false position to other vessels, wrong collision avoidance CPA, false voyage recorder data, weather routing from wrong position.

8. **Answer: c** - Clock skew fingerprinting targets TM2 (a different transmitter under another's address). A genuine device sending false values is TM3; its own timing would be expected to look normal, so value plausibility and cross-sensor checks are the relevant tools. Limits apply to every technique.

9. **Answer: a** - All course activities are on isolated test networks only; the class asks students to sign an ethics agreement first.

10. **Answer: d** - The class describes matching vessel motion as the lowest detection risk, not zero risk. Cross-validation, source checks and other layers remain available. No technique is guaranteed either way.

---

### Part 2: True/False

11. **False** - The class says chart plotters trust whatever arrives; there is no verification of message source.

12. **True** - Table: gradual drift has LOW detection risk because it looks like normal movement, though it takes longer to have effect.

13. **False** - Matching the rate is harder to detect by frequency alone but is not a guarantee; value checks, cross-validation and source checks can still notice it.

14. **True** - The class lists overwhelming (sending faster) as detectable by frequency monitoring.

15. **True** - Cascading effects include ECDIS showing a wrong position and AIS transmitting a false position to other vessels.

16. **False** - All activity is on isolated test networks only. Real vessels can be damaged and people can die; the instructor notes stress this.

---

### Part 3: Short Answer

17. **Expected Answer**:
    - Any four of: ECDIS shows the wrong position (wrong navigation picture, grounding risk); AIS transmits a false position to other vessels (collision risk and traffic confusion); collision-avoidance calculates the wrong CPA (wrong avoidance decisions); the voyage recorder logs false data (investigation and evidence problems); weather routing uses the wrong position (poor route decisions).
    - One input spreads because modern vessels are highly integrated and devices trust whatever data arrives; there is no verification of the message source, and crew may not notice subtle errors.

    **Grading**: Full credit (10 pts) for four systems with consequences and the integration/trust explanation; 8 pts for three systems or thin integration reasoning; 6 pts for two or generic effects; 4 pts for partial.

18. **Expected Answer**:
    - Value-delta monitoring: notices sudden jumps; limit: gradual drift looks like normal movement. Best suited to value-level falsehood from any source including TM3; weakest at drifting values.
    - Frequency baseline comparison: notices wrong rates, such as a second transmitter adding frames; limit: a source matching the baseline rate is not flagged by frequency alone. Best suited to TM2 (added or substituted transmitter); weakest against TM3.
    - Cross-validation (radar, visual, other sensors) or Kalman-style physics prediction: notices values inconsistent with other sources or motion; limit: needs independent, working sensors and good models. Suited to TM3 and TM1 where values change; applicable to any source.
    - Clock skew fingerprinting: notices source impersonation; best suited to TM2; weakest against TM3 because a genuine device's timing looks normal. TM1 (modified traffic) is about changed content in transit; value checks help there.
    - Accept any three layers with a stated limit and a defensible mapping; do not accept claims that a layer is certain.

    **Grading**: Full credit (10 pts) for three layers each with what it notices, a limit, and a defensible threat-model mapping; 8 pts if mappings are partly missing; 6 pts for layers without limits; 4 pts for a list of detection names only.

19. **Expected Answer**:
    - Isolation: the bus broadcasts to every device and receivers trust what arrives, so test data on a live network could be taken as real; isolation keeps consequences on the bench.
    - Ethics agreement: makes responsibility explicit and records that this knowledge is for defense; legal consequences are severe.
    - Harms (any two): vessel grounding, collisions, loss of life, environmental disasters.
    - Defensive framing (any two): understanding how spoofed data appears lets defenders build detection (value, frequency, cross-validation); defenders need to think like attackers; the class focuses on recognition, impact and detection.

    **Grading**: Full credit (10 pts) for isolation rationale, two harms and two defensive reasons; 8 pts if one element is thin; 6 pts for generic ethics statements; 4 pts for partial.

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
- Assigning clock skew fingerprinting to TM3; it targets source impersonation (TM2)
- Treating any single technique as certain to detect or fail

**Question 10 (Detection claims):**
- Believing physics-matched data is undetectable
- Believing gradual changes are always easiest to detect

**Question 18 (Layered detection):**
- Naming layers without limits
- Treating detection layers as guaranteed

**Question 19 (Ethics):**
- Treating isolation as a formality
- Describing the course as offensive rather than defensive training
---

## Study Tips for Next Quiz

- Review the Why Spoofing Works list and the receiver behavior bullet points
- Memorize the detection opportunities table and what each method notices
- Review the impact analysis and cascading effects lists
- Practice mapping each defense to TM1, TM2 or TM3 and stating its limit
- Reread the ethics warning and the safety notes
- Preview Class 06

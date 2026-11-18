---
title: "Quiz 14"
subtitle: "Defense Architecture and Capstone Review"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 14: Defense Architecture and Capstone Review

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

In the defense-in-depth model from class, which layer performs ensemble detection?

a) Layer 5: Operator Interface

b) Layer 3: Ensemble Detection

c) Layer 1: Data Collection

d) Layer 4: Alert Management

---

### Question 2

Which placement option does class recommend for most deployments, and why?

a) Inline monitor, because it can drop bad frames

b) Gateway integration, because it needs the least configuration

c) Either inline or gateway, because latency does not matter

d) Passive tap, because it is not a single point of failure, adds no latency and cannot accidentally block traffic

---

### Question 3

In the red team scenario table, which attack is expected to be detected by Frequency plus Entropy?

a) DoS flood using priority 0

b) Replay attack

c) Engine false alarm

d) Stealthy drift

---

### Question 4

In the capstone guidelines, which component carries 30% of the grade?

a) Implementation

b) Documentation

c) Evaluation

d) Presentation

---

### Question 5

In the blue team `DetectionAnalyzer`, how is a false positive counted?

a) Any attack that was not detected

b) An alert whose timestamp falls outside every logged attack window

c) An alert with severity 'low'

d) An alert that has more than one detection type

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 3 points.

### Question 6

**T / F**: A passive tap IDS can accidentally block bus traffic if it fails.

---

### Question 7

**T / F**: Class states that a well-designed defense-in-depth system detects every attack.

---

### Question 8

**T / F**: In the class IDS, an ensemble score of 0.75 produces severity 'high'.

---

### Question 9

**T / F**: A passive tap adds latency to messages travelling between the GPS and the chart plotter.

---

### Question 10

**T / F**: A device fingerprint check can be relied on to reveal a genuine enrolled device that reports false values (TM3).

---

### Question 11

**T / F**: The red team scorecard records which detection method, if any, caught each attack.

---

### Question 12

**T / F**: The capstone requires a working IDS with at least three detection methods.

---

### Question 13

**T / F**: Gateway integration can actively block attacks, but it is more complex and can affect availability.

---

### Question 14

**T / F**: The red team scenario table lists a rate-matched position spoof as expected to be caught by the Frequency detector.

---

### Question 15

**T / F**: The final exam is weighted 40% written, 40% practical and 20% capstone presentation.

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 16 (10 points)

Name the five layers of the maritime IDS architecture from class, from the bus upward, and describe in one phrase what each layer does.

**Answer:**

\vspace{3cm}

---

### Question 17 (10 points)

During a red team exercise 5 attacks were executed. The blue team recorded these first-detection delays: 0.5 s, 1.0 s, 1.5 s and 3.0 s for four detected attacks; the fifth was missed. Six alerts fell outside every attack window during a 30-minute benign period (hypothetical numbers).

Using the metrics defined by the `DetectionAnalyzer`, calculate the detection rate and the mean detection delay. Convert the false alerts to alerts per hour. State one reason the detection rate alone is not enough to judge the system.

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

Scenario 5 in the red team table (engine false alarm) lists ML plus Fingerprint as the expected detection. Using the three threat models, explain when the fingerprint detector could contribute and when it could not. Name one kind of evidence you would look for in the case where it could not.

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

1. **Answer: b** - Layer 3 holds the frequency, entropy, ML/LSTM and device fingerprint detectors. Layer 1 collects data, Layer 4 manages alerts and Layer 5 is the operator interface.

2. **Answer: d** - Class recommends Option B (passive tap) for most deployments for those three reasons. The gateway option is reserved for high-security cases because it can block attacks but is more complex and can affect availability.

3. **Answer: a** - The table pairs the priority-0 DoS flood with Frequency plus Entropy. Replay is paired with LSTM plus Entropy, engine false alarm with ML plus Fingerprint, and stealthy drift with the ensemble.

4. **Answer: c** - Evaluation (test against 5+ attack types, detection metrics, false positive analysis) is 30%. Implementation is 40%, documentation 20% and presentation 10%.

5. **Answer: b** - The analyzer counts alerts whose timestamp is not inside any logged attack window as false positives. It counts alerts, not distinct incidents or time.

---

### Part 2: True/False

6. **False** - A passive tap listens and cannot accidentally block traffic, which is one reason class recommends it. Blocking risk belongs to the inline and gateway options.

7. **False** - Class says defense is about raising the bar, not perfection, and that sophisticated attacks may succeed partially.

8. **True** - In `_create_alert`, scores of 0.7 up to (not including) 0.9 map to 'high'; 0.9 and above is 'critical' and 0.5 to 0.7 is 'medium'.

9. **False** - A passive tap sits beside the bus and adds no latency, whereas an inline monitor or gateway sits in the message path.

10. **False** - A fingerprint check compares a device's clock signature with its enrollment, and a genuine device keeps its own signature when it sends false values. That is TM3 and needs other evidence; fingerprinting addresses TM2.

11. **True** - The scorecard has columns for whether each attack was detected and by which method, plus evasion attempts.

12. **True** - Capstone requirements include a working IDS with at least 3 detection methods, ensemble logic and explained alerts.

13. **True** - Option C can actively block attacks but needs careful configuration and has potential availability impact.

14. **False** - The table assigns the rate-matched position spoof to Fingerprint, because a rate-matched message passes a rate check. The naive spoof (2x rate) is the one paired with Frequency.

15. **True** - The final exam format is Part A written 40%, Part B practical 40% and Part C capstone 20%.

---

### Part 3: Short Answer

16. **Expected Answer**:
- Layer 1, Data Collection: CAN interface, buffering, timestamping and storage
- Layer 2, Data Processing: parsing, feature extraction, baseline and normalization
- Layer 3, Ensemble Detection: frequency, entropy, ML/LSTM and device fingerprint detectors
- Layer 4, Alert Management: prioritization, correlation, suppression and logging
- Layer 5, Operator Interface: dashboard, alerts, reports, controls and explanations (XAI)

**Grading**: 2 pts per layer (name 1, function 1). Accept equivalent wording for functions. Deduct 1 overall if the order is reversed but all layers are correct.

17. **Expected Answer**:
- Detection rate = 4 / 5 = 0.80 (80%).
- Mean detection delay = (0.5 + 1.0 + 1.5 + 3.0) / 4 = 6.0 / 4 = 1.5 s. The analyzer divides by the number of detected attacks, so the missed attack is not included.
- False alerts per hour = 6 alerts / 0.5 h = 12 per hour.
- Detection rate alone ignores alert load (12 per hour could swamp operators), says nothing about which attack was missed, and depends on a small sample of only 5 attacks. Any one of these earns credit.

**Grading**: 3 pts for the detection rate, 3 pts for the mean delay, 2 pts for 12 per hour, 2 pts for a valid reason. Give 2 of 3 on the delay if the missed attack was included in the divisor (method understood, class definition not followed).

18. **Expected Answer**:
- Fingerprinting addresses TM2: if the false engine messages came from a different transmitter claiming the engine's source address, a clock-signature mismatch could contribute.
- If the false values came from the genuine engine device itself (TM3), its clock signature would match enrollment, so the fingerprint detector would not be expected to flag it. In TM1 cases, frequency, entropy or ML evidence matters more.
- Evidence for the TM3 case: values that are implausible for the engine state, inconsistent with other sensors or an independent reference (for example, other engine parameters or readings that disagree), or contradicting physical constraints.

**Grading**: 4 pts for correct TM2 reasoning, 4 pts for explaining why TM3 is outside fingerprinting, 2 pts for a reasonable alternative evidence type. Do not award credit for claims that any one detector covers all three threat models.

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

**Question 16 (Architecture Layers):**
- Mixing up Layer 3 (detection) and Layer 4 (alert management)
- Placing the operator interface at the bottom
- Naming detectors instead of layer functions

**Question 17 (Blue Team Metrics):**
- Including the missed attack in the delay average
- Reporting 6 false alerts instead of 12 per hour
- Treating a high detection rate as proof the system works

**Question 18 (Threat Models):**
- Claiming fingerprinting catches any false value
- Confusing TM2 (a different transmitter) with TM3 (a genuine device)
- Giving no alternative evidence for the case fingerprinting cannot cover

---

## Study Tips for Next Quiz

- Memorize the five architecture layers and what each does
- Review the three placement options and their trade-offs
- Practice computing detection rate, mean delay and false alerts per hour
- Review which threat model each detector addresses and which it cannot address
- Review capstone weights and the final exam format
- Prepare to explain each red team scenario and why a given detector is expected to see it

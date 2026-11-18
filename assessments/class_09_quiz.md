---
title: "Quiz 09"
subtitle: "Frequency-Based Anomaly Detection"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 09: Frequency-Based Anomaly Detection

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

A compass transmits heading (PGN 127250) at 10 Hz. What is the expected mean interval between its messages?

a) 1 s

b) 10 ms

c) 100 ms

d) 2 s

---

### Question 2

In a threshold of mean plus or minus k standard deviations, what happens as k is increased?

a) More false positives and fewer false negatives

b) Fewer false positives and more false negatives, so subtle attacks may be missed

c) Detection rate always improves

d) Nothing changes

---

### Question 3

Which frequency signature does class associate with a device failure, and which would also be seen if a legitimate sender were silenced?

a) Rate much greater than baseline

b) Rate equal to twice the baseline

c) Rate variance much larger than baseline

d) Rate equal to zero

---

### Question 4

For a safety-critical maritime IDS, which metric does class suggest prioritizing, accepting more false positives?

a) Recall (catching attacks), with human validation of alerts

b) Accuracy only

c) Fewest alerts possible

d) Precision only

---

### Question 5

Frequency-based detection is designed mainly to catch which threat model, and which is not caught by rate alone?

a) TM3 only

b) TM2 only

c) TM1 (flooding, naive injection); a genuine device sending false values (TM3) is not caught by rate alone

d) All three equally

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 3 points.

### Question 6

**T / F**: A false positive is an alert on normal traffic.

---

### Question 7

**T / F**: A baseline should be collected during normal operation, without attacks present.

---

### Question 8

**T / F**: Smart spoofing that matches the baseline rate is easy for a frequency detector to catch.

---

### Question 9

**T / F**: Window-based rate detection smooths out jitter and suits flood detection.

---

### Question 10

**T / F**: A frequency baseline may need updating after configuration changes to the network.

---

### Question 11

**T / F**: A frequency detector inspects the content of the data fields to find anomalies.

---

### Question 12

**T / F**: Choosing k = 2 gives a more sensitive detector than k = 4, at the cost of more false positives.

---

### Question 13

**T / F**: A genuine device that reports a false value at its normal rate would not be flagged by a rate-based detector.

---

### Question 14

**T / F**: Recall is the share of actual attacks that the detector identifies.

---

### Question 15

**T / F**: Capturing traffic on a vessel network for baseline building needs no authorization because it is passive.

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 16 (10 points)

Explain why a rate-based (frequency) detector can miss an attacker that keeps the same CAN ID and the same transmission rate as the real device and silences the real sender. Include what the detector actually observes, and name at least one complementary check, with a limitation of that check. Do not describe how to carry out the attack.

**Answer:**

\vspace{3cm}

---

### Question 17 (10 points)

A frequency detector is tested on 1,000 labeled intervals. It produces 40 true positives, 10 false positives, 940 true negatives and 10 false negatives. Calculate precision, recall, false positive rate and accuracy, showing your work. Then explain why accuracy alone is misleading here and what lowering k would do.

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

Class describes correlating the position (PGN 129025) and heading (PGN 127250) rates for one vessel. Explain the ratio check and what it reveals if spoofed position frames are added to the legitimate stream. Then state, for each of TM1, TM2 and TM3, whether frequency analysis can address it and what limit applies.

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

1. **Answer: c** - 10 Hz corresponds to 0.1 s between messages, that is 100 ms. Class builds baselines from the mean and standard deviation of intervals.

2. **Answer: b** - Higher k widens the acceptance band, so fewer normal messages are flagged but subtle deviations are missed. Class suggests k = 3 as a starting point.

3. **Answer: d** - Class lists device failure as rate = 0. The same signature appears if a legitimate sender goes silent, which is why low-rate alerts matter.

4. **Answer: a** - Class notes a safety-critical IDS prioritizes recall and accepts false positives, with human validation of alerts.

5. **Answer: c** - Class presents rate analysis as catching flooding and naive spoofing. It does not inspect content, so a genuine device sending false values at its normal rate (TM3) is not caught.

---

### Part 2: True/False

6. **True** - Class defines a false positive as a normal event flagged as an attack.

7. **True** - The instructor notes call for capturing normal operation, with no attacks, before building the baseline.

8. **False** - Class table says rate-matched smart spoofing is hard to detect; correlation across PGNs is proposed as a partial answer.

9. **True** - Class notes window-based detection smooths out jitter and is better for rate flooding.

10. **True** - Class suggests updating baselines weekly or after configuration changes.

11. **False** - Class lists as a limitation that frequency detection does not detect content anomalies.

12. **True** - Class states k = 2 is sensitive (more false positives), k = 3 balanced and k = 4 conservative.

13. **True** - A rate-only detector does not look at values; a genuine device sending false values at its baseline rate is TM3 and is not flagged.

14. **True** - Recall is true positives divided by true positives plus false negatives, as in the class evaluation code.

15. **False** - Even passive capture on a vessel network requires the owner's authorization; unauthorized monitoring is unethical and may be unlawful. Course work uses test networks.

---

### Part 3: Short Answer

16. **Expected Answer**:
    - The detector keys on (PGN, source address) and measures interval or rate. If the attacker uses the same identifier and the same rate, and the real sender is no longer heard, the stream seen has the baseline rate and interval statistics.
    - Nothing is added to the stream, so there is no 2x rate or ratio anomaly; the class table lists this as smart spoofing: rate equals baseline, hard to detect.
    - Possible residual signal: a brief gap or change in jitter at the moment of change, which may fall inside the tolerance band.
    - Complementary checks: content and plausibility checks, cross-sensor validation, entropy or machine-learning methods from later classes, transmitter fingerprinting (Week 12) for a substituted transmitter. Each has limits; none is guaranteed.

    **Grading**: Full credit (10 pts) for explaining that rate, identifier and interval statistics are unchanged, citing the class's smart-spoofing limit, and naming one complementary check with its limit; 8 pts for explanation without a complement; 6 pts for partial reasoning; 4 pts for stating only that the detector fails; partial credit for any correct point.

17. **Expected Answer**:
    - Precision = 40 / (40 + 10) = 0.80
    - Recall = 40 / (40 + 10) = 0.80
    - False positive rate = 10 / (10 + 940) = 0.0105 (about 1.1%)
    - Accuracy = (40 + 940) / 1000 = 0.98
    - Accuracy is high because normal traffic dominates, so it hides the missed attacks (recall is only 0.80).
    - Lowering k widens sensitivity: recall rises, false positives rise too; safety-critical use favors recall with human review of alerts.

    **Grading**: Full credit (10 pts) for four correct values plus the accuracy and k explanation; 8 pts for three correct values with explanation; 6 pts for correct formulas with arithmetic errors; 4 pts for partial calculations; partial credit for any correct step.

18. **Expected Answer**:
    - Normal: position and heading both at 10 Hz, ratio about 1.0.
    - Spoofed position added to legitimate: position about 20 Hz, heading 10 Hz, ratio about 2.0, an anomaly.
    - TM1: rate and correlation checks can catch injection that adds traffic; weaker if the attacker matches rates.
    - TM2: a substituted transmitter that matches ID and rate is not distinguished by rate alone; physical-layer fingerprinting (Week 12) is a different approach with its own limits.
    - TM3: a genuine device sending false values at its normal rate is not caught by rate checks.
    - Success against one threat model does not establish protection against the others.

    **Grading**: Full credit (10 pts) for the ratio explanation (about 1.0 versus 2.0) and correct statements for TM1, TM2 and TM3; 8 pts for ratio plus two threat models; 6 pts for ratio only; 4 pts for naming threat models without reasoning; partial credit for any correct point.

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

**Question 3 (silence):**
- Confusing the zero-rate signature with a flood
- Not linking silence to a missing legitimate sender

**Question 16 (rate-based limit):**
- Describing a 2x rate pattern rather than the same-ID, same-rate, silent-sender case
- Claiming a complementary check is guaranteed

**Question 17 (metrics):**
- Swapping precision and recall
- Computing the false positive rate with the wrong denominator
- Trusting accuracy alone

**Question 18 (threat models):**
- Claiming rate checks protect against all three threat models
- Missing that TM3 traffic is normal in rate

---

## Study Tips for Next Quiz

- Review the attack signature table and the smart-spoofing limit
- Practice computing mean, standard deviation, precision, recall and false positive rate
- Understand k selection and why recall matters for safety
- Review interval-based versus window-based detection
- Practice assigning detectors to TM1, TM2 or TM3 and stating what each cannot catch

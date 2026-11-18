---
title: "Quiz 13"
subtitle: "Ensemble Detection and Explainable AI"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 13: Ensemble Detection and Explainable AI

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

In the ensemble architectures from class, what is **stacking**?

a) Detectors vote and the majority decision wins

b) Each detector's weight is multiplied by 1.1 or 0.9 after every message

c) Detector outputs are used as inputs to a meta-model that is trained on labeled data

d) Detectors are run one after another on separate buses

---

### Question 2

In the `VotingEnsemble` strategies, which one raises an alert when at least one detector votes anomaly, and what is its expected effect?

a) `any`: more chances to detect, but more false alerts

b) `unanimous`: more chances to detect, but more false alerts

c) `majority`: no change in false alerts compared with a single detector

d) `any`: fewer false alerts, but attacks seen by only one detector are missed

---

### Question 3

According to class, when you evaluate whether an ensemble is worth using, what should you measure first?

a) F1 on the test file that contains the most attack traffic

b) Accuracy on the data used to train the detectors

c) How many detectors the ensemble contains

d) False alerts per hour on benign traffic

---

### Question 4

In the recommended `MaritimeIDSEnsemble`, the weights are frequency 0.25, entropy 0.20, ML 0.25, fingerprint 0.30, with a warning threshold of 0.5 and a critical threshold of 0.8. Frequency, entropy and ML each return a score of 1.0 and fingerprint returns 0.0. What alert level results?

a) normal

b) warning

c) critical

d) It cannot be determined without the raw frames

---

### Question 5

Which threat model does the device fingerprint detector primarily address?

a) TM2: substituted transmitter

b) TM1: modified traffic only through message rate

c) TM3: genuine device sending false values

d) All three threat models equally

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 3 points.

### Question 6

**T / F**: An ensemble is guaranteed to produce fewer false alerts than its best single detector.

---

### Question 7

**T / F**: Requiring several detectors to agree can lower false alerts but can miss an attack that only one detector sees.

---

### Question 8

**T / F**: Precision and F1 do not depend on how much attack traffic the test file contains.

---

### Question 9

**T / F**: A stacking ensemble needs labeled data to train its meta-model.

---

### Question 10

**T / F**: In the `VotingEnsemble` code, a detector that raises an exception is recorded as a vote for anomaly.

---

### Question 11

**T / F**: Adding several detectors that are very similar to each other adds as much value as adding diverse detectors.

---

### Question 12

**T / F**: A positive SHAP value means the feature pushed the anomaly score up for that prediction.

---

### Question 13

**T / F**: In `WeightedEnsemble`, the weights are normalized so that they sum to 1.

---

### Question 14

**T / F**: One stated reason for explainability is that operators must understand an alert in order to triage it.

---

### Question 15

**T / F**: A device fingerprint check can be relied on to flag a genuine, enrolled device that reports a false value (TM3).

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 16 (10 points)

A detector flags 90% of attack frames and falsely flags 5% of benign frames (hypothetical numbers). **File A** holds 100 attack frames and 900 benign frames. **File B** holds the same 100 attack frames and 9,900 benign frames.

Calculate the precision on each file. Then explain why an ensemble and its best single detector must be compared on the same test file, and why false alerts per hour on benign traffic should be reported first.

**Answer:**

\vspace{3cm}

---

### Question 17 (10 points)

A benign capture lasting 2 hours and an attack file with 6 attack events were run through four configurations (hypothetical numbers):

| Configuration | False alerts on benign capture | Attacks detected (of 6) |
|---|---|---|
| Frequency detector alone (best single detector) | 10 | 3 |
| Ensemble, majority vote | 2 | 4 |
| Ensemble, any vote | 24 | 6 |
| Ensemble, unanimous vote | 0 | 1 |

Calculate false alerts per hour for each configuration. Then state whether the majority ensemble and the any-vote ensemble each beat the best single detector, and name one caveat about drawing a conclusion from these results.

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

A detector reports that PGN 130306 from source address 35 is arriving at 30.0 Hz, while its baseline is 10.0 Hz. No other detector triggers. Assume each detector returns 1.0 when triggered and 0.0 otherwise, and use the `MaritimeIDSEnsemble` weights and thresholds from Question 4.

(a) Calculate the ensemble score and the alert level. (b) Write the one-sentence operator explanation that the frequency template would produce. (c) What does this result suggest about the recommended weights and thresholds, and how would you decide whether to change them?

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

1. **Answer: c** - Stacking feeds the outputs of the base detectors into a meta-model (logistic regression in class) that is trained on labeled normal and attack data. Voting needs no training.

2. **Answer: a** - The `any` strategy alerts if any single detector votes anomaly, which gives more chances to detect but also accumulates every detector's false alerts. Option d describes the opposite trade-off, which belongs to `unanimous`.

3. **Answer: d** - Class says an ensemble's benefit is a claim to measure, and to check benign traffic first (false alerts per hour) before looking at detection or F1. Accuracy on training data and detector count say nothing about operational alert load.

4. **Answer: b** - Score = 0.25 + 0.20 + 0.25 = 0.70, which is at least 0.5 (warning) but below 0.8 (critical). The score is a weighted sum of the individual scores, so raw frames are not needed.

5. **Answer: a** - Class lists fingerprinting as catching impersonation, and the course assigns it to TM2 (a different transmitter claiming an enrolled address). It does not address a genuine device reporting false values (TM3), and it is not a general rate detector.

---

### Part 2: True/False

6. **False** - Class says the benefit is a claim to measure, not assume. A configuration that accepts any single alert can produce more false alerts than the best single detector.

7. **True** - This is the trade-off stated in class: requiring agreement lowers false alerts, and accepting any single alert does the opposite.

8. **False** - Class notes that F1 and precision change with how much attack traffic the test file contains. The same detector looks worse on a file that is mostly benign.

9. **True** - The meta-model is fit with `train_meta_model(samples, labels)` on labeled normal and attack samples, so stacking needs labeled data.

10. **False** - On an exception the code appends a vote of 0 (and a vote of `None` in the details). The failed detector therefore counts as not voting anomaly, which means a broken detector silently stops contributing.

11. **False** - Class stresses that base detectors should be diverse. Similar detectors tend to make the same mistakes and add little.

12. **True** - Positive SHAP values increase the anomaly score for that prediction, negative values decrease it, and the magnitude shows importance.

13. **True** - The constructor divides the weights by their sum, and `update_weights` renormalizes after each adjustment.

14. **True** - Class lists trust, validation, debugging, compliance and learning as reasons, and the instructor note ties clear explanations to faster triage.

15. **False** - A fingerprint check compares a device's clock signature with its enrollment. A genuine device sending false values still has its own correct signature, so the check would not be expected to flag it; that is TM3, which needs other evidence.

---

### Part 3: Short Answer

16. **Expected Answer**:
- File A: TP = 0.9 × 100 = 90; FP = 0.05 × 900 = 45; precision = 90 / (90 + 45) = 0.667 (about 67%).
- File B: TP = 90; FP = 0.05 × 9,900 = 495; precision = 90 / (90 + 495) = 0.154 (about 15%).
- The detector did not change; only the mix of the test file did. Precision (and F1, which would be about 0.77 versus 0.26) depends on how much attack traffic the file holds.
- Compare on the same file so differences come from the configurations, not the data. Benign false alerts per hour first because it measures the alert load operators will live with and does not depend on the attack mix.

**Grading**: 3 pts for File A, 3 pts for File B (accept 0.67 and 0.15), 4 pts for explanation (2 for same-file comparison, 2 for benign false alerts per hour first). Award 2 of 3 for a correct method with an arithmetic slip.

17. **Expected Answer**:
- False alerts per hour over 2 hours: frequency alone 5.0; majority 1.0; any 12.0; unanimous 0.0.
- Majority: fewer false alerts (1.0 versus 5.0 per hour) and more attacks detected (4 versus 3 of 6), so on these numbers it beats the best single detector on both measures.
- Any: detects all 6 but at 12.0 false alerts per hour, which is 2.4 times the best single detector's rate, so it trades alert load for detection and does not simply beat it. Unanimous has no false alerts but detects only 1 of 6.
- Caveat (any one): only 6 attacks and 2 hours of benign traffic, so the differences may not hold up; one benign file and one attack file describe only those files; the weights or threshold may have been tuned on the same data; results change with attack mix.

**Grading**: 4 pts for the four rates (1 each), 4 pts for the assessment of majority and any (2 each), 2 pts for a valid caveat. Do not award credit for the claim that the ensemble is better without reference to the numbers.

18. **Expected Answer**:
- (a) Score = 0.25 × 1.0 = 0.25. This is below the 0.5 warning threshold, so the alert level is normal (no alert).
- (b) "Message rate for PGN 130306 from device 35 is 30.0 Hz, which is 3.0x higher than baseline (10.0 Hz)."
- (c) With these weights no single detector can reach 0.5 on its own (the largest weight is 0.30), so a clear rate anomaly seen by one detector raises no alert. Options are to raise weights, lower the threshold, or use an `any`-type rule for rate anomalies. The decision should be made by measuring false alerts per hour on benign traffic and detection on attack files for each choice, not by assumption.

**Grading**: 3 pts for 0.25, 2 pts for "normal", 3 pts for an accurate explanation sentence (rate, PGN, device, baseline, ratio), 2 pts for the implication and a measured approach. Give 1 of 2 on part (c) if the implication is correct but no way to evaluate the change is given.

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

**Question 16 (Test File Mix):**
- Reporting the same precision for both files because the detector is the same
- Treating false alerts as a fixed count rather than a share of benign frames
- Skipping the reason for comparing on the same file

**Question 17 (Measuring the Benefit):**
- Dividing by the number of attacks instead of by hours of benign traffic
- Declaring that any ensemble beats the best single detector without checking both false alerts and detection
- Ignoring the small sample size

**Question 18 (Weighted Score and Explanation):**
- Adding all weights (1.0) instead of only the triggered detector's weight
- Calling 0.25 a warning
- Writing an explanation without the PGN, device, baseline and ratio
- Concluding the rate detector is broken instead of examining weights and thresholds

---

## Study Tips for Next Quiz

- Practice computing weighted ensemble scores and mapping them to alert levels
- Review the three voting strategies and what each does to false alerts and missed attacks
- Be able to compute false alerts per hour and compare an ensemble with its best single detector
- Know why precision and F1 depend on the attack share of the test file
- Review which threat model each detector addresses and which it cannot address
- Review SHAP direction and magnitude and the alert explanation templates

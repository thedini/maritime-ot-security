---
title: "Quiz 11"
subtitle: "Machine Learning for Anomaly Detection"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 11: Machine Learning for Anomaly Detection

## Instructions

- Time Limit: 30 minutes
- Total Points: 100 points
- Passing Score: 70%
- Open book: No
- Collaboration: Individual work only
- Show your work for calculations
- Calculator allowed. For F1, you may use F1 = 2TP / (2TP + FP + FN)

## Part 1: Multiple Choice (40 points)

**Instructions**: Circle the best answer. Each question is worth 4 points.

### Question 1

Which training data does a One-Class SVM anomaly detector use in class?

a) Labeled examples of every attack type

b) Equal numbers of normal and attack windows

c) Normal traffic only

d) Raw timestamps with no features

---

### Question 2

In the lab, windows of CAN messages overlap and are split chronologically (first 70% for training, last 30% for testing). Why is a random shuffle of those windows into train and test sets a problem?

a) Neighboring windows share most of their messages, so near-copies of test windows end up in training and the results look better than they are

b) Random shuffling makes the scaler fail

c) Random shuffling removes all attack windows

d) Chronological order is required by scikit-learn

---

### Question 3

Which model in the class comparison table is described as capturing temporal patterns and scoring best on replay?

a) One-Class SVM

b) Random Forest

c) Isolation Forest

d) LSTM autoencoder

---

### Question 4

A trained detector uses window features (ID entropy, intervals, byte statistics) computed from bus traffic. A genuine, enrolled sensor starts reporting a false value that is plausible and within its normal range, at its normal rate. Which statement is best?

a) This is TM1, and the model should flag it because any false value is anomalous

b) This is TM3, and a traffic-feature model has little reason to flag it because the features look normal

c) This is TM2, and the model flags it because the transmitter changed

d) This is TM3, and a Random Forest will detect it because it is supervised

---

### Question 5

Detector X is run on two test sets. Its true positive rate (recall) and false positive rate are identical on both. Test set 1 is 50% attack windows; test set 2 is 10% attack windows. What happens to F1?

a) F1 is identical because recall and FPR are identical

b) F1 is higher on test set 2 because there are more normal windows

c) F1 is lower on test set 2, because precision falls when normal windows outnumber attack windows

d) F1 cannot be computed on test set 2

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 3 points.

### Question 6

**T / F**: A supervised classifier such as the class Random Forest needs labeled attack examples, while a One-Class SVM and an LSTM autoencoder are trained on normal traffic only.

---

### Question 7

**T / F**: A model that labels every window "normal" can score very high accuracy on a test set that is 99% normal windows.

---

### Question 8

**T / F**: The `normal_rate` the One-Class SVM reports on its own training data is a reliable estimate of how it will perform on new traffic.

---

### Question 9

**T / F**: In the class LSTM autoencoder, a sequence is flagged when its reconstruction error exceeds a threshold derived from errors on normal training data.

---

### Question 10

**T / F**: The feature scaler may be fit on the combined training and test data, since it only rescales values.

---

### Question 11

**T / F**: High accuracy on the lab's simulated attacks guarantees that a model will detect novel attacks on a real vessel.

---

### Question 12

**T / F**: Overlapping sliding windows from the same capture are not independent samples.

---

### Question 13

**T / F**: Recall is the fraction of actual attack windows that the detector flags.

---

### Question 14

**T / F**: Random Forest feature importances can help explain which features drive a decision and guide feature engineering.

---

### Question 15

**T / F**: The `nu` parameter of the One-Class SVM sets an upper bound on the fraction of training points treated as outliers.

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 16 (10 points)

A student builds windows of 100 messages that advance one message at a time, shuffles all windows randomly, and puts 80% in training and 20% in testing. The reported accuracy is 99%. Explain why this number overstates real performance, what the lab does instead, and give one further limit on how far the result can be trusted.

**Answer:**

\vspace{3cm}

---

### Question 17 (10 points)

A detector has a true positive rate of 90% and a false positive rate of 5%. Calculate precision, recall and F1 on (a) a test set of 500 attack windows and 500 normal windows, and (b) a test set of 100 attack windows and 900 normal windows. Explain why F1 differs and what should be reported alongside it.

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

For each threat model (TM1 modified traffic, TM2 substituted transmitter, TM3 genuine device sending false values), state whether a model trained on bus-traffic features (ID entropy, timing, byte statistics) is a suitable method, and give one reason. Then state one benefit of an unsupervised model and one cost of a supervised model.

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

1. **Answer: c** - The One-Class SVM learns a boundary around normal traffic and treats points outside it as anomalies. The Random Forest is the model that needs labeled attacks.

2. **Answer: a** - With windows of N messages advancing one message at a time, adjacent windows share most of their messages and operating conditions. A random split leaks near-duplicates of test windows into training, so measured performance (for example the false positive rate) looks better than it will on later, unseen traffic. The lab's chronological split avoids this.

3. **Answer: d** - The comparison table lists the LSTM as temporal and rates it "Excellent" for replay. The SVM and Random Forest are listed as non-temporal, and Isolation Forest is only a suggested reading.

4. **Answer: b** - A genuine device sending false values is TM3. A model that learns normal traffic features has little to react to when IDs, rates and value ranges stay normal. Supervision does not help because no attack-labeled pattern in the features exists.

5. **Answer: c** - Precision is TP / (TP + FP). With fixed TPR and FPR, fewer attack windows means fewer TP but the same FP rate over many more normal windows, so precision and F1 fall. F1 therefore cannot be compared across test sets with different attack proportions.

---

### Part 2: True/False

6. **True** - The class comparison table lists Random Forest as using labeled data and both SVM and LSTM as normal-only. The lack of labeled attacks is one of the ML challenges named in class.

7. **True** - If 99% of windows are normal, always predicting normal gives 99% accuracy and detects nothing (recall of 0). This is why recall, precision and F1 are reported and class balance is stated.

8. **False** - Performance on the training data says how well the model fits it, not how it generalizes. Evaluate on held-out traffic, split chronologically.

9. **True** - The class sets the threshold to the mean plus three standard deviations of reconstruction errors on normal training sequences and flags errors above it.

10. **False** - The scaler must be fit on training data only and then applied to the test data, as the class code does. Fitting on test data leaks information about the test distribution.

11. **False** - Results on simulated attacks show performance under the tested conditions only. Class lists overfitting and generalization to novel attacks as open challenges, and no technique is guaranteed.

12. **True** - Overlapping windows share messages and conditions, so they are highly correlated. That is the reason for splitting by time rather than by random window.

13. **True** - Recall = TP / (TP + FN), the share of real attack windows that were caught.

14. **True** - The class presents feature importance as a way to see what matters, guide feature engineering and explain decisions.

15. **True** - The class describes `nu` as an upper bound on the fraction of anomalies; in the standard formulation it bounds the fraction of training errors. It is a sensitivity control and not an expected attack rate.

---

### Part 3: Short Answer

16. **Expected Answer**:
    - Windows of 100 messages advancing by one share 99 messages with their neighbor, so after random shuffling almost every test window has near-identical copies in training. The model is partly tested on data it has effectively seen, inflating accuracy and understating the false positive rate.
    - The lab splits chronologically, for example training on the first 70% and testing on the last 30%, and does this per class so both parts contain normal and attack data; the model is tested on later traffic it has not seen.
    - Further limit (any one): attacks are simulated and may not match real ones; the data comes from one session or vessel, so results may not transfer to other days, wiring, or temperatures; normal behavior drifts over time (concept drift); the attack proportion in the test set affects precision and F1.

    **Grading**: Full credit (10 pts) for explaining the overlap and leakage mechanism, the chronological split, and one further limit; 8 pts for two of the three components fully explained; 6 pts for stating that overlap leaks information without describing the lab's remedy; 4 pts for saying only "shuffling is bad" or "overfitting"; partial credit for any correct component.

17. **Expected Answer**:
    ```
    (a) 500 attack, 500 normal:
        TP = 0.9*500 = 450, FN = 50, FP = 0.05*500 = 25
        precision = 450/(450+25) = 0.947
        recall = 450/500 = 0.90
        F1 = 2*450 / (2*450 + 25 + 50) = 900/975 = 0.923

    (b) 100 attack, 900 normal:
        TP = 90, FN = 10, FP = 0.05*900 = 45
        precision = 90/(90+45) = 0.667
        recall = 90/100 = 0.90
        F1 = 2*90 / (2*90 + 45 + 10) = 180/235 = 0.766
    ```
    - The detector is identical in both cases, but F1 falls from about 0.92 to about 0.77 because the same false positive rate is applied to many more normal windows, which lowers precision.
    - Report recall, false positive rate, and precision with the confusion matrix counts and the number of attack and normal windows in the test set, so results can be compared fairly.

    **Grading**: Full credit (10 pts) for correct calculations in both cases and the explanation of precision depending on the attack share; 8 pts for correct calculations with a weak explanation, or one small arithmetic error; 6 pts for correct method with errors in both parts; 4 pts for definitions of precision and recall only; partial credit for any correct step.

18. **Expected Answer**:
    - TM1 (modified traffic): suitable. Floods, injection and replay change timing, ID mix or byte statistics that the features capture. Coverage is not guaranteed, and attacks designed to look normal can pass.
    - TM2 (substituted transmitter): not suitable on its own. A substitute that sends the same IDs, content and rates produces similar window features. Telling transmitters apart needs a different measurement (Class 12), and it also has to be tested.
    - TM3 (genuine device, false values): not suitable. IDs, rates and ranges look normal, so the features have nothing to separate it; it needs an independent reference.
    - Unsupervised benefit (any): needs no attack labels (labeled attacks are scarce); can flag novel patterns.
    - Supervised cost (any): needs labeled attack data; may only recognize attack types it was trained on; may overfit the simulated attacks.

    **Grading**: Full credit (10 pts) for justified verdicts on all three threat models plus one benefit and one cost; 8 pts for all verdicts with thin justification or a missing benefit or cost; 6 pts for two threat models correct with reasons; 4 pts for TM1 only; partial credit for any correct component. Deduct for claims of guaranteed or complete detection.

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

**Question 16 (Evaluation Leakage):**
- Saying random shuffling is wrong only because "data is time-ordered", without mentioning shared messages between overlapping windows
- Proposing a larger test set as the fix, which does not remove the leakage
- Offering no remedy such as a chronological split

**Question 17 (F1 and Attack Share):**
- Applying the false positive rate to the attack count instead of the normal count
- Concluding that the detector got worse between the two test sets
- Reporting accuracy alone, or F1 with no counts of attack and normal windows

**Question 18 (Threat Models and Learning Type):**
- Treating a high-accuracy model as protection against all three threat models
- Claiming supervised models detect attack types they never saw
- Confusing unsupervised models (normal-only training) with unlabeled attack detection that needs no baseline

**Instructor note on class material:** The Class 11 `RandomForestDetector.train` example uses `train_test_split(..., random_state=42)`, which shuffles by default. The lab uses a chronological split, so students may notice the conflict. Question 2 and Question 16 follow the lab. The class also refers to an "OpenPlotter baseline" while the course now uses NEMO traffic.

---

## Study Tips for Next Quiz

- Contrast supervised, unsupervised and sequence models, and what each needs for training
- Practice computing precision, recall and F1 from confusion matrix counts
- Know how the proportion of attack windows changes precision and F1
- Explain why overlapping windows need a chronological or block split
- For each method, name the threat model it addresses and the ones it cannot
- Review how fingerprinting asks a different question: is this the same physical device (Class 12)

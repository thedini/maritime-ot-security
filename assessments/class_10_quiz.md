---
title: "Quiz 10"
subtitle: "Entropy-Based Anomaly Detection"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 10: Entropy-Based Anomaly Detection

## Instructions

- Time Limit: 30 minutes
- Total Points: 100 points
- Passing Score: 70%
- Open book: No
- Collaboration: Individual work only
- Show your work for calculations
- Calculator allowed; log base 2 values are given where needed (log2(2) = 1, log2(4) = 2, log2(8) = 3)

## Part 1: Multiple Choice (40 points)

**Instructions**: Circle the best answer. Each question is worth 4 points.

### Question 1

What is the Shannon entropy of a fair coin flip (p(H) = p(T) = 0.5)?

a) 0.5 bits

b) 1 bit

c) 2 bits

d) 0 bits

---

### Question 2

During a flooding denial-of-service attack, a single CAN ID dominates the bus. What happens to the CAN ID entropy of a sliding window?

a) It rises sharply because the bus is busier

b) It stays the same because the set of IDs is unchanged

c) It becomes undefined

d) It drops toward 0 bits

---

### Question 3

According to the class comparison of frequency and entropy detection, which kind of attack is entropy detection most likely to miss?

a) An attack that keeps the ID distribution and message rate close to normal

b) A flood in which one ID dominates the window

c) A burst of many previously unseen IDs

d) A replay that repeats identical payload bytes over and over

---

### Question 4

A genuine heading sensor, still wired to the bus under its own source address, begins reporting a false heading. It keeps its normal message rate and its normal CAN ID. Which threat model is this, and would CAN ID entropy be expected to flag it?

a) TM1 (modified traffic); yes, the ID distribution changes

b) TM2 (substituted transmitter); yes, a new device means new IDs

c) TM3 (genuine device, false values); no, the traffic distribution is unchanged

d) TM3 (genuine device, false values); yes, false values always change entropy

---

### Question 5

A detector reports normalized entropy of 1.0 for a window, where entropy is divided by log2 of the number of active IDs on the network. What does this mean?

a) One ID is sending all of the messages

b) Traffic is spread evenly across the active IDs

c) The window contains no messages

d) The IDs are 29 bits long

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 3 points.

### Question 6

**T / F**: A stream containing only one distinct symbol has an entropy of 0 bits.

---

### Question 7

**T / F**: For a window with n distinct symbols, the maximum possible entropy is log2(n), reached when all symbols are equally likely.

---

### Question 8

**T / F**: Frequency-based detection and entropy-based detection always catch exactly the same attacks.

---

### Question 9

**T / F**: A biased coin with p(H) = 0.9 has lower entropy than a fair coin because its outcome is more predictable.

---

### Question 10

**T / F**: An entropy baseline should be built from traffic that includes attacks, so the detector learns what attacks look like.

---

### Question 11

**T / F**: CAN ID entropy alone is well suited to detecting manipulation of payload bytes when the message IDs are unchanged.

---

### Question 12

**T / F**: In the class example, replayed data produced lower and more stable data-byte entropy than live sensor data.

---

### Question 13

**T / F**: If an injected stream preserves the normal ID distribution, the entropy detector will necessarily raise an alert.

---

### Question 14

**T / F**: The sliding-window detector in class does not compute entropy until the window has filled to the configured window size.

---

### Question 15

**T / F**: Injecting a spoofed message under a new ID at a modest rate can cause only a slight change in ID entropy, which may be hard to separate from normal variation.

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 16 (10 points)

Calculate by hand the Shannon entropy, in bits, of each symbol sequence below. Show your work, then state in one sentence what the three results tell you about predictability.

- [A, A, A, A]
- [A, B, A, B]
- [A, B, C, D]

**Answer:**

\vspace{3cm}

---

### Question 17 (10 points)

Explain why a DoS flood lowers CAN ID entropy, and describe one kind of traffic change that a CAN ID entropy detector could miss. Then, for each of the three threat models (TM1 modified traffic, TM2 substituted transmitter, TM3 genuine device sending false values), state whether CAN ID entropy monitoring is a suitable method and why.

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

A window of 8 messages contains four distinct CAN IDs with counts 4, 2, 1, and 1. Calculate (a) the entropy of the window and (b) the normalized entropy using log2 of the number of distinct IDs. Then, if the baseline entropy is 1.75 bits and the detector alerts when entropy falls more than 30% below baseline, would a 100-message window containing a single ID raise an alert? Show the deviation calculation.

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

1. **Answer: b** - H = -0.5 log2(0.5) - 0.5 log2(0.5) = 0.5 + 0.5 = 1 bit. A fair two-outcome source is the standard one-bit example from class.

2. **Answer: d** - When one ID is all of the traffic, p = 1 and log2(1) = 0, so entropy is 0 bits. The class DoS example shows 0.00 bits against a normal baseline above zero.

3. **Answer: a** - The class table lists "rate-matched attacks" as what entropy misses, and the instructor notes add that entropy can stay the same if the attack matches the distribution. Options b, c and d are the cases entropy is described as catching.

4. **Answer: c** - A legitimate device reporting false values is TM3. The IDs, sources and rates are unchanged, so an ID distribution does not move; detecting it needs a different kind of evidence, such as an independent reference.

5. **Answer: b** - Normalized entropy divides raw entropy by log2 of the number of active IDs, so 0 means a single ID and 1 means perfectly balanced traffic across the active IDs.

---

### Part 2: True/False

6. **True** - With one symbol p = 1 and log2(1) = 0, so entropy is the minimum of 0 bits (completely predictable).

7. **True** - Entropy is bounded above by log2(n) for n distinct values, reached with a uniform distribution. This is the basis for normalizing entropy.

8. **False** - The class table shows frequency detection catches rate changes and misses content changes, while entropy catches distribution changes. They are complementary, and the performance table shows they differ on replay.

9. **True** - The class computes 0.47 bits for p(H) = 0.9 against 1 bit for a fair coin. Lower entropy means more predictable.

10. **False** - The baseline is built from normal traffic with no attacks. Including attacks would teach the detector to treat attack traffic as normal and would distort the mean and standard deviation.

11. **False** - CAN ID entropy misses payload manipulation that reuses existing IDs. This is the motivation for data byte entropy and per-PGN data entropy.

12. **True** - The replay example shows data entropy dropping (about 4.2 bits against 5.0 plus or minus 0.5) and stabilizing. The lowered variation is the signature, though the class calls replay detection "tricky".

13. **False** - An injection that preserves the distribution can leave entropy unchanged, which is a known limitation noted in class (discussion question 2). Entropy is one signal and does not guarantee detection.

14. **True** - `calculate_window_entropy` returns None and `process_message` returns no alert until the buffer holds `window_size` messages. Early messages therefore go unevaluated.

15. **True** - The class spoofing example shows only a slight increase (about 2.3 to 2.4 bits) and labels the signature "may be subtle". Thresholds that are too tight produce false alarms, and thresholds that are too loose miss it.

---

### Part 3: Short Answer

16. **Expected Answer**:
    ```
    [A,A,A,A]: p(A)=1                      H = -1*log2(1)           = 0 bits
    [A,B,A,B]: p(A)=p(B)=0.5               H = 0.5 + 0.5            = 1 bit
    [A,B,C,D]: p = 0.25 each               H = 4 * (0.25 * 2)       = 2 bits
    ```
    - More variety and a flatter distribution give higher entropy; fully repeated data is perfectly predictable (0 bits).
    - The third value equals log2(4), the maximum for four symbols.

    **Grading**: Full credit (10 pts) for three correct values with work and a correct predictability statement; 8 pts for correct values with a weak or missing interpretation; 6 pts for two correct values or a sign or log error; 4 pts for correct formula with calculation errors; partial credit for any correct component.

17. **Expected Answer**:
    - A flood makes one ID dominate, so its probability approaches 1 and entropy approaches 0; the diversity of normal traffic disappears.
    - Missed: an injected or replayed stream that keeps the ID distribution (and rate) near normal; also payload changes under existing IDs when only ID entropy is measured. A subtle new ID at low rate may stay inside normal variation.
    - TM1 (modified traffic): suitable for floods and some injection or replay that shift the distribution. It is not guaranteed, because rate-matched traffic can evade it.
    - TM2 (substituted transmitter): not suitable on its own. If the substitute claims an enrolled source address and sends the same IDs at the same rates, the ID distribution is essentially unchanged; this is the subject of fingerprinting in Class 12.
    - TM3 (genuine device, false values): not suitable. The device's IDs and rates are normal, so ID entropy does not change. Data byte entropy may shift in some cases, but there is no guarantee.

    **Grading**: Full credit (10 pts) for the DoS explanation, one valid miss case, and a justified verdict for all three threat models; 8 pts for all components with thin justification; 6 pts for the DoS explanation plus threat models without reasons; 4 pts for the DoS explanation only; partial credit for any correct component. Deduct for claims that entropy fully protects against any threat model.

18. **Expected Answer**:
    ```
    p = 4/8, 2/8, 1/8, 1/8 = 0.5, 0.25, 0.125, 0.125
    (a) H = 0.5*1 + 0.25*2 + 0.125*3 + 0.125*3
          = 0.5 + 0.5 + 0.375 + 0.375 = 1.75 bits
    (b) Normalized = 1.75 / log2(4) = 1.75 / 2 = 0.875

    Single-ID window: H = 0 bits
    deviation = (0 - 1.75) / 1.75 = -1.0 (-100%)
    -1.0 < -0.3, so a LOW_ENTROPY alert is raised.
    ```

    **Grading**: Full credit (10 pts) for correct entropy, normalized value, deviation and alert decision; 8 pts for one minor arithmetic error; 6 pts for correct method with errors in two parts; 4 pts for correct formula only; partial credit for any correct step.

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

**Question 16 (Hand Entropy):**
- Forgetting the minus sign, giving a negative entropy
- Using natural log instead of log base 2
- Treating [A, B, A, B] as 2 bits because it has two symbols

**Question 17 (Entropy and Threat Models):**
- Saying entropy detects any attack that "looks different", without noting rate-matched traffic can pass
- Assuming a detector built for modified traffic also covers a substituted transmitter or a genuine device sending false values
- Confusing entropy dropping (flood) with entropy rising (new IDs)

**Question 18 (Window Entropy and Alerting):**
- Dividing by log2 of the wrong count when normalizing
- Using the raw drop (1.75 bits) rather than the ratio when comparing to the 30% threshold
- Forgetting that p = 1 gives log2(1) = 0, so the entropy is exactly 0

**Instructor note on class material:** The Class 10 expected output for the CAN ID example shows `Normal entropy: 1.92 bits`, but the six IDs in that list (counts 3, 2 and 1) give about 1.46 bits, and three distinct IDs cannot exceed log2(3), about 1.58 bits. Question 18 uses a verified calculation. Consider correcting the class file before students check the printed output.

---

## Study Tips for Next Quiz

- Practice computing entropy by hand for small counts
- Know the entropy range: 0 to log2(n)
- Be able to say what entropy catches and what it misses, and why
- For every detector, ask which threat model it addresses and which it cannot
- Review how a training set of ML features (including entropy features) is built from windows
- Think about how overlapping windows and chronological ordering affect evaluation

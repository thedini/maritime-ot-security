---
title: "Quiz 12"
subtitle: "Device Fingerprinting and Authentication"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 12: Device Fingerprinting and Authentication

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

A CAN controller has a nominal clock of 16.000000 MHz and an actual clock of 16.000800 MHz. Using skew = (actual - nominal) / nominal, what is the skew?

a) +5 ppm

b) +500 ppm

c) +50 ppm

d) +800 ppm

---

### Question 2

Which threat model does device fingerprinting in Class 12 address?

a) TM1, modified traffic, because it detects any injected message

b) TM3, a genuine device sending false values, because its clock is different when it lies

c) None of them, because fingerprints cannot be measured on a CAN bus

d) TM2, a substituted transmitter claiming an enrolled source address

---

### Question 3

A classifier separates the captures of Device A from Device B. Which conclusion is best supported by that result alone?

a) The classifier distinguished these two devices under the conditions of this test

b) Each device has a unique identity that no other device can reproduce

c) The classifier can identify any device on any vessel

d) The transmitter hardware is the cause of the difference

---

### Question 4

A student captured one long recording from each device and randomly assigned frames from each recording to train and test sets. What is the main flaw?

a) Too many frames were used for training

b) Frames from the same recording are not independent, so whole sessions should be held out for testing

c) CAN frames cannot be labeled by source address

d) Fingerprinting requires at least 1000 devices

---

### Question 5

Which control best tests whether a classifier is separating devices by message content instead of by transmitter?

a) Run the classifier with a larger number of trees

b) Collect more frames at the same temperature

c) Have both devices send the same message content and check whether the separation remains

d) Increase the match threshold

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 3 points.

### Question 6

**T / F**: A classifier can separate two devices because they are different models or run different firmware, which shows class-level difference rather than device identity.

---

### Question 7

**T / F**: Clock skew can move with temperature and supply voltage, and can differ between power-ups and sessions.

---

### Question 8

**T / F**: A device that answers a request has thereby been fingerprinted.

---

### Question 9

**T / F**: Random frames from a single recording are a sound way to build train and test sets for a fingerprinting experiment.

---

### Question 10

**T / F**: In the class fingerprint table, the set of PGNs a device sends is expected to be a weak discriminator.

---

### Question 11

**T / F**: A fingerprint of the transmitter hardware helps detect a genuine, enrolled device that reports a false value.

---

### Question 12

**T / F**: If a device does not support a documented stimulus used by an active method, the result should be reported as unsupported rather than forced.

---

### Question 13

**T / F**: A fingerprint match threshold that works on the bench guarantees detection of any impersonation on a vessel.

---

### Question 14

**T / F**: A classifier can learn wiring, loading or probe position rather than the device, so a changed wiring or probe position is a useful control.

---

### Question 15

**T / F**: A device must be enrolled before it can be protected by a fingerprint database.

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 16 (10 points)

A student reports that a classifier separates two devices with 99% accuracy and concludes that it has identified each physical device. Name three confounders that could explain the separation without identifying the transmitter hardware, and describe the test design (holding out data and controls) that would show whether the result is more than that.

**Answer:**

\vspace{3cm}

---

### Question 17 (10 points)

A periodic message is expected every 0.100000 s. Over 1000 messages, a regression of arrival time against message count gives a mean interval of 0.100005 s. (a) Using skew = (measured interval - expected interval) / expected interval, calculate the skew in ppm. (b) Another device measures 47 ppm. Give two reasons the two devices may not be separable using skew alone. (c) The arrival times were stamped by the receiver's own clock. What does that imply about what is being measured?

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

A classmate says: "An attacker who spoofs a source address cannot reproduce the real device's clock, so skew fingerprinting is unspoofable." Evaluate this claim. In your answer, state which threat model fingerprinting addresses and one it cannot, and describe what evidence would show how well a fingerprint resists imitation.

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

1. **Answer: c** - The difference is 0.0008 MHz on a 16 MHz nominal, which is 5 x 10^-5, or +50 ppm. This is the example worked in class.

2. **Answer: d** - Class 12 addresses the substituted transmitter threat model: a different transmitter claims an enrolled source address. It does not address a genuine device reporting false values, because that device's physical fingerprint is unchanged.

3. **Answer: a** - The class instructs that the claim stay at "distinguished these devices in this test". Differences in model, firmware, content or wiring can produce the same separation, so a single result does not show uniqueness, hardware cause or generality.

4. **Answer: b** - Frames within one recording are not independent, so random splitting leaks near-identical frames into the test set. The class says to hold out whole capture sessions or blocks.

5. **Answer: c** - The class lists "the same message content from both devices" as a control. If separation persists, content is less likely to be the driver; if it vanishes, content was the driver.

---

### Part 2: True/False

6. **True** - The class warns that a classifier can separate devices by model, firmware, message content, or wiring and loading. Separating two different models says nothing about telling two units of the same model apart.

7. **True** - The class states that skew moves with temperature and supply voltage, can change between power-ups and sessions, and that two devices can overlap. It recommends repeated measurement across days, warm and cold starts, and different wiring or load.

8. **False** - The class says a device that answers a request is not thereby fingerprinted. Active methods need a documented stimulus that every tested device supports.

9. **False** - Frames from one recording are not independent, so random splitting overstates accuracy. Hold out whole sessions or blocks.

10. **True** - The component table lists PGN set as low discriminating power, and the instructor notes call it weak and easily imitated. It adds little beyond other features.

11. **False** - The class states fingerprinting does not address a genuine device that reports false values, because its physical fingerprint is unchanged. That is TM3.

12. **True** - The class directs reporting devices that do not answer as unsupported rather than forcing a result, so failures and gaps stay visible.

13. **False** - A threshold tuned on one bench says nothing about other days, temperatures, wiring or vessels. The class asks for failures and untested conditions to be reported and gives no guarantee.

14. **True** - The class lists wiring and loading as confounders and includes "a changed wiring or probe position" among the controls. It also suggests excluding identifiers and payload from the features, or showing they do not drive the result.

15. **True** - The class notes the method requires a learning phase and that new devices must be enrolled before protection. Device replacement needs its own handling.

---

### Part 3: Short Answer

16. **Expected Answer**:
    - Confounders (any three): message content or payload and identifiers; wiring, loading, cable length or probe position; temperature or supply voltage; capture session or day; different model or firmware rather than different units.
    - Hold out whole sessions or blocks for testing rather than random frames from the same recording, and test on a session recorded on another day or after a power cycle.
    - Controls: have both devices send the same message content; test same-family devices (the same model); change the wiring or probe position; exclude identifiers and payload from the features or show they do not drive the result.
    - Report failures and what was not tested (other temperatures, days, vessels). Conclude only what was shown.

    **Grading**: Full credit (10 pts) for three valid confounders, held-out sessions, and at least two controls; 8 pts for three confounders and either held-out sessions or controls; 6 pts for two confounders with a partial test design; 4 pts for recognizing the result is not proof but giving no specifics; partial credit for any correct component. Deduct for statements that the result proves identity.

17. **Expected Answer**:
    ```
    (a) skew = (0.100005 - 0.100000) / 0.100000
            = 0.000005 / 0.1 = 5 x 10^-5 = 50 ppm
    ```
    - (b) 50 ppm and 47 ppm differ by 3 ppm, which is small compared with variation from temperature, supply voltage, jitter, and different power-ups. Two devices can overlap. The estimate has its own uncertainty with a finite number of samples.
    - (c) The measured skew is relative: the difference between the transmitter's clock and the receiver's clock. The receiver's own skew and drift are part of the result, so the measurement must be repeated and the receiver held constant.

    **Grading**: Full credit (10 pts) for correct 50 ppm calculation, two valid reasons, and the relative-measurement point; 8 pts for two of the three parts fully correct and the third partly; 6 pts for a correct calculation and one other component; 4 pts for correct formula with calculation errors; partial credit for any correct step.

18. **Expected Answer**:
    - The claim is too strong. The class says an attacker spoofing a source address does not automatically reproduce the physical differences, and that whether a measurement separates two transmitters depends on the bench, message content, wiring and enrollment data. It does not say imitation is impossible, and discussion question 4 asks whether a sophisticated attacker could defeat fingerprinting.
    - Addressed: TM2 (substituted transmitter claiming an enrolled source address). Not addressed: TM3 (genuine device sending false values), because the device's fingerprint is unchanged. TM1 floods or replay on the bus are not what skew measures.
    - Evidence: tests with held-out sessions, same-model devices and same-content controls; repeated measurements over days and temperatures; and an explicit test of attempts to imitate the enrolled device's timing, reporting detection and miss rates and what was not tested. This is a statement about measured results under stated conditions, not a proof.

    **Grading**: Full credit (10 pts) for rejecting the "unspoofable" claim with a reasoned argument, correct threat model addressed and not addressed, and a description of evidence; 8 pts for two of the three components with good reasoning; 6 pts for rejecting the claim without detail, or correct threat models only; 4 pts for partial reasoning; partial credit for any correct component. Deduct for any claim that a technique is guaranteed or unique.

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

**Question 16 (Confounders and Test Design):**
- Treating high accuracy as proof of device identity
- Splitting random frames from one recording and calling it held out
- Listing confounders without explaining how a control would test each one
- Forgetting that two different models differ for reasons other than the transmitter hardware

**Question 17 (Skew Calculation):**
- Mixing up ppm with percent, or dropping the 10^6 factor
- Treating the 3 ppm difference as clearly separable without considering drift and noise
- Forgetting that the receiver's clock is the reference

**Question 18 (Evaluating the Unspoofable Claim):**
- Repeating the claim that the clock "cannot be spoofed"
- Saying fingerprinting stops a genuine device sending false values
- Not naming the evidence that would support or weaken a claim

**Instructor note on class material:** The Class 12 instructor notes after the "Detecting Impersonation" section still say the attacker "CANNOT spoof their hardware clock" and call clock skew "hard to spoof", and the behavioral notes repeat "hard to spoof". These conflict with the rewritten body text. This quiz follows the body text.

---

## Study Tips for Next Quiz

- Be able to say the difference between class-level difference and device identity
- Know the confounders: message content, wiring and loading, temperature, session
- Explain why whole sessions are held out and what each control tests
- Practice skew calculations in ppm and explain why the measurement is relative
- For each method, name the threat model it addresses and the ones it cannot
- Review how methods are combined and the limits of each

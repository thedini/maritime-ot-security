---
title: "Quiz 01"
subtitle: "CAN Bus Protocol Deep Dive"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 01: CAN Bus Protocol Deep Dive

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

What is the maximum number of data bytes that can be transmitted in a Classical CAN frame?

a) 4 bytes

b) 8 bytes

c) 16 bytes

d) 64 bytes

---

### Question 2

In CAN arbitration, which message ID has the highest priority?

a) 0x000 (lowest numerical value)

b) 0x7FF (highest numerical value)

c) 0x400 (middle value)

d) Priority is random and not determined by ID

---

### Question 3

What type of signaling does CAN use on the physical layer?

a) Single-ended signaling with one wire

b) Differential signaling with CAN_H and CAN_L

c) Wireless radio frequency transmission

d) Optical fiber transmission

---

### Question 4

What does a "dominant" bit represent in CAN bus communication?

a) Binary 1 (recessive state)

b) Binary 0 (dominant state)

c) No signal present

d) Error condition

---

### Question 5

Which field in the CAN frame is used for error detection but NOT for security?

a) CRC (Cyclic Redundancy Check)

b) ACK (Acknowledgment)

c) SOF (Start of Frame)

d) EOF (End of Frame)

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 3 points.

### Question 6

**T / F**: CAN protocol was designed with built-in authentication mechanisms to prevent unauthorized message injection.

---

### Question 7

**T / F**: In CAN arbitration, a node that loses arbitration immediately stops transmitting and retries later when the bus is idle.

---

### Question 8

**T / F**: NMEA 2000 uses the Standard CAN frame format with 11-bit identifiers.

---

### Question 9

**T / F**: CAN-FD (Flexible Data-rate) addresses the security vulnerabilities present in Classical CAN.

---

### Question 10

**T / F**: All nodes on a CAN bus receive all messages transmitted on the network.

---

### Question 11

**T / F**: The termination resistors on a CAN bus should be 120 ohms at each end of the network.

---

### Question 12

**T / F**: An attacker can perform a Denial of Service (DoS) attack by flooding the CAN bus with high-priority messages (low ID values).

---

### Question 13

**T / F**: The RTR (Remote Transmission Request) bit is commonly used in modern CAN implementations.

---

### Question 14

**T / F**: When a CAN node's Transmit Error Counter (TEC) exceeds 255, the node enters Bus-Off state and isolates itself from the network.

---

### Question 15

**T / F**: CAN messages include timestamps to prevent replay attacks.

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 16 (10 points)

Explain why CAN protocol has no built-in authentication or encryption. What was the original design assumption that made security less of a concern when CAN was developed in 1986?

**Answer:**

\vspace{3cm}

---

### Question 17 (10 points)

Two CAN nodes attempt to transmit simultaneously. Node A sends ID 0x120 and Node B sends ID 0x220. At which bit position does Node B lose arbitration, and why? Show your work by converting the IDs to binary.

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

List three specific attack types that can be performed against CAN networks and briefly describe the impact of each attack on a maritime vessel.

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

1. **Answer: b** - Classical CAN frames can carry up to 8 data bytes (0-8 bytes). CAN-FD can carry up to 64 bytes, but the question asks about Classical CAN.

2. **Answer: a** - In CAN arbitration, lower numerical ID values have higher priority. 0x000 would have the highest priority (though this ID is often reserved).

3. **Answer: b** - CAN uses differential signaling with two wires: CAN_H and CAN_L. This provides noise immunity since noise affects both wires equally.

4. **Answer: b** - A dominant bit represents binary 0 and is created when CAN_H is at 3.5V and CAN_L is at 1.5V (differential voltage of 2V). Dominant always wins over recessive.

5. **Answer: a** - The CRC field provides error detection through a cyclic redundancy check, but it does NOT provide security authentication or message integrity protection against malicious actors.

---

### Part 2: True/False

6. **False** - CAN protocol has NO built-in authentication mechanisms. Security was not a design consideration in 1986 when CAN was developed.

7. **True** - This is the fundamental mechanism of CAN arbitration. When a node transmits recessive (1) but reads dominant (0), it immediately stops and waits to retry.

8. **False** - NMEA 2000 uses Extended CAN frame format with 29-bit identifiers, not the Standard 11-bit format.

9. **False** - CAN-FD improves data throughput and efficiency but does NOT address security vulnerabilities. It has the same security weaknesses as Classical CAN.

10. **True** - CAN is a broadcast network. All nodes receive all messages, which enables eavesdropping but also allows for flexible system design.

11. **True** - Proper CAN bus termination requires 120Ω resistors at each end of the bus, resulting in a total bus impedance of 60Ω.

12. **True** - Since lower IDs have higher priority, an attacker can starve legitimate messages by flooding with high-priority (low ID) messages, causing a DoS condition.

13. **False** - RTR is rarely used in modern implementations. Most CAN communication is periodic broadcasting rather than request-response.

14. **True** - The Bus-Off state is part of CAN's error handling. When TEC > 255, the node must disconnect to prevent further errors. This can be exploited in a Bus-Off attack.

15. **False** - CAN frames do NOT include timestamps. There is no built-in mechanism for message freshness, making replay attacks possible.

---

### Part 3: Short Answer

16. **Expected Answer**:
    - CAN was designed in 1986 for automotive applications
    - Original assumption: vehicles were isolated, closed systems with no external connectivity
    - All nodes on the network were assumed to be trusted
    - Focus was on reliability and real-time performance in harsh environments, not security
    - Security through obscurity (proprietary implementations)

    **Grading**: Full credit (10 pts) for mentioning isolation assumption and trusted environment; 7-8 pts for discussing design era; 5-6 pts for mentioning reliability focus; partial credit for any relevant points.

17. **Expected Answer**:
    - Node A: 0x120 = 0001 0010 0000 (binary)
    - Node B: 0x220 = 0010 0010 0000 (binary)
    - At bit position 9 (counting from bit 10 down to 0), Node B transmits 1 (recessive) but Node A transmits 0 (dominant)
    - Node B reads 0 on the bus, realizes it lost arbitration, and stops transmitting
    - Node A wins and continues unaware of the collision

    **Grading**: Full credit (10 pts) for correct binary conversion and identifying bit 9; 7-8 pts for correct concept but minor error; 5-6 pts for understanding arbitration but calculation error; partial credit for attempt.

18. **Expected Answer** (any three attacks):
    - **Eavesdropping**: Passive listening to all CAN traffic; attacker gains sensitive information about vessel position, speed, cargo, engine status
    - **Spoofing**: Injecting fake messages; attacker can send false navigation data, engine commands, or environmental readings, potentially causing unsafe conditions
    - **DoS (Flooding)**: Overwhelming bus with high-priority traffic; legitimate messages are blocked, causing loss of critical communications between systems
    - **DoS (Bus-Off)**: Forcing a specific node into Bus-Off state; can disable safety-critical systems like fire suppression or steering
    - **Replay Attack**: Retransmitting captured messages; attacker can repeat commands like "open cargo hatch" or navigation waypoint changes
    - **Fuzzing**: Injecting random or malformed messages; can cause unpredictable behavior, system crashes, or reveal vulnerabilities

    **Grading**: Full credit (10 pts) for three distinct attacks with maritime-specific impacts; 7-8 pts for three attacks with generic impacts; 5-6 pts for two attacks described well; partial credit for one attack or descriptions lacking detail.

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

---
title: "Quiz 02"
subtitle: "NMEA 2000 Protocol and PGN Structure"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 02: NMEA 2000 Protocol and PGN Structure

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

What is the standard bitrate for NMEA 2000 networks?

a) 125 kbps

b) 250 kbps

c) 500 kbps

d) 1 Mbps

---

### Question 2

NMEA 2000 is based on which automotive/industrial standard?

a) SAE J1939

b) ISO 9141

c) OBD-II

d) MOST

---

### Question 3

In NMEA 2000, what is a PGN?

a) Priority Group Number

b) Parameter Group Number

c) Protocol Gateway Node

d) Packet Generation Number

---

### Question 4

How many bits are in an NMEA 2000 Extended CAN identifier?

a) 8 bits

b) 11 bits

c) 29 bits

d) 32 bits

---

### Question 5

Which PGN provides vessel heading information?

a) 127250

b) 129025

c) 130306

d) 127488

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 3 points.

### Question 6

**T / F**: NMEA 2000 uses the same physical layer as automotive CAN but with marine-specific message types.

---

### Question 7

**T / F**: In NMEA 2000, the PGN is always equal to bits 8-25 of the CAN ID.

---

### Question 8

**T / F**: PGN 126996 (Product Information) reveals device manufacturer, model, software version, and serial number.

---

### Question 9

**T / F**: Fast Packet protocol allows NMEA 2000 messages to exceed the 8-byte limit of standard CAN frames.

---

### Question 10

**T / F**: NMEA 2000 device addresses are permanently assigned by the manufacturer and cannot be changed.

---

### Question 11

**T / F**: In PDU1 format (PF < 240), the PS field represents a destination address for peer-to-peer communication.

---

### Question 12

**T / F**: The "Rapid Update" PGNs (like position and heading) are transmitted at 10 Hz update rate.

---

### Question 13

**T / F**: NMEA 2000 includes built-in encryption to protect sensitive navigation data.

---

### Question 14

**T / F**: Multi-byte values in NMEA 2000 PGN data fields are encoded in little-endian format.

---

### Question 15

**T / F**: The Industry Group field value of 4 in the NAME structure indicates marine industry.

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 16 (10 points)

Decode the following CAN ID to extract the PGN and source address. Show your work.

**CAN ID: 0x09F80205**

Calculate:
- Priority
- PDU Format (PF)
- PDU Specific (PS)
- Source Address (SA)
- PGN

**Answer:**

\vspace{3cm}

---

### Question 17 (10 points)

Explain what information an attacker could gather by monitoring PGN 126996 (Product Information) on a vessel's NMEA 2000 network. Why is this information valuable during the reconnaissance phase of an attack?

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

Given the raw heading data `0x7C 0x22` from PGN 127250, calculate the heading in degrees. The format is: unsigned 16-bit value, resolution = 0.0001 radians, little-endian. Show your calculation steps.

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

1. **Answer: b** - NMEA 2000 networks operate at 250 kbps, the same bitrate as SAE J1939. This provides adequate bandwidth for maritime applications while maintaining reliability.

2. **Answer: a** - NMEA 2000 is built on the SAE J1939 standard used in heavy-duty trucks and buses. It uses the same protocol layers but with marine-specific PGNs.

3. **Answer: b** - PGN stands for Parameter Group Number. It identifies the type of data being transmitted (e.g., position, heading, engine RPM).

4. **Answer: c** - NMEA 2000 uses Extended CAN format with 29-bit identifiers, which allows encoding of priority, PGN, and source address within the ID.

5. **Answer: a** - PGN 127250 is "Vessel Heading" and provides heading sensor data. PGN 129025 is position, 130306 is wind data, and 127488 is engine parameters.

---

### Part 2: True/False

6. **True** - NMEA 2000 uses CAN 2.0B (Extended) physical layer at 250 kbps. The difference is in the higher-layer protocol and message definitions specific to marine applications.

7. **False** - The PGN calculation depends on the PDU Format value. If PF < 240 (PDU1), PGN does not include the PS field. If PF >= 240 (PDU2), PGN includes PS as a group extension.

8. **True** - PGN 126996 broadcasts device identification including NMEA version, product code, model ID, software version, model version, serial number, and certification level. This is reconnaissance gold for attackers.

9. **True** - Fast Packet protocol allows messages up to 223 bytes by fragmenting data across multiple CAN frames. The first frame includes sequence counter and total length.

10. **False** - NMEA 2000 uses dynamic address assignment through the Address Claim process (PGN 60928). Devices claim addresses based on their NAME, and conflicts are resolved by priority.

11. **True** - In PDU1 format (when PF < 240), the PS field serves as the destination address, allowing peer-to-peer communication rather than broadcast.

12. **True** - Navigation PGNs labeled "Rapid Update" (position, heading, COG/SOG) are transmitted at 10 Hz to provide timely data for navigation systems. These high-frequency messages are prime targets for attacks.

13. **False** - NMEA 2000 has NO built-in encryption. All data is transmitted in plaintext, making eavesdropping trivial for anyone with access to the network.

14. **True** - Multi-byte values in PGN data fields use little-endian byte order (least significant byte first), which is standard for CAN-based protocols.

15. **True** - The NAME structure includes an Industry Group field (bits 59-60) where value 4 indicates Marine industry. Other values include 0=Global, 1=On-Highway, 2=Agriculture, 3=Construction.

---

### Part 3: Short Answer

16. **Expected Answer**:
    ```
    CAN ID: 0x09F80205 = 0000 1001 1111 1000 0000 0010 0000 0101 (binary)

    Priority (bits 26-28):    000 = 0 (actually bits shift to 010 = 2)
    Reserved (bit 25):        0
    Data Page (bit 24):       0
    PDU Format (bits 16-23):  11111000 = 0xF8 = 248
    PDU Specific (bits 8-15): 00000010 = 0x02 = 2
    Source Address (bits 0-7):00000101 = 0x05 = 5

    Since PF = 248 >= 240, this is PDU2 format (broadcast)
    PGN = (DP << 16) | (PF << 8) | PS
    PGN = (0 << 16) | (248 << 8) | 2
    PGN = 0 | 63488 | 2 = 63490 (0xF802)

    Final answers:
    - Priority: 2 (high priority)
    - PGN: 63490
    - Source Address: 5
    ```

    **Grading**: Full credit (10 pts) for correct extraction of all fields and PGN calculation; 8 pts for correct method with minor calculation error; 6 pts for understanding PDU2 concept but errors in calculation; 4 pts for attempting binary conversion; partial credit for any correct component.

17. **Expected Answer**:
    - PGN 126996 reveals detailed device information that attackers can use for reconnaissance
    - Manufacturer name and model number help identify which devices are present
    - Software/firmware version reveals if device has known vulnerabilities
    - Serial number can help track specific device instances
    - Attackers use this to:
      - Build a network topology map
      - Identify vulnerable firmware versions for targeted exploits
      - Understand device capabilities and potential attack surfaces
      - Research vendor-specific vulnerabilities
      - Plan device-specific spoofing attacks
    - This information gathering is passive and undetectable

    **Grading**: Full credit (10 pts) for identifying specific information types and explaining reconnaissance value; 8 pts for listing info types with basic explanation; 6 pts for understanding it's valuable but lacking detail; 4 pts for mentioning reconnaissance generally; partial credit for any relevant points.

18. **Expected Answer**:
    ```
    Given: 0x7C 0x22 (little-endian, so read as 0x22 0x7C = 0x227C)

    Step 1: Convert to decimal
    0x227C = 8828 (decimal)

    Step 2: Apply resolution (0.0001 radians per unit)
    8828 × 0.0001 = 0.8828 radians

    Step 3: Convert radians to degrees
    0.8828 × (180 / π) = 0.8828 × (180 / 3.14159)
    = 0.8828 × 57.2958
    = 50.57 degrees

    Answer: ~50.6 degrees (or approximately 51°)
    ```

    **Grading**: Full credit (10 pts) for correct answer with all steps shown; 8 pts for correct answer with minor calculation error; 6 pts for understanding little-endian and resolution but calculation error; 4 pts for attempting conversion with conceptual understanding; 2 pts for recognizing need for conversion; partial credit for any correct step.

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

**Question 16 (PGN Decoding):**
- Forgetting that PGN calculation depends on PF value
- Using big-endian instead of proper bit extraction
- Not recognizing PDU2 vs PDU1 format

**Question 17 (Product Information):**
- Generic answers not specific to maritime security context
- Not explaining reconnaissance value
- Missing the passive nature of the attack

**Question 18 (Heading Calculation):**
- Forgetting little-endian byte order (most common mistake!)
- Wrong resolution factor
- Not converting radians to degrees
- Calculation errors in π conversion

---

## Study Tips for Next Quiz

- Practice binary/hex conversions
- Memorize common PGNs and their update rates
- Understand PDU1 vs PDU2 format differences
- Review data encoding (little-endian, resolution factors)
- Study Fast Packet protocol structure
- Review address claim process and NAME structure

---
title: "Quiz 03"
subtitle: "The NEMO Platform"
course: "Maritime OT Security"
instructor: "Constantine Macris"
date: "2026"
assessment_type: "quiz"
time_limit: "30 minutes"
points: 100
passing_score: 70
---

# Quiz 03: The NEMO Platform

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

Who designed the NEMO platform used in this course?

a) Constantine Macris

b) James Campbell

c) PJRC (the Teensy maker)

d) The NMEA organization

---

### Question 2

Which microcontroller board is at the center of NEMO?

a) Raspberry Pi 4

b) Arduino Uno

c) Teensy 4.0

d) ESP32

---

### Question 3

On a NEMO board, what are the roles of the two CAN interfaces?

a) CAN1 transmits (sensor simulation and demonstrations) and CAN2 monitors

b) CAN1 monitors and CAN2 transmits

c) Both only transmit, on different bitrates

d) Both only monitor, on different bitrates

---

### Question 4

Which statement about the CAN transceivers on NEMO is correct?

a) Each CAN interface uses a TJA1050 transceiver powered at 12 V vessel power

b) The Teensy needs no transceiver because FlexCAN drives the bus directly

c) Only CAN1 needs a transceiver

d) Each CAN interface uses a TJA1050 transceiver powered at 5 V

---

### Question 5

Which display does NEMO require, and what happens if the wrong one is fitted?

a) SSD1306; the display works normally

b) Any I2C OLED; they are interchangeable

c) SH1106; a different controller may leave the display garbled or dark

d) A parallel LCD; I2C is not used

---

### Question 6

How many 120 ohm termination resistors belong on a CAN bus, and where?

a) One, at the middle of the bus

b) Two, one at each end of the bus

c) Three, so every branch is terminated

d) None, because transceivers terminate the bus internally

---

### Question 7

Why does the course use a separate capture interface (for example a Raspberry Pi with candump) alongside NEMO?

a) NEMO cannot receive any CAN traffic

b) The capture interface encrypts traffic for storage

c) The capture interface is needed to flash NEMO firmware

d) NEMO has no serial capture mode, so an independent listen-only tool is used to record traffic for analysis

---

### Question 8

Which NEMO versions does the course support?

a) 1.0.0 and 1.0.1

b) Only 0.9.x

c) 2.0.0 and later

d) Any version, since all behave identically

---

### Question 9

NEMO can transmit under another device's source address. Which threat model does that capability stand in for, and which week examines it at the physical layer?

a) TM2 (substituted transmitter); Week 12

b) TM1 (modified traffic); Week 5

c) TM3 (genuine device sending false values); Week 3

d) TM1 (modified traffic); Week 12

---

### Question 10

Which rule applies when a NEMO board is used for demonstrations in the Attacks menu?

a) Use a vessel's network only while it is docked

b) Use any network if the instructor is not present

c) Use vessel power so the board behaves realistically

d) Use only an isolated test network and never connect it to a live vessel

---

## Part 2: True/False (30 points)

**Instructions**: Circle T for True or F for False. Each question is worth 5 points.

### Question 11

**T / F**: NEMO includes a built-in serial capture mode, so a second capture tool is unnecessary.

---

### Question 12

**T / F**: Each of NEMO's simulated sensor values follows one of its three potentiometers.

---

### Question 13

**T / F**: NEMO's live-data view discovers devices from ISO Address Claim messages and displays their parsed PGNs.

---

### Question 14

**T / F**: When building the firmware, you should open the repository root folder rather than the SRC folder in PlatformIO.

---

### Question 15

**T / F**: Bench work with NEMO uses USB power only; no vessel power is connected.

---

### Question 16

**T / F**: Because NEMO is an education platform, it is safe to connect it to a live vessel network as long as only the Sensor Readings screen is used.

---

## Part 3: Short Answer (30 points)

**Instructions**: Provide concise, complete answers. Show calculations where applicable.

### Question 17 (10 points)

NEMO uses two CAN interfaces and the course also requires a separate capture interface. Explain (a) what each of NEMO's two interfaces does and what the problem would be if one interface both transmitted and monitored, and (b) why NEMO's own display is not enough to analyze traffic.

**Answer:**

\vspace{3cm}

---

### Question 18 (10 points)

Every student will own a device that can transmit on a CAN network. Describe three risks this creates and three concrete controls from this class that reduce them. Include why isolation matters.

**Answer:**

\vspace{3cm}

---

### Question 19 (10 points)

A classmate flashes their NEMO board. The display stays dark, and after you fix that, the Live Data screen shows no devices. List the checks the class suggests for each symptom, and explain why a second device (the capture interface) is useful for deciding whether the problem is on the bus or in the board.

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

1. **Answer: b** - NEMO was designed by James Campbell. The course uses the thedini/NEMO repository, a copy of the original project.

2. **Answer: c** - NEMO is a Teensy 4.0 shield; the Teensy's built-in FlexCAN controllers provide the two CAN interfaces.

3. **Answer: a** - CAN1 (pins 22/23) carries sensor simulation and the demonstrations; CAN2 (pins 0/1) is the monitor side.

4. **Answer: d** - Each CAN interface needs a TJA1050 transceiver powered at 5 V; it converts logic levels to CAN bus signals. The class says nothing about vessel power on the bench.

5. **Answer: c** - The display is an SH1106 128x64 I2C OLED, explicitly not an SSD1306. A garbled or dark display should prompt a check of the display type, I2C address and wiring.

6. **Answer: b** - The bus needs 120 ohm at each end, so two in total. The safety notes say not to add a third.

7. **Answer: d** - The class states NEMO has no serial capture mode; a separate listen-only interface records traffic for analysis (see Lab 05).

8. **Answer: a** - Versions 1.0.0 and 1.0.1 are supported. The material follows 1.0.0 and the instructor notes any 1.0.1 difference.

9. **Answer: a** - Transmitting under another device's source address stands in for TM2, the substituted transmitter. The class says Week 12 examines TM2 at the physical layer. TM1 is modified traffic and TM3 is a genuine device sending false values.

10. **Answer: d** - Safety notes: NEMO transmits, so use only an isolated test network and never connect it to a live vessel. Report unexpected behavior to the instructor and unplug.

---

### Part 2: True/False

11. **False** - The class states NEMO has no serial capture mode; traffic is recorded with a separate capture interface.

12. **True** - Each simulated sensor value follows a potentiometer (three 10 k potentiometers, up to three simulated sensors).

13. **True** - Live Data discovers devices from ISO Address Claims and displays their parsed PGNs. If no devices appear, check wiring, termination and that other devices are transmitting.

14. **False** - Open the SRC folder, not the repository root. If upload stalls, press the button on the Teensy.

15. **True** - Electrical safety rule: USB power only, no vessel power on the bench.

16. **False** - NEMO transmits and must never be connected to a live vessel, regardless of which screen is in use. Only isolated test networks are permitted.

---

### Part 3: Short Answer

17. **Expected Answer**:
    - (a) CAN1 transmits (sensor simulation and the built-in demonstrations); CAN2 monitors. Separate controllers and transceivers keep transmit and monitor roles apart.
    - A single interface that both transmits and monitors would mix its own transmissions with the traffic it is trying to observe, and it could not independently observe what other nodes put on the bus while it was busy sending. (Accept any reasoned answer along these lines; the class poses this as a homework question rather than giving a fixed text.)
    - (b) NEMO's display shows live parsed values from discovered devices only; it cannot record traffic, has no serial capture mode, and offers no way to review timing or raw frames afterward. A separate listen-only capture interface (for example a Raspberry Pi with candump) records traffic for later analysis and is independent of NEMO.

    **Grading**: Full credit (10 pts) for correct roles of both interfaces, a reasoned single-interface problem, and a clear explanation of why recording needs an independent tool; 8 pts for one part thin; 6 pts for roles correct but weak reasoning; 4 pts for partial recall; partial credit for any correct component.

18. **Expected Answer**:
    - Risks (any three): accidental transmission on a live or shared network; a student's device disturbing other students' benches; misuse of the demonstrations outside the course; electrical hazards from wrong power; unexpected behavior that goes unreported.
    - Controls from class (any three): isolated test network only; never connect NEMO to a live vessel; USB power only, no vessel power on the bench; 120 ohm termination at both ends and no third; report unexpected network behavior to the instructor and unplug; use the demonstrations only in Weeks 5-8 on the isolated network; verify wiring against the schematic before power.
    - Isolation matters because NEMO transmits: other devices on a connected network trust what arrives, so test traffic could be taken as real data. Isolation limits consequences to the bench.

    **Grading**: Full credit (10 pts) for three risks, three controls tied to the class, and a clear isolation rationale; 8 pts if one element is short; 6 pts for generic safety statements not tied to the class; 4 pts for only risks or only controls.

19. **Expected Answer**:
    - Dark display: check the I2C wiring, that the display is an SH1106 (not SSD1306), and the I2C address (0x3C or 0x3D); garbled output suggests the same checks plus loose wires.
    - No devices in Live Data: check wiring, termination, and that other devices are actually transmitting.
    - A capture interface is independent of NEMO: if it sees Address Claims and other traffic on the bus while NEMO's Live Data is empty, the fault is more likely in NEMO's wiring or monitor side; if the capture sees nothing either, check the bus, termination and whether devices are transmitting. (This is a reasoning step; the class lists the checks and the capture role separately.)

    **Grading**: Full credit (10 pts) for both symptom checklists plus a sound use of the independent capture; 8 pts for one checklist complete and a reasonable capture argument; 6 pts for checks only; 4 pts for partial lists.

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

**Question 3 (Interface roles):**
- Swapping CAN1 and CAN2 (CAN1 transmits, CAN2 monitors)

**Question 5 (Display):**
- Treating SH1106 and SSD1306 as interchangeable

**Question 7 (Capture interface):**
- Believing NEMO's display or a serial mode can serve as the capture record

**Question 9 (Threat models):**
- Mixing up TM1, TM2 and TM3 (TM1 modified traffic, TM2 substituted transmitter, TM3 genuine device sending false values)
- Forgetting that Week 12 is the physical-layer examination of TM2

**Question 18 (Safety):**
- Listing generic risks without tying controls to the class safety notes
- Describing isolation as optional or only a formality
---

## Study Tips for Next Quiz

- Memorize the NEMO hardware block diagram: Teensy, two transceivers, display, buttons, potentiometers
- Know the pin table roles (CAN1 transmit, CAN2 monitor)
- Review the safety considerations and troubleshooting table
- Be able to state the three threat models in your own words and which ones NEMO stands in for
- Review how Class 04 uses captured traffic for reconnaissance and baselining

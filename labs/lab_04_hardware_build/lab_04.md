---
title: "Lab 04"
subtitle: "Build and Test a NEMO Board"
author: "Constantine Macris"
date: "2026"
titlepage: true
titlepage-color: "1E3A5F"
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "FFFFFF"
titlepage-rule-height: 2
book: true
classoption: oneside
code-block-font-size: \scriptsize
description: |
    Building and testing a NEMO board
---

# Lab 04 -- Build and Test a NEMO Board

## Lab Overview

**Duration**: 2 hours
**Prerequisites**: Labs 01-03; Class 03 reviewed
**Versions**: NEMO 1.0.0 and 1.0.1 (check the version on the silkscreen; your instructor notes any 1.0.1 difference)
**Materials required**:
- A NEMO board (assembled PCB, or the parts for a breadboard build)
- Micro USB data cable
- Computer with VS Code, PlatformIO and Teensyduino installed
- A second NEMO or other NMEA 2000 device, 120 ohm terminators and cabling for Part 4
- Multimeter

## Objectives

By the end of this lab, you will:

1. Inspect and verify a NEMO build against the schematic
2. Build and flash the firmware with PlatformIO
3. Operate the sensor simulator
4. Use the live-data view to see another device
5. Record your build for later labs

## Safety Notice

**CRITICAL**: NEMO can transmit on a CAN bus. Use isolated test networks only. Never connect to a live vessel without explicit authorization. USB power only.

## Part 1: Inspect the Hardware (30 minutes)

### 1.1 Gather and check components

```
[ ] NEMO board (or Teensy 4.0, 2x TJA1050, SH1106 display, 3 pots, 4 buttons, screw terminal)
[ ] Micro USB data cable (not charge-only)
[ ] Multimeter
```

### 1.2 Verify before powering

With the board unpowered:

1. Check the display is **SH1106**, not SSD1306.
2. Confirm both TJA1050 transceivers are fitted and are powered at 5 V (not 3.3 V).
3. With the multimeter, check there is no short between 5 V and GND and between 3.3 V and GND.
4. Compare the pin wiring against the table in Class 03 (CAN1 on pins 22/23, CAN2 on pins 0/1, I2C on 18/19, buttons on 2-5, potentiometers on 14-16).

**Record**: board version (silkscreen) ________  results of the checks ________

## Part 2: Software Setup (20 minutes)

1. Install VS Code and the PlatformIO extension; restart VS Code.
2. Install Teensyduino from PJRC (skip the Arduino step).
3. Clone the repository and open its `SRC` folder:

```bash
git clone https://github.com/thedini/NEMO.git
cd NEMO/SRC
```

Open **`SRC`**, not the repository root: PlatformIO needs `platformio.ini` at the root of the folder.

## Part 3: Build and Flash (20 minutes)

1. Connect the Teensy by USB.
2. Build (checkmark in the PlatformIO toolbar). The first build downloads libraries and is slow.
3. Upload (arrow in the toolbar). If it stalls, press the button on the Teensy.
4. Confirm the OLED shows the main menu and the buttons navigate it.

If the display stays dark, check the I2C wiring, display power, and try the Teensy reset button. If the display shows garbage, check for SH1106 vs SSD1306 and the 0x3C/0x3D address.

**Record**: build version ________  upload succeeded? Y / N

## Part 4: Operate NEMO (40 minutes)

Do this on an isolated bench with 120 ohm terminators at both ends of the bus.

### 4.1 Simulate a sensor

1. Main menu -> Configure -> Sensor 1.
2. Set the manufacturer and the device type (for example Wind Speed).
3. Set Active to Yes.
4. Turn potentiometer R1 and watch the value change.

### 4.2 View live data

With a second device on the bus (another NEMO, or a sensor), open Live Data. Confirm that your first board's sensor appears with its source address, then open it and read a PGN.

**Record**:

| Item | Observation |
|------|-------------|
| Sensor type and PGN | |
| Source address shown | |
| Value range as you turn the pot | |
| Devices seen in Live Data | |

### 4.3 Reflect

1. Why does the display show a device only after an ISO Address Claim?
2. What happens to a device that falls silent for 60 seconds?
3. Why would you not rely on NEMO's own display to analyze traffic?

## Part 5: Document Your Build (10 minutes)

Photograph the finished board, note the version, and list any deviations from the schematic. Bring the board to Lab 05.

## Deliverables

1. Completed record sheets from Parts 1, 3 and 4
2. Photograph and version of your board
3. Answers to the three reflection questions

## Grading

Follows the lab rubric (`templates/lab_rubric.md`): technical correctness, documentation, analysis.

## Troubleshooting

| Symptom | Check |
|---------|-------|
| No Teensy detected | Charge-only cable; another port; press the Teensy button |
| Build fails | Delete `.pio`; update PlatformIO |
| Upload times out | Press the Teensy button; close other serial programs |
| Display garbled | SH1106; I2C address; loose wires |
| No devices in Live Data | Termination; wiring; other device transmitting |

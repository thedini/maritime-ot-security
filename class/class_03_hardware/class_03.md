---
title: "Class 03"
subtitle: "The NEMO Platform"
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
    The NEMO NMEA 2000 education and research platform
---

# Class 03 -- The NEMO Platform

## Learning Outcomes

- Describe what NEMO is and what it can and cannot do
- Identify the parts of a NEMO board and what each does
- Explain why a second, independent capture interface is needed
- Build, flash and power a NEMO board (versions 1.0.0 and 1.0.1)
- Operate the sensor simulator and the live-data view

## Definitions

- **NEMO** -- NMEA 2000 Education and Maritime Operations platform: a Teensy 4.0 board with two CAN interfaces, a display, buttons, and potentiometers
- **FlexCAN** -- The CAN controllers built into the Teensy 4.0 (two are used)
- **CAN transceiver** -- Converts logic levels to CAN bus signals (TJA1050, 5 V)
- **Sensor simulation** -- NEMO transmits NMEA 2000 messages as a configured device
- **Capture interface** -- A separate listen-only tool (for example a Raspberry Pi with `candump`) used to record traffic for analysis
- **Termination** -- 120 ohm resistor at each end of the bus

## Credit and Versions

NEMO was designed by James Campbell. The course uses the `thedini/NEMO` repository
(a copy of the original project). NEMO versions 1.0.0 and 1.0.1 are supported by
this course. The material below follows the 1.0.0 documentation; your instructor
notes any 1.0.1 difference. Check the version on the board silkscreen and the
About screen before you start.

## Reading Assignment

- NEMO `Documentation/README.md`, `Getting_Started.md` and `Operations_Guide.md`
- NEMO `Documentation/NMEA2000.md`
- Teensy 4.0 pinout reference (PJRC)

## Why a Purpose-Built Platform?

| Tool | Price | Capability |
|------|-------|------------|
| Actisense NGT-1 | $300+ | Read/write gateway, well supported |
| Yacht Devices YDNU-02 | $200+ | Wi-Fi gateway |
| NEMO | about $50 in parts | Simulates sensors, shows live traffic, runs two built-in demonstrations; open hardware and firmware |

Commercial tools are built to connect equipment, not to teach. NEMO lets every
student own a device that behaves like a sensor on an NMEA 2000 network.

## What NEMO Does

1. **Simulates up to three sensors** (heading, depth, wind, engine RPM, speed, temperature and others); each value follows a potentiometer.
2. **Shows live data**: discovers devices from ISO Address Claims and displays their parsed PGNs.
3. **Runs two built-in demonstrations** on an isolated test network: a denial-of-service load and impersonation of a sensor's data.

NEMO has no serial capture mode. To record traffic for analysis, use a separate
capture interface (see Lab 05).

## Hardware

NEMO is a Teensy 4.0 shield that adds:

- Two CAN interfaces: CAN1 transmits (sensor simulation and demonstrations), CAN2 monitors
- An OLED display (SH1106) and four navigation buttons
- Three 10 k potentiometers for sensor values
- An NMEA 2000 connector

| Teensy pin | Function |
|-----|----------|
| 22 / 23 | CAN1 TX / RX (transmit side) |
| 0 / 1 | CAN2 TX / RX (monitor side) |
| 2, 3, 4, 5 | Buttons (left, down, right, up) |
| 14, 15, 16 | Potentiometers 3, 2, 1 |
| 18 / 19 | I2C SDA / SCL to display |

Each CAN interface needs a TJA1050 transceiver powered at **5 V**.

### Bill of Materials (about $50)

| Part | Notes |
|------|-------|
| Teensy 4.0 | SparkFun DEV-15583 |
| SH1106 128x64 I2C OLED | Not SSD1306 |
| 2x TJA1050 CAN transceiver | 5 V |
| 3x 10 k potentiometer | |
| 4x push buttons | |
| 3-position screw terminal | |
| NMEA 2000 connector | |
| Custom PCB (KiCad 9 files in the repo) or breadboard | |

## Build Options

- **PCB**: order the board from the files in `PCB/`, or request one through the project contact listed in the NEMO README.
- **Breadboard**: wire the same parts following the schematic in the NEMO repository.

Either way, verify wiring against the schematic before applying power.

## Firmware

NEMO firmware is built and uploaded with PlatformIO and Teensyduino:

1. Install VS Code and the PlatformIO extension.
2. Install Teensyduino (PJRC) for the Teensy Loader.
3. Clone the NEMO repository and open the `SRC` folder (not the repository root).
4. Build, then upload. If upload stalls, press the button on the Teensy.

After upload the OLED shows the main menu. If the display stays dark, check the
I2C wiring and that the display is an SH1106.

## Using NEMO

Main menu: Sensor Readings (live data), Configure (sensors and device settings),
Attacks, About. Navigate with the four buttons; set values with the potentiometers.
The demonstrations in the Attacks menu are used only in Weeks 5-8, on an isolated
network (see Class 05 and Class 07).

## Threat-Model Context

NEMO is the course's traffic source and the instrument for the first two threat models.
Simulated and impersonated sensors serve the *modified traffic* threat model (TM1).
Because NEMO can transmit under another device's source address, it also stands in for
the *substituted transmitter* threat model (TM2), which Week 12 examines at the
physical layer.

## Safety Considerations

- Electrical: USB power only; no vessel power on the bench.
- Network: NEMO transmits. Use only an isolated test network. Never connect it to a live vessel.
- Termination: 120 ohm at both ends of the bus; do not add a third.
- Report any unexpected network behavior to the instructor and unplug.

## Troubleshooting

| Symptom | Check |
|---------|-------|
| No Teensy detected | Charge-only USB cable; try another port; press the Teensy button |
| Build fails | Delete the `.pio` folder; update PlatformIO |
| Upload times out | Press the Teensy button; close other programs using the port |
| Display garbled | SH1106 vs SSD1306; I2C address 0x3C or 0x3D; loose wires |
| No devices in Live Data | Wiring, termination, and that other devices are transmitting |

## Lab Preview: Week 4

You will build or receive a NEMO board, flash the firmware, and operate the sensor
simulator and the live-data view on an isolated bench.

## Homework

1. Draw the block diagram of NEMO from the pin table: Teensy, two transceivers, display, buttons, potentiometers.
2. Why does NEMO use two CAN interfaces? What would happen on a single interface if it both transmitted and monitored?
3. Explain why NEMO's own display is not enough to analyze traffic.

## Discussion Questions

1. What can a $50 board show students that a commercial gateway cannot?
2. Which threat models can NEMO simulate, and which can it not?
3. What are the risks of giving every student a device that can transmit on a network?

## References

- NEMO repository documentation (Getting Started, Operations Guide, PCB Design)
- Teensy 4.0 and Teensyduino, PJRC
- NMEA 2000 and CAN: see Classes 01 and 02

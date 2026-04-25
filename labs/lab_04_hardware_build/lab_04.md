---
title: "Lab 04"
subtitle: "NEMO Hardware Assembly"
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
    Receiving, assembling, and programming the NEMO dual-bus NMEA 2000 board
---

# Lab 04 -- NEMO Hardware Assembly

## Lab Overview

**Duration**: 2 hours
**Prerequisites**: Lab 01–03 completed, Class 03 material reviewed
**Materials Required**:

- NEMO PCB (DIY-fabbed via JLCPCB *or* pre-built from `nemo@jamescampbell.org`)
- Component BOM (Class 03, full table) if Path A
- Teensy 4.0
- USB Micro-B cable
- Computer with VS Code + PlatformIO + Teensyduino installed

**For Path A (DIY) only:**

- Soldering iron (~30W or temperature-controlled), solder, flux
- Tip-cleaning sponge or brass wool
- Helping-hands or PCB vise
- Side cutters / flush cutters
- Multimeter

## Objectives

By the end of this lab, you will:

1. Inspect a NEMO PCB and verify components against the BOM
2. (Path A) Solder through-hole components to the PCB
3. Flash the NEMO firmware to the Teensy 4.0
4. Verify boot via OLED splash and `candump` serial output
5. Connect to an isolated test network and observe traffic
6. Document your build with photos and a written report

## Safety Notice

**CRITICAL**: This board can transmit on a CAN bus. All testing in this lab MUST be performed on isolated test networks only. **Never** connect to live vessel systems without explicit authorization.

Soldering creates burn and fume hazards. Use a fume extractor or work in a ventilated area; wear safety glasses; never leave a hot iron unattended.

## Procurement Path Reminder

Your instructor has chosen one of two paths for this course:

- **Path A (DIY)** — your group received an unpopulated NEMO PCB plus a parts kit. You will solder the through-hole components and (possibly) the surface-mount parts.
- **Path B (Pre-built)** — your group received a fully assembled NEMO board. Skip Part 2 (soldering) unless your instructor flagged specific parts that still need attaching (commonly the M12 connector or screw terminal).

The remaining parts of this lab are identical for both paths.

## Part 1: Inspect and Verify (30 minutes)

### 1.1 Visual Inspection

Place the NEMO board on a clean static-dissipative mat (a ream of printer paper works in a pinch).

Cross-check against the BOM:

```
□ Teensy 4.0 (NOT a Teensy 3.x — NEMO requires the i.MX RT1062)
□ TJA1050 CAN transceiver — 2 pieces (U2 = CAN1, U3 = CAN2)
□ SH1106 128×64 OLED, I2C
□ 10kΩ panel-mount potentiometer — 3 pieces
□ Tactile push button — 4 pieces
□ NMEA 2000 M12 micro-C connector
□ 3-pin screw terminal block
□ Custom NEMO PCB
```

Path B users: skim the surface of the board for cold joints, missing components, or solder bridges. Flag anything suspicious to the instructor before powering on.

### 1.2 PCB Inspection (silkscreen orientation)

Identify and record the location of:

- **U1** — Teensy 4.0 footprint (largest IC location)
- **U2** — TJA1050 #1 (CAN1 / attack bus)
- **U3** — TJA1050 #2 (CAN2 / monitor bus)
- **D-pad** — four tactile button positions (silkscreen marks UP/DOWN/LEFT/RIGHT or similar)
- **R1, R2, R3** — pot positions
- **OLED** — header location, four pins (GND, VCC, SDA, SCL)
- **3-pin screw terminal** — connects to CAN1
- **M12 connector** — connects to CAN2

If the silkscreen is unclear, refer to `PCB/NEMO.kicad_sch` in the [NEMO repo](https://github.com/Soups71/NEMO/tree/main/PCB).

### 1.3 Continuity Pre-Check (multimeter)

Before any soldering or power-up:

- VCC (5V) to GND: should read **open** (no short)
- 3.3V rail to GND: should read **open**
- CAN_H to CAN_L on M12 with Teensy/transceiver socket empty: should read **open**

Note any unexpected continuity in your lab notebook and stop until the instructor confirms.

## Part 2: Soldering (Path A only — 45 minutes)

**Path B users skip to Part 3.**

### 2.1 Solder Order

Work from shortest components to tallest:

1. Any 0805/SOIC SMD parts (TJA1050, decoupling caps) — likely pre-populated by JLCPCB if you ordered assembly. If not, this step is the hardest; ask the instructor for help.
2. Tactile buttons (THT, four)
3. 3-pin screw terminal
4. Pot footprints (three)
5. OLED header (4-pin female header on PCB; OLED itself plugs in)
6. Teensy headers (two strips along the edges)
7. M12 NMEA 2000 connector (often a flying lead — secure mechanically before final solder)

### 2.2 Soldering Tips

- 700°F / 370°C is fine for leaded solder; 750°F / 400°C for lead-free
- Touch the iron to the **pad and lead simultaneously**, then feed solder to the joint (not the iron tip)
- 1–2 seconds per joint; longer than 5 seconds risks lifting the pad
- Good joint = shiny, concave fillet covering the pad and the lead
- Cold joint = matte, ball-shaped, doesn't fully wet the pad → reflow with flux

### 2.3 Solder Verification (multimeter)

After soldering:

- Continuity from each Teensy header pin **to its destination on the PCB** (refer to schematic for any pin you're unsure about)
- No bridges between adjacent pins, especially on the Teensy headers and OLED header
- Re-check the VCC ↔ GND check from 1.3 — still open

### 2.4 Document Your Build

Take a clear photo of your finished, populated PCB for your lab report (top view + bottom view).

<!--
Instructor Notes:

Common soldering mistakes in week 4:
1. Inadequate pre-tinning of the iron
2. Holding solder against the tip instead of the joint
3. Pulling the iron away too early — joint not yet wetted
4. Bridges on Teensy headers from too much solder

Walk around constantly. Catch bad joints before students plug
in USB. A short between 5V and GND on the Teensy will damage
the regulator.

For programs without soldering capacity: order from JLCPCB with
their assembly service for the SMD parts, or request a
pre-built board from nemo@jamescampbell.org. The 4 push
buttons, screw terminal, OLED header, and Teensy headers can
all be done by the instructor pre-class if needed.
-->

## Part 3: Software Setup (20 minutes)

### 3.1 Verify VS Code + PlatformIO

You should have already installed VS Code and the PlatformIO IDE extension as homework. If not:

1. Install [Visual Studio Code](https://code.visualstudio.com/)
2. Open VS Code → Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search "PlatformIO IDE" → Install
4. Restart VS Code; wait for first-run dependency download

### 3.2 Install Teensyduino

1. Download from [pjrc.com/teensy/teensyduino.html](https://www.pjrc.com/teensy/teensyduino.html)
2. Run installer (skip the Arduino IDE step — PlatformIO doesn't need it)

The Teensy Loader is what actually pushes firmware to the board.

### 3.3 Clone the NEMO Repository

```bash
git clone https://github.com/Soups71/NEMO.git
cd NEMO
```

### 3.4 Open the Firmware Project

In VS Code:

1. **File → Open Folder**
2. Navigate to **`NEMO/SRC`** — open this folder, NOT the parent `NEMO` folder. PlatformIO needs `platformio.ini` at the project root.
3. Wait for PlatformIO to initialize and download dependencies (first time is slow).

You should see the PlatformIO toolbar at the bottom of VS Code.

## Part 4: Flash Firmware (15 minutes)

### 4.1 Connect Teensy

1. Insert the Teensy 4.0 into its socket on the NEMO PCB (note pin-1 marker; reversed insertion will damage the board on power-up).
2. Plug the USB Micro-B cable into the Teensy.
3. Plug the other end into your computer.
4. The Teensy's onboard LED should blink (default factory blink program).

### 4.2 Build

In VS Code, click the PlatformIO **Build** button (✓ icon, bottom toolbar). The first build pulls dependencies and takes a minute or two. Subsequent builds are fast.

If the build fails because `NMEA2000_Teensyx` or another library is missing, run:

```bash
pio pkg install
```

from the `SRC` directory. Note: it's **`NMEA2000_Teensyx`** — students with prior MCP2515 experience sometimes try `NMEA2000_mcp` out of habit. NEMO does not use the MCP2515.

### 4.3 Upload

Click the PlatformIO **Upload** (→) button. The Teensy Loader window will pop up. If prompted, press the small white button on the Teensy itself.

You should see:

```
Memory Usage -> [=         ]   ...
PROGRAMMING: ...
DONE
```

### 4.4 Open Serial Monitor

Click the PlatformIO **Serial Monitor** icon. Set baud rate to **115200** if not auto-detected.

You should see:

- A boot banner from NEMO
- (If anything is on CAN2) `candump`-format frames streaming, e.g.:

```
can2  09F80106   [8]  00 00 23 FF FF FF FF FF
can2  09F11001   [8]  01 18 27 4A 00 FF 64 00
```

The OLED should now display the NEMO splash, then the main menu.

### 4.5 Troubleshooting

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| No serial output | Wrong port selected | Click the gear icon in PlatformIO serial monitor; select the Teensy ACM/COM port |
| OLED blank, board otherwise alive | Solder joint on pin 18/19 (I2C) or wrong driver | Check joints; confirm SH1106 (not SSD1306) |
| `pio` not found | PlatformIO not installed properly | Reinstall the VS Code PlatformIO extension |
| `NMEA2000_Teensyx` not found | Library install failed | Run `pio pkg install` from `SRC/` |
| Teensy not recognized | Teensyduino not installed | Reinstall Teensyduino |
| Random reboots | Power instability — try a different USB cable / port | Cheap USB cables can drop the 5V rail under load |

<!--
Instructor Notes:

Most common Lab 04 issues:
1. Student opens the parent `NEMO` folder, not `NEMO/SRC` -> PlatformIO doesn't recognize it
2. Cold solder joint on the Teensy header -> intermittent USB / no boot
3. Wrong USB cable (data vs charge-only) -> Teensy Loader doesn't see the board
4. Skipped soldering on the OLED header -> board boots but display is blank

Have at least one fully-built reference board on the bench so
students can A/B test if they get stuck.
-->

## Part 5: Boot Verification (10 minutes)

### 5.1 OLED Splash

The OLED should briefly show the NEMO splash, then the main menu:

```
    MAIN MENU

> Live Data
  Configure
  Attacks
  About
```

Use the D-pad (left/up/down/right) to scroll. **Right** enters a submenu; **Left** backs out.

### 5.2 candump Stream

If the OLED works, your I2C and core firmware are healthy. The serial stream verifies CAN2:

- If something is connected to the M12 CAN2 input and traffic is on the bus, you should see frames in the serial monitor.
- If nothing is connected, the serial stream may show only the boot banner — that is expected.

### 5.3 Pots and Buttons

Navigate **Configure → Sensor 1**. The sensor configuration screen lets you:

- Cycle manufacturer ID (use Up/Down)
- Cycle device type / PGN (use Up/Down)
- Toggle "Active"
- Watch the value change as you turn pot R1

Each of the three pots maps to one of three independent virtual sensors. The four buttons drive the menu. If any input doesn't work, note which one and revisit Part 2.5 (solder verification) for that pin.

## Part 6: Network Connection Test (20 minutes)

### 6.1 Connect to Test Network

**Only with instructor approval.**

The test network is an isolated NMEA 2000 harness — never plug NEMO into a live vessel.

1. Plug the **M12 connector** into the test bus (this is CAN2 — listen-only, never transmits).
2. Power the test network if it is not already powered (instructor will help).
3. Confirm 120Ω termination at each end of the test harness (commercial NMEA 2000 networks have this built into the backbone).

### 6.2 Observe Traffic on CAN2

Navigate **Live Data** on the OLED. Within a few seconds you should see other devices on the test network appear with their source addresses in brackets:

```
   LIVE DATA

> GPS Unit       [50]
  Depth Sounder  [51]
  Test Sensor    [22]
```

Press Right on a device to drill down into its PGNs. Press Right on a PGN to see parsed fields.

In the PlatformIO serial monitor, you should now see `candump` frames stream in real time.

### 6.3 Inject Traffic on CAN1

1. Connect the **3-pin screw terminal** to the same test harness (this is CAN1 — transmit/inject side).
2. Navigate **Configure → Sensor 1** and configure a fake Wind sensor (PGN 130306).
3. Toggle Active = Yes.
4. Watch your fake sensor appear in the **Live Data** menu (NEMO is observing its own traffic on CAN2 while transmitting on CAN1 — this is the dual-bus architecture in action).
5. Turn pot R1 and watch the wind value change in real time on a classmate's NEMO or on OpenPlotter.

### 6.4 Capture for Offline Analysis

In a separate terminal (not the PlatformIO serial monitor — only one process can hold the port at a time):

```bash
# On Linux:
cat /dev/ttyACM0 > capture.candump

# On macOS:
screen /dev/cu.usbmodem* 115200
# Use Ctrl-A then H to start logging
```

This is the data-collection method used in Lab 09 and beyond.

## Part 7: Documentation (15 minutes)

### 7.1 Lab Report Requirements

Your lab report should include:

1. **Build Documentation**
   - Procurement path (A or B)
   - Photo(s) of the finished board (top + bottom view if Path A)
   - Any deviations from the BOM
2. **Firmware Configuration**
   - Screenshot of successful PlatformIO upload
   - Screenshot of the OLED main menu
3. **Test Results**
   - Boot banner / candump sample (10+ lines)
   - Live Data screenshot showing at least one observed device
   - Successful sensor injection (your fake sensor appearing in Live Data)
4. **Issues Encountered**
   - Problems and solutions
   - Soldering rework, if any (Path A)

### 7.2 Lab Notebook Entry

Record in your lab notebook:

```
Date: _______________
Lab: 04 - NEMO Hardware Assembly

Procurement path:    Path A (DIY)  /  Path B (Pre-built)
Teensy serial:       _______________
NEMO PCB rev:        _______________

Soldering (Path A only):
  Components soldered: _______________
  Rework required:     _______________

Test Results:
  Visual inspection:    PASS / FAIL
  Continuity pre-check: PASS / FAIL
  Firmware upload:      PASS / FAIL
  OLED splash + menu:   PASS / FAIL
  Pot R1 / R2 / R3:     ___ / ___ / ___
  Buttons U/D/L/R:      ___ / ___ / ___ / ___
  Live Data observed:   PASS / FAIL
  Injection on CAN1:    PASS / FAIL

Issues / Notes:
_________________________________
_________________________________
```

## Deliverables

Submit via course portal:

1. **Lab report** (PDF) — 2–3 pages
2. **Hardware photo(s)** — clear images showing the populated PCB
3. **Serial output log** — at least 50 lines from the candump stream

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Hardware inspected and (Path A) correctly soldered | 25 |
| Firmware built and uploaded | 20 |
| OLED + pots + buttons verified | 20 |
| Network connection test (Live Data + injection) | 20 |
| Documentation complete | 15 |
| **Total** | **100** |

## Troubleshooting Reference

### Build/Upload fails

1. Confirm you opened `NEMO/SRC` (not `NEMO`)
2. Run `pio pkg install` from `SRC/`
3. Check that Teensyduino is installed
4. Try a different USB cable (data, not charge-only)

### OLED blank but board otherwise responsive

1. Inspect solder joints on pins 18/19
2. Verify the OLED driver chip is SH1106 (some Amazon listings ship SSD1306 in identical packaging — incompatible without firmware change)
3. Reseat the OLED on its header

### CAN2 shows no traffic

1. Confirm test network is powered and has another node transmitting
2. Check M12 wiring (CAN_H, CAN_L, GND assignments)
3. Verify the 120Ω termination resistors on the test harness
4. Inspect U3 (the CAN2 transceiver) for solder defects

### CAN1 transmits but no other node sees it

1. Check 3-pin screw terminal wiring (CAN_H, CAN_L)
2. Confirm sensor is Active in the Configure menu
3. Verify the receiving node is on the same bus, not a sibling harness

## Next Lab Preview

In Lab 05, you will use your NEMO to:

- Profile a complete NMEA 2000 network
- Build a device inventory using the Live Data menu and `candump` capture
- Establish frequency baselines (per-PGN message rates)
- Identify high-value targets for the spoofing labs in Phase 2

**Ensure your hardware is fully operational before next lab.** Replacement boards from `nemo@jamescampbell.org` typically take 1+ weeks to ship; flag any unresolved issues to the instructor today.

## References

- [NEMO Repository (Soups71/NEMO)](https://github.com/Soups71/NEMO)
- [NEMO PCB Design Reference](https://github.com/Soups71/NEMO/blob/main/Documentation/PCB_Design.md)
- [NEMO Operations Guide](https://github.com/Soups71/NEMO/blob/main/Documentation/Operations_Guide.md)
- [Teensy 4.0 Documentation](https://www.pjrc.com/teensy/)
- [PlatformIO Documentation](https://docs.platformio.org/)
- [NMEA 2000 Library (Lappalainen)](https://github.com/ttlappalainen/NMEA2000)

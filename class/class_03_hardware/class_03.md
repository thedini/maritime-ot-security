---
title: "Class 03"
subtitle: "NEMO Hardware Build"
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
    Building the NEMO dual-bus NMEA 2000 interface
---

# Class 03 -- NEMO Hardware Build

## Learning Outcomes

- Identify the components on the NEMO PCB
- Explain why two CAN buses (TX + sniffer) is the central architectural choice
- Describe how the Teensy 4.0's native FlexCAN controllers replace an external CAN controller
- Assemble (or receive and verify) a NEMO board and flash the firmware
- Verify connectivity to an isolated NMEA 2000 test network

## Definitions

- **MCU** -- Microcontroller Unit
- **FlexCAN** -- The CAN peripheral built into NXP's i.MX RT1062 (the chip on the Teensy 4.0). Two independent FlexCAN controllers are exposed; NEMO uses both.
- **Transceiver** -- Converts logic levels to differential CAN bus signals (CAN_H, CAN_L)
- **TJA1050** -- 5V high-speed CAN transceiver IC (NEMO uses two)
- **Listen-only mode** -- A FlexCAN configuration in which the controller never asserts the bus, never ACKs frames, and is therefore invisible to other nodes
- **Termination** -- 120Ω resistor at each end of the CAN bus (provided by other nodes on a real NMEA 2000 network)

## Reading Assignment

- [NEMO Project Overview](https://github.com/Soups71/NEMO/blob/main/Documentation/README.md)
- [NEMO PCB Design Reference](https://github.com/Soups71/NEMO/blob/main/Documentation/PCB_Design.md)
- [NEMO Source Code Architecture](https://github.com/Soups71/NEMO/blob/main/Documentation/Source_Code_Architecture.md)
- Teensy 4.0 pinout reference (PJRC)

## Why Build Our Own?

### Commercial Maritime Cyber Tools

| Tool | Price | Capability |
|------|-------|------------|
| Actisense NGT-1 | $200–$300 | USB gateway, read-only |
| Yacht Devices YDNU-02 | $200+ | WiFi gateway |
| Maretron USB100 | $200–$500 | Passive analyzer (commercial software) |
| Fathom5 Maritime Cyber Training | $5,000–$15,000+ | Full training platform |

### NEMO

| Component | Price | Qty |
|-----------|-------|-----|
| Teensy 4.0 | $23 | 1 |
| TJA1050 CAN Transceiver | $1.50 | 2 |
| SH1106 128×64 OLED (I2C) | $5 | 1 |
| 10kΩ Potentiometer | $0.50 | 3 |
| Tactile Push Button | $0.20 | 4 |
| NMEA 2000 M12 Connector | $8–$15 | 1 |
| 3-Pin Screw Terminal | $0.50 | 1 |
| Custom NEMO PCB (JLCPCB) | $2–$5 | 1 |
| **Total** | **~$42–$55** | |

**Active testing capability — sensor simulation, attack injection, and passive monitoring — at roughly 1% of a Fathom5 platform's cost.**

<!--
Instructor Notes:

Emphasize the cost barrier for education:
- A classroom of 20 students with Fathom5 = $100,000+
- A classroom with NEMO = ~$1,000
- Makes hands-on OT security education accessible

Also emphasize what's unique vs the cheaper passive analyzers:
- NGT-1 / USB100 are read-only — cannot inject, cannot impersonate
- NEMO does both, AT THE SAME TIME, on two independent buses

We have full control of the firmware (open source).
Commercial tools are black boxes.
-->

## System Architecture

NEMO's central design choice is using **both** of the Teensy 4.0's native CAN controllers. No external CAN controller is needed (that's why there's no MCP2515 on the board).

```
                                          ┌──────────────┐
                                          │              │     ╔═══════════╗
                                ┌────────►│  TJA1050     ├────►║ Screw     ║
                                │  CAN1   │  Transceiver │     ║ Terminal  ║
                                │  TX/RX  │   (U2)       │     ║ (TX/inject║
                                │         │              │     ║  bench)   ║
                                │         └──────────────┘     ╚═══════════╝
┌─────────────────────────┐     │
│                         │     │  Pins 22 (TX), 23 (RX)
│   Teensy 4.0            │─────┘
│   (NXP i.MX RT1062)     │
│                         │     Pins 0 (TX, unused), 1 (RX)
│   - 600 MHz Cortex-M7   │─────┐
│   - FlexCAN1 + FlexCAN2 │     │  CAN2
│   - Native USB serial   │     │  Listen-only
│   - I2C, SPI, ADC, GPIO │     │
│                         │     │         ┌──────────────┐    ╔════════════╗
│   NEMO firmware         │     └────────►│  TJA1050     ├───►║ M12 NMEA   ║
│   (PlatformIO build)    │     RX only   │  Transceiver │    ║ 2000 conn. ║
└─────┬───────────────────┘               │   (U3)       │    ║ (passive   ║
      │                                   │              │    ║  monitor)  ║
      │ I2C (pins 18/19)                  └──────────────┘    ╚════════════╝
      ▼
┌─────────────────┐
│  SH1106 OLED    │   Plus: 3 pots (A0/A1/A2), 4 D-pad buttons (pins 2/3/4/5)
│  128×64 menu    │
└─────────────────┘
```

<!--
Instructor Notes:

Draw this on the board. Three things to drive home:

1. ONE chip, TWO buses. The Teensy 4.0 has two FlexCAN
   peripherals built in. We don't need an external SPI CAN
   controller because we're not bandwidth-starved at 250 kbps.

2. Listen-only is invisible. CAN2 never asserts the bus, never
   ACKs a frame. Real devices on the network cannot tell NEMO
   is there.

3. This is what makes the IDS data-collection use case work:
   inject attack traffic on CAN1 and observe the network's
   response on CAN2 simultaneously. No commercial sub-$500
   tool does this.
-->

## Component Deep Dive

### Teensy 4.0

- **Chip**: NXP i.MX RT1062, ARM Cortex-M7 @ 600 MHz
- **Memory**: 1 MB Flash, 512 KB RAM
- **CAN**: Two independent FlexCAN controllers (we use **both** — this is the reason we picked this chip)
- **USB**: Native USB with serial support (used for `candump` output)
- **Why Teensy?**: Arduino-compatible, fast enough to encode NMEA 2000 messages and run a UI in the same loop, and the dual FlexCAN closes the price/capability gap with commercial gear.

![Teensy 4.0 Pinout - CC BY-SA PJRC](../../images/teensy41_pinout.png)

**NEMO Pin Map** (from `SRC/src/main.cpp`):

| Pin | Function | Notes |
|-----|----------|-------|
| 0   | CAN2_TX | Monitor bus (unused in listen-only mode) |
| 1   | CAN2_RX | Monitor bus RX |
| 2   | BUTTON_LEFT | D-pad left / back |
| 3   | BUTTON_DOWN | D-pad down |
| 4   | BUTTON_RIGHT | D-pad right / select |
| 5   | BUTTON_UP | D-pad up |
| 14 (A0) | SENSOR_3 | Pot R3 |
| 15 (A1) | SENSOR_2 | Pot R2 |
| 16 (A2) | SENSOR_1 | Pot R1 |
| 18  | I2C SDA | OLED data |
| 19  | I2C SCL | OLED clock |
| 22  | CAN1_TX | Attack/transmit bus |
| 23  | CAN1_RX | Attack/transmit bus |

### TJA1050 CAN Transceiver (×2)

- **Function**: Converts the Teensy's 3.3V CAN logic to the differential CAN_H / CAN_L signals on the bus
- **Voltage**: 5V (NOT 3.3V — NEMO routes 5V to the transceivers and Teensy IO is 5V-tolerant on the CAN pins)
- **Speed**: Up to 1 Mbps; NMEA 2000 runs at 250 kbps
- **Two of them on the board**: U2 = CAN1 (attack/inject bus), U3 = CAN2 (sniffer bus)

### SH1106 128×64 OLED Display

- **Interface**: I2C (Teensy pins 18/19)
- **Driver**: VEGA_SH1106 (or compatible Adafruit SSD1306 with patches)
- **Role**: Hierarchical menu UI — sensor configuration, attack control, live device discovery (28+ screens)

### Three 10kΩ Potentiometers

- **Pins**: A0/A1/A2 (analog, 5-sample averaging in firmware)
- **Role**: Real-time control of three independent sensor values, or attack parameters in impersonation mode

### Four Tactile Buttons (D-pad)

- **Pins**: 2 (left/back), 3 (down), 4 (right/select), 5 (up)
- **Configuration**: Active-low with internal pull-ups; 250 ms debounce filter in firmware

### NMEA 2000 M12 Connector + 3-Pin Screw Terminal

- **M12 (CAN2 / monitor bus)**: Standard NMEA 2000 micro-C field connector for plugging into a real network passively
- **3-pin screw terminal (CAN1 / inject bus)**: Bench testing — connect attack traffic to a small isolated CAN harness without disturbing the M12 side

### Power

USB only. NEMO is **never** bus-powered. This prevents accidentally connecting USB 5V to a live 12V NMEA 2000 backbone.

<!--
Instructor Notes:

Show physical NEMO board to class:
- Point out the two TJA1050 chips (U2 and U3)
- Note that there is NO MCP2515 — the Teensy IS the CAN controller
- Show the OLED, pots, D-pad
- Show both connectors: 3-pin terminal and M12

Common confusion: students who have used Arduino+MCP2515 elsewhere
will ask "where's the SPI CAN controller?" Answer: Teensy 4.0 has
two on-die FlexCAN peripherals. SPI bridge is unnecessary.
-->

## Bill of Materials

| Qty | Component | Notes | Source |
|-----|-----------|-------|--------|
| 1 | Teensy 4.0 | NOT a Teensy 3.x — we need the iMX RT1062 dual FlexCAN | PJRC.com / SparkFun DEV-15583 |
| 2 | TJA1050 CAN Transceiver | 5V — verify before buying. Bare ICs OK; we provide the supporting circuitry on the PCB | Amazon / DigiKey |
| 1 | SH1106 128×64 OLED, I2C | Verify SH1106 (not SSD1306 variant) | Amazon |
| 3 | 10kΩ panel-mount potentiometer | Linear taper | Amazon |
| 4 | Tactile push button (THT) | 6 mm body, standard pitch | Amazon |
| 1 | NMEA 2000 M12 micro-C connector | Field-attachable, female | RS Components / DigiKey |
| 1 | 3-pin screw terminal block | 5 mm pitch | Amazon |
| 1 | Custom NEMO PCB | KiCad files in [NEMO repo](https://github.com/Soups71/NEMO/tree/main/PCB) | JLCPCB.com |
| 1 | USB Micro-B cable | Power + programming + serial | Any |
| 1 | 3D-printed enclosure (optional) | STLs in [NEMO repo](https://github.com/Soups71/NEMO/tree/main/Case_Design) | Local 3D printer |

### Optional Test Equipment

| Qty | Component | Notes |
|-----|-----------|-------|
| 1 | Logic analyzer | For debugging I2C to the OLED |
| 1 | Multimeter | Continuity check before first power-on |
| 2 | 120Ω resistors | Termination for a bench-only CAN harness (a real NMEA 2000 network already has them) |

## Getting a Board

Two procurement paths. Either is fine for the course; instructors should choose based on time and soldering-equipment availability.

### Path A: DIY from JLCPCB

1. Clone or download [Soups71/NEMO](https://github.com/Soups71/NEMO).
2. Open `PCB/NEMO.kicad_pro` in KiCad 9.0+ and export gerbers.
3. Upload to JLCPCB (or equivalent) and order — typical cost is $2–5 per board for small qty, plus shipping and ~2-week fab lead time.
4. Order remaining components (BOM above) in parallel.
5. In Lab 04, students inspect, solder, and program the board.

This is the recommended path: students see the full pipeline from KiCad files to a working board.

### Path B: Pre-built board

Email **`nemo@jamescampbell.org`** with subject **"Board Request"** to coordinate a shipped, pre-assembled NEMO. Use this path when:

- Your program lacks soldering stations
- The semester schedule does not allow 2+ week PCB fab lead time
- You're running an evening course or workshop and need turnkey hardware

Lab 04 covers both paths.

## Software Setup

NEMO uses **PlatformIO** (not the bare Arduino IDE). Arduino IDE works in a pinch but PlatformIO handles dependencies cleanly.

### Install PlatformIO

1. Install [Visual Studio Code](https://code.visualstudio.com/).
2. In VS Code, install the **PlatformIO IDE** extension.
3. Wait for first-run dependency download (a few minutes).

### Install Teensy Loader

1. Download Teensyduino from [pjrc.com/teensy/teensyduino.html](https://www.pjrc.com/teensy/teensyduino.html).
2. Run the installer. (You can skip the Arduino install step — PlatformIO doesn't need it.)
3. The Teensy Loader app is what physically pushes firmware to the board.

### NEMO Firmware Dependencies (handled by PlatformIO)

`SRC/platformio.ini` declares everything; PlatformIO downloads on first build:

| Library | Role |
|---------|------|
| `U8g2` | OLED text rendering |
| `Adafruit SSD1306` / `Adafruit GFX` | Display primitives |
| `VEGA_SH1106` | SH1106-specific driver |
| `NMEA2000` (Lappalainen) | NMEA 2000 protocol stack |
| `NMEA2000_Teensyx` (Lappalainen) | Teensy FlexCAN driver — note `_Teensyx`, NOT `_mcp` |

<!--
Instructor Notes:

If a student has used MCP2515-based Arduino projects before, they
may try to install NMEA2000_mcp out of habit. That is the WRONG
library for NEMO. NEMO uses NMEA2000_Teensyx because the CAN
peripheral is on-die.
-->

## NEMO Firmware

### Clone the Repo

```bash
git clone https://github.com/Soups71/NEMO.git
cd NEMO/SRC
```

### Open in PlatformIO

In VS Code: **File → Open Folder** → navigate to `NEMO/SRC` and open it. (Important: open `SRC` specifically, not the parent `NEMO` folder. PlatformIO needs `platformio.ini` in the root.)

### Configure (rarely needed)

`SRC/include/constants.h` holds tunables (debug flags, default device count, etc.). Defaults are fine for first boot.

### Build and Flash

1. Plug the Teensy in via USB.
2. Click the PlatformIO **Build** button (✓ icon, bottom toolbar).
3. Click **Upload** (→ icon). Press the white button on the Teensy if Loader prompts you.

### Verify Boot

Open the PlatformIO serial monitor at **115200 baud**. You should see the boot banner and `candump`-format frames if anything is on CAN2:

```
can2  09F80106   [8]  00 00 23 FF FF FF FF FF
can2  09F11001   [8]  01 18 27 4A 00 FF 64 00
```

The OLED should show the NEMO splash, then the main menu.

## Testing Your Build

### Test 1: FlexCAN Internal Loopback

You don't need to wire CAN_H to CAN_L externally — the FlexCAN peripheral has a built-in loopback mode. NEMO's benchmarking firmware (see paper) uses this for latency and throughput measurements. For Lab 04, the boot banner + OLED splash is sufficient evidence the peripheral is alive.

### Test 2: Connect to Test Network

**Only on an isolated test network with instructor supervision.**

1. Plug the M12 connector (CAN2) into the test bus.
2. Power on NEMO via USB.
3. From the main menu, navigate **Live Data → [device]** to confirm NEMO is hearing other nodes.
4. Plug the 3-pin screw terminal (CAN1) into the same harness if you want to inject. Navigate **Configure → Sensor 1** to spin up a fake sensor and watch it appear on the test network.

### Test 3: candump Capture

In the PlatformIO serial monitor, all CAN2 traffic streams in `candump` format at 115200 baud. Pipe to a file for offline analysis with [CANboat](https://github.com/canboat/canboat) — this is the data-collection setup used in Lab 09 and beyond.

```bash
# On Linux, while NEMO is connected:
cat /dev/ttyACM0 > capture.candump
```

## Operating NEMO

NEMO has its own UI on the OLED — there's no CSV command protocol. The full menu walkthrough lives in the [NEMO Operations Guide](https://github.com/Soups71/NEMO/blob/main/Documentation/Operations_Guide.md). The short version:

- **Live Data** — passive device discovery and PGN browser (uses CAN2)
- **Configure** — set up to three simultaneous fake sensors with selectable manufacturer ID, PGN, and pot-controlled value (uses CAN1)
- **Attacks** — DoS (address-claim flooding) and impersonation, target selectable from observed devices

The 28-PGN list and field-level spoofing menus are documented in the [Attacks doc](https://github.com/Soups71/NEMO/blob/main/Documentation/Attacks.md).

## Safety Considerations

### Electrical Safety

- Always disconnect USB before adjusting connectors.
- NEMO is USB-powered only — never connect bus power to the board.
- The PCB has reverse-polarity protection on the screw terminal, but the M12 doesn't carry power on NEMO regardless.

### Network Safety

- **NEVER connect to a live vessel without written authorization.**
- All lab exercises run on isolated test networks built from spare NMEA 2000 cabling and termination resistors.
- Understand that you are generating real CAN frames. NEMO can spoof safety-critical data — depth, position, engine RPM. Treat it accordingly.

### RF / Wiring

- Use twisted pair (CAT5/CAT6 spare pair is fine in the lab) for CAN_H / CAN_L on bench harnesses.
- A real NMEA 2000 backbone provides 120Ω termination at each end. A bench harness needs you to add them.

<!--
Instructor Notes:

CRITICAL safety briefing — same as before:
1. This hardware can affect real vessel systems
2. Spoofing navigation data is dangerous and illegal in some
   jurisdictions
3. All exercises on isolated networks only
4. Students sign ethics agreement before Lab 04

Legal: Even possessing tools to attack CAN bus may have legal
implications in some jurisdictions. We're using these for
EDUCATIONAL purposes only.
-->

## Troubleshooting

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| No serial output | Wrong COM/USB port | Check the PlatformIO serial monitor port selector |
| Teensy not recognized | Driver issue | Reinstall Teensyduino |
| OLED blank, board otherwise alive | Wrong I2C address or bad solder joint on pins 18/19 | Check joints; verify SH1106 vs SSD1306 driver |
| `candump` shows nothing on CAN2 | Bus has no traffic, OR CAN2 transceiver (U3) wired wrong | Use Live Data menu — if the splash works, bus is the problem; if not, check U3 |
| Pots read max all the time | Pot wiper not soldered, or 3.3V/GND swapped | Multimeter check the pot leads |
| TX appears to fail | No other node ACK'ing on the bus | Add a second node, or use FlexCAN loopback for solo tests |
| `NMEA2000_mcp` not found | Wrong library installed | Use `NMEA2000_Teensyx` — NEMO does not use MCP2515 |

## Lab Preview: Week 4

In Lab 04, you will:

1. Receive your NEMO board (DIY-fabbed or pre-built per Path A or B above)
2. Inspect the board for solder defects and verify components against the BOM
3. Solder any remaining through-hole parts (Teensy headers, screw terminal, M12 if not pre-attached)
4. Flash the firmware via PlatformIO
5. Verify boot (OLED splash, candump output)
6. Connect to the class test network and complete Test 2/3 above
7. Document your build with photos

**Bring**: soldering iron and flux (if not provided by the lab); USB Micro-B cable.

## Homework

### Required

1. **Confirm hardware path with instructor** — DIY (Path A) or pre-built (Path B)
2. **Install** VS Code + PlatformIO + Teensyduino
3. **Read** [NEMO Project Overview](https://github.com/Soups71/NEMO/blob/main/Documentation/README.md) and [Source Code Architecture](https://github.com/Soups71/NEMO/blob/main/Documentation/Source_Code_Architecture.md)
4. **Watch** (suggested): "Introduction to CAN Bus" (any of the better YouTube primers — verify with the instructor)

### Suggested

- Skim the Teensy 4.0 datasheet, focusing on the FlexCAN section
- Browse the NMEA2000 library examples (Lappalainen)
- Read the [NEMO Attacks doc](https://github.com/Soups71/NEMO/blob/main/Documentation/Attacks.md) so you understand what your board can do before Lab 04

## Discussion Questions

1. Why does NEMO use the Teensy's native FlexCAN instead of an external SPI CAN controller? What does the choice cost, and what does it enable?
2. What does CAN2's listen-only mode protect against, and how is it different from "just don't transmit"?
3. NEMO can transmit and monitor on the same network simultaneously. Why is that useful for IDS data collection but dangerous if used carelessly?
4. Why is open-source hardware important for security research?

## References

- [NEMO Project (Soups71/NEMO)]
- [NEMO PCB Design Reference]
- [NEMO Source Code Architecture]
- [PJRC Teensy 4.0]
- [NMEA 2000 Library (Lappalainen)]
- [NMEA 2000 Teensyx Driver]

[NEMO Project (Soups71/NEMO)]:https://github.com/Soups71/NEMO
[NEMO PCB Design Reference]:https://github.com/Soups71/NEMO/blob/main/Documentation/PCB_Design.md
[NEMO Source Code Architecture]:https://github.com/Soups71/NEMO/blob/main/Documentation/Source_Code_Architecture.md
[PJRC Teensy 4.0]:https://www.pjrc.com/teensy/
[NMEA 2000 Library (Lappalainen)]:https://github.com/ttlappalainen/NMEA2000
[NMEA 2000 Teensyx Driver]:https://github.com/ttlappalainen/NMEA2000_Teensyx

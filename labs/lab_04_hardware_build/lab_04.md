---
title: "Lab 04"
subtitle: "OpenBridge Hardware Assembly"
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
    Building and testing the OpenBridge NMEA 2000 interface
---

# Lab 04 -- OpenBridge Hardware Assembly

## Lab Overview

**Duration**: 2 hours
**Prerequisites**: Lab 01-03 completed, Class 03 material reviewed
**Materials Required**:
- Teensy 4.0 or 4.1
- MCP2515 CAN module
- Breadboard and jumper wires
- USB Micro cable
- Computer with Arduino IDE installed

## Objectives

By the end of this lab, you will:

1. Assemble OpenBridge hardware on breadboard
2. Flash firmware to Teensy
3. Verify CAN interface functionality
4. Connect to test network
5. Send and receive test messages

## Safety Notice

**CRITICAL**: This hardware can transmit on CAN bus. All testing MUST be performed on isolated test networks only. Never connect to live vessel systems without explicit authorization.

## Part 1: Hardware Assembly (45 minutes)

### 1.1 Gather Components

Verify you have all required components:

```
□ Teensy 4.0/4.1 microcontroller
□ MCP2515 CAN module (with TJA1050)
□ Breadboard (400+ points)
□ Jumper wires (male-to-male, 7 required)
□ USB cable (Micro-B for 4.0, or appropriate for 4.1)
```

### 1.2 Inspect the MCP2515 Module

Before connecting, identify the crystal oscillator on your module:

```
Look for small metal cylinder marked:
- "16.000" = 16 MHz crystal
- "8.000" = 8 MHz crystal

Record your crystal frequency: _____________ MHz
```

**This is critical for firmware configuration!**

### 1.3 Wire Power Connections

**Disconnect USB before wiring!**

| Teensy Pin | MCP2515 Pin | Wire Color (suggested) |
|------------|-------------|------------------------|
| 3.3V | VCC | Red |
| GND | GND | Black |

**Double-check polarity before proceeding!**

### 1.4 Wire SPI Interface

| Teensy Pin | MCP2515 Pin | Function |
|------------|-------------|----------|
| Pin 10 | CS | Chip Select |
| Pin 11 | SI (MOSI) | Data to CAN |
| Pin 12 | SO (MISO) | Data from CAN |
| Pin 13 | SCK | SPI Clock |

### 1.5 Wire Interrupt

| Teensy Pin | MCP2515 Pin | Function |
|------------|-------------|----------|
| Pin 2 | INT | CAN Interrupt |

### 1.6 Verification Checklist

Before applying power, verify each connection:

```
□ 3.3V → VCC (not 5V!)
□ GND → GND
□ Pin 10 → CS
□ Pin 11 → SI/MOSI
□ Pin 12 → SO/MISO
□ Pin 13 → SCK
□ Pin 2 → INT

□ No loose connections
□ No shorts between adjacent pins
□ Wires routed cleanly
```

### 1.7 Document Your Build

Take a clear photo of your assembled hardware for your lab report.

<!--
Instructor Notes:

Common assembly mistakes:
1. Wrong voltage (5V instead of 3.3V)
2. MOSI/MISO swapped
3. Loose connections
4. Wrong pins

Walk around and verify each student's build
BEFORE they apply power.

Have spare components available for failures.
-->

## Part 2: Software Setup (20 minutes)

### 2.1 Install Arduino IDE

If not already installed:

1. Download from https://www.arduino.cc/en/software
2. Install for your platform
3. Launch Arduino IDE

### 2.2 Install Teensyduino

1. Download from https://www.pjrc.com/teensy/td_download.html
2. Run installer
3. Point to your Arduino installation
4. Select all libraries when prompted

### 2.3 Install Required Libraries

In Arduino IDE: **Sketch → Include Library → Manage Libraries**

Search and install:
- `NMEA2000` by Timo Lappalainen
- `NMEA2000_mcp` by Timo Lappalainen
- `mcp_can` by Cory J Fowler

### 2.4 Clone OpenBridge Repository

```bash
# Clone the OpenBridge repository
git clone https://github.com/[org]/openbridge.git

# Navigate to firmware directory
cd openbridge/src/VERSION\ 2/
```

## Part 3: Firmware Configuration (15 minutes)

### 3.1 Configure Crystal Frequency

Open `openbridge.h` and locate the clock setting:

```cpp
// Set to match YOUR module's crystal
#define MCP_CLOCK MCP_16MHZ  // or MCP_8MHZ
```

**Change this to match your module's crystal!**

### 3.2 Verify Pin Configuration

Confirm pin settings match your wiring:

```cpp
#define MCP_CS_PIN 10
#define MCP_INT_PIN 2
```

### 3.3 Verify CAN Speed

For NMEA 2000:

```cpp
#define CAN_SPEED CAN_250KBPS
```

### 3.4 Save Configuration

Save your changes to `openbridge.h`.

## Part 4: Flash Firmware (15 minutes)

### 4.1 Connect Teensy

1. Connect USB cable to Teensy
2. Connect other end to computer
3. Teensy LED should light up

### 4.2 Select Board and Port

In Arduino IDE:

1. **Tools → Board → Teensy 4.0** (or 4.1)
2. **Tools → Port → [select Teensy port]**

### 4.3 Upload Firmware

1. Click **Upload** button (→)
2. If prompted, press button on Teensy
3. Wait for "Done uploading" message

### 4.4 Open Serial Monitor

1. **Tools → Serial Monitor**
2. Set baud rate: **115200**
3. You should see:

```
OpenBridge v2.0 initialized
CAN interface ready
Waiting for commands...
```

**If you see garbled text, check baud rate setting.**

### 4.5 Troubleshooting

| Symptom | Possible Cause | Solution |
|---------|---------------|----------|
| No serial output | Wrong port | Check Tools → Port |
| Garbled text | Wrong baud | Set to 115200 |
| "CAN init failed" | Wrong crystal | Check MCP_CLOCK |
| Teensy not recognized | Driver issue | Reinstall Teensyduino |

<!--
Instructor Notes:

Most common issues:
1. Crystal frequency mismatch (very common!)
2. Wrong COM port selected
3. SPI wiring errors

If CAN init fails:
- Check SPI wiring first
- Then verify crystal setting
- Power cycle and retry
-->

## Part 5: Loopback Test (15 minutes)

### 5.1 Create Loopback

To test without a CAN network, create a loopback:

1. Connect a jumper wire between CAN_H and CAN_L on your module
2. This creates a "network of one"

### 5.2 Send Test Message

In Serial Monitor, enter:

```
40,1,15.0,45.0,1
```

(This sends Wind Data: SID=1, Speed=15 knots, Angle=45°, Reference=Apparent)

### 5.3 Verify Response

You should see:

```
TX: PGN 130306 Wind Data
RX: PGN 130306 Wind Data (loopback)
```

**If you only see TX but no RX, check your loopback jumper.**

### 5.4 Test Multiple Commands

Try these commands:

```
# Position: 41.5°N, 71.4°W
4,41.5,-71.4

# Heading: 90 degrees magnetic
2,1,1.5708,0.0,0.0,1

# Engine RPM: 2500
50,1,2500
```

Record which commands work in your lab notebook.

### 5.5 Remove Loopback

**Remove the CAN_H/CAN_L jumper before proceeding!**

## Part 6: Network Connection Test (15 minutes)

### 6.1 Connect to Test Network

**Only with instructor approval!**

1. Identify CAN_H and CAN_L on test network
2. Connect your module:
   - Module CAN_H → Network CAN_H (White wire)
   - Module CAN_L → Network CAN_L (Blue wire)
3. Optionally connect ground

### 6.2 Enable Monitoring Mode

In Serial Monitor, enter:

```
monitor
```

You should see NMEA 2000 traffic scrolling:

```
RX: PGN 127250 Heading: 125.3°
RX: PGN 129025 Position: 41.4892, -71.4218
RX: PGN 130306 Wind: 12.5 kts @ 35°
...
```

### 6.3 Record Network Traffic

Record for 60 seconds and note:

- How many different PGNs do you see?
- What devices appear to be on the network?
- What is the approximate message rate?

### 6.4 Send a Test Message

Send a wind data message:

```
40,1,10.5,90.0,1
```

**Verify your message appears on another monitor (OpenPlotter or classmate's system).**

## Part 7: Documentation (15 minutes)

### 7.1 Lab Report Requirements

Your lab report should include:

1. **Build Documentation**
   - Photo of assembled hardware
   - Crystal frequency noted
   - Any modifications made

2. **Firmware Configuration**
   - Screenshot of successful upload
   - Any configuration changes

3. **Test Results**
   - Loopback test output
   - Network traffic sample (10+ lines)
   - Messages you successfully sent

4. **Issues Encountered**
   - Problems and solutions
   - Troubleshooting steps taken

### 7.2 Lab Notebook Entry

Record in your lab notebook:

```
Date: _______________
Lab: 04 - Hardware Build

Components Used:
- Teensy model: _______
- MCP2515 crystal: _______ MHz

Configuration:
- MCP_CLOCK: _______
- CAN_SPEED: _______

Test Results:
- Loopback: PASS / FAIL
- Network TX: PASS / FAIL
- Network RX: PASS / FAIL

Issues/Notes:
_________________________________
_________________________________
```

## Deliverables

Submit via course portal:

1. **Lab report** (PDF) - 2-3 pages
2. **Hardware photo** - Clear image showing wiring
3. **Serial output log** - Copy of successful communication

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Hardware correctly assembled | 25 |
| Firmware configured and uploaded | 20 |
| Loopback test successful | 20 |
| Network test successful | 20 |
| Documentation complete | 15 |
| **Total** | **100** |

## Troubleshooting Reference

### CAN Init Failed

1. Check SPI wiring (pins 10, 11, 12, 13)
2. Verify crystal frequency setting
3. Check power connections
4. Try different MCP2515 module

### No TX/RX on Network

1. Check CAN_H/CAN_L connections
2. Verify network has termination (120Ω)
3. Confirm CAN speed matches (250kbps)
4. Check if network is powered

### Garbled Serial Output

1. Set baud rate to 115200
2. Check USB cable connection
3. Try different USB port

## Next Lab Preview

In Lab 05, you will use your OpenBridge to:
- Profile a complete NMEA 2000 network
- Build device inventory
- Create frequency baselines
- Identify high-value targets

**Ensure your hardware is working before next lab!**

## References

- [Teensy Documentation](https://www.pjrc.com/teensy/)
- [MCP2515 Datasheet](https://www.microchip.com)
- [OpenBridge GitHub](https://github.com/[org]/openbridge)

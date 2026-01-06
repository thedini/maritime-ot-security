---
title: "Class 03"
subtitle: "OpenBridge Hardware Build"
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
    Building the OpenBridge NMEA 2000 interface
---

# Class 03 -- OpenBridge Hardware Build

## Learning Outcomes

- Identify components of the OpenBridge CAN interface
- Understand CAN transceiver operation
- Assemble Teensy + MCP2515 hardware
- Flash OpenBridge firmware
- Verify connectivity to NMEA 2000 network

## Definitions

- **MCU** -- Microcontroller Unit
- **SPI** -- Serial Peripheral Interface
- **Transceiver** -- Converts logic levels to CAN bus signals
- **MCP2515** -- CAN controller IC (SPI interface)
- **TJA1050** -- CAN transceiver IC
- **Termination** -- 120Ω resistor at bus ends

## Reading Assignment

- OpenBridge README and documentation
- Teensy 4.x pinout reference
- MCP2515 datasheet (overview sections)

## Why Build Our Own?

### Commercial NMEA 2000 Tools

| Tool | Price | Capability |
|------|-------|------------|
| Actisense NGT-1 | $300+ | Read/Write, well supported |
| Yacht Devices YDNU-02 | $200+ | WiFi gateway |
| Maretron USB100 | $400+ | Professional diagnostics |
| Simrad/Lowrance adapters | $150+ | Brand-specific |

### OpenBridge

| Component | Price |
|-----------|-------|
| Teensy 4.0 | ~$25 |
| MCP2515 module | ~$5 |
| TJA1050 (often included) | ~$3 |
| Breadboard + wires | ~$10 |
| **Total** | **~$43** |

**Same read/write capability at 1/10th the cost!**

<!--
Instructor Notes:

Emphasize the cost barrier for education:
- A classroom of 20 students with commercial tools = $6000+
- A classroom with OpenBridge = $860
- Makes hands-on OT security education accessible

Also: We have full control of the firmware (open source).
Commercial tools are black boxes.
-->

## System Architecture

```
┌─────────────────┐     SPI      ┌─────────────┐   CAN    ┌──────────────┐
│                 │◄────────────►│             │◄────────►│              │
│   Teensy 4.x    │              │   MCP2515   │          │  TJA1050     │
│   (MCU)         │              │   (CAN      │          │  (Trans-     │
│                 │              │   Controller)│          │   ceiver)    │
│   - USB Serial  │              │             │          │              │
│   - 600MHz ARM  │              │   - TX/RX   │          │   - CAN_H    │
│   - OpenBridge  │              │   - Filters │          │   - CAN_L    │
│     Firmware    │              │   - Buffers │          │              │
└─────────────────┘              └─────────────┘          └──────┬───────┘
                                                                 │
                                                          ═══════╧═══════
                                                          NMEA 2000 Bus
```

<!--
Instructor Notes:

Draw this diagram on board and explain data flow:

1. CSV command comes in USB serial from computer
2. Teensy parses command, builds CAN frame
3. Teensy sends frame to MCP2515 via SPI
4. MCP2515 handles CAN protocol (arbitration, CRC, ACK)
5. TJA1050 converts to differential CAN signals
6. Message appears on NMEA 2000 bus

Reverse path for receiving messages.
-->

## Component Deep Dive

### Teensy 4.0/4.1

- **Processor**: ARM Cortex-M7 @ 600 MHz
- **Memory**: 1MB Flash, 512KB RAM
- **USB**: Native USB with serial support
- **GPIO**: Multiple SPI interfaces
- **Why Teensy?**: Arduino-compatible, fast, affordable

![Teensy 4.1 Pinout - CC BY-SA PJRC](../../images/teensy41_pinout.png)

<!--
Image source: PJRC.com (Creative Commons)
Alternative: Create simple pinout diagram showing only SPI pins used
-->

### MCP2515 CAN Controller

- **Interface**: SPI (up to 10 MHz)
- **CAN**: ISO 11898-1 compliant
- **Buffers**: 2 receive, 3 transmit
- **Filters**: 6 acceptance filters, 2 masks
- **Oscillator**: External 8/16 MHz crystal

**Key pins:**
- VCC, GND: Power (5V or 3.3V)
- SCK, MOSI, MISO, CS: SPI interface
- INT: Interrupt output
- TXCAN, RXCAN: To transceiver

### TJA1050 CAN Transceiver

- **Function**: Converts logic to differential CAN
- **Output**: CAN_H, CAN_L
- **Protection**: ESD, short circuit
- **Speed**: Up to 1 Mbps

**Most MCP2515 modules include a TJA1050!**

<!--
Instructor Notes:

Show physical modules to class:
- MCP2515 module (blue PCB, typically)
- Point out the TJA1050 chip on board
- Show the crystal (8 or 16 MHz - check yours!)

Common issue: Crystal frequency mismatch
- Module has 8 MHz crystal
- Code configured for 16 MHz
- Result: Wrong bitrate!
-->

## Bill of Materials

| Qty | Component | Notes | Source |
|-----|-----------|-------|--------|
| 1 | Teensy 4.0 or 4.1 | 4.1 has more pins | PJRC.com |
| 1 | MCP2515 CAN Module | Usually includes TJA1050 | Amazon/AliExpress |
| 1 | Breadboard | 400 or 830 point | Amazon |
| 10+ | Jumper wires | Male-to-male | Amazon |
| 1 | USB Micro cable | For Teensy 4.0 | Any |
| 2 | 120Ω resistors | Termination (optional) | Any |

### Optional

| Qty | Component | Notes |
|-----|-----------|-------|
| 1 | NMEA 2000 cable | For real network connection |
| 1 | DeviceNet connector | Standard NMEA 2000 |
| 1 | Logic analyzer | For debugging |

## Wiring Diagram

```
Teensy 4.x                    MCP2515 Module
──────────                    ──────────────
   3.3V  ◄──────────────────►  VCC
   GND   ◄──────────────────►  GND
   Pin 10 ◄─────────────────►  CS (Chip Select)
   Pin 11 ◄─────────────────►  MOSI (SI)
   Pin 12 ◄─────────────────►  MISO (SO)
   Pin 13 ◄─────────────────►  SCK (Clock)
   Pin 2  ◄─────────────────►  INT (Interrupt)


MCP2515 Module                NMEA 2000 Bus
──────────────                ────────────
   CAN_H  ◄──────────────────►  CAN_H (White)
   CAN_L  ◄──────────────────►  CAN_L (Blue)
   GND    ◄──────────────────►  Shield/GND (optional)
```

<!--
Instructor Notes:

CRITICAL: Verify voltage compatibility!
- Teensy 4.x is 3.3V logic
- Some MCP2515 modules are 5V
- Most work with 3.3V - check module specs

Wire color convention for NMEA 2000:
- White: CAN_H (Net-H)
- Blue: CAN_L (Net-L)
- Bare/Shield: Ground
- Red: +12V (we don't need for our module)
- Black: Ground
-->

## Assembly Steps

### Step 1: Prepare Components

1. Unpack Teensy (do NOT plug in USB yet)
2. Unpack MCP2515 module
3. Gather 7 jumper wires
4. Have breadboard ready

### Step 2: Mount Components on Breadboard

1. Insert Teensy across center gap
2. Insert MCP2515 module with space between
3. Ensure all pins are seated properly

### Step 3: Wire Power

```
Teensy 3.3V → MCP2515 VCC
Teensy GND  → MCP2515 GND
```

**Double-check polarity before proceeding!**

### Step 4: Wire SPI Interface

```
Teensy Pin 10 → MCP2515 CS
Teensy Pin 11 → MCP2515 SI (MOSI)
Teensy Pin 12 → MCP2515 SO (MISO)
Teensy Pin 13 → MCP2515 SCK
```

### Step 5: Wire Interrupt

```
Teensy Pin 2 → MCP2515 INT
```

### Step 6: Verify Wiring

- Trace each wire from source to destination
- Check for loose connections
- Verify no shorts between adjacent pins

<!--
Instructor Notes:

BEFORE students power on:
- Walk around and check each build
- Common mistakes:
  - Reversed power (will damage chips!)
  - Wrong SPI pins
  - Loose connections
  - Teensy not seated properly

Have spare components for failures.
-->

## Software Setup

### Install Arduino IDE

1. Download from arduino.cc
2. Install for your platform
3. Open Arduino IDE

### Install Teensyduino

1. Download from pjrc.com/teensy/teensyduino.html
2. Run installer
3. Point to Arduino installation
4. Select all libraries

### Install Required Libraries

In Arduino IDE: Sketch → Include Library → Manage Libraries

Install:
- **NMEA2000** by Timo Lappalainen
- **NMEA2000_mcp** by Timo Lappalainen
- **mcp_can** (for standalone MCP2515 use)

<!--
Instructor Notes:

Timo Lappalainen's libraries are excellent:
- Well documented
- Active development
- Used by many marine projects

GitHub: https://github.com/ttlappalainen

Alternative: We can provide pre-configured Arduino portable folder.
-->

## OpenBridge Firmware

### Clone Repository

```bash
git clone https://github.com/[org]/openbridge.git
cd openbridge/src/VERSION\ 2/
```

### Configure Settings

Edit `openbridge.h`:

```cpp
// CAN bus speed (NMEA 2000 = 250kbps)
#define CAN_SPEED CAN_250KBPS

// MCP2515 crystal frequency (check your module!)
#define MCP_CLOCK MCP_16MHZ  // or MCP_8MHZ

// Chip select pin
#define MCP_CS_PIN 10

// Interrupt pin
#define MCP_INT_PIN 2
```

<!--
Instructor Notes:

IMPORTANT: Crystal frequency setting!

To check your module's crystal:
- Look at the small metal cylinder on the MCP2515 board
- It will be marked "16.000" or "8.000"
- 16.000 = 16 MHz
- 8.000 = 8 MHz

Wrong setting = CAN won't work at correct bitrate!
-->

### Upload Firmware

1. Connect Teensy via USB
2. Select Board: Tools → Board → Teensy 4.0 (or 4.1)
3. Select Port: Tools → Port → Teensy
4. Click Upload (→ button)
5. Press button on Teensy if prompted

### Verify Upload

Open Serial Monitor (Tools → Serial Monitor)
Set baud rate: 115200

You should see:
```
OpenBridge v2.0 initialized
CAN interface ready
Waiting for commands...
```

## Testing Your Build

### Test 1: Loopback Test

Connect CAN_H to CAN_L with a jumper (creates loopback)

Send test message:
```
40,1,10.5,45.0,1
```

You should receive back:
```
TX: PGN 130306 Wind Data
RX: PGN 130306 Wind Data
```

<!--
Instructor Notes:

Loopback test verifies:
- Teensy is working
- MCP2515 is communicating via SPI
- CAN TX and RX paths work

If this fails, check:
- SPI wiring
- Crystal frequency setting
- Power connections
-->

### Test 2: Connect to Test Network

**Only with instructor supervision!**

1. Connect to isolated test network
2. Monitor traffic:
   ```
   # In serial monitor, send:
   monitor
   ```
3. You should see NMEA 2000 messages scrolling

### Test 3: Send a Message

Send wind data to test network:
```
40,1,15.5,90.0,1
```

Verify on another monitor (OpenPlotter) that message appears.

## Command Reference

OpenBridge accepts CSV commands:

| Command ID | PGN | Description |
|------------|-----|-------------|
| 2 | 127250 | Vessel Heading |
| 4 | 129025 | Position Rapid Update |
| 5 | 129026 | COG & SOG Rapid Update |
| 40 | 130306 | Wind Data |
| 50 | 127488 | Engine Parameters Rapid |

### Example Commands

```
# Heading: 90 degrees magnetic
2,1,1.5708,0.0,0.0,1

# Position: 41.5°N, 71.4°W
4,41.5,-71.4

# Wind: 15 knots at 45 degrees apparent
40,1,15.0,45.0,1

# Engine: 2500 RPM
50,1,2500
```

<!--
Instructor Notes:

See openbridge.h for full command list.

Format: command_id,field1,field2,...

Units:
- Heading: radians
- Position: decimal degrees
- Wind speed: knots
- Wind angle: degrees
- RPM: revolutions per minute
-->

## Safety Considerations

### Electrical Safety

- Always disconnect USB before modifying wiring
- Check polarity before applying power
- Don't exceed voltage ratings

### Network Safety

- **NEVER connect to live vessel systems without authorization**
- All lab exercises use isolated test networks
- Understand you are generating real CAN traffic

### RF Considerations

- Keep wires short to reduce EMI
- Twisted pair for CAN_H/CAN_L recommended
- Proper termination reduces reflections

<!--
Instructor Notes:

CRITICAL safety briefing:
1. This hardware can affect real vessel systems
2. Spoofing navigation data is dangerous
3. All exercises on isolated networks only
4. Students sign ethics agreement

Legal: Even possessing tools to attack CAN bus
may have legal implications in some jurisdictions.
We're using these for EDUCATIONAL purposes only.
-->

## Troubleshooting

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| No serial output | Wrong COM port | Check Tools → Port |
| "CAN init failed" | SPI wiring | Verify connections |
| Wrong bitrate | Crystal mismatch | Check MCP_CLOCK setting |
| TX but no RX | Missing termination | Add 120Ω resistor |
| Garbage characters | Wrong baud rate | Set to 115200 |
| Teensy not recognized | Driver issue | Install Teensyduino |

## Lab Preview: Week 4

In Lab 04, you will:

1. Assemble your OpenBridge hardware
2. Flash and configure firmware
3. Verify operation with loopback test
4. Connect to class test network
5. Send and receive test messages
6. Document your build with photos

**Bring**: Soldering iron (if headers need soldering)

## Homework

### Required

1. **Order hardware** (if not provided by instructor)
2. **Install** Arduino IDE and Teensyduino
3. **Read** OpenBridge README
4. **Watch** [Suggested] "SPI Explained" (YouTube)

### Suggested

- Review: Teensy pinout diagram
- Explore: NMEA2000 library examples
- Read: MCP2515 datasheet (functional description)

## Discussion Questions

1. Why use SPI instead of UART for the CAN controller?
2. What happens if termination resistors are missing?
3. How could an attacker use this hardware maliciously?
4. Why is open-source hardware important for security research?

## References

- [PJRC Teensy Documentation]
- [MCP2515 Datasheet]
- [NMEA2000 Library]
- [OpenBridge GitHub]

[PJRC Teensy Documentation]:https://www.pjrc.com/teensy/
[MCP2515 Datasheet]:https://ww1.microchip.com/downloads/en/DeviceDoc/MCP2515-Stand-Alone-CAN-Controller-with-SPI-20001801J.pdf
[NMEA2000 Library]:https://github.com/ttlappalainen/NMEA2000
[OpenBridge GitHub]:https://github.com/[org]/openbridge

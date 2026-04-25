---
title: "Technology Requirements"
subtitle: "Maritime OT Security Course"
author: "Constantine Macris"
date: "2026"
---

# Technology Requirements: Maritime OT Security

## Table of Contents

1. [Overview](#overview)
2. [Hardware Requirements](#hardware-requirements)
3. [Software Requirements](#software-requirements)
4. [Lab Infrastructure](#lab-infrastructure)
5. [Network Configuration](#network-configuration)
6. [Budget Planning](#budget-planning)
7. [Vendor Information](#vendor-information)
8. [Alternative Configurations](#alternative-configurations)

---

## Overview

This document specifies all technology requirements for offering the Maritime OT Security course. The course emphasizes low-cost, open-source solutions to ensure accessibility for institutions with limited budgets.

**Design principles**:
- Student hardware cost under $55 per person (NEMO PCB-based kit)
- Preference for open-source software (no licensing fees)
- Open hardware: KiCad PCB files released, fabricated by any low-cost service (e.g., JLCPCB) or available pre-built from the NEMO maintainers
- Reproducible setup at any institution

**Minimum class size**: 8 students
**Maximum recommended**: 24 students (for one instructor without TA)

---

## Hardware Requirements

### Per-Student Hardware Kit

Each student (or pair of students) needs the following components to build a NEMO board. NEMO is a custom PCB built around the Teensy 4.0's two native FlexCAN controllers — there is **no external CAN controller** (no MCP2515). PCB design files (KiCad 9.0) and 3D-printable case STLs live in the [Soups71/NEMO](https://github.com/Soups71/NEMO) repository.

| Component | Specification | Quantity | Unit Cost | Source | Total |
|-----------|---------------|----------|-----------|--------|-------|
| **Teensy 4.0** | NXP i.MX RT1062, ARM Cortex-M7 @ 600 MHz, dual FlexCAN | 1 | $23.80 | PJRC.com / SparkFun DEV-15583 | $23.80 |
| **TJA1050 CAN Transceiver** | 5V high-speed CAN transceiver (one per bus) | 2 | $1.50 | Amazon / DigiKey | $3.00 |
| **SH1106 128×64 OLED** | I2C, monochrome | 1 | $5.00 | Amazon | $5.00 |
| **10kΩ Potentiometer** | Panel-mount, linear taper | 3 | $0.50 | Amazon | $1.50 |
| **Tactile Push Button** | THT, 6 mm body | 4 | $0.20 | Amazon | $0.80 |
| **NMEA 2000 M12 Connector** | Field-attachable, female (micro-C) | 1 | $8–$15 | RS Components / DigiKey | $8.00–$15.00 |
| **3-Pin Screw Terminal** | 5 mm pitch | 1 | $0.50 | Amazon | $0.50 |
| **Custom NEMO PCB** | KiCad files in NEMO repo | 1 | $2–$5 | JLCPCB.com (or equiv.) | $2.00–$5.00 |
| **USB Micro-B Cable** | Power + programming + serial | 1 | $3.00 | Amazon | $3.00 |
| | | | **Per-student total** | | **$47.60–$57.60** |

**Two procurement paths**:

- **Path A — DIY** (recommended for the educational experience): order the PCB and components per the BOM above, then have students assemble per Lab 04. Adds ~2 weeks of PCB fab lead time to the timeline.
- **Path B — Pre-built**: email `nemo@jamescampbell.org` with subject "Board Request" to coordinate shipped, pre-assembled NEMO boards. Use this when soldering capacity or schedule does not allow Path A.

**Optional but recommended**:
- **3D-printed enclosure** (~$1 in filament): STLs in the NEMO repo; protects the board and gives students a finished product to pocket
- **Logic analyzer** ($8): Shared among groups for I2C / OLED debugging (USB Logic Analyzer 8CH)
- **Carrying case** ($5): Protection for hardware kit

#### Hardware Notes

**Teensy 4.0 vs 4.1**:
- Teensy 4.0 is the canonical NEMO MCU and matches the PCB footprint
- Teensy 4.1 has more I/O, Ethernet PHY, and an SD card slot but is **not a drop-in** for the NEMO PCB — only switch if you also redo the board
- Both have the same dual FlexCAN; either works at the firmware level

**TJA1050 vs Alternatives**:
- The NEMO PCB is laid out for two TJA1050s (one per bus)
- TJA1051 is electrically compatible and acceptable
- Verify the part is the **5V** variant — NEMO routes 5V to the transceivers

**OLED Driver Chip**:
- NEMO firmware uses `VEGA_SH1106` plus Adafruit GFX
- Some Amazon listings ship SSD1306 modules in identical-looking packaging; verify SH1106 before ordering
- I2C address typically 0x3C; a few modules use 0x3D — confirm in the firmware if using a non-default

**Cable Specifications**:
- CAN requires twisted pair (reduces EMI)
- Standard: CAT5/CAT6 cable works well (use one pair)
- Industrial: NMEA 2000 micro-C or DeviceNet cable (more expensive but field-correct)
- Length: 1-2 meters sufficient for lab benches; commercial NMEA 2000 networks have 120Ω termination built in

#### Procurement Timeline (Path A — DIY)

**8 weeks before semester start**:
- Decide procurement path (A vs B). Path B (pre-built) skips the PCB fab steps below — coordinate with `nemo@jamescampbell.org` for ship date
- Place PCB order at JLCPCB (or equivalent): export gerbers from `Soups71/NEMO/PCB/NEMO.kicad_pro`, upload, order quantity = (class size × 1.2) for 20% spares. Typical fab + ship time is 2–3 weeks
- Optionally enable JLCPCB's SMD assembly service for the surface-mount parts (TJA1050s, decoupling caps); this raises per-board cost slightly but eliminates the hardest soldering step

**6 weeks before semester start**:
- Place bulk order for Teensy 4.0 boards (PJRC.com — educational discount on 20+)
- Order TJA1050 transceivers, OLEDs, pots, buttons, screw terminals, USB cables (Amazon / DigiKey)
- Order NMEA 2000 M12 connectors (RS Components / DigiKey — slowest line item)

**4 weeks before**:
- Receive PCBs and components; inspect against BOM
- Assemble 2-3 spare kits (for failures/loaners)
- Build one complete reference kit end-to-end and verify boot + Live Data

**2 weeks before**:
- Prepare kit bags/boxes for each student
- Label kits with inventory checklist
- Pre-flash firmware on the Teensy if you want students to skip Part 4 of Lab 04 on day 1

**Week 1**:
- Distribute kits to students
- Collect checkout forms (students responsible for return)

#### Recommended Vendors

**Primary sources**:
- **PJRC.com**: Teensy 4.0 boards (official source, reliable)
- **JLCPCB**: Custom NEMO PCB fabrication (KiCad files in [Soups71/NEMO](https://github.com/Soups71/NEMO/tree/main/PCB))
- **NEMO maintainers**: Pre-built boards via `nemo@jamescampbell.org` (Path B)
- **Amazon**: TJA1050s, OLEDs, pots, buttons, USB cables, screw terminals
- **DigiKey / Mouser**: M12 NMEA 2000 connectors, precision components, resistors
- **RS Components**: NMEA 2000-grade M12 micro-C field connectors

**Bulk pricing**:
- PJRC offers educational discounts for orders of 20+ Teensy 4.0 boards (`sales@pjrc.com`)
- JLCPCB volume discounts kick in at 5+ boards; combine with neighboring instructors if needed
- Pre-built board pricing depends on quantity; contact `nemo@jamescampbell.org` for a quote

**Spare parts inventory**:
- Keep 15-20% extra components for failures (PCB fab is slow; you don't want to wait 3 weeks mid-semester for a replacement)
- Most common failures: USB cables, OLED solder joints, button caps

---

### Instructor / Lab Infrastructure Hardware

The instructor station provides traffic generation and network backbone.

| Component | Specification | Quantity | Unit Cost | Total |
|-----------|---------------|----------|-----------|-------|
| **Raspberry Pi 4** | 4GB or 8GB RAM | 1-3 | $55-75 | $165 |
| **CAN Hat** | Waveshare 2-CH CAN or PiCAN2 | 1-3 | $25 | $75 |
| **MicroSD Card** | 32GB Class 10, A1 rating | 1-3 | $8 | $24 |
| **Power Supply** | USB-C 3A official Raspberry Pi PSU | 1-3 | $8 | $24 |
| **Ethernet Switch** | 8-port gigabit (for management) | 1 | $25 | $25 |
| **CAN Bus Cable** | 25-50m spool, twisted pair | 1 | $30 | $30 |
| **Screw Terminals** | For CAN bus distribution | 10 | $3 | $30 |
| **120Ω Terminators** | Professional CAN terminators (DB9) | 4 | $8 | $32 |
| **Power Strip** | 12-outlet for student stations | 2 | $20 | $40 |
| **USB Hub** | 10-port powered hub (for Teensy programming) | 1 | $30 | $30 |
| **Storage Cabinet** | Lockable, for equipment storage | 1 | $150 | $150 |
| | | | **Infrastructure total** | **$625** |

**Optional but enhances experience**:
- **Chart Plotter Display** ($200-500): Garmin or Raymarine to show spoofed navigation data visually
- **OpenPlotter Node** ($100): Pre-configured Raspberry Pi with NMEA 2000 simulator
- **Network TAP** ($50): Passive monitoring device for demonstrations
- **Projector / Large Display** ($300-500): To show network traffic in real-time
- **Video Camera** ($100): Record capstone exercise for post-mortem analysis

#### Infrastructure Configurations

**Minimal Configuration** (1 instructor station):
- Single Raspberry Pi with CAN hat generating traffic
- All students connect to single shared CAN bus
- Cost: ~$200 + student kits

**Recommended Configuration** (2-3 instructor stations):
- Multiple isolated CAN networks
- Allows simultaneous different labs (e.g., one group on attacks, another on detection)
- Cost: ~$500-600 + student kits

**Advanced Configuration** (with physical simulators):
- Helm simulator with autopilot
- Engine control simulator
- Chart plotter displays
- Cost: ~$2000-3000 + student kits

### Shared Lab Equipment

Equipment that students share (not per-person):

| Equipment | Purpose | Quantity | Cost | Notes |
|-----------|---------|----------|------|-------|
| **Oscilloscope** | Viewing CAN differential signals, I2C debug | 1-2 | $400 | Entry-level DSO (Rigol DS1054Z) |
| **Logic Analyzer** | Capture I2C / GPIO for OLED and button debug | 2-4 | $50-200 | USB logic analyzer or Saleae clone |
| **Multimeter** | Voltage, continuity testing on populated PCBs | 4-6 | $20 | Basic digital multimeter sufficient |
| **Soldering Station** | Populating NEMO PCB (THT + optional SMD rework) | 2-4 | $40 | Temperature-controlled — required for Path A |
| **Fume Extractor** | Soldering safety | 1-2 | $30 | Fan with filter |
| **Wire Stripper** | Cable preparation | 2-4 | $10 | Automatic stripper recommended |
| **Heat Shrink Kit** | Cable management | 1 | $15 | Assorted sizes |
| | | **Shared equipment total** | **~$1200** | |

**Lab safety equipment**:
- Fire extinguisher (Type C for electrical)
- First aid kit
- Safety glasses (for soldering)
- ESD wrist straps (optional but recommended)

---

## Software Requirements

All software for this course is **open-source and free**.

### Student Laptop Requirements

**Operating System**: Linux preferred (Ubuntu 20.04+ or Debian 11+)
- Windows 10/11 with WSL2 or VM also supported
- macOS possible but requires more setup (limited `can-utils` support)

**Minimum specs**:
- CPU: Dual-core 2.0 GHz or better
- RAM: 8GB (16GB recommended for ML labs)
- Storage: 20GB free space
- USB: At least one USB-A or USB-C port

**Administrator access**: Required for installing software and configuring network interfaces

### Required Software Stack

#### 1. Embedded Development Environment

NEMO uses the [PlatformIO](https://platformio.org/) build system inside Visual Studio Code. PlatformIO handles the Teensyduino toolchain and library dependencies (NMEA2000, NMEA2000_Teensyx, U8g2, Adafruit GFX, VEGA_SH1106) automatically — students do not need to install Arduino IDE.

**Visual Studio Code**:
- Download: https://code.visualstudio.com
- Platforms: Windows, macOS, Linux

**PlatformIO IDE extension**:
- Install from the VS Code Extensions panel (Ctrl+Shift+X / Cmd+Shift+X)
- Search "PlatformIO IDE" → Install
- First launch downloads the toolchain (a few minutes — do this before lab day)

**Teensyduino**:
- Download: https://www.pjrc.com/teensy/td_download.html
- Provides the Teensy Loader (the GUI utility that pushes firmware to the board) and udev rules
- Skip the Arduino IDE step in the installer — PlatformIO doesn't need it

**Installation instructions**:
```bash
# Linux (apt-based)
sudo apt-get update
sudo apt-get install code  # if not already installed

# Download Teensyduino installer (Linux x64)
wget https://www.pjrc.com/teensy/td_159/TeensyduinoInstall.linux64
chmod +x TeensyduinoInstall.linux64
./TeensyduinoInstall.linux64

# udev rules for Teensy programming (Linux)
sudo cp 00-teensy.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules

# Windows/macOS: Use graphical installers for VS Code, PlatformIO, Teensyduino
```

**Note on libraries**: `SRC/platformio.ini` declares all firmware dependencies. PlatformIO downloads them on first build. Use **`NMEA2000_Teensyx`** (the FlexCAN driver) — NEMO does **not** use `NMEA2000_mcp` or any MCP2515-based path.

**Required Arduino Libraries**:
- FlexCAN_T4 (for Teensy 4.x CAN support)
- SPI (included with Arduino)

#### 2. CAN Bus Tools

**can-utils** (Linux):
- Suite of command-line tools for CAN
- Tools used: `candump`, `cansend`, `canplayer`, `cansniffer`
- Essential for traffic capture and injection

```bash
# Ubuntu/Debian
sudo apt-get install can-utils

# Arch Linux
sudo pacman -S can-utils

# Compile from source (if not in package manager)
git clone https://github.com/linux-can/can-utils
cd can-utils
./autogen.sh
./configure
make
sudo make install
```

**SocketCAN** (Linux kernel module):
- Usually included in modern kernels (3.x+)
- Provides virtual CAN interfaces

```bash
# Load kernel modules
sudo modprobe can
sudo modprobe can_raw
sudo modprobe vcan

# Verify
lsmod | grep can
```

**Windows alternative**: PCAN-View (free from PEAK-System)

#### 3. Network Analysis Tools

**Wireshark**:
- Version: 3.x or 4.x
- CAN dissector support required
- Download: https://www.wireshark.org

```bash
# Ubuntu/Debian
sudo apt-get install wireshark

# Add user to wireshark group (for non-root capture)
sudo dpkg-reconfigure wireshark-common
sudo usermod -a -G wireshark $USER
```

**Configuration**:
- Enable SocketCAN interface capture
- Import CAN database (.dbc) files if available

#### 4. Python Environment

**Python Version**: 3.8, 3.9, 3.10, or 3.11
- Python 3.7 minimum, 3.12 may have library compatibility issues

**Package manager**: pip3 or conda

**Required Python libraries**:

```bash
# Create virtual environment (recommended)
python3 -m venv maritime-ot-venv
source maritime-ot-venv/bin/activate  # Linux/macOS
# OR
maritime-ot-venv\Scripts\activate  # Windows

# Install dependencies
pip install --upgrade pip
pip install numpy pandas matplotlib seaborn
pip install scikit-learn scipy
pip install torch torchvision  # PyTorch for LSTM labs
pip install jupyter notebook jupyterlab
pip install cantools python-can  # CAN parsing libraries
```

**requirements.txt** (provide to students):
```
numpy>=1.21.0
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
scikit-learn>=1.0.0
scipy>=1.7.0
torch>=1.10.0
jupyter>=1.0.0
cantools>=36.0.0
python-can>=4.0.0
```

#### 5. Version Control

**Git**:
- For cloning course repository
- Submission of lab reports (if using Git workflow)

```bash
# Ubuntu/Debian
sudo apt-get install git

# Windows: Git for Windows
# Download from https://git-scm.com/download/win
```

#### 6. Optional but Recommended

**Visual Studio Code**:
- Modern code editor with Python support
- Extensions: Python, Jupyter, C/C++ (for Arduino)
- Download: https://code.visualstudio.com

**Jupyter Notebook**:
- Included in Python requirements
- Used for ML labs and data analysis

**SQLite Browser**:
- For exploring PGN database (optional lab extension)
- Download: https://sqlitebrowser.org

---

## Lab Infrastructure

### Physical Lab Setup

#### Lab Room Requirements

**Space**:
- Minimum: 500 sq ft for 12 students (42 sq ft per pair)
- Preferred: 800-1000 sq ft for 24 students + instructor station
- Ceiling height: Standard 8-10 ft

**Furniture**:
- Lab benches or tables: 6 ft x 2.5 ft per pair
- Adjustable-height chairs
- Instructor desk with demo station
- Storage cabinet (lockable)
- Whiteboard or projector screen

**Electrical**:
- Power outlets: At least 2 per student station
- Dedicated circuits for high-power equipment (soldering)
- UPS backup for instructor station (recommended)

**Network**:
- Air-gapped from campus network (CRITICAL for security)
- Ethernet for management/file sharing (isolated)
- WiFi disabled or separate SSID

**Environmental**:
- Adequate ventilation (for soldering)
- Climate control (sensitive electronics)
- Good lighting (overhead + task lighting)

#### Network Topology

**Isolated CAN Network Design**:

```
                    [Instructor Station]
                          (Raspberry Pi + CAN Hat)
                                  |
                                [CAN Bus]
                                  |
              +-------------------+-------------------+
              |                   |                   |
         [Student 1]         [Student 2]    ...  [Student N]
            (NEMO)              (NEMO)             (NEMO)
```

**Physical wiring**:
- Linear bus topology (daisy-chain, NOT star!)
- CAN_H and CAN_L twisted pair
- 120Ω termination at both physical ends
- Maximum bus length: 40m @ 250kbps

**Management network** (separate from CAN):
- Ethernet switch for file sharing, remote access
- No connection to campus network or internet
- Instructor laptop can bridge (for software updates)

### Virtual Machine Option

For institutions without dedicated lab space, provide VM image:

**VM Specifications**:
- Base OS: Ubuntu 22.04 LTS Desktop
- RAM: 4GB allocated (8GB host minimum)
- Storage: 25GB virtual disk
- USB: USB 2.0/3.0 passthrough enabled

**Pre-installed software**:
- All software from requirements list
- Course materials cloned in `/home/student/maritime-ot-security`
- Virtual CAN interfaces (vcan0) configured
- Sample PCAP files for analysis

**VM distribution**:
- Format: OVA (Open Virtualization Appliance)
- Compression: ~8GB download
- Platforms: VirtualBox (recommended), VMware, Hyper-V

**Limitations of VM approach**:
- USB passthrough can be finicky (Teensy programming)
- Cannot fully replicate physical CAN bus
- No hands-on hardware assembly experience
- Best used as supplement, not replacement

---

## Network Configuration

### CAN Bus Physical Layer

**NMEA 2000 Standard Parameters**:
- **Bitrate**: 250 kbps (standard, do not change)
- **Cable**: Twisted pair, 120Ω characteristic impedance
- **Voltage**: CAN_H = 3.5V, CAN_L = 1.5V (recessive), differential 2V (dominant)
- **Termination**: 120Ω resistors at both physical ends of bus
- **Topology**: Linear bus (not star, not ring)

**Network sizing**:
- Maximum nodes: 254 (NMEA 2000 limit)
- Maximum bus length: 200m @ 250kbps (practical: <100m)
- Maximum stub length: 6m from backbone to node

**Configuration command** (Linux SocketCAN):
```bash
# Bring up CAN interface at 250kbps
sudo ip link set can0 type can bitrate 250000
sudo ip link set can0 up

# Verify
ip -details link show can0
```

### Virtual CAN Interfaces (for testing)

Useful for development without physical hardware:

```bash
# Load virtual CAN module
sudo modprobe vcan

# Create virtual interface
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

# Test
cansend vcan0 123#DEADBEEF
candump vcan0
```

### Traffic Generation (Instructor Station)

**OpenPlotter Configuration**:
- Install Signal K server (generates NMEA 2000 data)
- Configure CAN output
- Simulate vessel moving on chart

**Alternatives**:
- canboat analyzer with replay files
- Python scripts using python-can library
- Pre-recorded PCAP files with canplayer

**Sample traffic script**:
```python
#!/usr/bin/env python3
import can
import time

bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Simulate position message (PGN 129025) every 1 second
while True:
    msg = can.Message(
        arbitration_id=0x09F10D23,  # Priority 0, PGN 129025, SA 0x23
        data=[0xFF, 0x7F, 0xFB, 0xFF, 0xFF, 0x7F, 0xFF, 0xFF],
        is_extended_id=True
    )
    bus.send(msg)
    time.sleep(1.0)
```

### Firewall and Access Control

**Lab network security**:
- No internet access from lab machines (air-gapped)
- Instructor laptop can bridge for updates (temporary)
- File sharing: Local NFS or SMB server on instructor machine

**Campus IT coordination**:
- Notify security team about isolated network
- Ensure no accidental connection to production networks
- Document network isolation in lab procedures

---

## Budget Planning

### Budget Summary by Class Size

**Cost per student**: ~$50 (NEMO hardware kit; range $48–$58 depending on M12 connector and PCB fab pricing)
**Fixed costs**: $625 (infrastructure) + $1200 (shared equipment) = $1825

| Class Size | Student Kits | Infrastructure | Shared Equip | Total | Per Student |
|------------|--------------|----------------|--------------|-------|-------------|
| 10 students | $500 | $625 | $1200 | $2,325 | $232.50 |
| 15 students | $750 | $625 | $1200 | $2,575 | $171.67 |
| 20 students | $1,000 | $625 | $1200 | $2,825 | $141.25 |
| 24 students | $1,200 | $625 | $1200 | $3,025 | $126.04 |

**Amortization**: Infrastructure and shared equipment last 5+ years, so effective per-student cost decreases with multiple course offerings.

### Funding Sources

**Internal**:
- Department instructional budget
- Lab fee ($50-100 per student)
- College technology refresh funds

**External**:
- NSF grants (cybersecurity education initiatives)
- Department of Homeland Security (maritime security focus)
- Industry partnerships (classification societies, shipping companies)
- Alumni donations

**Cost recovery**:
- Students keep hardware kits (factor into course fee)
- OR collect kits at semester end for reuse (reduces long-term cost)

### Cost Reduction Strategies

**Hardware**:
- Bulk purchasing (20+ Teensy 4.0 boards = educational discount from PJRC)
- Single combined PCB run from JLCPCB across all sections (volume discount)
- Pair students instead of individual kits (halves hardware cost)
- Reuse boards from previous semesters (NEMO PCBs are durable; replace consumables only)
- Skip the 3D-printed enclosure for cost-sensitive offerings

**Software**:
- Already 100% open-source (no licensing fees)

**Lab infrastructure**:
- Start with minimal configuration (1 Raspberry Pi)
- Add additional nodes as budget allows
- Use existing lab computers instead of dedicated machines

### Maintenance and Replacement

**Annual costs** (estimated):
- Component replacement: 10-15% of initial hardware ($50-75 for 20 students)
- Consumables: Solder, wire, resistors ($50)
- Total ongoing: ~$100-150/year

**Replacement schedule**:
- Teensy 4.0 boards: 5+ years (very reliable)
- NEMO PCBs: 5+ years (no electromechanical wear; replace if physically damaged)
- TJA1050 transceivers: 5+ years (most common failure point is solder fatigue, not the IC)
- OLEDs: 3-5 years (the displays themselves dim slowly under heavy use)
- Buttons / pots: 2-3 years (mechanical wear)
- Cables: 3-5 years
- Raspberry Pi: 5+ years
- Oscilloscope / shared equipment: 10+ years

---

## Vendor Information

### Primary Vendors

#### PJRC (Teensy)
- **Website**: https://www.pjrc.com
- **Contact**: sales@pjrc.com
- **Shipping**: USA (2-5 business days), international available
- **Educational discount**: Available for 20+ units
- **Notes**: Official source, excellent support, USA-based

#### JLCPCB (NEMO PCB fabrication)
- **Website**: https://jlcpcb.com
- **Products**: Custom PCB fab from KiCad files; optional SMD assembly service
- **Advantages**: Very low per-board cost ($2–$5 for small qty), reliable quality, optional SMT assembly removes the hardest soldering step
- **Disadvantages**: 2–3 week lead time including shipping; minimum batch size (typically 5 boards)
- **Recommendation**: Order in bulk for the whole class; use KiCad files in [Soups71/NEMO/PCB](https://github.com/Soups71/NEMO/tree/main/PCB)

#### NEMO Maintainers (Pre-built boards, Path B)
- **Contact**: `nemo@jamescampbell.org`
- **Subject line**: "Board Request"
- **Use when**: your program lacks soldering capacity, the schedule does not allow PCB fab lead time, or you are running an evening class / workshop and need turnkey hardware
- **Pricing**: depends on quantity and assembly state; contact for quote

#### Amazon
- **Products**: TJA1050 transceivers, OLEDs, pots, buttons, screw terminals, USB cables
- **Advantages**: Fast shipping (Prime), easy returns
- **Disadvantages**: Variable quality (especially OLED driver chip variants), some counterfeit components
- **Recommendation**: Check reviews; verify OLED is SH1106 (not SSD1306); buy 20% extras

#### DigiKey
- **Website**: https://www.digikey.com
- **Products**: Resistors, connectors, professional-grade components
- **Advantages**: Reliable, datasheets available, good for small quantities
- **Disadvantages**: Higher prices than bulk Chinese suppliers
- **Recommendation**: Use for precision components (resistors, terminators)

#### Mouser Electronics
- **Website**: https://www.mouser.com
- **Similar to DigiKey**: Professional component distributor
- **Advantages**: Sometimes better pricing, good international shipping

#### Adafruit
- **Website**: https://www.adafruit.com
- **Products**: CAN transceivers, prototyping supplies, educational kits
- **Advantages**: High quality, tutorials, USA-based
- **Disadvantages**: Higher prices
- **Recommendation**: Good for instructor demo kits

#### SparkFun
- **Website**: https://www.sparkfun.com
- **Similar to Adafruit**: Education-focused electronics retailer

#### AliExpress (budget option)
- **Website**: https://www.aliexpress.com
- **Products**: TJA1050 ICs, OLEDs, buttons, pots, USB cables
- **Advantages**: Very low cost (often 1/3 of Amazon)
- **Disadvantages**: 3-6 week shipping, variable quality, no easy returns
- **Recommendation**: Order early, buy extras, test thoroughly

### Purchasing Workflow

**Step 1: Centralized ordering** (instructor or department coordinator)
- Consolidate orders for bulk pricing
- Single vendor per component type if possible

**Step 2: Receiving and inventory**
- Check shipments against packing slips
- Test 10% of components before distributing
- Store in labeled bins

**Step 3: Kit assembly**
- Assemble into individual student kits
- Label with inventory checklist
- Bag or box for distribution

**Step 4: Distribution**
- Issue kits in Week 1 or Week 4 (depending on course structure)
- Collect signed checkout forms
- Note serial numbers if applicable

**Step 5: End-of-semester return** (if kits are not kept by students)
- Inspect for damage
- Replace consumables (wires, resistors)
- Replenish inventory for next semester

---

## Alternative Configurations

### Low-Budget Option (<$1000 total)

**Changes**:
- Pair students (12 students = 6 NEMO kits)
- Procurement Path B (pre-built boards from `nemo@jamescampbell.org`) to skip soldering equipment
- Single Raspberry Pi instructor station
- No oscilloscope (use $10 USB logic analyzer only)
- Reuse boards semester-to-semester

**Cost breakdown**:
- 6 NEMO kits @ $50 = $300
- 1 Raspberry Pi setup = $100
- Logic analyzers and shared tools = $200
- Cables and infrastructure = $100
- **Total**: ~$700

**Trade-offs**:
- Limited to smaller class sizes
- Students share hardware (less hands-on time)
- Harder to debug issues without oscilloscope

### High-End Option ($5000+ total)

**Enhancements**:
- Individual kits for 24 students
- 3 Raspberry Pi stations (multiple networks)
- Chart plotter displays ($500 each)
- Professional logic analyzer (Saleae)
- Helm simulator with autopilot
- Video recording system for capstone
- Spare kit inventory (20% extra)

**Benefits**:
- Better learning experience
- More realistic scenarios
- Easier troubleshooting
- Parallel labs (attack/defense simultaneously)

### Online/Hybrid Option

**For remote students**:
- Ship hardware kits to students ($10 shipping each)
- Provide VM image for software environment
- Remote access to instructor CAN network (VPN + virtual CAN bridge)
- Zoom/Teams for lab sessions with screen sharing

**Additional costs**:
- Shipping: $10 per student
- Virtual infrastructure: Server for remote access ($500)
- Course management: LMS integration ($0 if using existing)

**Challenges**:
- Hardware troubleshooting at distance
- Synchronous lab time coordination
- Assessment integrity (exams)

### Raspberry Pi as Student Device (NEMO Alternative)

**Option**: Use Raspberry Pi Zero W + CAN hat instead of NEMO

**Pros**:
- Linux environment directly on device
- WiFi for remote access
- More familiar for students

**Cons**:
- Comparable cost (~$30 for Pi Zero + $25 for CAN hat = $55 vs ~$50 for NEMO)
- Single CAN bus only (no dual-bus inject + monitor architecture)
- Larger form factor; no integrated UI
- Requires microSD card management
- Power consumption higher
- Cannot run the NEMO firmware as-is — different software stack

**Verdict**: NEMO is the canonical platform for this curriculum. Its dual-bus architecture is the reason the IDS labs (lab_09 onward) work as designed. The Raspberry Pi alternative is suitable only for limited-scope variants of the course.

---

## Software Licensing and Open Source

### All Software is Free and Open Source

**Course philosophy**: No proprietary software or licensing fees
- Ensures accessibility
- Students can continue using tools after course
- Reproducible at any institution

### License Summary

| Software | License | Commercial Use | Redistribution |
|----------|---------|----------------|----------------|
| Arduino IDE | GPL / LGPL | Yes | Yes |
| Teensyduino | MIT (mostly) | Yes | Yes |
| can-utils | GPL v2 | Yes | Yes |
| Wireshark | GPL v2 | Yes | Yes |
| Python | PSF License | Yes | Yes |
| NumPy/Pandas/etc | BSD | Yes | Yes |
| PyTorch | BSD-style | Yes | Yes |
| scikit-learn | BSD | Yes | Yes |
| OpenPlotter | GPL v3 | Yes | Yes |
| Course Materials | CC BY-SA 4.0 | Yes | Yes with attribution |

**No license compliance issues**: All tools are GPL-compatible or more permissive

---

## Technical Support Resources

### Manufacturer Support

**PJRC (Teensy)**:
- Forum: https://forum.pjrc.com
- Very active community, Paul Stoffregen (creator) responds directly
- Excellent documentation and tutorials

**Arduino**:
- Forum: https://forum.arduino.cc
- Extensive tutorials and examples
- Reference documentation

**python-can library**:
- GitHub: https://github.com/hardbyte/python-can
- Documentation: https://python-can.readthedocs.io
- Active development

### Student Resources (Provide These Links)

- Course GitHub repository
- CAN bus protocol references (Bosch specification)
- NMEA 2000 PGN library
- OpenBridge project documentation
- Stack Overflow (for programming questions)
- Linux CAN documentation (https://www.kernel.org/doc/html/latest/networking/can.html)

### Instructor Support Network

- Maritime cybersecurity education community
- NICE K-12 Cybersecurity Education resources
- CAE-CDE (Centers of Academic Excellence in Cyber Defense Education)
- Industry contacts (classification societies, maritime companies)

---

## Appendix: Sample Purchase Order

### Bill of Materials for 20-Student Class

**Vendor: PJRC.com**
| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| Teensy 4.0 | 22 | $23.80 | $523.60 |
| Shipping | | | $15.00 |
| **PJRC Total** | | | **$538.60** |

**Vendor: JLCPCB (NEMO PCB fabrication)**
| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| NEMO PCB (5-up panel, 5 panels = 25 boards) | 25 | $1.00 | $25.00 |
| SMD assembly service (TJA1050s + caps, optional) | 25 | $5.00 | $125.00 |
| Shipping | | | $25.00 |
| **JLCPCB Total** | | | **$175.00** |

**Vendor: Amazon**
| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| TJA1050 CAN Transceiver (10-pack, if not pre-assembled) | 5 | $7.00 | $35.00 |
| SH1106 128×64 OLED I2C | 25 | $5.00 | $125.00 |
| 10kΩ Potentiometer (linear, panel-mount) | 75 | $0.50 | $37.50 |
| Tactile push button (THT, 100-pack) | 1 | $8.00 | $8.00 |
| 3-pin screw terminal (10-pack) | 3 | $5.00 | $15.00 |
| USB Micro-B cable (5-pack) | 5 | $10.00 | $50.00 |
| **Amazon Total** | | | **$270.50** |

**Vendor: DigiKey / RS Components**
| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| NMEA 2000 M12 micro-C connector (female, field-attachable) | 25 | $10.00 | $250.00 |
| 120Ω resistors (1/4W, 100-pack) — for bench-only termination | 1 | $8.50 | $8.50 |
| CAN cable (twisted pair, 50m) | 1 | $35.00 | $35.00 |
| Shipping | | | $15.00 |
| **DigiKey Total** | | | **$308.50** |

**Vendor: Adafruit (Instructor Station)**
| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| Raspberry Pi 4 (4GB) | 2 | $55.00 | $110.00 |
| Waveshare CAN Hat | 2 | $25.00 | $50.00 |
| MicroSD 32GB | 2 | $8.00 | $16.00 |
| USB-C Power Supply | 2 | $8.00 | $16.00 |
| Shipping | | | $10.00 |
| **Adafruit Total** | | | **$202.00** |

**Grand Total**: $1,494.60 (~$75/student for 20-student class with 5 spare boards)

*(Add shared equipment and infrastructure as needed per budget. M12 connectors dominate the per-board cost. For tighter budgets, substitute a second 3-pin screw terminal for the M12 — the network connection is then bench-only.)*

**Path B alternative** (pre-built boards):
- 22 NEMO boards (20 students + 2 spares) via `nemo@jamescampbell.org`: contact for current pricing, typical range $60–$90 per board fully assembled
- Eliminates JLCPCB + Amazon component lines (saves ~$445 in parts coordination overhead but raises per-board cost)
- Recommended for programs without soldering capacity or with very short procurement windows

---

**Document Version**: 2.0 (NEMO PCB migration)
**Last Updated**: 2026-04-25
**Author**: Constantine Macris
**License**: CC BY-SA 4.0

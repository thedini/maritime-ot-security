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
- Student hardware cost under $50 per person
- Preference for open-source software (no licensing fees)
- Standard off-the-shelf components (no custom fabrication)
- Reproducible setup at any institution

**Minimum class size**: 8 students
**Maximum recommended**: 24 students (for one instructor without TA)

---

## Hardware Requirements

### Per-Student Hardware Kit

Each student (or pair of students) needs the following components to build an OpenBridge CAN interface:

| Component | Specification | Quantity | Unit Cost | Source | Total |
|-----------|---------------|----------|-----------|--------|-------|
| **Teensy 4.0 or 4.1** | ARM Cortex-M7 @ 600MHz, 1MB RAM | 1 | $23.80 | PJRC.com | $23.80 |
| **MCP2515 CAN Module** | SPI-to-CAN controller with oscillator | 1 | $4.50 | Amazon/AliExpress | $4.50 |
| **TJA1050 Transceiver** | CAN transceiver (usually included on MCP2515 board) | 1 | $0 | Included | $0 |
| **Solderless Breadboard** | 400 or 830 tie-points | 1 | $3.50 | Amazon | $3.50 |
| **Jumper Wire Kit** | Male-male, male-female, various lengths | 1 set | $5.00 | Amazon | $5.00 |
| **USB Cable** | Micro-B (Teensy 4.0) or Micro-B/C (Teensy 4.1) | 1 | $3.00 | Amazon | $3.00 |
| **CAN Cable** | 2-conductor twisted pair, 1-2 meters | 1 | $2.00 | DigiKey/Local | $2.00 |
| **120Ω Resistors** | 1/4W termination resistors | 2 | $0.20 | DigiKey | $0.40 |
| | | | **Per-student total** | | **$42.20** |

**Optional but recommended**:
- **Soldering iron kit** ($15-25): If students solder headers on Teensy (more permanent)
- **Logic analyzer** ($8): Shared among groups for SPI debugging (USB Logic Analyzer 8CH)
- **Carrying case** ($5): Protection for hardware kit

#### Hardware Notes

**Teensy 4.0 vs 4.1**:
- Teensy 4.0: Sufficient for this course, lower cost
- Teensy 4.1: More I/O pins, Ethernet PHY, SD card slot (useful for extensions)
- Both use same firmware; choice depends on budget and future plans

**MCP2515 Module Variants**:
- Ensure module includes TJA1050 or similar transceiver
- Some modules have voltage level converters (3.3V/5V)
- Verify 8MHz or 16MHz crystal oscillator (affects bitrate configuration)
- Recommended: "MCP2515 CAN Bus Module TJA1050 Receiver SPI" on Amazon (~$5 for 2)

**Breadboard Quality**:
- Higher-quality breadboards have better contact reliability
- Avoid ultra-cheap options that cause intermittent connections
- Consider "proto boards" for more permanent assemblies

**Cable Specifications**:
- CAN requires twisted pair (reduces EMI)
- Standard: CAT5/CAT6 cable works well (use one pair)
- Industrial: DeviceNet or CAN-specific cable (more expensive)
- Length: 1-2 meters sufficient for lab benches

#### Procurement Timeline

**6 weeks before semester start**:
- Place bulk order for Teensy boards (PJRC.com)
- Order MCP2515 modules, breadboards, wire kits (Amazon)
- Order cable and resistors (DigiKey or local electronics supplier)

**4 weeks before**:
- Receive and inventory all components
- Assemble 2-3 spare kits (for failures/loaners)
- Test one complete kit end-to-end

**2 weeks before**:
- Prepare kit bags/boxes for each student
- Label kits with inventory checklist
- Flash firmware on USB sticks for distribution

**Week 1**:
- Distribute kits to students
- Collect checkout forms (students responsible for return)

#### Recommended Vendors

**Primary sources**:
- **PJRC.com**: Teensy boards (official source, reliable)
- **Amazon**: MCP2515 modules, breadboards, cables, wire kits
- **DigiKey / Mouser**: Resistors, connectors, professional-grade components
- **AliExpress**: Budget alternative for MCP2515 (slower shipping, 3-4 weeks)

**Bulk pricing**:
- PJRC offers educational discounts for orders of 20+ Teensy boards
- Contact: sales@pjrc.com with institution details

**Spare parts inventory**:
- Keep 10-15% extra components for failures
- Most common failures: USB cables, breadboard contacts, MCP2515 modules

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
| **Oscilloscope** | Debugging SPI, viewing CAN signals | 1-2 | $400 | Entry-level DSO (Rigol DS1054Z) |
| **Logic Analyzer** | Capture digital signals | 2-4 | $50-200 | USB logic analyzer or Saleae clone |
| **Multimeter** | Voltage, continuity testing | 4-6 | $20 | Basic digital multimeter sufficient |
| **Soldering Station** | Attaching headers to Teensy | 2-4 | $40 | Temperature-controlled preferred |
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

#### 1. Arduino Development Environment

**Arduino IDE**:
- Version: 1.8.19 or 2.x
- Download: https://www.arduino.cc/en/software
- Platforms: Windows, macOS, Linux

**Teensyduino Add-on**:
- Version: Must match Arduino IDE version
- Download: https://www.pjrc.com/teensy/td_download.html
- Adds Teensy board support to Arduino IDE

**Installation instructions**:
```bash
# Linux (apt-based)
sudo apt-get update
sudo apt-get install arduino

# Download Teensyduino installer
wget https://www.pjrc.com/teensy/td_159/TeensyduinoInstall.linux64
chmod +x TeensyduinoInstall.linux64
./TeensyduinoInstall.linux64

# Windows/macOS: Use graphical installers
```

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
         (Teensy+MCP2515)    (Teensy+MCP2515)
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

**Cost per student**: $42 (hardware kit)
**Fixed costs**: $625 (infrastructure) + $1200 (shared equipment) = $1825

| Class Size | Student Kits | Infrastructure | Shared Equip | Total | Per Student |
|------------|--------------|----------------|--------------|-------|-------------|
| 10 students | $420 | $625 | $1200 | $2,245 | $224.50 |
| 15 students | $630 | $625 | $1200 | $2,455 | $163.67 |
| 20 students | $840 | $625 | $1200 | $2,665 | $133.25 |
| 24 students | $1,008 | $625 | $1200 | $2,833 | $118.04 |

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
- Bulk purchasing (20+ Teensy boards = educational discount)
- AliExpress for MCP2515 modules (slower shipping, lower cost)
- Pair students instead of individual kits (halves hardware cost)
- Reuse kits from previous semesters (replace damaged components only)

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
- Teensy boards: 5+ years (very reliable)
- MCP2515 modules: 2-3 years (most common failure)
- Breadboards: 2-3 years (contacts wear out)
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

#### Amazon
- **Products**: MCP2515 modules, breadboards, cables, wire kits
- **Advantages**: Fast shipping (Prime), easy returns
- **Disadvantages**: Variable quality, some counterfeit components
- **Recommendation**: Check reviews, prefer "Amazon's Choice" items

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
- **Products**: MCP2515 modules, cables, breadboards
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
- Pair students (12 students = 6 kits)
- Single Raspberry Pi instructor station
- No oscilloscope (use $10 USB logic analyzer only)
- Minimal soldering (use pre-soldered Teensy or solderless headers)
- Reuse kits semester-to-semester

**Cost breakdown**:
- 6 student kits @ $42 = $252
- 1 Raspberry Pi setup = $100
- Logic analyzers and shared tools = $200
- Cables and infrastructure = $100
- **Total**: ~$650

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

### Raspberry Pi as Student Device (Teensy Alternative)

**Option**: Use Raspberry Pi Zero W + CAN hat instead of Teensy

**Pros**:
- Linux environment directly on device
- WiFi for remote access
- More familiar for students

**Cons**:
- Higher cost (~$30 for Pi Zero + $25 for CAN hat = $55 vs $42 for Teensy)
- Larger form factor
- Requires microSD card management
- Power consumption higher

**Verdict**: Teensy is more cost-effective and pedagogically better (teaches embedded programming)

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

**Vendor: Amazon**
| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| MCP2515 CAN Module (2-pack) | 11 | $9.00 | $99.00 |
| Breadboard 400-point (5-pack) | 5 | $12.00 | $60.00 |
| Jumper wire kit | 20 | $5.00 | $100.00 |
| USB Micro-B cable (5-pack) | 5 | $10.00 | $50.00 |
| **Amazon Total** | | | **$309.00** |

**Vendor: DigiKey**
| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| 120Ω resistors (1/4W, 100-pack) | 1 | $8.50 | $8.50 |
| CAN cable (twisted pair, 50m) | 1 | $35.00 | $35.00 |
| Screw terminals | 10 | $2.50 | $25.00 |
| Shipping | | | $8.00 |
| **DigiKey Total** | | | **$76.50** |

**Vendor: Adafruit (Instructor Station)**
| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| Raspberry Pi 4 (4GB) | 2 | $55.00 | $110.00 |
| Waveshare CAN Hat | 2 | $25.00 | $50.00 |
| MicroSD 32GB | 2 | $8.00 | $16.00 |
| USB-C Power Supply | 2 | $8.00 | $16.00 |
| Shipping | | | $10.00 |
| **Adafruit Total** | | | **$202.00** |

**Grand Total**: $1,126.10

*(Add shared equipment and infrastructure as needed per budget)*

---

**Document Version**: 1.0
**Last Updated**: 2026-01-06
**Author**: Constantine Macris
**License**: CC BY-SA 4.0

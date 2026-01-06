---
title: "Class 00"
subtitle: "Introduction to Maritime Cybersecurity"
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
    Course introduction and maritime cybersecurity landscape
---

# Class 00 -- Introduction to Maritime Cybersecurity

## Learning Outcomes

- Understand course structure and expectations
- Explain the maritime cybersecurity threat landscape
- Identify key differences between IT and OT security
- Describe regulatory frameworks (IMO, IEC 61162, classification societies)

## Definitions

- **OT** -- Operational Technology: Hardware and software for monitoring/controlling physical devices
- **IT** -- Information Technology: Computing systems for data processing
- **CAN** -- Controller Area Network: Serial communication protocol
- **NMEA 2000** -- National Marine Electronics Association standard for vessel networks
- **PGN** -- Parameter Group Number: Message identifier in NMEA 2000
- **IDS** -- Intrusion Detection System

## Why Maritime Cybersecurity?

- Over 90% of global trade travels by sea
- Modern vessels are floating networks of connected systems
- Attacks can result in loss of life, environmental disasters, economic damage
- Legacy systems + modern connectivity = expanded attack surface

![Maritime Trade Routes](../../images/maritime_trade.png)

<!--
Instructor Notes:

Welcome the class and set expectations. This is a hands-on course - we will be building hardware, writing code, and attacking/defending simulated vessel networks.

Key points to emphasize:
- All attacks are on ISOLATED test networks only
- Students will sign ethics agreement before attack labs
- The goal is to understand threats to better defend against them

Show recent maritime cyber incidents:
- 2017 Maersk NotPetya ($300M+ damage)
- 2018 COSCO ransomware attack
- 2020 IMO website attack
- GPS spoofing incidents in Black Sea, Persian Gulf

Ask students: "What systems on a vessel might be networked together?"
Expected answers: GPS, radar, autopilot, engine controls, ballast, cargo systems
-->

## Course Overview

| Unit | Weeks | Focus |
|------|-------|-------|
| 1: Foundations | 1-4 | Protocols, hardware, fundamentals |
| 2: Attack Techniques | 5-8 | Reconnaissance, spoofing, DoS |
| 3: Detection | 9-12 | Frequency, entropy, ML, fingerprinting |
| 4: Defense | 13-14 | Ensemble IDS, architecture, capstone |

## What Makes Maritime OT Different?

| Aspect | IT Security | Maritime OT Security |
|--------|-------------|---------------------|
| Availability | Important | **Critical** (safety of life) |
| Latency | Flexible | Real-time required |
| Patching | Regular updates | Difficult at sea |
| Lifespan | 3-5 years | 20+ years |
| Environment | Data center | Salt, vibration, temperature |
| Connectivity | Always-on | Intermittent (satellite) |

<!--
Instructor Notes:

Emphasize that OT security priorities are often the inverse of IT:
- IT: Confidentiality > Integrity > Availability
- OT: Availability > Integrity > Confidentiality

A vessel losing GPS is very different from a laptop losing internet.

Discuss the challenge of patching systems while at sea for months.
-->

## Real-World Maritime Incidents

### NotPetya and Maersk (2017)

- Ransomware spread through Ukrainian tax software
- Maersk: 45,000 PCs, 4,000 servers destroyed
- 10 days to rebuild entire IT infrastructure
- Cost: $250-300 million
- Lesson: IT/OT convergence creates pathways

### GPS Spoofing in the Black Sea (2017)

- Ships reported GPS positions 25+ miles inland
- Over 20 vessels affected simultaneously
- Suspected state-sponsored attack
- Lesson: Navigation systems are vulnerable

<!--
Instructor Notes:

For Maersk case:
- Show timeline of attack
- Discuss how they recovered (one domain controller survived in Ghana due to power outage)
- Emphasize interconnection between IT and OT

For GPS spoofing:
- This is exactly what we'll learn to do in Week 6
- Discuss implications for autonomous vessels
- Mention AIS spoofing as related threat

Good video: YouTube search "DEF CON GPS spoofing ships"
-->

## The Jeep Cherokee Hack (2015)

A watershed moment for vehicle cybersecurity:

1. **Initial Access**: Exploited cellular connection to infotainment system
2. **Lateral Movement**: Compromised SPI connection to CAN controller
3. **Impact**: Full control of steering, brakes, engine

**Maritime Parallel**: Modern vessels have similar architectures
- Satellite/cellular connections
- IT systems bridged to OT networks
- CAN-based control systems

<!--
Instructor Notes:

This case is from the literature review Section 3.

Key points:
- Attackers only needed to know the vehicle's IP address
- Sprint blocked port 6667 after disclosure
- 1.4 million vehicles recalled

Show Miller/Valasek DEF CON presentation if time permits (YouTube)

Ask: "What's the maritime equivalent of each attack step?"
- Cellular = Satellite VSAT connection
- Infotainment = Bridge systems, crew WiFi
- CAN bus = NMEA 2000 network
-->

## Regulatory Landscape

### International Maritime Organization (IMO)

- **MSC-FAL.1/Circ.3**: Guidelines on maritime cyber risk management
- **MSC.428(98)**: Cyber risk in Safety Management Systems
- Required in Safety Management Systems since Jan 2021

### IEC 61162 Standard Family

- **IEC 61162-1**: NMEA 0183 (serial)
- **IEC 61162-3**: NMEA 2000 (CAN-based)
- **IEC 61162-450**: Ethernet interconnection
- **IEC 61162-460**: Safety and security requirements

### Classification Societies

- DNV: Cyber Security Rules, Cyber Resilience notation
- ABS: Cyber Safety Framework
- Lloyd's Register: Cyber-enabled ships guidance
- ClassNK: Guidelines for Cyber Security Onboard Ships

<!--
Instructor Notes:

These are from literature review Section 7.

Key points:
- IMO requirements now mandatory in ISM Code
- Flag states enforce through Port State Control
- Classification societies offer voluntary notations

Quiz question idea: "Which standard covers NMEA 2000?" (IEC 61162-3)

Provide links to freely available guidance documents for student reading.
-->

## Defense in Depth for Maritime

![Defense in Depth](../../images/defense_in_depth.png)

**Layers** (from outside in):
1. Perimeter: Satellite/shore connections
2. Network: Segmentation, firewalls
3. System: Hardening, patching
4. Application: Secure protocols
5. Data: Encryption, integrity
6. **Detection**: Anomaly detection (our focus!)

<!--
Instructor Notes:

Draw this on the board as you discuss each layer.

Emphasize that we're focused on the Detection layer in this course.

Why detection?
- Prevention fails eventually
- Need to know when attacks occur
- Enable response and recovery
-->

## OpenBridge: Our Platform

Low-cost NMEA 2000 simulation and testing platform:

- **Hardware**: Teensy 4.x + MCP2515 (~$43)
- **Software**: Open-source Arduino libraries
- **Capability**: Send/receive 49 PGN types
- **Purpose**: Education, research, testing

![OpenBridge Hardware](../../images/openbridge_hardware.jpg)

**We will build this in Week 4!**

<!--
Instructor Notes:

Show the hardware components:
- Teensy microcontroller
- MCP2515 CAN controller
- TJA1050 transceiver

Emphasize:
- Much cheaper than commercial NMEA 2000 tools ($1000+)
- Same capability for our educational purposes
- Open source = we can modify and extend

Have a completed unit to pass around if available.
-->

## Course Tools

| Tool | Purpose |
|------|---------|
| OpenBridge | NMEA 2000 simulation |
| OpenPlotter | Real vessel data capture |
| can-utils | CAN bus analysis (candump, cansend) |
| Wireshark | Protocol analysis |
| Python | Analysis and ML |
| vessel_lstm | Anomaly detection |

## Homework (Non-Graded)

1. **Read**: Syllabus (come with questions)
2. **Read**: IMO MSC-FAL.1/Circ.3 Guidelines (skim for overview)
3. **Watch**: [Suggested] DEF CON - GPS spoofing ships
4. **Setup**: GitHub account (if you don't have one)
5. **Setup**: Python environment with numpy, pandas, matplotlib
6. **Research**: Find one recent maritime cyber incident and prepare 2-minute summary

## References

- [IMO Cyber Security Guidelines]
- [NotPetya Maersk Case Study]
- [IEC 61162 Overview]
- [OpenBridge GitHub]

[IMO Cyber Security Guidelines]:https://www.imo.org/en/OurWork/Security/Pages/Cyber-security.aspx
[NotPetya Maersk Case Study]:https://www.wired.com/story/notpetya-cyberattack-ukraine-russia-code-crashed-the-world/
[IEC 61162 Overview]:https://www.nmea.org/nmea-2000.html
[OpenBridge GitHub]:https://github.com/[org]/openbridge

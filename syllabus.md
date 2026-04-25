---
title: "Syllabus"
subtitle: "Maritime OT Security"
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
    OpenBridge: Maritime Operational Technology Security
---

# Syllabus

## Welcome

Welcome to Maritime OT Security! This course provides hands-on experience securing operational technology systems in the maritime domain. We'll explore the unique challenges of protecting vessel control networks using the open-source OpenBridge platform.

## Instructor

Constantine Macris is a PhD candidate at the University of Rhode Island researching maritime cybersecurity and anomaly detection. He holds a Master's in Business Administration from UConn and a Bachelor's from the US Merchant Marine Academy. Constantine is a USCG licensed Chief Engineer and Certified Information Systems Security Professional (CISSP).

<!--
Instructor Notes:
- Modify bio as needed for your institution
- Include office hours and contact information
- Add TA information if applicable
-->

## Course Description

This course introduces students to the fundamentals of maritime operational technology (OT) security. Building on networking fundamentals, students explore CAN bus and NMEA 2000 protocols, analyze vessel network traffic, implement attack scenarios in a controlled environment, and develop anomaly detection systems. The course emphasizes hands-on learning using low-cost hardware (~$50) and open-source software.

## Prerequisites

- Networking fundamentals (TCP/IP, OSI model)
- Basic programming (Python preferred)
- Linux command line familiarity
- No prior maritime or CAN bus experience required

## Learning Objectives

Upon completion, students will be able to:

1. Explain CAN bus protocol vulnerabilities and their implications for maritime safety
2. Decode and construct NMEA 2000 Parameter Group Number (PGN) messages
3. Build and program a Teensy-based CAN interface for under $50
4. Perform reconnaissance on maritime CAN networks
5. Execute and detect spoofing, replay, and denial-of-service attacks
6. Implement frequency-based and entropy-based anomaly detection
7. Apply machine learning techniques (SVM, LSTM) to intrusion detection
8. Analyze clock skew for device fingerprinting
9. Evaluate IDS performance using standard metrics (TPR, FPR, F1, AUC)
10. Design defense-in-depth architectures for vessel networks

## NICE Framework Alignment

| NICE Work Role | Knowledge/Skills |
|----------------|------------------|
| Cyber Defense Analyst (PR-CDA-001) | K0046, K0058, K0324 - Network traffic analysis |
| Security Architect (SP-ARC-001) | K0179, K0211 - Security architecture design |
| Vulnerability Assessment Analyst (PR-VAM-001) | K0013, K0068 - Vulnerability analysis |
| Cyber Defense Incident Responder (PR-CIR-001) | K0042, K0157 - Incident response |

## Required Materials

### Hardware (per student or pair)

The course uses **NEMO**, an open-source dual-bus NMEA 2000 board built around the Teensy 4.0's two native FlexCAN controllers. Two procurement paths are supported:

**Path A — DIY (recommended for the educational experience):** order the PCB from JLCPCB (or equivalent) using the KiCad files in the [NEMO repository](https://github.com/Soups71/NEMO/tree/main/PCB) and assemble per Lab 04.

**Path B — Pre-built board:** for time-constrained programs, email `nemo@jamescampbell.org` with subject "Board Request" to coordinate a shipped, pre-assembled NEMO.

| Item | Approximate Cost | Qty | Source |
|------|------------------|-----|--------|
| Teensy 4.0 | $23 | 1 | PJRC.com / SparkFun DEV-15583 |
| TJA1050 CAN Transceiver | $1.50 | 2 | Amazon |
| SH1106 128×64 OLED (I2C) | $5 | 1 | Amazon |
| 10kΩ Potentiometer (panel-mount) | $0.50 | 3 | Amazon |
| Tactile Push Button | $0.20 | 4 | Amazon |
| NMEA 2000 M12 Connector | $8–$15 | 1 | RS Components / DigiKey |
| 3-Pin Screw Terminal Block | $0.50 | 1 | Amazon |
| Custom NEMO PCB (JLCPCB) | $2–$5 | 1 | JLCPCB.com |
| **Total** | **~$42–$55** | | |

<!--
Instructor Notes:
- Order PCBs from JLCPCB 4-6 weeks before course starts (fabrication + shipping ~2-3 weeks)
- Consider a single bulk PCB run for the whole class to lower per-board cost
- Have 2-3 spare kits for failures/loaners
- For programs without soldering capacity, request pre-built boards via nemo@jamescampbell.org
- Pre-solder Teensy headers and surface-mount parts before student lab if soldering time is limited
-->

### Software (all open-source)

- Arduino IDE with Teensyduino add-on
- Python 3.x with: numpy, pandas, scikit-learn, pytorch, matplotlib
- can-utils package (Linux)
- Wireshark with CAN dissector
- OpenBridge firmware (provided)

### Lab Infrastructure

- Isolated NMEA 2000 test network (NOT connected to live vessel)
- OpenPlotter Raspberry Pi with CAN interface (instructor-managed)
- Logic analyzer (shared, 1 per 4 students recommended)

## Texts and References

### Primary Readings

- Course literature review: "Anomaly Detection in CAN Bus Networks" (provided)
- Hoppe et al. (2008): "Security threats to automotive CAN networks"
- Cho & Shin (2016): "Fingerprinting ECUs for Vehicle Intrusion Detection"

### Supplementary References

- IMO MSC-FAL.1/Circ.3: Guidelines on Maritime Cyber Risk Management
- IEC 61162-3: NMEA 2000 Standard
- NIST SP 800-82: Guide to ICS Security

## Course Schedule

| Week | Topic | Lab |
|------|-------|-----|
| 1 | Introduction to Maritime Cybersecurity | Network Reconnaissance |
| 2 | CAN Bus Protocol Deep Dive | CAN Frame Decoding |
| 3 | NMEA 2000 and PGN Structure | PGN Parser Development |
| 4 | OpenBridge Hardware Build | Hardware Assembly |
| 5 | Reconnaissance Techniques | Network Profiling |
| 6 | Navigation Spoofing Attacks | GPS/Heading Spoofing |
| 7 | Engine System Attacks | Engine Data Spoofing |
| 8 | DoS and Replay Attacks | **MIDTERM** |
| 9 | Frequency-Based Detection | Frequency IDS |
| 10 | Entropy-Based Detection | Entropy IDS |
| 11 | Machine Learning Approaches | ML-Based Detection |
| 12 | Clock Skew Fingerprinting | Device Fingerprinting |
| 13 | Ensemble Detection and XAI | Integrated IDS |
| 14 | Defense Architecture | **Capstone Exercise** |

## Assessment

| Component | Weight | Description |
|-----------|--------|-------------|
| Lab Reports | 40% | Weekly hands-on deliverables |
| Midterm Exam | 15% | Practical skills assessment (Week 8) |
| Final Exam | 20% | Written + practical components |
| Capstone Exercise | 15% | Red Team vs Blue Team |
| Participation | 10% | Class discussion, peer review |

### Labs

Labs are due before the following lab session. Late submissions receive 10% penalty per day. Lab reports should include:

- Objective summary
- Methodology and commands used
- Screenshots/captures as evidence
- Analysis and conclusions
- Answers to lab questions

### Exams

- **Midterm (Week 8)**: Practical skills - decode traffic, identify attacks, propose mitigations
- **Final**: Written theory questions + practical component

### Capstone (Week 14)

Red Team vs Blue Team exercise on simulated vessel network. Teams rotate roles for comprehensive experience.

## Policies

### Academic Integrity

All work submitted must be your own. Collaboration is encouraged for labs but each student must submit their own report with their own analysis. Quizzes and exams are individual work.

### Safety and Ethics

All attack activities are conducted on isolated test networks ONLY. Students sign an ethics agreement before attack labs. Unauthorized attacks on any system are strictly prohibited and may result in course failure and disciplinary action.

### Attendance

Class attendance is expected. Labs require presence for equipment access. If you must miss class, notify the instructor in advance and arrange to complete lab work.

## Resources

- Course GitHub Repository: [Link to be provided]
- OpenBridge Project: github.com/[org]/openbridge
- NMEA 2000 PGN Reference: [Link to be provided]
- Discussion: [Platform TBD - Slack/Discord/Teams]

## Equality and Inclusion

This course is committed to providing an inclusive learning environment. All students are valued regardless of background. If you need accommodations, please contact the instructor.

<!--
Instructor Notes:
- Update all links before semester
- Create isolated test network topology diagram
- Prepare ethics agreement document
- Set up communication platform
- Brief IT/security on isolated lab network
-->

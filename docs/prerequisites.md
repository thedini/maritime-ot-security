---
title: "Student Prerequisites"
subtitle: "Maritime OT Security Course"
author: "Constantine Macris"
date: "2026"
---

# Student Prerequisites: Maritime OT Security

## Table of Contents

1. [Overview](#overview)
2. [Required Knowledge](#required-knowledge)
3. [Recommended Courses](#recommended-courses)
4. [Self-Assessment Checklist](#self-assessment-checklist)
5. [Preparatory Resources](#preparatory-resources)
6. [Special Considerations](#special-considerations)

---

## Overview

This document outlines the knowledge, skills, and background expected of students entering the Maritime OT Security course. The course builds on foundational computer science and networking concepts, applying them to operational technology security in the maritime domain.

**Target student level**: Upper-division undergraduate (junior/senior) or graduate students

**Prerequisites are enforced**: Students lacking required background will struggle with lab exercises and may not succeed in the course. Self-assessment is critical before enrolling.

**No prior maritime or CAN bus experience required**: We teach domain-specific knowledge from scratch. However, you must have the computing fundamentals described below.

---

## Required Knowledge

### 1. Networking Fundamentals (CRITICAL)

You must be comfortable with:

**Network Protocols**:
- OSI model layers (physical, data link, network, transport, application)
- TCP/IP stack and addressing
- Difference between connection-oriented (TCP) and connectionless (UDP) protocols
- Basic understanding of how protocols encapsulate data

**Network Analysis**:
- Reading packet captures with Wireshark or tcpdump
- Understanding protocol headers (IP, TCP, UDP)
- Following network conversations
- Filtering traffic by protocol, port, or address

**Binary and Hexadecimal**:
- Converting between binary, hexadecimal, and decimal
- Reading hex dumps
- Understanding bit-level data representation
- Bitwise operations (AND, OR, XOR, shifts)

**Subnetting and Addressing** (less critical, but helpful):
- IP addressing and subnet masks
- Broadcast vs unicast
- Network/host portions of addresses

**Where this is used in the course**:
- Week 1-2: Analyzing CAN bus traffic (similar to network packet analysis)
- Week 2-3: Decoding binary CAN frames and NMEA 2000 messages
- Week 5-8: Reconnaissance and attack labs require packet capture and injection
- Week 9-13: Detection systems analyze network-level patterns

**If you lack this**: Take an introductory networking course first (e.g., "Computer Networks", "Data Communications"). Read *Computer Networking: A Top-Down Approach* by Kurose & Ross.

---

### 2. Programming (CRITICAL)

You must be proficient in at least one programming language, with Python strongly preferred.

**Python Skills Required**:
- Variables, data types (int, float, str, list, dict)
- Control flow (if/else, for, while)
- Functions and parameters
- File I/O (reading/writing files)
- String manipulation and parsing
- Using external libraries (import statements)
- Basic debugging (print statements, error messages)

**Python Libraries Used** (we teach these, but basic familiarity helps):
- NumPy (arrays, numerical operations)
- Pandas (data frames, CSV processing)
- Matplotlib/Seaborn (plotting)
- scikit-learn (machine learning)
- PyTorch (deep learning for LSTM labs)

**C/C++ (helpful but not required)**:
- Basic syntax (for Arduino/Teensy firmware)
- We provide firmware templates; you modify, not write from scratch
- Understanding of pointers, structs helps but isn't mandatory

**Where this is used in the course**:
- Week 2-3: Writing Python scripts to decode CAN frames and parse PGNs
- Week 4: Modifying Arduino/C++ firmware for Teensy (templates provided)
- Week 6-8: Attack scripts in Python to inject messages
- Week 9-13: Detection algorithms implemented in Python (frequency, entropy, ML)

**If you lack this**: Complete an introductory programming course (e.g., CS101, "Introduction to Python"). Work through *Automate the Boring Stuff with Python* by Al Sweigart (free online).

---

### 3. Linux Command Line (CRITICAL)

You must be comfortable working in a Linux terminal.

**Required Skills**:
- Navigating directories (`cd`, `ls`, `pwd`)
- File operations (`cp`, `mv`, `rm`, `mkdir`)
- Viewing files (`cat`, `less`, `head`, `tail`)
- Editing files (`nano`, `vim`, or other editor)
- File permissions (`chmod`, `chown`, understanding rwx)
- Running programs (`./script.py`, `python3 script.py`)
- Installing software (`apt-get install`, `pip install`)
- Managing processes (`ps`, `kill`, background jobs with `&`)
- Using pipes and redirection (`|`, `>`, `>>`)
- Environment variables (`export`, `$PATH`)

**Where this is used in the course**:
- Week 1+: All lab work uses Linux command-line tools
- Week 1-2: CAN utilities (`candump`, `cansend`, `canplayer`)
- Week 4+: Configuring CAN interfaces (`ip link set can0 up`)
- Week 5-8: Running attack scripts from terminal
- Week 9-13: Processing data files, running ML training scripts

**If you lack this**: Complete a Linux/Unix tutorial (e.g., "Linux Journey" website, "The Linux Command Line" by William Shotts). Use Linux as your daily driver OS for a month before course starts.

---

### 4. Basic Mathematics and Statistics (IMPORTANT)

You should understand:

**Algebra and Functions**:
- Linear functions (y = mx + b)
- Exponents and logarithms
- Reading graphs and plots

**Statistics** (for detection modules):
- Mean, median, standard deviation
- Normal distribution (bell curve)
- Confidence intervals and z-scores
- Type I vs Type II errors (false positive vs false negative)

**Linear Algebra** (for ML modules):
- Vectors and matrices (basic understanding)
- Matrix multiplication (conceptual, not by hand)

**Calculus** (helpful but not required):
- Derivatives and gradients (for understanding ML optimization)
- Not required to calculate by hand—library functions handle it

**Where this is used in the course**:
- Week 9: Frequency-based detection uses statistical thresholds (mean ± k*std)
- Week 10: Entropy calculation uses logarithms
- Week 11: ML algorithms use linear algebra and calculus (libraries handle computation)
- Week 12: Fingerprinting uses linear regression (least squares)

**If you lack this**: Review introductory statistics (Khan Academy, "Statistics for Data Science" courses). For ML labs, conceptual understanding suffices—deep math not required.

---

### 5. Computer Systems Concepts (HELPFUL)

Understanding of how computers work:

**Hardware**:
- CPU, memory, storage basics
- Input/output devices
- Serial communication concepts (UART, SPI, USB)

**Operating Systems**:
- Processes and threads
- File systems
- Device drivers (conceptual)

**Embedded Systems** (we teach this, but exposure helps):
- Microcontrollers vs microprocessors
- Real-time constraints
- Hardware interfaces

**Where this is used in the course**:
- Week 4: Building the NEMO board (Teensy 4.0 + dual TJA1050 transceivers, custom PCB)
- Week 4: Understanding the Teensy's native FlexCAN controllers and why NEMO uses two of them simultaneously
- Throughout: Appreciating real-time constraints of OT systems

**If you lack this**: Optional, but reading about Arduino/Raspberry Pi projects provides useful context. *Make: Electronics* by Charles Platt is an excellent intro.

---

## Recommended Courses

### Must-Have (Absolutely Required)

1. **Computer Networks** (or equivalent)
   - Topics: OSI model, TCP/IP, packet analysis, network protocols
   - Typical course codes: CS 352, CSE 461, EECS 489, COE 379

2. **Introduction to Programming** (Python preferred)
   - Topics: Variables, control flow, functions, data structures, file I/O
   - Typical course codes: CS 101, CS 111, CSE 142, COMP 110

3. **Linux/Unix Systems** (or equivalent experience)
   - Can be self-taught if comfortable with command line
   - Some programs offer "Linux for Engineers" courses

### Strongly Recommended

4. **Introduction to Cybersecurity**
   - Topics: Confidentiality/integrity/availability, threat modeling, attack/defense basics
   - Provides context for why we study OT security
   - Typical course codes: CS 365, CSEC 201, EECE 412

5. **Data Structures and Algorithms**
   - Topics: Arrays, lists, dictionaries, searching, sorting
   - Helps with efficient data processing in labs
   - Typical course codes: CS 201, CS 210, CSE 373

6. **Probability and Statistics**
   - Topics: Distributions, hypothesis testing, regression
   - Essential for detection modules (Weeks 9-13)
   - Typical course codes: STAT 401, MATH 318, ECE 302

### Nice to Have (Not Required)

7. **Machine Learning**
   - We teach ML concepts as needed, but prior exposure helps
   - Typical course codes: CS 4774, CSE 446, EECS 445

8. **Computer Systems / Operating Systems**
   - Understanding of low-level hardware/software interaction
   - Typical course codes: CS 2505, CSE 351, EECS 370

9. **Embedded Systems**
   - Experience with Arduino, Raspberry Pi, or microcontrollers
   - Typical course codes: ECE 4564, CSE 466, EECS 373

---

## Self-Assessment Checklist

Use this checklist to gauge your readiness. Be honest—your success depends on it.

### Networking Skills

- [ ] I can explain the OSI model layers and give examples of protocols at each layer
- [ ] I can open a PCAP file in Wireshark and identify protocols being used
- [ ] I can apply display filters in Wireshark (e.g., `tcp.port == 80`)
- [ ] I understand how TCP performs a three-way handshake
- [ ] I can convert hexadecimal to binary (e.g., 0x3F = 0011 1111)
- [ ] I can read a hex dump and identify patterns
- [ ] I understand what a broadcast message is
- [ ] I can explain the difference between connection-oriented and connectionless protocols

**If you checked fewer than 6**: Review networking fundamentals before enrolling.

---

### Programming Skills

**Python**:
- [ ] I can write a Python script that reads a file line-by-line
- [ ] I can parse strings (e.g., extract fields using `split()` or regex)
- [ ] I can use lists and dictionaries to store data
- [ ] I can write functions with parameters and return values
- [ ] I can install Python libraries using pip
- [ ] I can import and use external libraries (e.g., `import numpy as np`)
- [ ] I can debug errors using print statements and reading error messages
- [ ] I have written at least 500 lines of Python code total (across projects)

**If you checked fewer than 6**: Take an introductory Python course first.

**C/C++ (optional but helpful)**:
- [ ] I can read C code and understand basic syntax (variables, functions, loops)
- [ ] I have compiled and run a C program
- [ ] I understand what pointers are (even if I don't use them confidently)

**Unchecked C/C++ items are okay**—we provide firmware templates.

---

### Linux Command Line Skills

- [ ] I can navigate directories without a graphical file manager
- [ ] I can create, copy, move, and delete files from the command line
- [ ] I can view file contents using `cat`, `less`, or `more`
- [ ] I can edit files using a terminal editor (`nano`, `vim`, `emacs`)
- [ ] I understand file permissions (`rwx` for owner, group, other)
- [ ] I can install software using `apt-get` or `yum`
- [ ] I can run Python scripts from the command line
- [ ] I can use pipes to connect commands (e.g., `ls -l | grep .txt`)
- [ ] I can redirect output to a file (e.g., `candump can0 > capture.log`)
- [ ] I have used Linux for at least 20 hours total (not just WSL one-offs)

**If you checked fewer than 7**: Spend a week using Linux full-time before course starts.

---

### Mathematics and Statistics

- [ ] I can calculate mean and standard deviation of a dataset
- [ ] I understand what a normal distribution is
- [ ] I can explain what a "95% confidence interval" means
- [ ] I know what a false positive and false negative are
- [ ] I can read and interpret scatter plots and line graphs
- [ ] I understand logarithms conceptually (even if I use a calculator)
- [ ] I have taken at least one statistics course

**If you checked fewer than 5**: Review introductory statistics (Khan Academy is sufficient).

---

### General Computing Concepts

- [ ] I can describe what a CPU, RAM, and storage are
- [ ] I understand what an operating system does
- [ ] I know what USB is and how devices connect to computers
- [ ] I have used a breadboard or worked with electronics (even simple circuits)
- [ ] I have heard of Arduino or Raspberry Pi (even if never used)
- [ ] I can troubleshoot basic computer problems (driver issues, software installation)

**If you checked fewer than 4**: Read introductory materials on computer architecture.

---

### Cybersecurity Awareness

- [ ] I understand the CIA triad (Confidentiality, Integrity, Availability)
- [ ] I can explain what an intrusion detection system (IDS) does
- [ ] I know what a vulnerability, threat, and exploit are
- [ ] I understand the difference between offensive (red team) and defensive (blue team) security
- [ ] I am familiar with basic attack types (DoS, spoofing, replay)

**If you checked fewer than 3**: Take an introductory cybersecurity course or read *Cybersecurity Essentials* materials first.

---

## Preparatory Resources

### If You're Missing Networking Background

**Free online courses**:
- **Coursera**: "Computer Networking" by University of Illinois
- **edX**: "Introduction to Computer Networking" by Stanford
- **YouTube**: NetworkChuck (practical tutorials), Professor Messer (CompTIA Network+)

**Books**:
- *Computer Networking: A Top-Down Approach* by Kurose & Ross (textbook, thorough)
- *The TCP/IP Guide* by Charles Kozierok (comprehensive, free online version)

**Hands-on practice**:
- **Wireshark tutorials**: https://www.wireshark.org/docs/wsug_html/
- Capture your own traffic (web browsing, streaming) and analyze it

**Time investment**: 40-60 hours to gain sufficient background

---

### If You're Missing Programming Background

**Python courses**:
- **Automate the Boring Stuff with Python** (free book): https://automatetheboringstuff.com
- **MIT OpenCourseWare**: "Introduction to Computer Science and Programming in Python"
- **Codecademy**: "Learn Python 3" (interactive)
- **Coursera**: "Python for Everybody" by University of Michigan

**Practice platforms**:
- **HackerRank**: Python basics challenges
- **LeetCode**: Easy problems for practice
- **Project Euler**: Math-focused programming problems

**Time investment**: 60-80 hours for basics, 100+ hours for fluency

---

### If You're Missing Linux Background

**Linux tutorials**:
- **Linux Journey**: https://linuxjourney.com (excellent beginner resource)
- **The Linux Command Line** by William Shotts (free PDF)
- **OverTheWire Bandit**: https://overthewire.org/wargames/bandit/ (gamified learning)

**Hands-on setup**:
- Install Ubuntu 22.04 in VirtualBox or dual-boot
- Use it for daily tasks (web, email, coding) for a week
- Force yourself to use terminal instead of GUI

**Time investment**: 20-30 hours

---

### If You're Missing Math/Statistics Background

**Statistics resources**:
- **Khan Academy**: Statistics and Probability (free, interactive)
- **Coursera**: "Statistics with Python" by University of Michigan
- **OpenStax**: *Introductory Statistics* (free textbook)

**Machine learning math**:
- **3Blue1Brown** (YouTube): "Essence of Linear Algebra" series
- **Khan Academy**: Linear Algebra

**Time investment**: 30-40 hours for statistics basics

---

### Crash Course Before Semester

If you're close but need a refresher, we recommend:

**2 weeks before course starts**:
- **Week 1**: Review networking and binary/hex conversions
  - Read OSI model, TCP/IP basics
  - Practice Wireshark on sample captures
  - Do binary/hex conversion exercises

- **Week 2**: Brush up on Python and Linux
  - Write 3-4 small Python scripts (file parsing, data analysis)
  - Set up Linux environment
  - Practice command-line tools daily

**Weekend before Week 1**:
- Review course syllabus
- Read Class 00 materials (introduction)
- Ensure Python environment set up (requirements.txt installed)
- Test that you can run a simple Python script and use `candump` (if possible)

---

## Special Considerations

### For Maritime/Marine Engineering Students

**Strengths**:
- You understand vessel systems, navigation, propulsion (huge advantage!)
- Domain knowledge makes attack/defense scenarios more meaningful
- Understanding of safety implications

**Likely gaps**:
- Programming (especially Python)
- Networking fundamentals
- Linux command line

**Recommendation**: Focus prep time on programming and Linux. Your domain expertise will carry you through the maritime-specific content.

---

### For Computer Science Students

**Strengths**:
- Programming, networking, and Linux skills (likely strong)
- Comfortable with algorithms and data structures
- Familiar with development workflows

**Likely gaps**:
- No maritime domain knowledge (that's okay—we teach it!)
- May not have hardware experience (soldering, electronics)
- Possibly weak on statistics (if ML track, likely okay)

**Recommendation**: You'll excel at coding labs. Embrace the hardware build (Week 4) as a learning experience. Read about vessel systems to provide context.

---

### For Cybersecurity Students

**Strengths**:
- Security mindset and threat modeling
- Understanding of attack/defense dynamics
- Familiarity with IDS concepts

**Likely gaps**:
- OT vs IT differences (critical to understand early)
- Embedded systems and real-time constraints
- May not have deep networking protocol knowledge

**Recommendation**: Focus on understanding OT priorities (availability > integrity > confidentiality). Recognize that OT security tools differ from IT penetration testing.

---

### For Students with Hardware/Electrical Engineering Background

**Strengths**:
- Comfortable with circuits, soldering, oscilloscopes
- Understand serial communication (SPI, UART, CAN physical layer)
- Hardware troubleshooting skills

**Likely gaps**:
- Programming (may be stronger in C than Python)
- Software development workflows
- Networking at higher layers (may be strong on physical layer, weak on protocols)

**Recommendation**: Your hardware skills will shine in Week 4. Focus Python prep on data analysis (Pandas, NumPy) for later labs.

---

### For Non-Traditional / Self-Taught Students

**Strengths**:
- Practical experience often exceeds classroom theory
- Strong problem-solving and resourcefulness
- Comfortable with self-directed learning

**Likely gaps**:
- Varies—use self-assessment checklist carefully
- May have knowledge gaps in specific areas (e.g., strong Python but no networking)

**Recommendation**: Be honest about gaps and address them proactively. Reach out to instructor with questions—we value diverse backgrounds!

---

## What About Maritime or CAN Bus Experience?

**Short answer**: Not required at all.

**What we assume**: Zero maritime knowledge. Zero CAN bus knowledge.

**What we teach**:
- Week 0-1: Maritime systems overview, threat landscape
- Week 1-2: CAN bus protocol from scratch
- Week 2-3: NMEA 2000 standard and PGN structure
- Throughout: Domain-specific context as needed

**Prior maritime experience is helpful but not necessary**. If you've never been on a boat, that's fine. If you've never heard of CAN bus, that's expected—most students haven't.

**What matters**: Computing fundamentals (networking, programming, Linux) so you can learn the domain-specific material efficiently.

---

## Recommended Preparation Timeline

### 3+ Months Before Course

If you're missing core prerequisites:
- Enroll in prerequisite courses (networking, programming)
- Work through online tutorials systematically
- Build foundational skills

### 1 Month Before Course

If you need a refresher:
- Review networking concepts (OSI, TCP/IP, Wireshark)
- Write Python scripts daily
- Use Linux as primary OS
- Read introductory materials on CAN bus (optional but helpful)

### 2 Weeks Before Course

Final preparation:
- Set up Python environment (install libraries from requirements.txt)
- Test Linux command-line tools (can-utils if possible)
- Review binary/hexadecimal conversions
- Read course syllabus and Class 00 materials

### 1 Week Before Course

- Ensure hardware ordered (if students purchase individually)
- Charge laptop, verify it meets specs
- Join course communication platform (Slack/Discord/Teams)
- Review self-assessment checklist one final time

---

## Still Not Sure If You're Ready?

**Contact the instructor**:
- Describe your background
- Share specific concerns
- Ask about preparatory materials

**Attend first class**:
- Week 1 material reviews fundamentals
- You'll get a sense of the pace
- Can drop/add within first week if necessary

**Work with a study group**:
- Form groups with complementary skills
- CS student + maritime student = powerful team
- Peer learning is highly effective

---

## Final Thoughts

**This course is challenging but accessible** to students with the right background. If you meet the prerequisites, you'll succeed with effort. If you're missing background, invest time in preparation—it will pay off.

**The course is hands-on and practical**. You'll build hardware, write real code, and see attacks succeed (and fail). This is not a lecture-heavy theory course.

**We're here to help**. Office hours, discussion forums, peer study groups—use all available resources. Struggling is part of learning, but you won't be alone.

**Good luck!** We look forward to teaching you maritime OT security.

---

## Appendix: Quick Reference

### Minimum Prerequisites Summary

| Area | Requirement | Verified By |
|------|-------------|-------------|
| **Networking** | Computer Networks course | Wireshark quiz in Week 1 |
| **Programming** | Python proficiency | Coding labs starting Week 2 |
| **Linux** | Command-line comfort | Lab work requires terminal |
| **Math/Stats** | Introductory statistics | Needed for Weeks 9+ |
| **Hardware** | Basic electronics (optional) | Helpful for Week 4 hardware build |

### Self-Prep Checklist (2 Weeks)

- [ ] Review OSI model and TCP/IP stack
- [ ] Practice Wireshark on sample captures (5+ hours)
- [ ] Write 5 Python scripts parsing files and processing data
- [ ] Convert 20 hex/binary numbers by hand for practice
- [ ] Use Linux terminal exclusively for 1 week
- [ ] Install Python libraries: `pip install -r requirements.txt`
- [ ] Test can-utils (if possible): `candump vcan0`
- [ ] Read course syllabus completely
- [ ] Join course communication platform

### Emergency Prep (1 Weekend)

If you only have a weekend:
1. **Day 1 Morning**: Review binary/hex conversions, practice 50 problems
2. **Day 1 Afternoon**: Wireshark tutorial, analyze 3 capture files
3. **Day 1 Evening**: Write Python script to parse CSV file
4. **Day 2 Morning**: Linux command-line practice (LinuxJourney.com)
5. **Day 2 Afternoon**: Install all software, test Python environment
6. **Day 2 Evening**: Read Class 00 and Class 01 materials

---

**Document Version**: 1.0
**Last Updated**: 2026-01-06
**Author**: Constantine Macris
**License**: CC BY-SA 4.0

---
title: "Instructor Guide"
subtitle: "Maritime OT Security"
author: "Constantine Macris"
date: "2026"
---

# Instructor Guide: Maritime OT Security

## Table of Contents

1. [Course Overview and Philosophy](#course-overview-and-philosophy)
2. [Pedagogical Approach](#pedagogical-approach)
3. [Suggested Pacing (14 Weeks)](#suggested-pacing-14-weeks)
4. [Technology Requirements](#technology-requirements)
5. [Lab Setup Instructions](#lab-setup-instructions)
6. [Module-by-Module Teaching Tips](#module-by-module-teaching-tips)
7. [Common Student Questions and Misconceptions](#common-student-questions-and-misconceptions)
8. [Safety and Ethics Guidance](#safety-and-ethics-guidance)
9. [Assessment Rubrics](#assessment-rubrics)
10. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## Course Overview and Philosophy

### Course Purpose

This course teaches maritime operational technology (OT) security through hands-on exploration of CAN bus and NMEA 2000 protocols. Unlike traditional cybersecurity courses focused on enterprise IT, this curriculum addresses the unique challenges of securing real-time, safety-critical systems with 20+ year lifespans operating in harsh environments.

### Educational Philosophy

**Learn by Doing**: Students build physical hardware, capture real network traffic, execute attacks in controlled environments, and implement detection systems. Theory reinforces practice, not vice versa.

**Attacker Mindset for Better Defense**: Understanding attack techniques isn't about creating hackers—it's about developing security professionals who can anticipate threats and design effective defenses.

**Ethics First**: Every attack lab begins with safety warnings and ethics discussions. Students sign agreements acknowledging the serious consequences of misusing this knowledge.

**Open Source and Accessible**: Using low-cost hardware (~$43) and open-source software ensures the course is reproducible at any institution without expensive proprietary equipment.

### Course Narrative Arc

The course follows a natural progression:

1. **Weeks 1-4: Foundation** - Build literacy in maritime systems, understand protocols, construct hardware
2. **Weeks 5-8: Offense** - Learn attack techniques, culminating in midterm assessment
3. **Weeks 9-12: Defense** - Develop detection systems using statistical and ML approaches
4. **Weeks 13-14: Integration** - Combine techniques in realistic red team/blue team scenarios

### Target Audience

- Computer science students with networking background
- Maritime/engineering students interested in cybersecurity
- Graduate students in cybersecurity programs
- Professional development for maritime industry personnel

**Prerequisites are critical** - see `prerequisites.md`. Students weak in Python or networking fundamentals will struggle.

---

## Pedagogical Approach

### Bloom's Taxonomy Mapping

The course intentionally scaffolds from lower to higher cognitive levels:

| Week | Module | Bloom's Level | Activities |
|------|--------|---------------|------------|
| 1 | Introduction | **Remember/Understand** | Define OT vs IT, identify threats |
| 2 | CAN Protocol | **Understand/Apply** | Decode frames, explain arbitration |
| 3 | NMEA 2000 | **Apply** | Parse PGN messages, construct data |
| 4 | Hardware Build | **Apply/Analyze** | Assemble circuits, debug connections |
| 5-7 | Attack Techniques | **Analyze/Evaluate** | Identify vulnerabilities, assess impact |
| 8 | Midterm | **Analyze** | Diagnose attacks from captures |
| 9-12 | Detection Methods | **Apply/Analyze/Create** | Implement algorithms, evaluate performance |
| 13-14 | Defense Architecture | **Evaluate/Create** | Design systems, justify decisions |

### Constructivist Learning

Students construct understanding through:
- **Physical manipulation**: Soldering, wiring, hardware debugging
- **Active experimentation**: Injecting messages, observing effects
- **Reflection**: Lab reports require analysis, not just procedure documentation
- **Peer collaboration**: Capstone teams learn from each other's approaches

### Flipped Classroom Elements

- **Pre-class reading**: Literature review sections assigned before lecture
- **Class time**: Discussion, demonstrations, hands-on activities (not pure lecture)
- **Lab time**: Application of concepts with instructor as facilitator
- **Post-lab reflection**: Written analysis connecting theory to observations

---

## Suggested Pacing (14 Weeks)

### Week-by-Week Schedule

#### **Week 1: Introduction to Maritime Cybersecurity**
- **Class**: Overview, threat landscape, IT vs OT differences
- **Lab 01**: Network reconnaissance with Wireshark and candump
- **Deliverables**: Lab report identifying baseline traffic patterns
- **Instructor prep**: Set up isolated test network, verify all equipment

#### **Week 2: CAN Bus Protocol Deep Dive**
- **Class**: CAN frame structure, arbitration, error handling
- **Lab 02**: CAN frame decoding and binary analysis
- **Deliverables**: Python decoder with header breakdown
- **Common issues**: Students confuse bit numbering (MSB vs LSB), arbitration priority

#### **Week 3: NMEA 2000 and PGN Structure**
- **Class**: J1939 addressing, PGN calculation, field encoding
- **Lab 03**: PGN parser development
- **Deliverables**: Parser for position, heading, engine data
- **Common issues**: Sign extension for negative values, unit conversions

#### **Week 4: OpenBridge Hardware Build**
- **Class**: Teensy architecture, MCP2515 configuration, SPI communication
- **Lab 04**: Hardware assembly and firmware flashing
- **Deliverables**: Working OpenBridge device with test traffic
- **Common issues**: Wiring errors, SPI bus conflicts, termination resistors
- **NOTE**: Order hardware 4-6 weeks in advance!

#### **Week 5: Reconnaissance Techniques**
- **Class**: Passive monitoring, device enumeration, timing analysis
- **Lab 05**: Network profiling and baseline establishment
- **Deliverables**: Comprehensive baseline report
- **Teaching tip**: Emphasize that reconnaissance is often the longest phase of real attacks

#### **Week 6: Navigation Spoofing Attacks**
- **Class**: GPS spoofing theory, position encoding, attack timing
- **Lab 06**: Position and heading spoofing
- **Deliverables**: Attack documentation with chart plotter screenshots
- **CRITICAL**: Ethics agreement must be signed before lab
- **Teaching tip**: Show real-world GPS spoofing incidents (Black Sea, Persian Gulf)

#### **Week 7: Engine System Attacks**
- **Class**: Engine control architecture, safety interlocks, alarm systems
- **Lab 07**: Engine parameter spoofing
- **Deliverables**: Multi-PGN attack scenario
- **Teaching tip**: Discuss cascading failures and why engine attacks are particularly dangerous

#### **Week 8: DoS, Replay Attacks, and Midterm**
- **Class**: Denial of service techniques, replay attack theory
- **Lab 08**: DoS and replay implementation
- **Midterm**: Practical skills assessment (2 hours)
- **Midterm format**:
  - Part 1: Decode unknown traffic capture
  - Part 2: Identify attack type and parameters
  - Part 3: Propose mitigation strategies

#### **Week 9: Frequency-Based Detection**
- **Class**: Statistical process control, baseline modeling, threshold selection
- **Lab 09**: Frequency IDS implementation
- **Deliverables**: Working frequency monitor with evaluation metrics
- **Teaching tip**: Connect to manufacturing quality control concepts (many students have internship experience)

#### **Week 10: Entropy-Based Detection**
- **Class**: Information theory, Shannon entropy, payload analysis
- **Lab 10**: Entropy IDS implementation
- **Deliverables**: Entropy calculator with ROC curve analysis
- **Common issues**: Window size selection, understanding entropy units (bits vs nats)

#### **Week 11: Machine Learning Approaches**
- **Class**: SVM, Random Forest, LSTM autoencoders, supervised vs unsupervised
- **Lab 11**: ML-based detection implementation
- **Deliverables**: Trained model with performance comparison
- **Teaching tip**: Emphasize that ML is not magic—garbage in, garbage out
- **Common issues**: Overfitting, insufficient training data, feature engineering mistakes

#### **Week 12: Clock Skew Fingerprinting**
- **Class**: Hardware timing variations, least squares fitting, device identification
- **Lab 12**: Fingerprinting implementation
- **Deliverables**: Device fingerprint database
- **Teaching tip**: This is often the most challenging technical concept—plan extra office hours

#### **Week 13: Ensemble Detection and XAI**
- **Class**: Combining detectors, voting systems, explainable AI, reducing false positives
- **Lab 13**: Integrated IDS with multiple detection methods
- **Deliverables**: Complete IDS with dashboard
- **Teaching tip**: Discuss real-world IDS deployment challenges (alert fatigue, tuning)

#### **Week 14: Defense Architecture and Capstone**
- **Class**: Defense-in-depth, network segmentation, incident response
- **Lab 14**: Red team vs blue team capstone exercise (3 hours)
- **Deliverables**: Team report and individual reflection
- **Capstone logistics**:
  - Pre-assign teams (mix skill levels)
  - Prepare scoring rubric
  - Have backup equipment ready
  - Video record sessions for later review

### Flexibility and Adaptation

**15-Week Semester**: Add a buffer week before midterm or final for review/catch-up

**10-Week Quarter**: Compress by combining related topics:
- Weeks 2-3 → One week on protocols
- Weeks 6-7 → One week on spoofing attacks
- Weeks 9-10 → One week on statistical detection
- Skip Class 08 lecture, do midterm during lab time

**Hybrid/Online Format**:
- Ship hardware kits to students
- Use remote access to lab equipment for attack/defense labs
- Synchronous sessions for team exercises
- Asynchronous lecture videos with discussion forums

---

## Technology Requirements

See detailed `technology_requirements.md`, but key instructor considerations:

### Hardware Ordering Timeline

- **6 weeks before course**: Order all components
- **4 weeks before**: Test hardware, flash firmware
- **2 weeks before**: Assemble loaner kits, verify network setup
- **Week 1**: Distribute hardware to students

### Lab Infrastructure

**Minimum setup** (budget-conscious institutions):
- 1 Raspberry Pi with CAN interface as traffic generator
- Student hardware connects to shared CAN bus
- USB logic analyzer for shared use

**Recommended setup**:
- 2-3 isolated CAN networks (allows simultaneous attack/defense labs)
- OpenPlotter installation per network with simulated vessel data
- Dedicated chart plotter displays for visual feedback
- Network switches for air-gapped security

**Advanced setup**:
- Physical helm simulator with autopilot integration
- Engine control simulator
- Multiple OpenPlotter nodes simulating different vessel systems

### Software Environment

**Option 1: Linux native** (recommended)
- Students use personal Linux laptops or VMs
- `can-utils` for traffic capture
- Python environment with requirements.txt

**Option 2: Virtual machine**
- Provide pre-configured VM image with all tools
- Students run on Windows/Mac via VirtualBox/VMware
- Requires USB passthrough for hardware

**Option 3: Docker containers**
- Containerized development environment
- Consistent across platforms
- Requires host kernel CAN support

---

## Lab Setup Instructions

### Initial Test Network Configuration

#### Equipment List (Instructor Station)
- Raspberry Pi 4 (4GB+ recommended)
- Waveshare 2-channel CAN hat or PiCAN
- 120Ω termination resistors (2)
- Power supply
- MicroSD card (32GB+)
- CAN cables (twisted pair recommended)

#### Software Installation

**1. Install OpenPlotter on Raspberry Pi**

```bash
# Download OpenPlotter image
wget https://cloud.openmarine.net/s/xxx/download

# Flash to SD card (adjust device path!)
sudo dd if=openplotter-xxx.img of=/dev/sdX bs=4M status=progress
```

**2. Configure CAN Interface**

```bash
# Enable CAN kernel modules
sudo modprobe can
sudo modprobe can_raw
sudo modprobe mcp251x

# Bring up CAN0 at 250kbps (NMEA 2000 standard)
sudo ip link set can0 type can bitrate 250000
sudo ip link set can0 up

# Make persistent
echo "auto can0" | sudo tee -a /etc/network/interfaces
echo "iface can0 inet manual" | sudo tee -a /etc/network/interfaces
echo "    pre-up /sbin/ip link set can0 type can bitrate 250000" | sudo tee -a /etc/network/interfaces
```

**3. Generate Simulated Traffic**

```bash
# Install NMEA 2000 simulator
git clone https://github.com/canboat/canboat
cd canboat
make

# Run analyzer with simulated data
./analyzer -json -file sample_data.log > /dev/null 2>&1 &
```

**4. Verify Traffic**

```bash
# Capture to verify
candump can0

# Should see messages like:
# can0  09F10D23   [8]  FF 7F FB FF FF 7F FF FF
# can0  09F11323   [8]  00 FC FF 7F 00 00 00 FF
```

### Student Workstation Setup

Each student (or pair) needs:

**1. Hardware connection**
```
[OpenBridge Device] ---> [Instructor CAN Bus]
       |
    [Laptop USB]
```

**2. Software tools**

```bash
# Ubuntu/Debian
sudo apt-get install can-utils python3-pip wireshark

# Python environment
pip3 install -r requirements.txt
# Contents: numpy pandas scikit-learn matplotlib seaborn torch
```

**3. Permissions**

```bash
# Add user to dialout group for USB access
sudo usermod -a -G dialout $USER

# Wireshark packet capture permissions
sudo dpkg-reconfigure wireshark-common
sudo usermod -a -G wireshark $USER
```

### Safety: Isolated Network

**CRITICAL**: The lab network must be physically isolated from:
- Any real vessel systems
- The internet
- Campus production networks

**Verification checklist**:
- [ ] No Ethernet cables to campus network
- [ ] WiFi disabled on all lab equipment
- [ ] Air-gapped switch dedicated to lab
- [ ] Instructor verifies isolation weekly
- [ ] Signs posted: "ISOLATED TEST NETWORK ONLY"

### Troubleshooting Lab Setup

**Problem**: Students can't see CAN traffic
- Check physical connections (common: termination missing)
- Verify bitrate (must be 250kbps)
- Check if interface is up: `ip link show can0`
- Listen on all interfaces: `candump any`

**Problem**: Teensy not recognized
- Windows: Install Teensy drivers from PJRC
- Linux: Check permissions (dialout group)
- Try different USB cable (data vs charge-only)

**Problem**: SPI communication fails**
- Verify wiring: MOSI, MISO, SCK, CS pins
- Check 3.3V vs 5V logic levels
- Measure with oscilloscope if available

---

## Module-by-Module Teaching Tips

### Class 00: Introduction

**Learning objectives**: Set expectations, motivate the topic, establish safety culture

**Engagement strategies**:
- **Opening question**: "What do you think is on a ship's network?" (whiteboard brainstorm)
- **Video clip**: NotPetya impact on Maersk (available on YouTube)
- **Interactive demo**: Show OpenPlotter chart display with live position data

**Key points to emphasize**:
1. OT security priority: Availability > Integrity > Confidentiality (opposite of IT)
2. Maritime incidents have real consequences (grounding, collision, environmental damage)
3. Isolation is critical—explain air-gapped lab network
4. This is a hands-on course, not lecture-based

**Common pitfall**: Students expect traditional cybersecurity (penetration testing, web hacking). Frame early that this is about embedded systems and industrial control.

**Time management**:
- 20 min: Intro and logistics
- 20 min: Maritime threat landscape
- 20 min: OT vs IT discussion
- 10 min: Course structure and expectations

---

### Class 01: CAN Protocol

**Learning objectives**: Understand CAN frame structure, arbitration, error handling

**Difficult concepts**:
1. **Bit arbitration**: Use the "shouting match" analogy—lowest ID speaks first
2. **Bit stuffing**: Explain as clock synchronization technique
3. **CRC calculation**: Skip the math, focus on error detection purpose

**Hands-on demo**:
- Project CAN bus oscilloscope trace on screen
- Show recessive (1) vs dominant (0) voltage levels
- Demonstrate arbitration with two Teensys sending different IDs

**Board work**:
Draw CAN frame bit-by-bit:
```
[ SOF | ID (11-bit) | RTR | IDE | r0 | DLC | Data (0-8 bytes) | CRC | ACK | EOF ]
```

Walk through example: `0x123` sending `[0x01, 0x02, 0x03]`

**Lab 01 prep**: Explain Wireshark CAN dissector, show sample capture

**Assessment check**: Before leaving class, ask students to decode a frame on paper

---

### Class 02: NMEA 2000

**Learning objectives**: Map NMEA 2000 to CAN, understand PGN structure, decode messages

**Most confusing topic**: PGN calculation from CAN header
- Spend 30+ minutes on this with multiple examples
- Provide flowchart handout
- Work through position message (PGN 129025) step-by-step

**Interactive activity**:
1. Give students 5 different CAN IDs
2. Have them calculate PGN in groups
3. Review on board, identify errors

**Practical examples**:
- Position (129025): GPS coordinates
- Speed (127251): Vessel speed over ground
- Engine RPM (127488): Tachometer reading

Show how these appear on a real chart plotter

**Common errors**:
- Forgetting reserved bits
- Source Address vs Group Extension confusion
- Little-endian byte order in data fields

**Lab 02 prep**: Show students the PGN library, explain how to look up field definitions

---

### Class 03: Hardware Build

**Learning objectives**: Understand Teensy platform, interface with MCP2515, debug hardware

**This is not a lecture class**: Make it a workshop
- Tables with hardware stations
- Instructor circulates helping with assembly
- TAs or advanced students can assist

**Safety first**:
- Soldering iron safety review
- ESD precautions
- Proper wire stripping technique

**Assembly stations**:
1. Soldering station (headers on Teensy and MCP2515)
2. Wiring station (breadboard connections)
3. Testing station (firmware upload and verification)

**Provide**:
- Wiring diagrams printed in color
- Multimeter for continuity testing
- Pre-flashed firmware on SD card (backup)

**Common issues**:
- Reversed polarity on power
- Crossed MOSI/MISO
- Insufficient 3.3V power supply
- Missing termination resistors when testing

**Success criteria**: Device connects, sends/receives message

---

### Class 04: Reconnaissance

**Learning objectives**: Passive monitoring, baseline establishment, device enumeration

**Emphasize patience**: Real-world reconnaissance takes days/weeks
- Show timeline of APT attack (months of recon)
- Discuss signal intelligence parallels

**Technical skills**:
- Filtering CAN traffic by ID
- Frequency analysis with timestamps
- Identifying patterns and correlations

**Lab connection**: Lab 05 baseline will be used for all subsequent attack labs

**Group discussion**: "What would you look for to profile a network?"
- Expected answers: Message types, frequencies, device addresses, timing patterns

---

### Class 05-07: Attack Techniques

**ETHICS EMPHASIS**: Start each class with safety reminder

**Standard attack class structure**:
1. Why this attack matters (real-world incident)
2. Technical prerequisites (what you need to know)
3. Attack mechanics (how it works)
4. Detection challenges (why it's hard to catch)
5. Evasion techniques (how to avoid detection)

**Class 05: Navigation Spoofing**
- Show GPS spoofing kit (if available)
- Discuss maritime GPS dependency
- Video: GPS spoofing demonstration

**Class 06: Engine Attacks**
- Explain engine control systems
- Discuss safety interlocks
- Consequence modeling

**Class 07: DoS and Replay**
- Distinguish DoS from jamming
- Replay attack timing considerations
- Message validation (or lack thereof)

**Teaching approach**: "Red team mindset"
- Think like an attacker to defend better
- Understand attacker goals and constraints
- Defense requires threat modeling

---

### Class 08: Midterm

**Format**: 2-hour practical exam

**Part 1: Traffic Analysis (40 points, 30 min)**
- Provide PCAP file with unknown traffic
- Students decode messages, identify PGNs, interpret data

**Part 2: Attack Identification (40 points, 45 min)**
- Provide capture with embedded attack
- Students identify attack type, parameters, affected systems

**Part 3: Mitigation (20 points, 30 min)**
- Short answer: Propose defenses for scenario

**Grading rubric**:
- Technical accuracy: 60%
- Explanation quality: 30%
- Completeness: 10%

**Preparation**:
- Review sessions week before
- Practice PCAP files available
- Office hours for questions

---

### Class 09: Frequency-Based Detection

**Learning objectives**: Statistical baseline, threshold selection, false positive management

**Key concepts**:
1. Baseline modeling (mean, std dev)
2. Threshold selection (sensitivity vs specificity)
3. Window size trade-offs

**Mathematical background**:
- Z-scores and standard deviations
- Confidence intervals
- Type I vs Type II errors

Most students have seen this in stats class—make connections

**Lab prep**: Discuss threshold selection
- Too sensitive → false positives → alert fatigue
- Too loose → miss attacks → false negatives
- No perfect threshold—depends on risk tolerance

**Demo**: Show frequency IDS catching message injection in real-time

---

### Class 10: Entropy-Based Detection

**Learning objectives**: Information theory basics, entropy calculation, payload analysis

**Challenging concept**: What is entropy?
- Use coin flip analogy (1 bit)
- Fair coin vs weighted coin (reduced entropy)
- Apply to CAN message payloads

**Mathematical notation**: Keep it simple
- H = -Σ p(x) log₂ p(x)
- Focus on interpretation, not derivation

**Practical application**:
- Normal messages have predictable patterns
- Attacks often have uniform/different distributions
- Example: Random replay vs structured spoofing

**Lab connection**: Entropy IDS catches what frequency misses

---

### Class 11: Machine Learning

**Learning objectives**: Supervised vs unsupervised learning, feature engineering, model evaluation

**Demystify ML**: It's pattern matching, not magic
- Models learn from examples
- Quality of training data matters most
- Overfitting is common pitfall

**Algorithms covered**:
1. **SVM**: Binary classification (normal vs attack)
2. **Random Forest**: Multi-class (attack type identification)
3. **LSTM Autoencoder**: Sequence anomaly detection

**Feature engineering**:
- What features to extract from CAN traffic?
- Time-domain: frequency, inter-arrival time
- Payload: entropy, byte distribution
- Sequential: n-grams, temporal patterns

**Model evaluation**:
- Training vs validation vs test split
- Confusion matrix interpretation
- ROC curves and AUC

**Common student mistakes**:
- Training and testing on same data
- Not normalizing features
- Choosing overly complex models

**Lab prep**: Provide labeled dataset (normal + attack captures)

---

### Class 12: Fingerprinting

**Learning objectives**: Clock skew analysis, device identification, hardware characteristics

**Most technically challenging class**: Be prepared for confusion

**Clock skew explanation**:
- All oscillators drift slightly
- Drift is consistent per device (hardware-dependent)
- Measure timestamp offsets over time
- Least squares regression to estimate skew

**Visual aids critical**:
- Plot timestamp offsets showing linear drift
- Show different slopes for different devices
- Demonstrate fingerprint matching

**Math background**:
- Linear regression review
- Residual analysis
- Confidence intervals

**Practical limitations**:
- Requires many messages over time
- Sensitive to temperature changes
- Distinguishes hardware, not software changes

**Lab prep**: Explain that fingerprinting is slowest IDS—complementary, not primary

---

### Class 13: Ensemble and XAI

**Learning objectives**: Combining detectors, voting strategies, explainable AI, dashboard design

**Ensemble approaches**:
1. **Parallel**: All detectors run, vote on decision
2. **Serial**: First detector filters, others refine
3. **Hierarchical**: Fast detectors first, slow ones on suspicious traffic

**Voting strategies**:
- Majority vote
- Weighted vote (based on historical accuracy)
- Threshold: N out of M detectors must agree

**Explainable AI (XAI)**:
- Why did IDS trigger alert?
- Which feature(s) were anomalous?
- Human-readable explanations

**Dashboard design**:
- Real-time vs historical views
- Alert prioritization
- Investigation workflow

**Lab prep**: This is the culmination—student dashboards should integrate all prior work

---

### Class 14: Defense Architecture

**Learning objectives**: Defense-in-depth, network segmentation, incident response, capstone preparation

**Defense-in-depth layers**:
1. Physical security (access control)
2. Network segmentation (VLANs, air gaps)
3. Device authentication (if possible)
4. Intrusion detection (this course's focus)
5. Incident response (playbooks)

**Capstone briefing**:
- Team assignments
- Rules of engagement
- Scoring criteria
- Timeline

**Red team vs blue team**:
- Explain role rotation (everyone plays both)
- Emphasize learning, not competition
- Document everything for later analysis

**Capstone logistics**:
- 3-hour lab block
- Instructor monitors all activity
- Video recording for post-mortem

---

## Common Student Questions and Misconceptions

### Questions About Course Content

**Q: "Do we need to know maritime/boating stuff?"**
**A:** No prior maritime knowledge required. We teach the relevant domain knowledge as needed. However, curiosity about how vessels work helps with motivation and context.

**Q: "I've never soldered before. Will I break something?"**
**A:** Soldering is a learned skill. We provide instruction, supervision, and spare components. Most students successfully build hardware with no prior experience. Practice on scrap wire first.

**Q: "Can we use this to hack real boats?"**
**A:** Absolutely not. All activities are on isolated test networks. Unauthorized access to vessel systems is illegal and dangerous. This course teaches defense through understanding offense.

**Q: "Will we learn about GPS spoofing with radios?"**
**A:** This course focuses on network-level spoofing (injecting false CAN messages), not RF GPS spoofing. Network spoofing is sufficient to manipulate vessel systems without jamming GPS signals.

**Q: "Why CAN bus? Don't ships use Ethernet now?"**
**A:** Modern vessels use both. CAN/NMEA 2000 remains the backbone for real-time sensor and control systems due to determinism and reliability. Ethernet is used for IT systems (email, navigation software) but not safety-critical controls.

**Q: "How much programming is required?"**
**A:** Labs involve Python scripting for traffic analysis and ML implementation. You should be comfortable with loops, functions, file I/O, and using libraries. We provide code templates, but you must understand and modify them.

**Q: "Is the hardware reusable after the course?"**
**A:** Yes! The OpenBridge device is yours to keep (if hardware budget allows). Many students use it for senior projects, research, or personal maritime projects.

### Common Misconceptions

**Misconception 1: "This is like web hacking with SQL injection and XSS"**
**Reality**: This is embedded systems and industrial control security. The attack surface, tools, and defenses are completely different. Network protocols, not application vulnerabilities, are the focus.

**Misconception 2: "Machine learning will perfectly detect all attacks"**
**Reality**: ML is one tool in the toolbox. It has false positives, requires training data, and can be evaded. Ensemble approaches combining multiple techniques work best.

**Misconception 3: "We can just encrypt CAN messages to solve security"**
**Reality**: CAN was designed for real-time, low-latency control. Adding encryption/authentication is challenging due to 8-byte payload limits and timing constraints. Industry is working on CAN-FD with security features, but retrofit is difficult.

**Misconception 4: "If I can attack the test network, I understand security"**
**Reality**: Attacking is the easy part. Defending—designing systems that resist attacks while maintaining safety and availability—is much harder. That's why the second half focuses on detection and defense.

**Misconception 5: "All vessels use NMEA 2000"**
**Reality**: NMEA 2000 is common on smaller vessels (yachts, fishing boats). Large commercial vessels often use proprietary systems or fieldbus protocols (Profibus, NMEA 0183). However, CAN principles apply broadly.

**Misconception 6: "Frequency-based detection will catch spoofing"**
**Reality**: Sophisticated attackers match message timing to legitimate devices. Frequency IDS catches careless attacks but must be combined with other methods (entropy, fingerprinting) for robust detection.

### Technical Confusions

**Confusion: Big-endian vs little-endian**
**Clarification**: CAN headers are big-endian (most significant byte first), but NMEA 2000 data fields are little-endian. Always check the PGN specification for field byte order.

**Confusion: Source Address vs Device Instance**
**Clarification**: Source Address (SA) identifies the device on the network (0-253). Device Instance distinguishes multiple devices of the same type (e.g., two GPS receivers). They're different fields.

**Confusion: PGN vs CAN ID**
**Clarification**: CAN ID (29-bit) contains priority, PGN, and source address. PGN (Parameter Group Number) is extracted from bits within the CAN ID. One PGN can have multiple CAN IDs depending on source.

**Confusion: Frequency detection "window size"**
**Clarification**: Window size is the time period over which messages are counted (e.g., 1 second, 10 seconds). Smaller windows detect attacks faster but have more noise. Larger windows are more stable but slower.

**Confusion: Entropy calculation**
**Clarification**: For CAN payloads, entropy is calculated over byte value frequencies within a window of messages. A payload of all zeros has zero entropy; random bytes have maximum entropy (~8 bits per byte).

**Confusion: LSTM autoencoder "reconstruction error"**
**Clarification**: The model learns to reproduce normal sequences. For normal traffic, reconstruction error is low. For attacks (different patterns), error is high. Threshold on error determines anomaly detection.

---

## Safety and Ethics Guidance

### Teaching Attack Techniques Responsibly

**Core principles**:
1. **Context matters**: Teach attacks to develop defenders, not to enable malicious activity
2. **Ethics precede techniques**: Discuss consequences before teaching methods
3. **Controlled environment**: All attacks on isolated, air-gapped test networks
4. **Legal compliance**: Unauthorized access is illegal—emphasize federal/state laws
5. **Responsible disclosure**: If vulnerabilities found, report through proper channels

### Ethics Agreement (Before Attack Labs)

**Required before Week 6**: Students must sign and understand ethics agreement covering:

- All attack activities confined to isolated test network
- No application of techniques to real vessels without authorization
- Potential legal consequences (CFAA, state laws)
- Professional responsibility as cybersecurity practitioners
- Reporting suspected misuse to instructor immediately

**Instructor responsibility**: Verify signed agreements on file before allowing access to attack labs.

### Safety Warnings (Every Attack Lab)

Standard opening for Labs 06-08:

> **CRITICAL SAFETY WARNING**
>
> The attacks demonstrated in this lab, if applied to real vessel systems, could cause:
> - Vessel grounding or collision
> - Loss of human life
> - Environmental disasters (oil spills, pollution)
> - Economic damage (ship loss, cargo damage)
>
> All activities in this course are conducted on ISOLATED TEST NETWORKS ONLY.
>
> Unauthorized access to computer systems is illegal under federal law (Computer Fraud and Abuse Act) and state laws. Penalties include:
> - Federal prison sentences up to 20 years
> - Fines up to $250,000
> - Civil liability for damages
> - Permanent criminal record affecting employment
>
> This knowledge is taught for DEFENSIVE purposes—to train cybersecurity professionals who can protect maritime systems.

**Read this aloud at the start of each attack lab**. Require verbal acknowledgment from each student.

### Recognizing Warning Signs

Be alert for students who:
- Express interest in applying techniques outside lab environment
- Ask about evading detection on "real networks"
- Discuss targeting specific vessels or organizations
- Attempt to access non-isolated networks from lab computers

**If concerning behavior observed**:
1. Document the incident
2. Have private conversation with student about ethics and legal risks
3. Report to department chair or dean of students if behavior continues
4. Consider removing student from course if serious violation

### Legal Knowledge for Instructors

**Key laws**:
- **Computer Fraud and Abuse Act (CFAA)**: Federal law prohibiting unauthorized computer access
- **State computer crime laws**: Vary by state, often more restrictive than CFAA
- **Maritime security regulations**: IMO, Coast Guard regulations on vessel cybersecurity

**Institution policies**:
- Review your institution's acceptable use policy
- Ensure IRB approval if using real vessel data
- Coordinate with IT security about isolated network
- Have legal counsel review course materials if concerns arise

### Creating Ethical Culture

**Throughout the course**:
- Emphasize defender's mindset
- Share stories of responsible disclosure
- Discuss career paths in maritime cybersecurity (USCG, classification societies, shipping companies)
- Invite guest speakers from industry discussing real-world defense challenges
- Highlight the NICE Framework and professional certifications (CISSP, GICSP)

**Positive framing**: "We're learning to be protectors, not attackers. Understanding threats makes us better defenders."

---

## Assessment Rubrics

### Lab Report Rubric (40% of grade)

Each lab report graded on 100-point scale:

| Criterion | Excellent (90-100) | Good (80-89) | Satisfactory (70-79) | Needs Improvement (<70) |
|-----------|-------------------|--------------|----------------------|------------------------|
| **Objective Summary** (10 pts) | Clear, concise summary of lab goals | Summarizes most objectives | Vague or incomplete | Missing or incorrect |
| **Methodology** (25 pts) | Detailed steps, commands with explanations | Commands included, minimal explanation | Steps present but unclear | Steps missing or incorrect |
| **Evidence** (20 pts) | Screenshots/captures with annotations | Screenshots present, minimal context | Evidence insufficient | Evidence missing |
| **Analysis** (30 pts) | Deep analysis connecting theory to results | Basic analysis, some connections | Minimal analysis, mostly descriptive | No analysis, just procedure |
| **Answers to Questions** (10 pts) | All questions answered completely | Most questions answered | Some questions incomplete | Questions unanswered |
| **Writing Quality** (5 pts) | Professional, clear, error-free | Minor grammatical issues | Several errors affecting clarity | Difficult to understand |

**Late policy**: -10% per day late, up to 3 days. After 3 days, no credit.

### Midterm Exam Rubric (15% of grade)

**Part 1: Traffic Decoding (40 points)**
- Header decode (10 pts): Priority, PGN, SA correctly extracted
- PGN identification (10 pts): Correct PGN names and types
- Data interpretation (20 pts): Field values correctly calculated and interpreted

**Part 2: Attack Identification (40 points)**
- Attack type (15 pts): Correctly identifies spoofing, DoS, or replay
- Parameters (15 pts): Attack timing, frequency, injected values
- Impact assessment (10 pts): Explains effect on vessel systems

**Part 3: Mitigation (20 points)**
- Defense strategies (10 pts): Proposes appropriate countermeasures
- Justification (10 pts): Explains why strategies would work

**Grading notes**: Partial credit for methodology even if wrong answer. Show your work!

### Capstone Exercise Rubric (15% of grade)

**Team deliverables (70 points)**:
- Attack plan creativity (15 pts)
- Attack execution (20 pts)
- Defense configuration (15 pts)
- Detection accuracy (20 pts)

**Individual deliverables (30 points)**:
- Written reflection (15 pts): What worked, what didn't, lessons learned
- Peer evaluation (15 pts): Contribution to team effort

**Bonus points** (up to 10):
- Most creative evasion technique
- Best defense architecture
- Most thorough documentation

### Participation Rubric (10% of grade)

Assessed throughout semester:

| Level | Description | Grade |
|-------|-------------|-------|
| **Excellent** | Regular attendance, active in discussions, helps peers, asks insightful questions | 90-100 |
| **Good** | Regular attendance, participates when called on, completes peer review | 80-89 |
| **Satisfactory** | Attends most classes, minimal participation, basic peer engagement | 70-79 |
| **Needs Improvement** | Frequent absences, no participation, does not contribute to team | <70 |

---

## Troubleshooting Common Issues

### Hardware Problems

#### Problem: Teensy not recognized by computer

**Symptoms**: Device not appearing in Arduino IDE, can't upload firmware

**Solutions**:
1. Try different USB cable (some are charge-only, need data cable)
2. Install Teensy drivers (Windows): https://www.pjrc.com/teensy/td_download.html
3. Check USB port isn't damaged
4. Try another computer to isolate issue
5. Press reset button on Teensy while uploading

#### Problem: CAN messages not being sent/received

**Symptoms**: `candump` shows no traffic from student device

**Solutions**:
1. Check wiring: MOSI (11), MISO (12), SCK (13), CS (10) for Teensy 4.x
2. Verify CAN_H and CAN_L connections (not swapped)
3. Check termination resistors (120Ω) at both ends of bus
4. Measure voltage: CAN_H should be ~3.5V, CAN_L ~1.5V when idle
5. Verify bitrate: 250kbps for NMEA 2000
6. Check if CAN interface is up: `ip link show can0`

#### Problem: MCP2515 communication failure

**Symptoms**: SPI errors, initialization fails

**Solutions**:
1. Verify 3.3V or 5V logic level compatibility
2. Check SPI bus not shared with SD card or other peripherals
3. Measure with oscilloscope if available (clock, data lines)
4. Try lower SPI clock speed in firmware
5. Replace MCP2515 module (manufacturing defects happen)

### Software Problems

#### Problem: Python import errors

**Symptoms**: `ModuleNotFoundError: No module named 'pandas'`

**Solutions**:
1. Install requirements: `pip3 install -r requirements.txt`
2. Check Python version: `python3 --version` (need 3.7+)
3. Verify virtual environment activated
4. Use correct pip: `which pip3` (should match Python path)

#### Problem: Permission denied accessing CAN interface

**Symptoms**: `Operation not permitted` when running `candump`

**Solutions**:
1. Add user to dialout group: `sudo usermod -a -G dialout $USER`
2. Log out and back in for group change to take effect
3. Check interface permissions: `ls -l /dev/ttyACM0`
4. Run with sudo as temporary workaround (not recommended long-term)

#### Problem: Wireshark not showing CAN traffic

**Symptoms**: Interface doesn't appear or no packets captured

**Solutions**:
1. Install Wireshark with CAN support: `sudo apt-get install wireshark`
2. Add user to wireshark group: `sudo usermod -a -G wireshark $USER`
3. Enable SocketCAN interface in Wireshark settings
4. Verify traffic with `candump` first (troubleshoots Wireshark vs actual traffic)

### Lab-Specific Problems

#### Lab 04: Hardware assembly issues

**Symptom**: Device built but not working

**Checklist**:
- [ ] Power LED on Teensy illuminated?
- [ ] MCP2515 power connections correct?
- [ ] SPI wiring: MOSI, MISO, SCK, CS correct pins?
- [ ] CAN_H and CAN_L not swapped?
- [ ] Termination resistors present (120Ω)?
- [ ] Firmware uploaded successfully?
- [ ] Correct Teensy board selected in Arduino IDE?

#### Lab 06: Spoofing not affecting chart plotter

**Symptom**: Injected position messages not displayed

**Solutions**:
1. Verify PGN encoding (129025 for position)
2. Check byte order (little-endian for NMEA 2000)
3. Verify Source Address doesn't conflict with legitimate GPS
4. Check message timing—may need higher frequency to override
5. Ensure chart plotter listening to correct device instance
6. Try spoofing with higher priority (lower priority byte value)

#### Lab 09: Frequency IDS false positive rate too high

**Symptom**: Detection system triggers on normal traffic

**Solutions**:
1. Increase baseline observation period (collect more data)
2. Adjust threshold (increase Z-score cutoff)
3. Check for legitimate traffic variability (some devices have irregular periods)
4. Implement separate baselines per PGN (not global threshold)
5. Use median absolute deviation instead of standard deviation (robust to outliers)

#### Lab 11: ML model not training/poor performance

**Symptom**: Model accuracy below 80%, loss not decreasing

**Solutions**:
1. Check training data balance (equal normal and attack samples)
2. Verify features normalized (mean=0, std=1)
3. Reduce model complexity (fewer layers, smaller hidden size)
4. Increase training data size (need hundreds of examples minimum)
5. Check for data leakage (test data in training set)
6. Try different hyperparameters (learning rate, batch size)
7. Visualize features with scatter plot (verify classes are separable)

### Network Problems

#### Problem: Entire lab network down

**Symptom**: No student can see traffic

**Emergency checklist**:
1. Check instructor Raspberry Pi is powered on
2. Verify simulator running: `ps aux | grep canboat`
3. Check CAN interface up: `ip link show can0`
4. Restart CAN interface:
   ```bash
   sudo ip link set can0 down
   sudo ip link set can0 up type can bitrate 250000
   ```
5. Check termination resistors not disconnected
6. Restart traffic simulator

#### Problem: Intermittent packet loss

**Symptom**: Some messages missing, `ifconfig` shows errors

**Solutions**:
1. Check cable quality (twisted pair recommended)
2. Verify single-point grounding (no ground loops)
3. Reduce bus length if exceeds 100m
4. Check for electrical noise sources nearby
5. Verify 120Ω termination at both ends (not middle)
6. Lower bitrate if necessary (250kbps standard, but can reduce)

---

## Additional Resources for Instructors

### Recommended Background Reading

**Maritime Cybersecurity**:
- IMO MSC-FAL.1/Circ.3: "Guidelines on Maritime Cyber Risk Management"
- "Cybersecurity for Ports and Port Systems" (MITRE, 2016)
- BIMCO's "Guidelines on Cyber Security Onboard Ships"

**CAN Bus Security**:
- Miller & Valasek (2015): "Remote Exploitation of an Unaltered Passenger Vehicle"
- Hoppe et al. (2008): "Security Threats to Automotive CAN Networks—Practical Examples and Selected Short-Term Countermeasures"
- Checkoway et al. (2011): "Comprehensive Experimental Analyses of Automotive Attack Surfaces"

**Industrial Control Systems Security**:
- NIST SP 800-82: "Guide to Industrial Control Systems (ICS) Security"
- SANS ICS Security Reading Room
- ICS-CERT advisories and publications

### Professional Development

**Certifications relevant to instructors**:
- GICSP (Global Industrial Cyber Security Professional)
- CISSP (Certified Information Systems Security Professional)
- GCDA (GIAC Certified Detection Analyst)

**Conferences**:
- Black Hat / DEF CON (Industrial Village)
- S4x Events (ICS security)
- ICCWS (International Conference on Cyber Warfare and Security)

**Online communities**:
- Reddit: r/ICS, r/cybersecurity
- Twitter: #ICSsecurity, #maritime cybersecurity
- SANS ICS mailing list

### Staying Current

**Maritime cybersecurity evolves rapidly**. Keep course current by:

1. **Subscribe to advisories**:
   - ICS-CERT (CISA)
   - Coast Guard Maritime Commons
   - Classification society bulletins (ABS, DNV, Lloyd's)

2. **Monitor incidents**:
   - Maritime security news sites
   - Lloyd's List Intelligence
   - Fairplay shipping news

3. **Industry engagement**:
   - Guest speakers from shipping companies, classification societies
   - Internship partnerships
   - Advisory board with maritime industry representatives

4. **Research integration**:
   - Assign students to read recent papers
   - Incorporate new detection techniques as discovered
   - Update attack lab scenarios with real-world incidents

### Course Improvement

**After each semester**:
1. Collect student feedback (course evaluations)
2. Review lab completion rates (identify bottlenecks)
3. Analyze exam performance (weak topics)
4. Update content based on industry changes
5. Refresh hardware/software as needed

**Maintain version control**: Keep course materials in Git repository with changelog documenting updates.

---

## Conclusion

Teaching maritime OT security is rewarding but challenging. Students leave with skills directly applicable to protecting critical infrastructure. The hands-on approach—building hardware, executing attacks, implementing defenses—creates deep understanding that pure theory cannot match.

**Key success factors**:
1. **Safety first**: Establish ethical culture from day one
2. **Hands-on focus**: Minimize lecture, maximize lab time
3. **Real-world connections**: Use actual incidents and industry examples
4. **Supportive environment**: Encourage questions, celebrate failures as learning
5. **Industry relevance**: Align with NICE Framework, teach practical skills

By the end of 14 weeks, students will have:
- Built a CAN interface from scratch
- Decoded NMEA 2000 messages
- Executed realistic attacks in controlled environment
- Implemented multiple detection algorithms
- Designed defense architecture
- Developed attacker mindset to become better defenders

These are skills that employers in maritime, automotive, aviation, and industrial control systems value highly.

**Good luck with your course!** Reach out to the maritime cybersecurity education community for support—we're all working toward the same goal of securing critical infrastructure.

---

**Document Version**: 1.0
**Last Updated**: 2026-01-06
**Author**: Constantine Macris
**License**: CC BY-SA 4.0

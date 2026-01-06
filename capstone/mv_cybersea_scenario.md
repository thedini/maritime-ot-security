---
title: "M/V CyberSea: Vessel Scenario & Specifications"
vessel_type: "Container Ship"
owner: "CyberSea Shipping Lines"
classification: "Fictional Training Scenario"
purpose: "Capstone Project Context"
---

# M/V CyberSea: Vessel Scenario & Specifications

## Executive Summary

The **M/V CyberSea** is a modern, digitally integrated container ship operated by CyberSea Shipping Lines. As maritime operations become increasingly connected, the company recognizes the growing cybersecurity risks to vessel operations, cargo integrity, and crew safety. Your team has been hired to conduct a comprehensive security assessment and design a robust cybersecurity architecture for this vessel.

This document provides the detailed context, technical specifications, and constraints for your capstone project.

---

## Vessel Overview

### Basic Specifications

| Specification | Value |
|--------------|-------|
| **Vessel Name** | M/V CyberSea |
| **Vessel Type** | Container Ship (Fully Cellular) |
| **Flag State** | Panama |
| **Classification Society** | Lloyd's Register |
| **IMO Number** | 9876543 (fictional) |
| **Call Sign** | H3CS (fictional) |
| **Owner/Operator** | CyberSea Shipping Lines |
| **Management Company** | CyberSea Ship Management Ltd. |
| **Built** | 2021 |
| **Shipyard** | Hyundai Heavy Industries, South Korea |

### Physical Characteristics

| Characteristic | Value |
|---------------|-------|
| **Length Overall (LOA)** | 300 meters (984 feet) |
| **Beam** | 48.2 meters (158 feet) |
| **Draft (Maximum)** | 14.5 meters (47.6 feet) |
| **Gross Tonnage** | 85,000 GT |
| **Deadweight Tonnage** | 95,000 DWT |
| **TEU Capacity** | 8,500 TEU (Twenty-foot Equivalent Units) |
| **Reefer Plugs** | 1,000 (for refrigerated containers) |
| **Service Speed** | 22 knots |
| **Main Engine** | MAN B&W 9S90ME-C10.5 (two-stroke diesel) |
| **Auxiliary Engines** | 4 × Wärtsilä 8L46F (diesel generators) |
| **Propulsion** | Single fixed-pitch propeller |
| **Bow Thruster** | Yes (for maneuvering in port) |

### Crew & Operations

| Aspect | Details |
|--------|---------|
| **Crew Complement** | 24 officers and ratings |
| **Bridge Officers** | Master, Chief Officer, 2nd Officer, 3rd Officer, 4 Junior Officers |
| **Engineering Officers** | Chief Engineer, 2nd Engineer, 3rd Engineer, 4th Engineer, 2 Junior Engineers |
| **Ratings** | Bosun, ABs, Oilers, Electrician, Fitter, Cook, Steward |
| **Voyage Duration** | Typical: 30-45 days (Asia-Europe route) |
| **Port Calls** | 8-12 ports per voyage |
| **Flag State Inspections** | Annual + Port State Control inspections |

---

## Operational Profile

### Trade Routes

M/V CyberSea primarily operates on the **Asia-Europe trade route**, one of the world's busiest shipping lanes:

**Typical Route**:
1. **Shanghai, China** (load port)
2. **Ningbo, China**
3. **Yantian, China**
4. **Singapore** (fuel bunker, transshipment)
5. **Suez Canal transit**
6. **Rotterdam, Netherlands** (discharge/load)
7. **Hamburg, Germany**
8. **Felixstowe, UK**
9. **Le Havre, France**
10. **Return voyage** (reverse route with some variation)

**Voyage Characteristics**:
- **Distance**: ~11,000 nautical miles (one way)
- **Duration**: 30-35 days (round trip)
- **At Sea**: 60-70% of voyage time
- **In Port**: 30-40% of voyage time (cargo operations, crew changes, maintenance)

### Cargo Profile

M/V CyberSea carries diverse containerized cargo:

- **Dry containers**: 70% (consumer goods, machinery, automotive parts)
- **Refrigerated containers (reefers)**: 20% (food products, pharmaceuticals)
- **Dangerous goods (IMO Classes 1-9)**: 5% (regulated under IMDG Code)
- **High-value cargo**: 5% (electronics, luxury goods)

**Cargo Information Systems**:
- Electronic cargo manifests
- Reefer container monitoring (temperature, humidity, alarms)
- Dangerous goods tracking and compliance
- Integration with port EDI (Electronic Data Interchange) systems

---

## Technology & Systems Architecture

### Bridge & Navigation Systems

The bridge is equipped with modern integrated navigation systems:

**Integrated Navigation System (INS)**:
- **Manufacturer**: Wärtsilä NACOS Platinum
- **Components**: ECDIS, radar, GPS, AIS, autopilot, gyrocompass
- **Redundancy**: Dual ECDIS, dual radar (X-band + S-band), backup GPS

**Electronic Chart Display and Information System (ECDIS)**:
- **Primary**: Wärtsilä ECDIS (Windows 7 Embedded, as of scenario date)
- **Backup**: Wärtsilä ECDIS (separate hardware)
- **Chart Provider**: Admiralty Vector Chart Service (AVCS)
- **Updates**: Quarterly via CD-ROM or USB (manual installation)

**GPS & Positioning**:
- **Primary GPS**: Furuno GP-170
- **Backup GPS**: Hemisphere Vector VS330
- **Differential GPS (DGPS)**: Fugro Starfix HP (satellite corrections)
- **Gyrocompass**: Tokyo Keiki TG-8000

**Radar Systems**:
- **X-band Radar**: Furuno FAR-3210 (primary target detection)
- **S-band Radar**: Furuno FAR-2228 (backup, long-range)
- **ARPA**: Automatic Radar Plotting Aid (collision avoidance)

**Automatic Identification System (AIS)**:
- **Transponder**: Furuno FA-170
- **Function**: Broadcasts vessel position, course, speed; receives data from nearby vessels
- **Integration**: Feeds to ECDIS and radar displays

**Autopilot**:
- **System**: Simrad AP505
- **Integration**: Receives input from gyrocompass, GPS, wind sensors
- **Modes**: Heading hold, track follow, turn control

**Communication Systems**:
- **GMDSS**: Global Maritime Distress and Safety System (SOLAS compliance)
  - **VHF Radio**: Furuno FM-8900S
  - **MF/HF Radio**: Furuno FS-5000
  - **Inmarsat-C**: Furuno Felcom 500 (distress alerts, SafetyNET)
  - **EPIRB**: Emergency Position Indicating Radio Beacon (Jotron Tron 60S)
- **VSAT Satellite Internet**: KVH TracPhone V11 (Fleet Xpress via Inmarsat)
  - **Bandwidth**: 2 Mbps down / 512 Kbps up (shared across vessel)
  - **Uses**: Fleet management, email, crew welfare, weather routing

**Voyage Data Recorder (VDR)**:
- **System**: Furuno VR-7000
- **Function**: "Black box" recording audio, position, radar, alarms, bridge communications
- **Storage**: 30 days rolling (tamper-proof capsule)

**Weather Routing**:
- **System**: SPOS Weather Routing System
- **Function**: Optimized routing for fuel efficiency and weather avoidance
- **Data Source**: Commercial weather service via satellite

**Bridge Alert Management System (BAMS)**:
- **Function**: Centralized alarm and alert management (IMO MSC.302(87) compliance)
- **Integration**: Aggregates alarms from navigation, engine, cargo systems

**Ship Security Alert System (SSAS)**:
- **Function**: Covert distress signal to flag state and company in case of piracy or hijacking
- **Activation**: Hidden buttons on bridge

### Engine & Machinery Control

The engine control room and machinery spaces are equipped with:

**Engine Control System (ECS)**:
- **System**: MAN B&W ECS-11
- **Platform**: Industrial PC running Windows Embedded or proprietary RTOS
- **Function**: Monitor and control main engine, auxiliaries, fuel, lube oil, cooling
- **Interface**: HMI (Human-Machine Interface) touchscreen displays

**Propulsion Control**:
- **Main Engine Telegraph**: Electronic control from bridge to engine control
- **Propeller Pitch**: Fixed (no CPP control)
- **Remote Control**: Bridge control of engine from bridge console

**Auxiliary Systems**:
- **Generator Control**: Wärtsilä WECS 8000 (load management, generator sequencing)
- **Fuel Management**: Automated fuel transfer, filtering, heating for HFO (Heavy Fuel Oil)
- **Ballast Control**: Automated ballast pump control for trim and stability
- **Bilge & Firefighting**: Pump control systems

**Monitoring & Sensors**:
- **Temperature**: Engine, exhaust, cooling water, lube oil
- **Pressure**: Fuel, lube oil, air, hydraulic
- **Level**: Fuel tanks, lube oil sumps, bilge, ballast
- **Flow Meters**: Fuel consumption, seawater cooling

**Emissions Monitoring**:
- **System**: Continuous Emissions Monitoring System (CEMS) for SOx, NOx compliance
- **Regulations**: IMO MARPOL Annex VI (sulfur limits, NOx Tier III in ECAs)

**Shaft Power Monitoring**:
- **Torque Meter**: Real-time propeller shaft power measurement
- **Purpose**: Performance monitoring, fuel efficiency optimization

**Alarm & Safety Systems**:
- **Engine Room Alarm System**: Temperature, pressure, level alarms
- **Fire Detection**: Smoke and heat detectors throughout machinery spaces
- **Fixed Fire Suppression**: CO2 flooding system
- **Emergency Shutdown (ESD)**: Automatic shutdown on critical alarms

### Cargo Management Systems

**Container Tracking System**:
- **System**: CargoSmart Container Tracking
- **Function**: Real-time location and status of containers (loaded, discharged, on board)
- **Integration**: Interfaces with port EDI systems, shipping line databases

**Reefer Container Monitoring**:
- **System**: Carrier Transicold Remote Container Management
- **Function**: Monitor temperature, humidity, power consumption, alarms for refrigerated containers
- **Interface**: Web-based dashboard accessible from bridge and shore
- **Alerting**: Email/SMS alerts for temperature deviations or failures

**Cargo Loading Computer**:
- **System**: Navis StowMan
- **Function**: Calculate stability, stress, trim; generate loading plans
- **Input**: Container weights, positions, ballast
- **Output**: Loading instructions for stevedores, stability documents

**Dangerous Goods Tracking**:
- **Function**: Maintain manifest of IMDG Class cargo (segregation, emergency response)
- **Compliance**: SOLAS, IMDG Code requirements

**Lashing & Securing Monitors**:
- **System**: Manual inspections logged digitally
- **Purpose**: Ensure containers properly secured (prevent shifting in heavy weather)

### IT & Enterprise Systems

**Network Architecture**:
- **Core Switch**: Cisco Catalyst 2960 (24-port, managed)
- **Wireless Access Points**: Ubiquiti UniFi AP AC (crew areas, bridge, offices)
- **Firewall**: Fortinet FortiGate 60E (between IT network and external communications)
- **DMZ**: Separate zone for email relay, fleet management gateway

**Servers**:
- **Email Server**: Microsoft Exchange 2016 (on-premises)
- **File Server**: Windows Server 2019 (crew documents, manuals, forms)
- **Fleet Management Gateway**: Dell PowerEdge T340 (interfaces with shore-based fleet system)

**Workstations**:
- **Bridge**: 2 × Dell OptiPlex (Windows 10) for administrative tasks, weather, email
- **Ship Office**: 2 × Dell OptiPlex (Windows 10) for Master, Chief Officer
- **Engine Office**: 1 × Dell OptiPlex (Windows 10) for Chief Engineer
- **Crew Lounge**: 2 × shared laptops (Windows 10)

**Email & Communications**:
- **Shore Email**: Microsoft Outlook via VSAT
- **Fleet Messaging**: Inmarsat C (text messaging for critical ops)
- **Video Conferencing**: Zoom (limited use due to bandwidth)

**Software**:
- **Office Suite**: Microsoft Office 2019
- **PDF Reader**: Adobe Acrobat Reader
- **Technical Manuals**: Electronic documentation (vendor PDFs)
- **Antivirus**: McAfee Endpoint Security (definitions updated monthly via VSAT)

**Backup & Recovery**:
- **Backup System**: USB hard drives (manual weekly backups)
- **No automated backup**: Limited IT support onboard

### Crew Welfare & Personal Devices

**Crew Wi-Fi Network**:
- **System**: Separate SSID ("CyberSea_Crew") from operational networks
- **Bandwidth**: Limited allocation from VSAT (256 Kbps shared among crew)
- **Devices**: Personal laptops, smartphones, tablets
- **Usage**: Social media, email, messaging, video calls to family
- **Policy**: No official BYOD policy; crew discouraged from connecting personal devices to operational networks

**Entertainment Systems**:
- **TV/Satellite**: DirecTV or similar satellite TV service
- **Movie Server**: Local media server with movies and TV shows

---

## Current Security Posture

### Existing Security Measures

CyberSea Shipping Lines has implemented some basic cybersecurity measures, but gaps remain:

**Network Security**:
- **Firewall**: Fortinet FortiGate at perimeter (DMZ to internet)
  - **Rule Quality**: Basic rules; some "any/any" rules for convenience
  - **Management**: Rarely updated; last reviewed 18 months ago
- **VLAN Segmentation**: Limited (IT and OT on some separate VLANs, but not comprehensive)
- **Crew Wi-Fi**: Separate SSID, but on same physical network infrastructure

**Endpoint Security**:
- **Antivirus**: McAfee installed on Windows workstations
  - **Update Frequency**: Monthly (manual download via VSAT due to bandwidth)
  - **Coverage**: IT workstations only; no AV on ECDIS or ECS systems
- **Patching**: Ad-hoc; no formal patch management process
  - **ECDIS**: Windows 7 Embedded (EOL January 2020), no updates since 2019
  - **ECS**: Vendor proprietary; patches require vendor technician visit (rare)
  - **Workstations**: Occasional Windows updates, not consistently applied

**Access Controls**:
- **Passwords**: Basic password policy (8 characters, no complexity requirements)
  - **Default Passwords**: Some systems (engine controls, switches) still use vendor defaults
- **User Accounts**: Shared accounts common (e.g., "Master" account on bridge workstations)
- **Physical Access**: Badge system for bridge and engine control room; many areas unlocked

**Monitoring & Detection**:
- **No IDS/IPS**: No intrusion detection or prevention systems deployed
- **Logging**: Basic logs on firewalls and servers, but not centralized or reviewed
- **SIEM**: None
- **Alerting**: No automated security alerting

**Incident Response**:
- **Plan**: Generic IT incident response plan (not maritime-specific)
- **Training**: No crew training on cybersecurity incident response
- **Drills**: No cyber incident drills conducted
- **Contacts**: Limited contact list for cybersecurity incidents

**Operational Security**:
- **USB Policy**: Informal policy discouraging USB use, but not enforced
- **BYOD**: No formal policy; crew connect personal devices to crew Wi-Fi (unmanaged)
- **Vendor Access**: Third-party vendors (ECDIS, engine systems) connect via laptops during port calls; access not always monitored

**Security Awareness**:
- **Training**: Brief cybersecurity section in onboarding (30 minutes, outdated content)
- **Phishing Awareness**: None
- **Crew Culture**: General awareness of cybersecurity, but not prioritized

### Known Vulnerabilities

Based on industry reports and initial assessments, M/V CyberSea likely has vulnerabilities similar to other modern vessels:

1. **Outdated Operating Systems**: ECDIS on Windows 7 (EOL), vulnerable to known exploits
2. **Unpatched Systems**: Lack of regular patching across IT and OT systems
3. **Weak Network Segmentation**: Potential for lateral movement from IT to OT networks
4. **Default Credentials**: Some systems using vendor default passwords
5. **Lack of Monitoring**: No visibility into network traffic or security events
6. **USB Risks**: No technical controls on USB ports; risk of malware introduction
7. **Crew Device Risks**: Personal devices on crew Wi-Fi with no security posture checks
8. **VSAT Exposure**: Direct internet connectivity with basic firewall protection
9. **Vendor Access**: Uncontrolled third-party remote access during maintenance

### Recent Incidents

CyberSea Shipping Lines has experienced minor security incidents:

- **6 months ago**: Crew member's laptop infected with malware (adware); spread to another workstation via shared USB drive. Remediated by reformatting laptops.
- **1 year ago**: Phishing email targeted Master; Master did not click link, but reported no formal procedure for reporting.
- **2 years ago**: Port-side shore connection introduced malware to file server; detected when files became corrupted. Restored from backup.

**No major incidents** affecting navigation or propulsion to date, but the company recognizes the risk.

---

## Regulatory & Compliance Requirements

### International Maritime Organization (IMO)

CyberSea must comply with:

**IMO Resolution MSC-FAL.1/Circ.3** (July 2017):
- **Guidelines on Maritime Cyber Risk Management**
- **Requirement**: Cyber risks to be addressed in Safety Management Systems (SMS) by January 1, 2021 (already in effect)
- **Functional Elements**: Identify, Protect, Detect, Respond, Recover

**SOLAS (Safety of Life at Sea)**:
- **Chapter V**: Safety of navigation (includes cybersecurity implications for navigation systems)
- **Chapter XI-2**: Ship and port facility security (ISPS Code)

**MARPOL Annex VI**:
- **Emissions Monitoring**: Cybersecurity of CEMS (Continuous Emissions Monitoring Systems)

### Flag State Requirements

**Panama Maritime Authority**:
- Compliance with IMO resolutions
- Annual flag state inspections include SMS review (cyber risk management required)

### Classification Society

**Lloyd's Register**:
- **Cyber Rules**: Optional cyber resilience notation (CY-SCM, CY-SPM)
- **Requirement**: For new notation, demonstrate cyber risk management aligned with IMO guidelines

### Port State Control

**Port State Control (PSC) Inspections**:
- European Maritime Safety Agency (EMSA) and U.S. Coast Guard conduct PSC inspections
- Increasing focus on cybersecurity in recent years
- Non-compliance can lead to detention (vessel held in port until deficiencies corrected)

### Insurance & Charterers

**Cyber Insurance**:
- CyberSea has cyber insurance policy covering ransomware, data breach, business interruption
- **Premium**: $100,000/year
- **Requirement**: Annual cybersecurity audit; potential premium reduction for strong controls

**Charterers (Cargo Customers)**:
- Major container lines (Maersk, MSC, CMA CGM) increasingly require cybersecurity due diligence
- **Questionnaires**: Vessel cybersecurity posture questionnaires as part of charter contracts

---

## Business & Operational Constraints

### Budget

Your security architecture must be implemented within:

**Capital Budget**: **$500,000 USD**
- Hardware (firewalls, IDS appliances, servers, network equipment)
- Software (SIEM licenses, IDS/IPS signatures, EDR, training platforms)
- Professional services (consultants, penetration testing, training)
- Vendor support (ECDIS upgrades, OT system hardening)

**Annual Operating Budget** (post-implementation): **$50,000 USD/year**
- Software license renewals
- Signature and threat intelligence updates
- Annual penetration testing
- Training refreshers
- Vendor support contracts

**Justification**: Budget must demonstrate ROI (risk reduction, compliance, operational efficiency)

### Implementation Timeline

**Deadline**: 12 months from project approval
- Phased implementation to minimize operational disruption
- Coordinate with voyage schedule (prefer implementation during port stays or drydock)
- Vendor coordination required (ECDIS, ECS, network equipment)

### Operational Constraints

**Criticality**: Safety-critical systems cannot be disrupted
- ECDIS, GPS, radar, AIS must remain operational at all times at sea
- Engine control systems must not be taken offline while underway
- Implementation during port stays preferred

**Crew Capabilities**:
- Limited IT expertise onboard (no dedicated IT staff)
- Chief Engineer has basic IT knowledge; takes on informal IT role
- Security solutions must be manageable by crew with training
- Shore-based support available but limited (time zones, communication delays)

**Bandwidth Limitations**:
- VSAT bandwidth is limited (2 Mbps down / 512 Kbps up)
- Security solutions should minimize bandwidth consumption
- Updates, patches, signatures should be efficient or staged

**Vendor Dependencies**:
- ECDIS and ECS systems are proprietary; vendor support required for changes
- Vendor technician visits expensive and time-consuming
- Solutions should work within vendor constraints

**Drydock Schedule**:
- M/V CyberSea scheduled for drydock in 18 months (major maintenance, inspections)
- Opportunity for major system upgrades, but beyond current project timeline
- Minor upgrades can be done during port stays

---

## Threat Landscape

### Relevant Threats to M/V CyberSea

Based on maritime industry threat intelligence, M/V CyberSea faces:

**Ransomware**:
- **Incident Examples**: NotPetya (Maersk 2017, $300M loss), Ryuk (various shipping companies)
- **Attack Vector**: Phishing email, infected USB, shore-side network connection
- **Impact**: Operational shutdown, cargo delays, ransom demands

**GPS Spoofing**:
- **Incident Examples**: Black Sea GPS spoofing (2017-present), maritime incidents in Middle East
- **Attack Vector**: RF interference/spoofing of GPS signals
- **Impact**: False position data, potential grounding or collision

**AIS Spoofing/Manipulation**:
- **Incident Examples**: Ghost ships (AIS transmitting false positions), AIS jamming
- **Attack Vector**: AIS transmitter spoofing, software manipulation
- **Impact**: Collision risk, piracy facilitation, regulatory violations

**ECDIS Malware**:
- **Incident Examples**: Malware on ECDIS via USB updates or infected files
- **Attack Vector**: Infected USB drives, compromised chart updates
- **Impact**: Corrupted charts, false navigation data, system instability

**Insider Threats**:
- **Incident Examples**: Sabotage by disgruntled crew, data theft for competitors
- **Attack Vector**: Authorized access misuse, physical access to systems
- **Impact**: System damage, data exfiltration, operational disruption

**Phishing & Social Engineering**:
- **Incident Examples**: Business Email Compromise (BEC) targeting maritime executives
- **Attack Vector**: Phishing emails to Master, officers, shore staff
- **Impact**: Credential theft, financial fraud, malware delivery

**Cargo Data Theft**:
- **Incident Examples**: Theft of cargo manifests for organized crime (cargo theft planning)
- **Attack Vector**: Compromise of cargo systems or shore-side interfaces
- **Impact**: Cargo theft, competitive intelligence loss

---

## Stakeholder Expectations

### CyberSea Shipping Lines Management

**Chief Executive Officer (CEO)**:
- Expects cybersecurity to reduce business risk and protect company reputation
- Concerned about ransomware and operational disruption
- Wants compliance with IMO and insurance requirements
- **Key Question**: "What's the ROI on this investment?"

**Chief Operating Officer (COO)**:
- Prioritizes operational continuity and safety
- Concerned about disruption during implementation
- Wants crew-friendly solutions that don't add excessive workload
- **Key Question**: "Will this slow down our operations?"

**Chief Financial Officer (CFO)**:
- Budget-conscious; wants cost-effective solutions
- Interested in insurance premium reductions
- Concerned about annual operating costs post-implementation
- **Key Question**: "Can we get the same security for less money?"

**Fleet Manager**:
- Oversees day-to-day vessel operations
- Concerned about crew training and support burden
- Wants shore-based monitoring and support capabilities
- **Key Question**: "Who will support this system when something goes wrong?"

### Vessel Leadership

**Master (Captain)**:
- Ultimate responsibility for vessel safety and security
- Concerned about navigation safety and cyber threats to ECDIS/GPS
- Wants clear incident response procedures
- **Key Question**: "If we're hacked at sea, what do I do?"

**Chief Engineer**:
- Responsible for machinery and systems
- Concerned about engine control system security
- De facto IT manager onboard; wants manageable solutions
- **Key Question**: "Can I maintain this system with my limited IT background?"

**Chief Officer**:
- Cargo operations and crew welfare
- Concerned about cargo data security and crew device policies
- **Key Question**: "How will this affect crew internet access and morale?"

### External Stakeholders

**Flag State (Panama Maritime Authority)**:
- Expects compliance with IMO guidelines
- Conducts annual inspections
- **Key Question**: "Can you demonstrate cyber risk management in your SMS?"

**Classification Society (Lloyd's Register)**:
- Evaluates vessel compliance with rules and standards
- May offer cyber resilience notation
- **Key Question**: "Do you meet our cyber rules for certification?"

**Cyber Insurance Provider**:
- Wants to reduce risk exposure
- Offers premium discounts for strong controls
- **Key Question**: "What security controls do you have to prevent ransomware?"

**Charterers (Cargo Customers)**:
- Want assurance that cargo data is secure and operations reliable
- **Key Question**: "How do you protect our cargo information from cyber threats?"

---

## Success Criteria

Your cybersecurity architecture for M/V CyberSea will be considered successful if it:

1. **Reduces Risk**: Demonstrably lowers likelihood and impact of cyber incidents
2. **Ensures Safety**: Does not compromise safety of navigation, life, or environment
3. **Maintains Operations**: Minimizes disruption to vessel operations during implementation and steady state
4. **Achieves Compliance**: Meets IMO, flag state, classification society requirements
5. **Within Budget**: Stays within $500K capital budget and $50K annual operating budget
6. **Crew-Friendly**: Can be operated and maintained by crew with training
7. **Demonstrates ROI**: Provides quantifiable benefits (risk reduction, insurance savings, compliance)
8. **Scalable**: Can be replicated across CyberSea's fleet (20 vessels)

---

## Additional Context

### Industry Trends

- **Increasing Connectivity**: More vessels adopting VSAT, IoT sensors, remote monitoring
- **Regulatory Pressure**: IMO 2021 deadline has passed; flag states increasingly enforcing
- **Insurance Market**: Cyber insurance premiums rising; insurers demanding better controls
- **Threat Evolution**: Ransomware targeting maritime sector increasing; nation-state interest in maritime infrastructure

### Company Culture

- **Safety-First**: CyberSea prioritizes safety; security must support, not hinder, safety
- **Cost-Conscious**: Competitive industry with thin margins; justification required for investments
- **Traditional**: Maritime industry historically slow to adopt new technology; change management important
- **Crew-Centric**: Company values crew welfare and morale; security policies should not unduly burden crew

---

## Questions from Teams

**Q: Can we assume vendor cooperation for ECDIS and ECS upgrades?**
A: Yes, but vendors require payment for upgrades and technician visits. Budget accordingly. Vendor response times can be 2-4 weeks.

**Q: Is the vessel currently in drydock or at sea?**
A: Assume the vessel is in normal operations (at sea and in port). Drydock is scheduled for 18 months from now, beyond your implementation timeline. Plan for port-based and at-sea implementation.

**Q: Can we increase the budget if we provide strong justification?**
A: The $500K budget is firm (CEO mandate). Justify ROI within this constraint. If you identify critical needs beyond budget, note them as "future enhancements."

**Q: Are there any specific threat actors targeting CyberSea Shipping Lines?**
A: No specific APT targeting (that you're aware of), but the company operates in geopolitically sensitive regions (South China Sea, Suez Canal, Straits of Hormuz). Generic threats (ransomware, opportunistic attackers) are most likely.

**Q: Can we assume shore-based SOC (Security Operations Center) support?**
A: The company does not currently have a SOC. Your design can include shore-based monitoring, but factor in costs for personnel or third-party SOC services if you propose it.

**Q: What is the crew's cybersecurity awareness level?**
A: Low to moderate. Crew understands basic concepts (passwords, malware) but lack deep knowledge. Assume training is necessary as part of your solution.

---

## Document Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-06 | Initial scenario document for capstone project | Course Instructor |

---

## Contact for Scenario Questions

If you have questions about the M/V CyberSea scenario:

- **Instructor Office Hours**: Tuesday/Thursday, 2-4 PM
- **Email**: instructor@university.edu
- **Slack**: #capstone-scenario channel

---

**Welcome aboard the M/V CyberSea. The security of this vessel is now in your hands!**

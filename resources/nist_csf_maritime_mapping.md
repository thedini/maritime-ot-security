---
title: NIST Cybersecurity Framework - Maritime OT Application Guide
framework_version: NIST CSF 1.1
type: reference
audience: Maritime security professionals, vessel operators, OT engineers
last_updated: 2026-01-06
---

# NIST Cybersecurity Framework - Maritime OT Application Guide

## Introduction

The NIST Cybersecurity Framework (CSF) provides a risk-based approach to managing cybersecurity that is technology-agnostic and scalable. This guide maps NIST CSF functions, categories, and subcategories to maritime Operational Technology (OT) environments aboard vessels.

## Framework Overview

### The Five Core Functions

1. **IDENTIFY (ID):** Understand cyber risks to systems, assets, data, and capabilities
2. **PROTECT (PR):** Implement safeguards to ensure delivery of critical services
3. **DETECT (DE):** Develop and implement capabilities to identify cybersecurity events
4. **RESPOND (RS):** Take action regarding a detected cybersecurity incident
5. **RECOVER (RC):** Restore capabilities impaired by a cybersecurity incident

### Why NIST CSF for Maritime?

- **Alignment:** IMO MSC-FAL.1/Circ.3 explicitly references NIST CSF structure
- **Risk-Based:** Focus resources on highest-risk systems (critical for budget-constrained maritime operations)
- **Flexible:** Adaptable to different vessel types, ages, and operational profiles
- **Comprehensive:** Covers technical, procedural, and organizational controls
- **Maturity Model:** Enables progressive improvement from Partial (Tier 1) to Adaptive (Tier 4)

## Function 1: IDENTIFY (ID)

**Goal:** Develop organizational understanding of managing cybersecurity risk to systems, people, assets, data, and capabilities.

### ID.AM: Asset Management

**Purpose:** Identify and manage physical devices, systems, software, data, and services that require protection.

#### ID.AM-1: Physical devices and systems within the organization are inventoried

**Maritime Application:**

Create comprehensive inventory of shipboard OT and IT systems:

**Navigation and Bridge Systems:**
- Electronic Chart Display and Information System (ECDIS)
- GPS/GNSS receivers
- Automatic Identification System (AIS) transponders
- Radar systems (X-band, S-band)
- Autopilot systems
- Gyrocompass and magnetic compass
- VHF radio and Digital Selective Calling (DSC)
- GMDSS equipment (INMARSAT, Iridium terminals)
- Voyage Data Recorder (VDR)
- Speed logs and echo sounders

**Propulsion and Machinery Systems:**
- Engine control systems
- Fuel management systems
- Ballast control systems
- Power management systems (PMS)
- Alarm monitoring systems
- Remote diagnostic systems

**Cargo Systems:**
- Cargo tank monitoring (tankers)
- Container tracking and monitoring (container ships)
- Refrigerated container monitoring (reefers)
- Loading computer systems
- Inert gas systems

**Safety and Security Systems:**
- Fire detection and suppression
- Bilge alarm systems
- Emergency shutdown systems
- CCTV surveillance
- Access control systems
- Ship Security Alert System (SSAS)

**Communications and IT Systems:**
- Email servers
- Crew internet access points
- Administrative computers
- VSAT or Fleet Broadband terminals
- Phone systems (internal and external)

**Documentation:**
- Maintain spreadsheet or database with: System name, manufacturer, model, software version, criticality rating, network connectivity, physical location
- Update inventory when systems added, modified, or decommissioned
- Tag physical equipment with asset IDs

#### ID.AM-2: Software platforms and applications within the organization are inventoried

**Maritime Application:**

Document all software running on shipboard systems:

**Operating Systems:**
- Windows versions (XP, 7, 10, 11) on various systems
- Linux distributions (often on radar, communications)
- Proprietary real-time operating systems (RTOS) on control systems

**Applications:**
- ECDIS software (Transas, Furuno, Sperry Marine, etc.)
- Weather routing software
- Planned maintenance systems (PMS)
- Voyage planning software
- Chart updates and correction software
- Remote monitoring agents (shore-based condition monitoring)

**Firmware:**
- Firmware versions on navigation equipment
- Firmware on engine control units
- Firmware on network switches and routers

**Third-Party and Support Software:**
- Antivirus/antimalware
- Backup software
- Remote access software (TeamViewer, VNC, etc.)
- OEM diagnostic tools

**Documentation:**
- Track software versions, patch levels, licensing
- Identify end-of-life software requiring migration
- Maintain software asset register alongside hardware inventory

#### ID.AM-3: Organizational communication and data flows are mapped

**Maritime Application:**

Map network architecture and data flows:

**Network Segments:**
```
Zone 1: Critical Navigation & Control
  - ECDIS (primary and backup)
  - Autopilot
  - GPS/GNSS
  - Gyro compass
  - Engine telegraph
  - Steering gear control
  [Isolated or strict firewall from other zones]

Zone 2: Machinery and Cargo Systems
  - Engine control room computers
  - Fuel and ballast systems
  - Cargo management systems
  - Remote monitoring systems
  [Controlled connection to shore-based monitoring]

Zone 3: Safety and Security Systems
  - Fire detection
  - CCTV
  - Access control
  [Separate network, limited interconnection]

Zone 4: Administrative and Operations
  - Voyage planning (office network)
  - Planned maintenance system
  - Crew administration
  - Email server
  [Internet access via VSAT]

Zone 5: Crew and Guest Access
  - Crew WiFi
  - Guest internet (cruise ships, ferries)
  - Entertainment systems
  [Isolated from operational systems]
```

**Data Flows:**
- Document where data moves between zones
- Identify external connections (VSAT, shore-based monitoring, port WiFi)
- Map removable media usage (USB drives for chart updates, software patches)

**Tools:**
- Network diagrams (Visio, draw.io, or hand-drawn)
- Data flow diagrams
- Connection matrix showing which systems communicate

#### ID.AM-4: External information systems are catalogued

**Maritime Application:**

Identify systems outside direct control that interact with ship systems:

**Shore-Based Systems:**
- Fleet management systems
- Condition-based monitoring (CBM) services
- Remote technical support (OEM portals)
- Weather routing services
- Chart provider services (UKHO, NOAA, PRIMAR)

**Port Systems:**
- Port community systems (PCS)
- Just-in-time arrival systems
- Automated Mooring systems
- Shore power connections with data interfaces

**Third-Party Services:**
- VSAT/satellite communications providers
- Class society remote surveys
- Insurance telematics (some insurers)
- Cargo tracking services

**Supply Chain:**
- Software/firmware update sources
- Spare parts ordering systems
- Victualling and supply systems

**Documentation:**
- List external systems, their functions, data exchanged
- Document access methods (VPN, web portal, API)
- Identify contractual security requirements
- Assess third-party cyber risks

#### ID.AM-5: Resources (hardware, devices, data, time, personnel) are prioritized based on classification, criticality, and business value

**Maritime Application:**

Classify systems by criticality to safety, security, environmental protection, and operations:

**Classification Scheme:**

**Critical (Priority 1):**
- Systems essential for safe navigation and collision avoidance
- Systems essential for propulsion and steering
- Emergency systems (fire, flooding, abandon ship)
- Examples: ECDIS, radar, autopilot, main engine control, steering gear, emergency generator

**High (Priority 2):**
- Systems important for efficient operations or required by regulation
- Secondary navigation systems
- Cargo management systems
- Communications systems (VHF, GMDSS)
- Examples: AIS, backup ECDIS, cargo tank monitoring, VSAT communications

**Medium (Priority 3):**
- Systems that support operations but have manual workarounds
- Administrative systems
- Examples: Planned maintenance system, email, voyage planning software

**Low (Priority 4):**
- Systems that provide convenience or efficiency but are not operationally essential
- Examples: Crew internet, entertainment systems, weather fax

**Resource Allocation:**
- Focus cybersecurity investments on Critical and High priority systems
- Implement strongest controls (network isolation, monitoring) on Priority 1 systems
- Accept higher risk for Priority 4 systems

#### ID.AM-6: Cybersecurity roles and responsibilities for the entire workforce and third-party stakeholders are established

**Maritime Application:**

Define clear roles and responsibilities:

**Master:**
- Ultimate responsibility for vessel cybersecurity
- Approve cybersecurity procedures
- Lead cyber incident response
- Ensure crew trained and aware
- Report cyber incidents to company and authorities

**Chief Officer / Safety Officer:**
- Often designated as shipboard Cyber Security Officer (CSO)
- Conduct periodic cyber risk assessments
- Coordinate cybersecurity training and drills
- Maintain cybersecurity documentation
- Interface with shore-based support

**Chief Engineer:**
- Responsible for machinery and control system cybersecurity
- Oversee patch management and system updates
- Manage remote access for OEM support
- Monitor engine and cargo system security

**Radio Officer / IT Officer (if carried):**
- Manage communications systems security
- Oversee network infrastructure
- Manage user accounts and access control
- Monitor network for anomalies

**All Crew:**
- Follow cybersecurity procedures
- Report suspicious activities or anomalies
- Practice good cyber hygiene (passwords, USB drives, email)
- Participate in training and drills

**Shore-Based:**
- **Designated Person Ashore (DPA):** Incorporate cyber incidents in SMS oversight
- **Company Cyber Security Manager:** Develop policies, conduct fleet-wide risk assessments, coordinate incident response
- **IT Support:** Provide technical support, manage shore-based systems, coordinate patch management

**Third Parties:**
- **OEM Support Engineers:** Follow access control procedures, use secure remote access, document all changes
- **Port Agents and Contractors:** Escorted access to systems, use approved devices only
- **Class Surveyors:** Follow confidentiality agreements, secure handling of ship data

**Documentation:**
- Organization chart with cybersecurity responsibilities
- Job descriptions including cyber duties
- Authority matrix (who can approve changes, authorize access)

### ID.BE: Business Environment

**Purpose:** Understand the organization's mission, objectives, stakeholders, and activities.

#### ID.BE-1-5: Maritime Application

**Mission and Objectives:**
- Primary mission: Safe, secure, environmentally compliant transport of cargo/passengers
- Cybersecurity supports mission by ensuring availability and integrity of critical systems

**Critical Services:**
- Navigation and collision avoidance
- Propulsion and steering
- Cargo operations
- Communications (safety and operational)
- Safety systems (fire, flooding, abandon ship)

**Dependencies:**
- GPS/GNSS for positioning (dependency on external infrastructure)
- Electronic charts (dependency on chart providers)
- Shore-based support for some systems (remote monitoring, technical support)
- Communications satellite services

**Resilience Requirements:**
- Must maintain safe navigation even if electronic systems fail (backup paper charts, manual navigation)
- Redundancy for critical systems (e.g., primary and backup ECDIS, multiple GPS receivers)
- Manual overrides for automated systems

### ID.GV: Governance

**Purpose:** Policies, procedures, and processes to manage and monitor regulatory, legal, risk, environmental, and operational requirements.

#### ID.GV-1: Organizational cybersecurity policy is established and communicated

**Maritime Application:**

Develop company and vessel cybersecurity policy:

**Policy Elements:**
- Commitment to cyber risk management
- Scope (fleet-wide, vessel-specific)
- Roles and responsibilities
- Risk management approach
- Integration with SMS
- Compliance with IMO, flag state, class requirements
- Incident reporting and response
- Training and awareness
- Review and update frequency

**Communication:**
- Include policy in SMS manual
- Brief crew during familiarization
- Post key points in crew areas
- Reference in company security instructions

#### ID.GV-2-4: Legal, regulatory, and contractual requirements regarding cybersecurity are understood and managed

**Maritime Application:**

**Regulatory Compliance:**
- IMO Resolution MSC.428(98) - cyber risk in SMS
- Flag state specific requirements
- Port state control expectations
- Class society cyber notations (if applicable)
- USCG requirements for U.S. operations
- EU NIS2 Directive (if applicable)

**Contractual Requirements:**
- Charter party cyber security clauses (BIMCO Cyber Clause)
- Insurance requirements (P&I, H&M)
- Terminal and port facility security requirements
- Cargo owner security requirements (especially for valuable or hazardous cargos)

**Legal Considerations:**
- Data protection (GDPR for crew data if EU-flagged or calling EU ports)
- Incident reporting obligations
- Liability for cyber incidents

**Management:**
- Maintain register of applicable requirements
- Review requirements during contract negotiations
- Ensure SMS and procedures address requirements
- Verify compliance during internal audits

### ID.RA: Risk Assessment

**Purpose:** Understand cybersecurity risk to organizational operations, assets, and individuals.

#### ID.RA-1: Asset vulnerabilities are identified and documented

**Maritime Application:**

Identify vulnerabilities in shipboard systems:

**Common Technical Vulnerabilities:**
- **Outdated Software:** Windows XP/7 on ECDIS, chart systems (no security updates)
- **Default Passwords:** Many systems ship with default passwords unchanged
- **Lack of Segmentation:** Navigation systems on same network as crew internet
- **Unencrypted Protocols:** Telnet, FTP, HTTP used for system management
- **No Authentication:** Some systems lack user authentication
- **Open Ports:** Unnecessary network services and ports enabled
- **Physical Access:** Equipment accessible to unauthorized personnel
- **Removable Media:** USB ports for chart updates also accept any USB drive

**Common Procedural Vulnerabilities:**
- No formal patch management process
- Inconsistent access control (shared passwords, no account management)
- Lack of system monitoring or logging
- No backup/recovery procedures
- Inadequate incident response capability

**Human Vulnerabilities:**
- Crew susceptible to phishing (email-based malware)
- Use of personal USB drives
- Connecting personal devices to ship networks
- Poor password practices
- Lack of cybersecurity awareness

**Documentation:**
- Vulnerability register with severity ratings
- Plan for remediation (technical controls, compensating controls, or accepted risk)

#### ID.RA-2: Cyber threat intelligence is received from information sharing forums and sources

**Maritime Application:**

Stay informed of maritime cyber threats:

**Information Sources:**
- **IMO Circulars:** Official guidance and threat warnings
- **Flag State Advisories:** Security bulletins from flag administration
- **Class Societies:** Cyber threat intelligence from DNV, Lloyd's, ABS
- **Industry Associations:** ICS, BIMCO, INTERTANKO threat briefings
- **Maritime CERTs:** Maritime Cybersecurity Operations Center (MARSOC), etc.
- **Coast Guards:** USCG Maritime Security Alerts (MSIB)
- **ENISA:** European Union Agency for Cybersecurity (maritime sector reports)
- **Cybersecurity Vendors:** Threat intelligence from security companies serving maritime
- **NIST NVD:** National Vulnerability Database for known vulnerabilities in software

**Recent Maritime Threats (examples):**
- GPS spoofing and jamming (reported in Persian Gulf, Black Sea, others)
- Ransomware targeting shipping companies (NotPetya impact on Maersk 2017)
- AIS spoofing (ghost ships, false positions)
- ECDIS malware (proof-of-concept research)
- Supply chain attacks (compromised software updates)

**Action:**
- Subscribe to threat feeds
- Assign personnel to monitor and disseminate
- Assess applicability to own vessels
- Update risk assessments based on emerging threats
- Implement recommended mitigations

#### ID.RA-3: Threats, both internal and external, are identified and documented

**Maritime Application:**

**External Threats:**
- **Cyber Criminals:** Ransomware, data theft (crew data, commercial info), fraud
- **Nation-State Actors:** Espionage, sabotage (especially military or strategic cargos)
- **Hacktivists:** Protest-motivated attacks (oil/gas tankers, whaling ships)
- **Terrorists:** Potential for cyber-physical attacks on vessels
- **Competitors:** Industrial espionage, commercial advantage

**Internal Threats:**
- **Disgruntled Crew:** Insider sabotage, data theft
- **Negligent Users:** Unintentional introduction of malware, poor cyber hygiene
- **Contractors/Visitors:** Port workers, ship chandlers, OEM engineers with system access

**Threat Scenarios:**
- Ransomware via email attachment locks ECDIS or engine control systems
- GPS spoofing causes navigation error
- AIS manipulation for piracy facilitation
- Unauthorized access to cargo system causing spill or explosion
- Data breach of crew personal information
- Denial of service against communications systems
- Malware introduced via USB drive during chart update

#### ID.RA-4-6: Potential impacts and likelihoods of events are determined; risk is determined and prioritized

**Maritime Application:**

Conduct risk analysis using likelihood and impact:

**Example Risk Scenarios:**

**Scenario 1: Ransomware Infection of ECDIS**
- **Threat:** Ransomware via email attachment or USB
- **Vulnerability:** Outdated Windows OS, crew email access, USB ports
- **Likelihood:** Medium (ransomware prevalent, maritime targeted)
- **Impact:** High (loss of primary navigation system, regulatory requirement for backup)
- **Risk Level:** HIGH
- **Treatment:** Network segmentation (isolate ECDIS from email network), disable USB ports or strict USB policy, crew training, maintain paper chart backup

**Scenario 2: GPS Spoofing**
- **Threat:** External GPS spoofing (nation-state or other actor)
- **Vulnerability:** GPS receivers accept any signal without authentication
- **Likelihood:** Low-Medium (area-dependent: high in conflict zones, low elsewhere)
- **Impact:** High (navigation error, potential grounding or collision)
- **Risk Level:** MEDIUM-HIGH
- **Treatment:** Train crew to recognize GPS anomalies, use multiple positioning methods (radar, visual, dead reckoning), monitor RAIM warnings

**Scenario 3: Unauthorized Remote Access**
- **Threat:** Hacker gaining remote access via shore-based monitoring connection
- **Vulnerability:** Weak authentication on remote access system, always-on connection
- **Likelihood:** Low (requires specific knowledge of vessel systems)
- **Impact:** Critical (potential control of critical systems)
- **Risk Level:** HIGH
- **Treatment:** Strong authentication (VPN, multi-factor where possible), restrict remote access to specific systems, monitor and log all remote sessions, disable remote access when not needed

**Scenario 4: Crew Internet Malware**
- **Threat:** Malware downloaded on crew internet system
- **Vulnerability:** Crew internet on same network as operational systems
- **Likelihood:** High (crew will use internet, malware common)
- **Impact:** Low-Medium (if segmented, impact limited to crew systems; if not, could spread)
- **Risk Level:** MEDIUM
- **Treatment:** Network segmentation, antivirus on crew systems, user training, acceptable use policy

**Prioritization:**
- Address HIGH and CRITICAL risks immediately
- Plan mitigation for MEDIUM risks
- Accept or monitor LOW risks

### ID.RM: Risk Management Strategy

**Purpose:** Organization's priorities, constraints, risk tolerances, and assumptions are established and used to support operational risk decisions.

#### ID.RM-1-3: Maritime Application

**Risk Tolerance:**
- **Safety-Critical Systems:** Very low risk tolerance (must maintain safe navigation)
- **Operational Systems:** Low-medium tolerance (downtime acceptable if safety not compromised)
- **Administrative Systems:** Medium tolerance (inconvenience acceptable)

**Risk Management Strategy:**
- Prioritize safety-critical systems for protection
- Use network segmentation as primary control
- Balance security with operational needs
- Accept some risks on low-criticality systems if mitigation cost-prohibitive
- Plan for degraded operations (manual backup methods)

**Constraints:**
- Limited budget for cybersecurity investments
- Legacy systems with limited security features
- Small crew size (limited IT expertise)
- Operational environment (difficult to apply patches at sea, limited bandwidth)

## Function 2: PROTECT (PR)

**Goal:** Develop and implement appropriate safeguards to ensure delivery of critical services.

### PR.AC: Access Control

**Purpose:** Limit access to authorized users, processes, and devices.

#### PR.AC-1: Identities and credentials are issued, managed, verified, revoked, and audited

**Maritime Application:**

**User Account Management:**
- Create individual user accounts for each crew member (no shared accounts)
- Use role-based access (Master, Chief Officer, OOW, Chief Engineer, Engineer, Ratings)
- Assign minimum necessary privileges
- Disable or delete accounts when crew sign off
- Regularly review account lists for unauthorized or obsolete accounts

**Password Management:**
- Change ALL default passwords on delivery or installation
- Implement password policy:
  - Minimum 8 characters (12+ preferred)
  - Mix of uppercase, lowercase, numbers, symbols
  - No dictionary words or personal information
  - Different password for each system
- Change passwords after crew changes (especially for privileged accounts)
- Avoid posting passwords on equipment (common bad practice)

**Multi-Factor Authentication (MFA):**
- Implement where possible (shore-based systems, remote access)
- Recognize limitations (many OT systems don't support MFA)

**Physical Access:**
- Restrict physical access to critical systems (locked bridge, engine control room, server room)
- Escort port visitors and contractors
- Log access to sensitive areas

#### PR.AC-2: Physical access to assets is managed and protected

**Maritime Application:**

- Keep bridge door locked when unattended
- Restrict access to engine control room and machinery spaces
- Secure IT/communications equipment rooms
- Escort visitors at all times
- ISPS Code access control integrated with cyber physical security
- Consider tamper-evident seals on critical equipment
- CCTV monitoring of critical system locations

#### PR.AC-3: Remote access is managed

**Maritime Application:**

**Shore-Based Monitoring:**
- Use VPN or encrypted connection for condition-based monitoring
- Authenticate remote sessions
- Log all remote access
- Restrict remote access to specific systems (not full network)
- Disable remote access when not actively needed
- Require approval from Master or Chief Engineer for remote sessions

**OEM Remote Support:**
- Schedule remote support sessions (no unannounced access)
- Use one-time or time-limited credentials
- Supervise all remote support sessions (engineer present)
- Require contractor to follow ship security procedures
- Disconnect remote access immediately after session
- Review and approve any configuration changes

**Crew Personal Remote Access:**
- Prohibit crew from installing remote access software (TeamViewer, etc.) on operational systems
- Restrict personal remote access to crew internet zone only

#### PR.AC-4: Access permissions and authorizations are managed

**Maritime Application:**

**Principle of Least Privilege:**
- Grant only access needed for job function
- Junior officers: Read-only access to navigation systems (except when on watch)
- Engineers: Access to machinery systems, not navigation systems
- Ratings: No access to critical system configurations

**Privilege Review:**
- Review access permissions during crew changes
- Audit privileged accounts quarterly
- Remove unnecessary administrative accounts

**Emergency Access:**
- Document emergency access procedures (e.g., Master override)
- Log all emergency access use

#### PR.AC-5: Network integrity is protected (e.g., network segregation, network segmentation)

**Maritime Application:**

**Network Segmentation Strategy:**

```
[Critical Navigation] <--Firewall(Deny All, Allow Specific)--> [Engineering Systems]
         |                                                              |
         | Firewall (Deny All, Allow Specific)                         | Firewall (Allow Monitoring)
         |                                                              |
         V                                                              V
[Administrative Network] <--Firewall(Deny All)--> [Crew Internet]      [Shore Monitoring]
```

**Segmentation Controls:**
- Physical separation (separate switches, cables) for highest security
- VLANs for logical separation
- Firewalls between segments with default-deny rules
- Allow only necessary traffic between segments (e.g., alarm data from engine systems to bridge display)

**Critical System Isolation:**
- ECDIS, GPS, autopilot, radar on dedicated network
- No internet connection to critical navigation systems
- USB ports disabled or limited to authorized devices only

**Crew Internet Isolation:**
- Crew WiFi completely separate from operational networks
- Guest WiFi (cruise ships) further isolated from crew

### PR.AT: Awareness and Training

**Purpose:** Personnel and partners are provided awareness education and training.

#### PR.AT-1-5: Maritime Application

**Cyber Awareness Training:**
- Initial training during familiarization (shipboard orientation)
- Annual refresher training
- Updates when new threats emerge

**Training Topics:**
- Why cybersecurity matters for maritime safety
- Common threats (phishing, malware, USB drives)
- Recognizing suspicious activity
- Proper system use (passwords, access control)
- Email and internet safe use
- Incident reporting
- Role-specific responsibilities

**Training Methods:**
- Crew briefings
- Computer-based training (CBT) modules
- Tabletop exercises
- Simulated cyber incidents
- Posters and reminders in crew areas

**Third-Party Training:**
- Brief contractors and port workers on security procedures before granting access
- Require OEM engineers to acknowledge security requirements

**Privileged User Training:**
- Additional training for system administrators (Master, Chief Officer, Chief Engineer, IT officer)
- Safe remote access practices
- Patch management procedures
- Incident response procedures

### PR.DS: Data Security

**Purpose:** Information and records are managed consistent with the organization's risk strategy.

#### PR.DS-1-8: Maritime Application

**Data at Rest Protection:**
- Encrypt sensitive data where possible (crew personal data, commercial information)
- Physical security of computers and storage media
- Secure disposal of old equipment (wipe disks before disposal)

**Data in Transit Protection:**
- Use encrypted connections for shore communications (VPN, HTTPS)
- Be cautious of unencrypted emails containing sensitive information
- Avoid transmitting sensitive data over port WiFi

**Data Integrity:**
- Protect critical data from unauthorized modification:
  - Navigation routes and plans
  - Chart data
  - System configurations
  - Safety and security procedures
- Use checksums or digital signatures for software updates and chart updates
- Maintain backup copies of critical data

**Data Backup:**
- Regular backups of critical data (routes, configurations, logs)
- Store backups separately from primary systems
- Test restoration procedures
- Include system images for rapid recovery

**Data Retention:**
- Maintain records per regulatory requirements:
  - VDR data (last 12 hours continuous)
  - Logbooks (varies by regulation)
  - Incident records (per SMS)
- Securely delete data when no longer needed

**Removable Media:**
- Scan all USB drives for malware before use
- Use dedicated USB drives for specific purposes (e.g., chart updates only)
- Prohibit personal USB drives on operational systems
- Consider write-only USB ports or USB port locks

### PR.IP: Information Protection Processes and Procedures

**Purpose:** Security policies, processes, and procedures are maintained and managed.

#### PR.IP-1-12: Maritime Application

**SMS Integration:**
- Document cyber risk management in SMS manual
- Integrate cyber procedures into existing SMS structure (don't create separate documentation)

**Configuration Management:**
- Document baseline configurations for all systems
- Manage changes through change control process
- Test changes before implementation
- Document all configuration changes

**System Development and Acquisition:**
- Include cybersecurity requirements in specifications for new systems
- Request information on known vulnerabilities from manufacturers
- Verify security features before acceptance (changeable passwords, network controls, logging)
- Include cybersecurity in commissioning tests

**Patch Management:**
- Develop patch management procedure
- Monitor for security updates from OEMs
- Test patches in non-operational environment if possible
- Schedule patching during port stays or calm weather
- Document patch status for all systems
- Implement compensating controls for systems that cannot be patched (legacy systems)

**Secure System Disposal:**
- Wipe or destroy data storage media before disposal
- Decommission accounts and credentials associated with retired systems
- Update network diagrams and asset inventory

**Incident Response Planning:**
- Develop and document cyber incident response plan
- Define roles and responsibilities
- Establish communication procedures (who to notify, when, how)
- Create response checklists
- Identify external support resources (OEMs, cybersecurity consultants, IT support)

**Vulnerability Management:**
- Conduct periodic vulnerability assessments
- Track known vulnerabilities
- Prioritize remediation based on risk
- Implement workarounds or compensating controls for vulnerabilities that cannot be fixed

### PR.MA: Maintenance

**Purpose:** Maintenance and repairs of assets are performed and logged.

#### PR.MA-1-2: Maritime Application

**Maintenance Tools:**
- Control use of diagnostic and maintenance tools (laptops, software utilities)
- Require authorization for system maintenance
- Use only trusted maintenance tools and software
- Scan maintenance tools for malware before use

**Remote Maintenance:**
- Follow remote access procedures (see PR.AC-3)
- Approve remote maintenance sessions
- Supervise remote maintenance
- Verify integrity after maintenance

**Logging:**
- Log all maintenance activities (planned maintenance system)
- Document configuration changes
- Record software/firmware updates
- Maintain audit trail

### PR.PT: Protective Technology

**Purpose:** Technical security solutions are managed to ensure resilience of systems.

#### PR.PT-1-5: Maritime Application

**Audit Logging:**
- Enable logging on systems that support it
- Collect logs centrally if possible
- Review logs periodically for anomalies
- Retain logs per regulatory requirements (VDR, SMS)
- Protect log integrity (prevent tampering)

**Removable Media Protection:**
- Implement technical controls:
  - Disable USB ports where not needed (e.g., via BIOS or physical blocks)
  - Configure systems to not auto-run from USB drives
  - Antivirus scanning of USB drives before use

**Least Functionality:**
- Disable unnecessary services and protocols:
  - Telnet (use SSH instead)
  - FTP (use SFTP instead)
  - Unused network ports
  - Unnecessary software on systems
- Configure firewalls to block all except explicitly allowed traffic

**Communications Security:**
- Use encrypted protocols where possible (HTTPS, SSH, VPN)
- Secure configuration of wireless networks (WPA3 or WPA2, strong passwords)
- Disable WiFi on operational systems if not needed
- Monitor network traffic for anomalies

**Resilience:**
- Implement redundancy for critical systems (dual ECDIS, backup GPS, redundant engines/generators)
- Test failover procedures
- Maintain manual backup methods (paper charts, magnetic compass, sextant)

## Function 3: DETECT (DE)

**Goal:** Develop and implement appropriate activities to identify the occurrence of a cybersecurity event.

### DE.AE: Anomalies and Events

**Purpose:** Anomalous activity is detected and the potential impact is understood.

#### DE.AE-1-5: Maritime Application

**Baseline Normal Operations:**
- Document normal system behavior and performance
- Record baseline network traffic patterns
- Note typical system logs and alarms
- Understand expected values (GPS accuracy, system response times)

**Anomaly Detection:**

**Navigation System Anomalies:**
- GPS position jumps or inconsistent with dead reckoning
- AIS displaying incorrect ship information or position
- ECDIS chart update failures or unexpected behavior
- Radar contacts not correlating with AIS
- Autopilot unexpected course changes
- Compass discrepancies beyond normal deviation

**Machinery System Anomalies:**
- Unexpected alarms or alarm floods
- System performance degradation (slow response)
- Unexplained parameter changes
- Control system unresponsive or erratic

**Network Anomalies:**
- Unusual network traffic volumes or patterns
- Connections to unknown external IP addresses
- Failed login attempts
- Unexpected network devices
- Slow network performance

**System Anomalies:**
- Unexpected system restarts
- New or unfamiliar programs running
- Changed file dates or sizes
- Disabled antivirus or security tools
- Pop-ups or unusual error messages

**Human Anomalies:**
- Unauthorized access attempts
- Personnel accessing systems outside their role
- Unusual activity outside normal working hours

**Alert Thresholds:**
- Define what constitutes an actionable anomaly (vs. normal variance)
- Balance sensitivity (catch threats) vs. false positives (alarm fatigue)

### DE.CM: Security Continuous Monitoring

**Purpose:** Information systems and assets are monitored to identify cybersecurity events.

#### DE.CM-1-8: Maritime Application

**Monitoring Activities:**

**Daily Checks:**
- Review critical system status during bridge and engine room handovers
- Check GPS positioning accuracy (RAIM, cross-check with other methods)
- Verify AIS display matches ship status
- Check network connectivity and performance
- Review recent system logs for errors

**Weekly Checks:**
- Review access logs (login attempts, failures)
- Check for system updates and patches available
- Review antivirus status and quarantine logs
- Check backup completion status

**Monthly Checks:**
- Review full system logs for anomalies
- Check for unauthorized software or configuration changes
- Review user account list for orphaned accounts
- Verify security control effectiveness

**Monitoring Tools:**
- System built-in monitoring and alerting
- Antivirus/antimalware logs
- Firewall logs
- Windows Event Viewer
- Network monitoring tools (if available)

**Physical Monitoring:**
- CCTV of critical system areas
- Access logs for secure areas
- Visual inspections for tampering

**External Threat Monitoring:**
- Subscribe to maritime cyber threat intelligence
- Monitor for GPS/AIS anomalies reported in area
- Check for advisories relevant to ship's systems

**Baseline Comparison:**
- Compare current state to documented baseline
- Investigate deviations from normal operations

### DE.DP: Detection Processes

**Purpose:** Detection processes and procedures are maintained and tested.

#### DE.DP-1-5: Maritime Application

**Detection Procedures:**
- Document how to monitor systems (who, what, when, how)
- Create checklists for routine monitoring tasks
- Define escalation procedures (when to escalate, to whom)
- Integrate detection into watchkeeping routines

**Testing Detection:**
- Conduct tabletop exercises (simulate cyber incident, test detection)
- Test anomaly reporting procedures
- Verify alerts and alarms function correctly
- Practice detection during cyber drills

**Roles and Responsibilities:**
- Officer of the Watch: Monitor navigation system status and performance
- Engineering Watch: Monitor machinery control systems
- Radio Officer/IT Officer: Monitor networks and communications systems
- All Crew: Report any suspicious or anomalous behavior

**Continuous Improvement:**
- Update detection procedures based on lessons learned
- Incorporate new threats into detection monitoring
- Update baselines as systems change

**Communication:**
- Train crew on what to look for and how to report
- Encourage reporting without fear of blame
- Provide feedback on reported anomalies

## Function 4: RESPOND (RS)

**Goal:** Develop and implement appropriate activities to take action regarding a detected cybersecurity incident.

### RS.RP: Response Planning

**Purpose:** Response processes and procedures are executed and maintained.

#### RS.RP-1: Maritime Application

**Cyber Incident Response Plan:**

**1. Preparation:**
- Establish incident response team:
  - Master (Incident Commander)
  - Chief Officer / Cyber Security Officer (Coordinator)
  - Chief Engineer (Technical Lead for machinery systems)
  - Radio Officer / IT Officer (Technical Lead for IT/networks)
- Create contact lists (company DPA, IT support, OEM contacts, flag state, coast guard)
- Prepare response checklists and procedures
- Establish communication protocols

**2. Incident Types and Classification:**
- **Minor:** Isolated malware detection, unsuccessful attack, no impact on operations
- **Moderate:** System performance degradation, limited spread, minimal operational impact
- **Major:** Critical system affected, safety implications, significant operational impact
- **Critical:** Multiple systems compromised, imminent safety threat, loss of key capabilities

**3. Response Procedures by Phase:**

**Detection and Reporting:**
- Any crew member detecting anomaly reports to Officer of the Watch or Duty Engineer
- OOW/Engineer reports to Master
- Master activates incident response as appropriate

**Assessment:**
- Determine scope (which systems affected)
- Assess severity (impact on safety, operations)
- Classify incident
- Decide on response level

**Containment:**
- Isolate affected systems (disconnect from network, power off if necessary)
- Prevent spread (block network traffic, disable USB ports)
- Maintain critical functions (switch to backup systems, manual operations)

**Eradication:**
- Remove malware or threat
- Close unauthorized access
- Patch vulnerabilities exploited

**Recovery:**
- Restore systems from known-good backups
- Verify system integrity before reconnection
- Monitor for reoccurrence

**Post-Incident:**
- Document incident timeline and actions
- Conduct lessons learned review
- Update procedures based on experience
- Report to stakeholders

**4. Decision-Making:**
- Master has ultimate authority for incident response
- Prioritize safety of ship and crew above all
- Coordinate with shore-based support as available
- Document decisions and rationale

### RS.CO: Communications

**Purpose:** Response activities are coordinated with internal and external stakeholders.

#### RS.CO-1-5: Maritime Application

**Internal Communications:**
- **Master to Crew:** Brief crew on situation, response actions, any changes to operations
- **Incident Response Team:** Regular updates and coordination
- **Watch Handovers:** Ensure ongoing situation communicated during watch changes

**External Communications:**

**Company (DPA):**
- Notify immediately for major or critical incidents
- Provide regular updates
- Request support as needed

**Flag State Administration:**
- Report per flag state requirements (some flags require reporting of cyber incidents)
- Comply with investigation requests

**Coast Guard / Port State:**
- Report if required by regulation or if incident affects safety
- Coordinate for emergency response if needed

**Class Society:**
- Notify if incident affects classed systems
- Request technical support

**OEM Technical Support:**
- Contact for system-specific incidents
- Request remote support for recovery (following remote access procedures)

**Insurance (P&I Club, H&M Underwriter):**
- Notify per policy requirements
- Coordinate for cyber insurance coverage (if applicable)

**Port Authority / Terminal:**
- Notify if incident affects arrival or operations
- Coordinate security if incident involves security threat

**Other Vessels / Coast Guard:**
- Broadcast warnings if incident affects navigation systems (e.g., GPS spoofing in area)
- Use appropriate safety communications (GMDSS, VHF)

**Communication Principles:**
- Timely and accurate reporting
- Protect sensitive information (don't disclose vulnerabilities publicly)
- Coordinate messaging (company may handle external media communications)
- Document all communications

### RS.AN: Analysis

**Purpose:** Analysis is conducted to ensure effective response and support recovery activities.

#### RS.AN-1-5: Maritime Application

**Incident Analysis:**
- Collect evidence (logs, screenshots, timeline)
- Determine root cause (how did it happen?)
- Identify attack vector (email, USB, network?)
- Assess impact (what was affected, how severely?)
- Determine if data exfiltrated or systems manipulated

**Forensics:**
- Preserve evidence (don't overwrite logs, take photos)
- Maintain chain of custody for evidence (if legal action potential)
- Engage forensic experts if needed (company IT, third-party consultants)

**Analysis Questions:**
- How did the incident occur?
- Why did controls fail to prevent or detect it?
- What was the full extent of the compromise?
- Are there other affected systems not yet discovered?
- What is the risk of reoccurrence?

**Information Sharing:**
- Share lessons learned with company fleet (anonymized)
- Report to industry ISACs (information sharing centers)
- Contribute to maritime cyber threat intelligence

### RS.MI: Mitigation

**Purpose:** Activities are performed to prevent expansion of an event and mitigate its effects.

#### RS.MI-1-3: Maritime Application

**Immediate Mitigation:**
- Isolate affected systems (network disconnection, power off)
- Block malicious network traffic (firewall rules)
- Disable compromised user accounts
- Stop malicious processes
- Prevent lateral movement to other systems

**Operational Mitigation:**
- Switch to backup systems
- Revert to manual operations
- Use alternative methods (e.g., paper charts if ECDIS compromised)
- Maintain safe navigation (anchor, reduce speed, request tug assistance if needed)

**Technical Mitigation:**
- Remove malware
- Apply emergency patches
- Reset passwords
- Restore from backups
- Rebuild compromised systems

**Safety Mitigation:**
- Ensure situational awareness maintained
- Post additional lookouts if systems degraded
- Navigate conservatively
- Consider safe haven or anchoring if critical systems unavailable

### RS.IM: Improvements

**Purpose:** Organizational response activities are improved by incorporating lessons learned.

#### RS.IM-1-2: Maritime Application

**Post-Incident Review:**
- Conduct lessons learned meeting with incident response team
- Document what worked well and what didn't
- Identify gaps in procedures, training, or technology
- Develop corrective action plan

**Procedure Updates:**
- Revise incident response plan based on experience
- Update detection procedures
- Improve monitoring based on indicators discovered
- Enhance training based on gaps identified

**Control Improvements:**
- Implement new security controls to prevent recurrence
- Fix vulnerabilities exploited
- Improve network segmentation
- Enhance access controls

**Training Enhancements:**
- Update crew training to address incident type
- Conduct drills based on incident scenario
- Share lessons learned with all crew

**Communication of Improvements:**
- Brief crew on changes to procedures
- Update SMS documentation
- Report improvements to company and stakeholders

## Function 5: RECOVER (RC)

**Goal:** Develop and implement appropriate activities to maintain resilience and restore any capabilities impaired by a cybersecurity incident.

### RC.RP: Recovery Planning

**Purpose:** Recovery processes and procedures are executed and maintained.

#### RC.RP-1: Maritime Application

**Recovery Plan Elements:**

**Recovery Priorities:**
1. **Life Safety:** Ensure crew and passengers safe
2. **Safe Navigation:** Restore navigation and positioning systems
3. **Propulsion and Steering:** Restore main engines and steering gear
4. **Communications:** Restore VHF, GMDSS for safety communications
5. **Cargo/Environmental:** Restore cargo and ballast systems
6. **Operational Systems:** Restore other operational systems
7. **Administrative Systems:** Restore office IT systems

**Recovery Procedures:**
- System-specific recovery steps (documented for each critical system)
- Backup restoration procedures
- System rebuild procedures
- Alternative/manual operation procedures

**Recovery Team:**
- Master (Recovery Coordinator)
- Chief Engineer (Machinery Systems)
- Chief Officer (Navigation and Cargo Systems)
- Radio Officer / IT Officer (IT Systems)

**Recovery Resources:**
- Backup media (USB drives, external hard drives)
- Spare equipment (spare laptop, spare navigation computer)
- Contact information for OEM support
- System documentation and manuals
- Recovery software and tools

**Recovery Testing:**
- Test backup restoration regularly (monthly or quarterly)
- Conduct recovery drills (tabletop and live)
- Verify backup integrity
- Time recovery procedures (know how long it takes)

### RC.IM: Improvements

**Purpose:** Recovery planning and processes are improved by incorporating lessons learned.

#### RC.IM-1-2: Maritime Application

**Recovery Lessons Learned:**
- Evaluate effectiveness of recovery procedures
- Identify what delayed or complicated recovery
- Assess adequacy of backup systems
- Evaluate communication effectiveness during recovery

**Recovery Improvements:**
- Update recovery procedures based on experience
- Enhance backup and restoration processes
- Improve documentation
- Add resources or tools identified as needed
- Adjust recovery priorities based on operational experience

**Resilience Enhancements:**
- Implement additional redundancy for critical systems
- Improve system segmentation to limit incident impact
- Enhance monitoring to detect issues earlier (faster recovery)
- Improve training to speed recovery

### RC.CO: Communications

**Purpose:** Restoration activities are coordinated with internal and external parties.

#### RC.CO-1-3: Maritime Application

**Recovery Communications:**

**Internal:**
- Notify crew when systems restored
- Brief on any operational changes or limitations post-recovery
- Recognize crew contributions to successful recovery

**External:**
- Notify company of recovery completion
- Update flag state and coast guard on return to normal operations
- Notify port and terminal of operational status
- Inform customers of cargo operations status
- Update insurance

**Communication Timeline:**
- Initial notice: Incident occurred, response underway
- Progress updates: Regular intervals during response and recovery
- Final notice: Recovery complete, return to normal operations
- Follow-up: Lessons learned, improvements implemented

## Implementation Roadmap

### Phase 1: Identify (Months 1-3)

- Conduct asset inventory
- Create network diagrams
- Perform initial risk assessment
- Identify critical systems and prioritize
- Define roles and responsibilities
- Establish baseline configurations

### Phase 2: Protect (Months 4-9)

- Implement network segmentation
- Establish access controls (change default passwords, manage accounts)
- Develop cybersecurity policies and procedures
- Integrate cyber procedures into SMS
- Begin crew training program
- Implement basic protective technologies (antivirus, firewalls)

### Phase 3: Detect (Months 6-12)

- Establish monitoring procedures
- Train crew on anomaly detection
- Implement logging and review procedures
- Develop indicators of compromise
- Test detection capabilities

### Phase 4: Respond & Recover (Months 9-12)

- Develop incident response plan
- Establish recovery procedures
- Conduct tabletop exercises
- Test backup and restoration
- Validate external support contacts
- Conduct live drill

### Phase 5: Continuous Improvement (Ongoing)

- Conduct annual risk reassessments
- Update procedures based on lessons learned
- Stay informed of emerging threats
- Participate in information sharing
- Conduct regular training and drills
- Monitor control effectiveness

## NIST CSF Tiers for Maritime

The NIST CSF defines Implementation Tiers describing the maturity of cybersecurity risk management:

**Tier 1 - Partial:**
- Risk management is ad hoc
- Limited awareness
- No formal processes
- Reactive response

*Maritime Example:* Vessel has basic antivirus, crew told not to click suspicious emails, but no formal procedures, no monitoring, no risk assessment.

**Tier 2 - Risk Informed:**
- Risk management approved by management
- Some awareness
- Processes defined but not consistently implemented
- Awareness of threats but response is reactive

*Maritime Example:* Company has cyber policy, conducted risk assessment, crew trained, but implementation inconsistent across fleet, monitoring informal, incident response not tested.

**Tier 3 - Repeatable:**
- Risk management formally approved and expressed as policy
- Consistent implementation across organization
- Regular updates to procedures
- Proactive monitoring and response

*Maritime Example:* Company has comprehensive cyber risk management in SMS, consistent implementation fleet-wide, regular training and drills, monitoring and detection capabilities, tested incident response.

**Tier 4 - Adaptive:**
- Risk management integrated into organization culture
- Continuous improvement
- Advanced detection and threat intelligence
- Adaptive risk management based on lessons learned

*Maritime Example:* Company culture prioritizes cybersecurity, shares threat intelligence with industry, continuous monitoring with advanced analytics, adaptive risk management, regular red team exercises, industry leadership.

**Realistic Maritime Target:** Most maritime organizations should target Tier 2 initially, working toward Tier 3. Tier 4 is aspirational for most.

## Key Takeaways

1. **NIST CSF is Flexible:** Can be adapted to maritime environment and scaled to vessel size and operations
2. **Not All-or-Nothing:** Implement progressively, prioritizing highest-risk systems
3. **Integrated Approach:** Combine technical, procedural, and human controls
4. **Safety-Focused:** Maritime application emphasizes maintaining safe navigation and operations
5. **Practical Constraints:** Recognize limitations (budget, legacy systems, crew size) and work within them
6. **Continuous Process:** Cybersecurity is ongoing, not a one-time project
7. **Compliance Alignment:** NIST CSF approach satisfies IMO, flag state, class, and insurance requirements

## Additional Resources

- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- IMO Guidelines Summary: `/home/vessel/vessel_lstm/maritime-ot-security/resources/imo_guidelines_summary.md`
- Compliance Checklist: `/home/vessel/vessel_lstm/maritime-ot-security/resources/compliance_checklist.md`
- Compliance Overview: `/home/vessel/vessel_lstm/maritime-ot-security/class/class_00_introduction/compliance_overview.md`

---

*Document Version: 1.0*
*Last Updated: January 6, 2026*
*Based on: NIST Cybersecurity Framework Version 1.1 (April 2018)*

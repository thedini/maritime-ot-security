---
title: "Phase 3: Defense Architecture Design"
phase: 3
duration: "Weeks 9-12"
weight: "30% of Project Grade"
deliverable: "Defense Architecture Document"
page_target: "30-40 pages"
---

# Phase 3: Defense Architecture Design

## Overview

In Phase 3, your team designs a comprehensive security architecture to protect the M/V CyberSea's operational technology and IT systems. Building on the vulnerabilities and risks identified in Phase 2, you will develop a defense-in-depth strategy that includes network segmentation, intrusion detection, monitoring, incident response, and security operations.

This phase aligns with the **Protect**, **Detect**, and **Respond** functions of the NIST Cybersecurity Framework and represents the core technical deliverable of the capstone project.

**Duration**: Weeks 9-12
**Deliverable**: Defense Architecture Document (30-40 pages)
**Due Date**: End of Week 12, 11:59 PM
**Weight**: 30% of total project grade

## Learning Objectives

By completing Phase 3, your team will:

- **Design** defense-in-depth security architecture for maritime OT environments
- **Specify** network segmentation strategies and enforcement mechanisms
- **Plan** intrusion detection and prevention system (IDS/IPS) deployment
- **Develop** security monitoring and logging strategies
- **Create** incident response procedures tailored to maritime operations
- **Define** security controls for each network zone
- **Propose** security awareness training programs for crew
- **Justify** design decisions with cost-benefit analysis

## Phase Activities

### Week 9: Architecture Planning & Network Segmentation Design

**Tasks**:
1. Review Phase 2 feedback and finalize priorities
2. Research maritime defense architectures (Purdue Model adaptation)
3. Design network segmentation strategy
4. Specify firewall placement and rule requirements
5. Plan VLAN architecture and enforcement

**Deliverables**:
- Network segmentation diagram (updated from Phase 1)
- Firewall rule matrix (conceptual)
- Architecture design document outline

### Week 10: IDS/IPS & Monitoring Design

**Tasks**:
1. Select IDS/IPS technologies for OT and IT networks
2. Design sensor placement for optimal coverage
3. Develop signature/rule strategy for maritime protocols
4. Plan SIEM and log aggregation architecture
5. Define alerting and escalation procedures
6. Design network monitoring dashboards

**Deliverables**:
- IDS/IPS deployment diagram
- SIEM architecture design
- Alert taxonomy and thresholds

### Week 11: Incident Response & Security Operations

**Tasks**:
1. Develop incident response plan (IRP) tailored to vessel operations
2. Create incident classification and severity matrix
3. Write response playbooks for common scenarios (ransomware, GPS spoofing, etc.)
4. Define roles and responsibilities (shipboard and shore-based)
5. Plan incident communication procedures (internal and external)
6. Design security awareness training program

**Deliverables**:
- Incident Response Plan
- Response playbooks (3-5 scenarios)
- Security awareness training outline

### Week 12: Integration, Cost Analysis & Finalization

**Tasks**:
1. Integrate all design components into cohesive architecture
2. Conduct cost-benefit analysis for major investments
3. Develop phased implementation plan (12-month roadmap)
4. Map controls to IEC 62443 Security Levels
5. Write executive summary
6. Final document review and polish
7. Submit Phase 3 deliverable
8. Prepare for Phase 4 presentation

**Deliverables**:
- Complete Defense Architecture Document
- Implementation roadmap
- Budget breakdown
- Draft presentation slides

## Required Content

Your Phase 3 deliverable must include the following sections:

### 1. Executive Summary (2-3 pages)

A high-level overview for executive leadership covering:

- **Current State**: Summary of Phase 2 findings (vulnerabilities, risks)
- **Proposed Architecture**: High-level description of defense strategy
- **Key Components**: Network segmentation, IDS/IPS, SIEM, incident response
- **Security Improvements**: How the architecture addresses identified vulnerabilities
- **Compliance**: Alignment with IMO, BIMCO, IEC 62443
- **Implementation Plan**: 12-month phased rollout
- **Budget**: Total cost ($500K constraint) and ROI justification
- **Benefits**: Quantified risk reduction, operational resilience, regulatory compliance

**Tone**: Strategic, business-focused, emphasizes risk reduction and compliance

### 2. Architecture Overview (3-4 pages)

Introduce the overall defense-in-depth strategy.

#### Defense-in-Depth Philosophy

Explain the layered security approach:

- **Layer 1: Perimeter Defense** - Firewalls, edge protection, external attack surface reduction
- **Layer 2: Network Segmentation** - Zoning, VLANs, microsegmentation
- **Layer 3: Endpoint Protection** - Antivirus, whitelisting, hardening
- **Layer 4: Monitoring & Detection** - IDS/IPS, SIEM, anomaly detection
- **Layer 5: Data Protection** - Encryption, backup, integrity checks
- **Layer 6: Incident Response** - Detection, containment, recovery procedures
- **Layer 7: People & Process** - Training, policies, awareness

#### Architectural Principles

Define guiding principles:

1. **Safety First**: Security controls must not compromise vessel safety or emergency operations
2. **Operational Continuity**: Minimize disruption to normal vessel operations
3. **Defense-in-Depth**: No single point of failure; multiple overlapping controls
4. **Least Privilege**: Minimize access rights for users and systems
5. **Segmentation**: Isolate critical OT systems from IT and external networks
6. **Monitoring**: Comprehensive visibility into network activity
7. **Resilience**: Ability to detect, respond, and recover from incidents
8. **Compliance**: Meet or exceed IMO, BIMCO, IEC 62443 requirements
9. **Cost-Effectiveness**: Maximize security within $500K budget
10. **Maintainability**: Solutions must be supportable by crew and shore staff

#### Architecture Diagram

Create a high-level architecture diagram showing:
- All network zones (from Phase 1, now with security controls)
- Firewalls and trust boundaries
- IDS/IPS sensors
- SIEM and monitoring infrastructure
- Backup and recovery systems
- External communication paths with security controls
- Data flow with encryption points

Use color coding and clear labels. This is the "hero diagram" that ties everything together.

### 3. Network Segmentation Design (5-7 pages)

Design a robust network segmentation strategy based on the Purdue Model adapted for maritime environments.

#### Purdue Model for Maritime OT

Adapt the industrial control system (ICS) Purdue Model:

**Level 0: Physical Processes** (Vessel Equipment)
- Engines, propellers, steering gear, ballast pumps
- Sensors: temperature, pressure, speed, position

**Level 1: Intelligent Devices** (Controllers & PLCs)
- Engine control units, propulsion controllers
- NMEA 2000 sensors and actuators
- CAN bus devices

**Level 2: Control Systems** (Supervisory Control)
- Engine Control System (ECS)
- Integrated Navigation System (INS)
- Bridge workstations (ECDIS, radar, AIS)
- Cargo management systems

**Level 3: Operations Management** (HMI & Engineering)
- Engineering workstations
- Voyage planning systems
- Maintenance management systems

**Level 4: Business Planning & Logistics** (Enterprise IT)
- Administrative workstations
- Email servers, file servers
- Fleet management integration
- Documentation systems

**Level 5: Enterprise Network** (Shore-Based)
- Corporate headquarters
- Fleet operations centers
- Remote monitoring

**DMZ: Internet-Facing Services**
- VSAT gateway
- External email relay
- Fleet management data exchange

**Guest Network: Crew Welfare**
- Crew Wi-Fi
- Personal devices
- Entertainment systems

#### Zone Definitions

For each zone, define:

**Zone 1: Critical Navigation Systems (OT-Critical)**
- **Purpose**: Safety-critical navigation and communication
- **Systems**: ECDIS, GPS, AIS, radar, INS, gyrocompass, VDR, GMDSS
- **Security Level**: IEC 62443 SL 3 (target)
- **Isolation**: Air-gapped or strictly firewalled; no direct internet access
- **Monitoring**: Dedicated IDS, anomaly detection
- **Access Control**: Physical and logical access tightly controlled; two-person rule for changes
- **Data Flows**:
  - Inbound: Time sync (NTP), chart updates (via secure media transfer)
  - Outbound: VDR data to secure storage, navigation data to Level 3 (one-way where possible)

**Zone 2: Engine & Propulsion Control (OT-Critical)**
- **Purpose**: Propulsion, power generation, machinery control
- **Systems**: ECS, fuel management, ballast control, emission monitoring
- **Security Level**: IEC 62443 SL 3 (target)
- **Isolation**: Air-gapped or strictly firewalled; no direct internet access
- **Monitoring**: Industrial IDS with OT protocol awareness (Modbus, CAN bus)
- **Access Control**: Physical access via engine control room; logical access with MFA
- **Data Flows**:
  - Inbound: Control commands (authenticated), sensor data from Level 1
  - Outbound: Telemetry to Level 3, alarms to bridge

**Zone 3: Cargo & Auxiliary Systems (OT-Standard)**
- **Purpose**: Cargo monitoring, non-critical operational systems
- **Systems**: Container tracking, reefer monitoring, HVAC, lighting
- **Security Level**: IEC 62443 SL 2
- **Isolation**: Firewalled from OT-Critical zones; limited IT integration
- **Monitoring**: Network IDS
- **Access Control**: RBAC with individual accounts
- **Data Flows**:
  - Inbound: Configuration updates, cargo data from IT systems
  - Outbound: Status data to IT systems, port authorities

**Zone 4: Enterprise IT (IT Network)**
- **Purpose**: Administrative, business, and communications
- **Systems**: Workstations, email server, file server, fleet integration
- **Security Level**: Standard IT security best practices
- **Isolation**: Firewalled from all OT zones
- **Monitoring**: Endpoint detection & response (EDR), network IDS
- **Access Control**: Active Directory, MFA for remote access
- **Data Flows**:
  - Inbound: Email, fleet management data, shore-side communications
  - Outbound: Reports to shore, operational data (non-critical)

**Zone 5: DMZ (Perimeter Network)**
- **Purpose**: External communications gateway
- **Systems**: VSAT gateway, email relay, fleet management interface, VPN concentrator
- **Security Level**: Hardened, minimal attack surface
- **Isolation**: Strict firewall rules to all internal zones
- **Monitoring**: IDS/IPS with aggressive blocking, web application firewall
- **Access Control**: Strong authentication, certificate-based where possible
- **Data Flows**:
  - Inbound: Internet traffic (filtered), shore-side connections (VPN)
  - Outbound: Sanitized data only; no direct OT data

**Zone 6: Crew Welfare Network (Guest Network)**
- **Purpose**: Crew personal internet access
- **Systems**: Wi-Fi access points, crew devices (BYOD)
- **Security Level**: Isolated guest network
- **Isolation**: Completely isolated from all operational networks; internet-only
- **Monitoring**: Basic traffic logging, content filtering
- **Access Control**: WPA3, captive portal, per-device registration
- **Data Flows**:
  - Inbound: Internet traffic (filtered for malware, policy compliance)
  - Outbound: Internet traffic only; no access to vessel systems

#### Segmentation Implementation

Specify technical implementation:

**Physical Segmentation**:
- Separate network switches for OT-Critical zones
- Dedicated cabling (e.g., red cables for critical OT)
- Physically separate Wi-Fi access points for guest network

**Logical Segmentation**:
- VLANs for each zone with strict inter-VLAN routing policies
- 802.1X network access control where feasible
- MAC address filtering on OT networks

**Firewall Placement**:
- Industrial firewall between OT zones and IT/DMZ
- Enterprise firewall between IT and DMZ
- Stateful inspection firewalls between all zones
- Next-generation firewall (NGFW) at perimeter

#### Firewall Rule Matrix

Develop a high-level firewall policy:

| Source Zone | Destination Zone | Protocol/Port | Action | Justification |
|-------------|------------------|---------------|--------|---------------|
| Navigation (Zone 1) | Engine (Zone 2) | DENY ALL | BLOCK | No operational need; prevent lateral movement |
| Navigation (Zone 1) | DMZ (Zone 5) | NTP (UDP 123) | ALLOW | Time synchronization for navigation |
| Engine (Zone 2) | IT (Zone 4) | Syslog (UDP 514) | ALLOW | Centralized logging |
| IT (Zone 4) | Navigation (Zone 1) | DENY ALL | BLOCK | IT compromise should not affect navigation |
| DMZ (Zone 5) | Navigation (Zone 1) | DENY ALL | BLOCK | Prevent external attack on critical systems |
| Crew (Zone 6) | Any Internal Zone | DENY ALL | BLOCK | Guest isolation |
| Any Zone | DMZ (Zone 5) | HTTPS (TCP 443) | ALLOW (inspected) | Internet access, chart updates |

**Rule Principles**:
- Default deny (whitelist approach)
- Minimum necessary access
- Unidirectional data flows where possible (data diodes for critical systems)
- Logging and alerting on all DENY actions
- Regular review and audit of rules

#### Network Diagrams

Provide detailed diagrams:
1. **Logical Network Diagram**: Showing zones, VLANs, IP subnets
2. **Physical Network Diagram**: Showing switches, cables, physical locations
3. **Data Flow Diagram**: Showing allowed communications between zones

### 4. Intrusion Detection & Prevention (4-6 pages)

Design IDS/IPS deployment for comprehensive threat detection.

#### Technology Selection

**OT Network IDS** (for Navigation, Engine, Cargo zones):
- **Recommended**: Industrial IDS with OT protocol support (e.g., Claroty, Nozomi Networks, Dragos)
- **Capabilities Required**:
  - NMEA 2000, Modbus/TCP, CAN bus protocol parsing
  - Asset discovery and profiling
  - Baseline anomaly detection
  - Signature-based detection for known ICS threats
  - Passive monitoring (no inline deployment for safety-critical systems)

**IT Network IDS/IPS** (for IT, DMZ, Crew zones):
- **Recommended**: Enterprise IDS/IPS (e.g., Snort, Suricata, Cisco Firepower)
- **Capabilities Required**:
  - Signature-based detection (Snort rules, ET Open)
  - Anomaly detection (traffic baselines)
  - Protocol analysis (HTTP, SMTP, DNS, etc.)
  - Inline prevention mode at perimeter (DMZ)
  - SSL/TLS inspection for encrypted traffic

#### Sensor Placement

**OT IDS Sensors**:
- **Navigation Network**: Passive tap on switch mirror port; monitor all ECDIS, radar, AIS traffic
- **Engine Network**: Passive tap on ECS network; monitor Modbus/TCP and CAN bus traffic
- **Cargo Network**: Passive tap on cargo management switch

**IT IDS Sensors**:
- **IT Network**: Span port on core IT switch; monitor workstation and server traffic
- **DMZ**: Inline IPS between firewall and VSAT gateway; active blocking enabled
- **Crew Network**: Passive monitoring for malware distribution; low-priority

**Placement Principles**:
- Passive taps for OT to avoid disrupting operations
- Inline prevention at perimeter to block external threats
- Sensors on both sides of critical firewalls to detect policy violations

#### Detection Strategies

**Signature-Based Detection**:
- ICS-CERT advisories for maritime and OT systems
- MITRE ATT&CK for ICS technique signatures
- Custom signatures for maritime-specific threats (AIS spoofing, GPS jamming indicators)

**Anomaly-Based Detection**:
- Baseline normal behavior for each OT network (message rates, protocols, device communications)
- Alert on deviations: new devices, protocol violations, unexpected traffic patterns
- Machine learning for advanced anomaly detection (if budget allows)

**Protocol Analysis**:
- Deep packet inspection (DPI) of NMEA, Modbus, CAN bus messages
- Validate message structure, detect malformed packets
- Identify unauthorized commands or parameter changes

**Threat Intelligence Integration**:
- Maritime threat intelligence feeds (IMO, ICS-CERT)
- General threat feeds (Emerging Threats, Abuse.ch)
- Vendor-specific advisories for vessel systems

#### Alert Configuration

**Alert Taxonomy**:
- **Critical**: Confirmed attack on safety-critical system; immediate response required
- **High**: Likely attack or significant anomaly; investigate within 1 hour
- **Medium**: Suspicious activity; investigate within 24 hours
- **Low**: Minor deviation or informational; log for analysis
- **Informational**: Audit events, non-security alerts

**Alert Tuning**:
- Tune signatures to reduce false positives (tuning period: 2-4 weeks post-deployment)
- Whitelist known-good behavior (e.g., regular maintenance scans)
- Suppress noisy rules that don't indicate actual threats
- Regular review of suppressed alerts to avoid blind spots

**Escalation Procedures**:
- Critical/High alerts: Immediate notification to bridge officer and CSSO (Cyber Security and Safety Officer)
- Medium alerts: Daily summary report to CSSO
- Low/Informational: Weekly report, stored in SIEM for analysis

#### IDS/IPS Deployment Diagram

Create a detailed diagram showing:
- Sensor locations (physical or virtual)
- Management console (onboard and shore-based access)
- Data flows from sensors to SIEM
- Alert notification paths

### 5. Security Monitoring & SIEM (3-5 pages)

Design centralized security monitoring and log management.

#### SIEM Architecture

**SIEM Platform Selection**:
- **Options**: Splunk, Elastic Stack (ELK), IBM QRadar, or open-source (Wazuh)
- **Requirements**:
  - Support for OT protocols and log formats
  - Onboard deployment (limited internet connectivity)
  - Dashboard and alerting capabilities
  - Long-term log retention (regulatory requirements)
  - Shore-based replication for backup and analysis

**SIEM Components**:
- **Log Collectors**: Installed on each zone's systems
- **SIEM Server**: Centralized onboard server (Zone 4 or dedicated management VLAN)
- **Storage**: Sufficient capacity for 12 months of logs (estimate based on log volume)
- **Dashboards**: Real-time monitoring screens for bridge and CSSO
- **Alerting**: Email, SMS, and onboard notification system integration

#### Log Sources

Collect logs from all security-relevant systems:

**OT Systems**:
- IDS alerts from all OT zones
- Firewall logs (allowed and denied connections)
- ECDIS, ECS, and other critical system event logs
- Protocol gateway logs (NMEA, Modbus)

**IT Systems**:
- Windows event logs (authentication, account changes, application errors)
- Linux syslog (if applicable)
- Active Directory logs (login failures, privilege escalations)
- Antivirus/EDR alerts

**Network Infrastructure**:
- Switch port status changes, VLAN changes
- Router ACL violations
- DHCP and DNS logs
- VPN authentication logs

**Physical Security**:
- Access control system logs (badge swipes)
- CCTV motion detection events (if integrated)

**Log Retention**:
- **Hot storage**: 90 days (searchable in SIEM)
- **Warm storage**: 12 months (archived, retrievable)
- **Cold storage**: 7 years (compliance, backup to shore)

#### Monitoring Dashboards

Design real-time dashboards for:

**CSSO Dashboard** (Cyber Security and Safety Officer):
- Alert summary (critical, high, medium counts)
- Top attacked systems
- Geographic threat map (source IPs)
- Recent authentication failures
- Firewall block statistics

**Network Operations Dashboard**:
- Network health (bandwidth utilization, latency)
- Device status (online/offline)
- VLAN traffic patterns
- Top talkers (source/destination IPs)

**OT Security Dashboard**:
- ICS protocol anomalies
- Unauthorized device detection
- Configuration changes in OT systems
- Safety system status

**Compliance Dashboard**:
- Patch status across all systems
- Antivirus definition age
- Backup success/failure
- Policy violation summary

#### Correlation Rules

Develop SIEM correlation rules to detect complex attacks:

**Example Rule 1: Potential Lateral Movement**
- Trigger: Multiple failed login attempts from IT zone to OT zone, followed by successful login
- Action: Critical alert, block source IP at firewall

**Example Rule 2: Possible Insider Threat**
- Trigger: USB device insertion on ECDIS + large file transfer to external email
- Action: High alert, investigate user activity

**Example Rule 3: GPS Spoofing Indicator**
- Trigger: Sudden GPS position jump inconsistent with vessel speed + AIS position mismatch
- Action: Critical alert, notify bridge immediately

**Example Rule 4: Ransomware Activity**
- Trigger: High volume of file modifications + encryption-related process names + SMB traffic surge
- Action: Critical alert, isolate affected systems

### 6. Incident Response Plan (5-7 pages)

Develop comprehensive incident response procedures tailored to maritime operations.

#### Incident Response Framework

Adopt NIST SP 800-61 Incident Response Lifecycle:

1. **Preparation**: Establish IR capability, train crew, prepare tools
2. **Detection & Analysis**: Identify incidents, determine scope and severity
3. **Containment, Eradication, Recovery**: Limit damage, remove threats, restore operations
4. **Post-Incident Activity**: Lessons learned, improve defenses

#### Roles & Responsibilities

Define incident response team structure:

**Onboard Roles**:
- **Incident Commander (IC)**: Master or Chief Officer; overall incident authority
- **Cyber Security and Safety Officer (CSSO)**: Lead technical response; may be Chief Engineer or IT-trained officer
- **Network Administrator**: Technical execution (isolate systems, collect evidence)
- **Bridge Officer**: Liaison for navigation safety, ensure incident response doesn't compromise safety
- **Communications Officer**: Internal and external notifications

**Shore-Based Roles**:
- **Fleet Cyber Security Manager**: Overall incident coordination, resource allocation
- **Incident Response Team**: Technical experts, forensics specialists
- **Legal Counsel**: Regulatory notification, liability management
- **Public Relations**: Media inquiries, customer communications

**External Parties**:
- **Vendors**: System manufacturers (ECDIS, ECS) for technical support
- **Coast Guard/Flag State**: Regulatory reporting
- **Port Authorities**: If incident affects port operations
- **Cyber Insurance**: Incident notification per policy
- **Law Enforcement**: If criminal activity suspected

#### Incident Classification

**Severity Levels**:

**Level 1 - Critical**:
- Impact on safety of navigation, life, or environment
- Compromise of ECDIS, GPS, or steering systems
- Ransomware affecting critical operations
- **Response Time**: Immediate (minutes)
- **Escalation**: Master, Fleet Manager, Coast Guard

**Level 2 - High**:
- Compromise of non-critical OT systems (cargo, ballast)
- Significant IT network disruption (email, communications)
- Data breach with PII or operational data
- **Response Time**: <1 hour
- **Escalation**: Master, Fleet Manager

**Level 3 - Medium**:
- Malware contained to single IT workstation
- Suspicious network activity, no confirmed compromise
- Policy violations (unauthorized USB, device)
- **Response Time**: <24 hours
- **Escalation**: CSSO, Fleet Manager (if ongoing)

**Level 4 - Low**:
- Minor security events (failed logins, blocked malware)
- Security testing or false positives
- **Response Time**: <72 hours
- **Escalation**: Document and report in weekly summary

#### Incident Response Playbooks

Develop step-by-step playbooks for common scenarios:

---

**Playbook 1: Ransomware Incident**

**Detection Indicators**:
- SIEM alert for rapid file encryption
- User reports files inaccessible or ransom note
- IDS detects SMB exploit or suspicious network traffic

**Immediate Actions (First 15 Minutes)**:
1. **Isolate**: Disconnect affected systems from network (pull network cable if necessary)
2. **Alert**: Notify IC, CSSO, bridge officer
3. **Assess**: Determine which systems affected (OT or IT? Critical?)
4. **Preserve**: Take screenshots, note time, do NOT power off (preserves evidence)

**Containment (First Hour)**:
1. **Network Segmentation**: Block affected VLAN at firewall
2. **Disable Accounts**: Suspend user accounts that may be compromised
3. **Scan**: Run antivirus scan on adjacent systems
4. **Backup Check**: Verify backup integrity, ensure backups not encrypted

**Eradication & Recovery (Hours to Days)**:
1. **Shore Contact**: Engage Fleet Cyber Security Manager, incident response team
2. **Forensics**: If safe, collect forensic images of affected systems
3. **Reimagine**: Wipe affected systems, rebuild from known-good images
4. **Restore Data**: Restore from clean backups (test before full restoration)
5. **Patch**: Ensure vulnerabilities exploited are patched before bringing systems online

**Post-Incident**:
1. **Lessons Learned**: What allowed ransomware to spread? Update controls
2. **Report**: Notify cyber insurance, legal counsel, flag state (if required)
3. **Training**: Conduct crew briefing on incident, update security awareness

**Do NOT**:
- Pay ransom without consulting legal, insurance, and fleet management
- Power off systems immediately (can lose memory evidence)
- Restore to network until threat eradicated

---

**Playbook 2: GPS Spoofing Detected**

**Detection Indicators**:
- Sudden GPS position jump inconsistent with vessel speed
- Mismatch between GPS position and AIS, radar, visual navigation
- SIEM correlation rule triggered

**Immediate Actions (First 5 Minutes)**:
1. **Verify**: Check multiple positioning sources (GPS, AIS, radar, visual)
2. **Alert**: Notify bridge officer immediately
3. **Navigation**: Switch to manual navigation, use alternative position sources
4. **Isolate**: Disconnect GPS from automatic systems (autopilot, ECDIS) if spoofing confirmed

**Investigation (First Hour)**:
1. **Source**: Attempt to identify spoofing source (RF direction finding if equipment available)
2. **Extent**: Check all GPS receivers (backup GPS, AIS, timing systems)
3. **Log**: Record time, position discrepancies, navigation actions taken

**Mitigation**:
1. **Manual Navigation**: Continue with manual positioning until threat clears
2. **Report**: Notify Coast Guard, flag state, and other vessels in area (GMDSS alert)
3. **Document**: Log all position data for post-incident analysis

**Recovery**:
1. **Verify Clear**: Confirm GPS signals return to normal (consistent with other sources)
2. **Gradual Integration**: Slowly reintroduce GPS to navigation systems, monitor for anomalies
3. **Post-Event**: Report incident to IMO, industry groups for threat intelligence

---

**Playbook 3: Insider Threat Detected**

**Detection Indicators**:
- SIEM alert for unauthorized access attempt to OT systems
- USB device insertion on critical system
- After-hours access to restricted areas
- Data exfiltration indicators (large file transfers to personal email)

**Immediate Actions**:
1. **Do Not Alert Suspect**: Avoid tipping off the insider
2. **Notify**: Inform Master and CSSO discreetly
3. **Monitor**: Increase surveillance (network, physical) of suspect's activity

**Investigation**:
1. **Log Review**: Examine SIEM logs for suspect's user account (logins, file access, email)
2. **Physical Access**: Review badge access logs, CCTV footage
3. **Interviews**: Discreetly interview colleagues, supervisors
4. **Evidence Collection**: Preserve digital evidence (do not alter logs, take forensic images if warranted)

**Containment**:
1. **Restrict Access**: Revoke network and physical access if threat confirmed
2. **Account Suspension**: Disable user account, change passwords for critical systems
3. **Search**: If warranted, search personal effects, quarters (per maritime law and company policy)

**Legal & HR**:
1. **Legal Counsel**: Consult before taking actions against crew member
2. **HR Process**: Follow company disciplinary procedures
3. **Law Enforcement**: Contact authorities if criminal activity suspected

**Post-Incident**:
1. **Review Access Controls**: Implement principle of least privilege more strictly
2. **Monitoring Enhancements**: Increase user activity monitoring
3. **Crew Vetting**: Review background check processes

---

*Include 2-3 additional playbooks for: AIS Spoofing, ECDIS Malware, Phishing Email, Network Intrusion from Crew Device*

#### Communication Plan

**Internal Communications**:
- Bridge-to-CSSO: Direct radio or intercom
- Crew Notification: PA announcement if necessary (avoid panic, provide clear instructions)
- Fleet Manager: Secure satellite phone, encrypted email

**External Communications**:
- **Coast Guard/Flag State**: Immediate notification for Level 1 incidents affecting safety
- **Port Authorities**: If incident affects port operations or cargo
- **Customers/Charterers**: Per contractual notification requirements
- **Media**: Only through designated company spokesperson; no crew comments

**Communication Templates**:
Provide templates for:
- Initial incident notification (internal)
- Regulatory notification (to Coast Guard)
- Customer notification (non-technical summary)

### 7. Security Controls by Zone (3-5 pages)

Specify detailed security controls for each network zone.

For each zone defined in Section 3, document:

#### Zone 1: Critical Navigation Systems

**Access Controls**:
- Physical: Locked bridge, badge access restricted to deck officers
- Logical: Individual user accounts, MFA for configuration changes, two-person integrity for critical changes

**Endpoint Security**:
- Application whitelisting (only approved navigation software can execute)
- USB port disabled or physically locked
- Antivirus (updated via secure media transfer, not internet)
- Host-based firewall with deny-all default

**Network Security**:
- Dedicated firewall (industrial firewall recommended)
- Unidirectional gateway for data export to VDR, Level 3 systems
- IDS monitoring with maritime protocol awareness
- Network access control (802.1X) if supported by devices

**Operational Controls**:
- Chart updates: Manual process via verified media (CD/USB with digital signatures)
- Software patches: Tested in lab environment, applied during maintenance window with vendor support
- Configuration management: All changes logged and auditable
- Regular backups: Daily backup of ECDIS routes, settings

**Monitoring**:
- Continuous IDS monitoring
- Configuration change detection
- Device connectivity monitoring (alert on new device)
- Integration with SIEM

---

*Repeat for Zone 2 (Engine Control), Zone 3 (Cargo), Zone 4 (IT), Zone 5 (DMZ), Zone 6 (Crew Welfare)*

### 8. Security Awareness Training Program (2-3 pages)

Design a crew training program to strengthen the human element of security.

#### Training Objectives

- Recognize phishing emails and social engineering
- Understand personal device (BYOD) security risks
- Follow USB and removable media policies
- Report security incidents promptly
- Apply operational security practices

#### Training Modules

**Module 1: Maritime Cybersecurity Basics** (1 hour)
- Why cybersecurity matters for maritime
- Real-world maritime cyber incidents (case studies)
- Threat actors targeting vessels
- Crew responsibilities for security

**Module 2: Phishing & Social Engineering** (30 minutes)
- Identifying phishing emails
- Verifying sender authenticity
- Avoiding malicious links and attachments
- Reporting suspicious emails

**Module 3: Device & USB Security** (30 minutes)
- Risks of personal devices onboard
- BYOD policy and crew Wi-Fi use
- USB and removable media policy
- What to do if you find an unknown USB device

**Module 4: Incident Reporting** (30 minutes)
- What constitutes a security incident
- How to report incidents (who, when, how)
- Importance of timely reporting
- No-blame culture for reporting

**Module 5: Operational Security (OPSEC)** (30 minutes)
- Protecting sensitive vessel information
- Social media guidelines for crew
- Visitor and contractor management
- Port security practices

**Module 6: Emergency Response** (30 minutes)
- Role during cyber incidents
- Bridge procedures if navigation systems compromised
- Communication protocols
- Safety vs. security decisions

#### Training Delivery

- **Initial Training**: All crew upon joining vessel (4 hours total)
- **Annual Refresher**: 2 hours yearly for all crew
- **Role-Specific**: Additional training for Master, Chief Engineer, CSSO (8 hours)
- **Tabletop Exercises**: Annual cyber incident drill (2 hours)
- **Phishing Simulations**: Quarterly simulated phishing emails to test and train

**Format**:
- Onboard: Computer-based training (CBT) modules, instructor-led sessions
- Shore-based: Training before joining vessel
- Multilingual: Available in primary crew languages

**Assessment**:
- Quiz at end of each module (80% passing score)
- Phishing simulation click rates (target: <10% click rate)
- Incident reporting metrics (increase in reports indicates better awareness)

#### Training Materials

- Video modules (short, 5-10 minute segments)
- Posters for crew areas ("Think Before You Click")
- Pocket cards with reporting procedures
- Case study handouts (real maritime incidents)

### 9. Implementation Roadmap (3-4 pages)

Develop a phased implementation plan over 12 months.

#### Implementation Phases

**Phase 1: Foundation (Months 1-3)**
- **Objective**: Address critical vulnerabilities, establish monitoring baseline
- **Activities**:
  - Deploy firewalls between OT and IT zones
  - Implement basic network segmentation (VLANs)
  - Install OT IDS on Navigation and Engine networks (passive mode)
  - Deploy SIEM (initial configuration)
  - Disable SMBv1 across all Windows systems
  - Patch critical vulnerabilities from Phase 2
  - Conduct initial security awareness training
- **Budget**: $150,000
- **Risk**: Prioritizes most critical security gaps

**Phase 2: Detection & Response (Months 4-6)**
- **Objective**: Build detection capabilities and response procedures
- **Activities**:
  - Complete IDS/IPS deployment (IT, DMZ, Crew zones)
  - Configure SIEM correlation rules
  - Tune IDS to reduce false positives
  - Implement centralized logging for all zones
  - Deploy endpoint detection & response (EDR) on IT systems
  - Finalize incident response playbooks
  - Conduct tabletop exercise for ransomware response
- **Budget**: $125,000
- **Risk**: Establishes ability to detect and respond to incidents

**Phase 3: Hardening & Controls (Months 7-9)**
- **Objective**: Strengthen endpoint and application security
- **Activities**:
  - Deploy application whitelisting on ECDIS and other OT workstations
  - Implement USB port controls (disable or lock)
  - Upgrade ECDIS to supported OS (coordinate with vendor)
  - Strengthen authentication (MFA for privileged accounts)
  - Implement network access control (802.1X) on IT zone
  - Enhance crew Wi-Fi isolation
  - Deploy data loss prevention (DLP) for sensitive data
- **Budget**: $125,000
- **Risk**: Reduces likelihood of compromise

**Phase 4: Optimization & Compliance (Months 10-12)**
- **Objective**: Refine controls, validate compliance, establish sustainment
- **Activities**:
  - Conduct penetration testing to validate defenses
  - Perform IEC 62443 gap analysis and remediation
  - Optimize SIEM rules based on operational experience
  - Complete security awareness training for all crew (refresher)
  - Establish patch management process with vendors
  - Document all security configurations
  - Conduct final tabletop exercise (GPS spoofing scenario)
  - Transition to steady-state operations (BAU)
- **Budget**: $100,000
- **Risk**: Ensures long-term sustainability and compliance

#### Implementation Gantt Chart

Create a visual timeline showing:
- Milestones for each phase
- Dependencies between activities
- Resource allocation (network admin, vendor support, crew training)
- Go/no-go decision points

#### Risk Management During Implementation

**Implementation Risks**:
- **Operational Disruption**: Mitigation: Schedule changes during port stays, maintenance windows
- **Vendor Delays**: Mitigation: Order hardware early, have backup vendors
- **Crew Resistance**: Mitigation: Communicate benefits, involve crew in design, provide training
- **Budget Overruns**: Mitigation: Contingency reserve (10%), phased approach allows re-prioritization

**Rollback Plans**:
- Document pre-change configurations
- Test changes in lab when possible
- Have rollback procedures ready
- Maintain old firewall rules until new rules validated

### 10. Cost-Benefit Analysis (2-3 pages)

Justify the $500,000 investment with quantitative and qualitative benefits.

#### Cost Breakdown

| Category | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Total |
|----------|---------|---------|---------|---------|-------|
| Hardware (firewalls, IDS appliances, servers) | $80K | $60K | $50K | $20K | $210K |
| Software (SIEM, IDS licenses, EDR, AV) | $30K | $40K | $40K | $30K | $140K |
| Professional Services (consulting, pen testing) | $25K | $15K | $20K | $35K | $95K |
| Training (CBT platform, instructor, materials) | $10K | $5K | $10K | $10K | $35K |
| Vendor Support (ECDIS upgrade, maintenance) | $5K | $5K | $5K | $5K | $20K |
| **Total** | **$150K** | **$125K** | **$125K** | **$100K** | **$500K** |

#### Quantifiable Benefits

**Risk Reduction**:
- **Avoided Ransomware Incident**: Avg maritime ransomware cost: $2M (downtime, ransom, recovery)
  - Probability reduction: 60% → 10% over 3 years
  - Expected value: $2M × (60% - 10%) = **$1M savings**

**Operational Efficiency**:
- **Reduced Incident Response Time**: Faster detection and response reduces downtime
  - Estimated savings: $50K/year in reduced manual investigations
  - 3-year value: **$150K savings**

**Insurance Premiums**:
- Cyber insurance discount for strong controls: 15-20%
  - Estimated annual premium: $100K; 15% discount = $15K/year
  - 3-year value: **$45K savings**

**Regulatory Compliance**:
- Avoid fines for non-compliance with IMO guidelines
  - Potential fine for major incident: $500K-$5M
  - Risk reduction: **Unquantified but significant**

**Total Quantifiable 3-Year Benefit**: ~$1.2M (ROI: 240%)

#### Qualitative Benefits

- **Enhanced Safety**: Reduced risk of navigation system compromise
- **Reputation**: Demonstrates cybersecurity leadership to customers, insurers, regulators
- **Crew Confidence**: Crew feel supported and secure in digital environment
- **Competitive Advantage**: Cybersecurity as differentiator in charter contracts
- **Regulatory Preparedness**: Ahead of pending IMO and flag state requirements

### 11. Compliance Mapping (2-3 pages)

Demonstrate alignment with maritime cybersecurity standards.

#### IEC 62443 Security Levels

Map your architecture to IEC 62443-3-3 Security Levels:

| System/Zone | Target SL | Achieved SL | Gap |
|-------------|-----------|-------------|-----|
| Navigation Systems | SL 3 | SL 2 (post-Phase 3) | Require additional authentication hardening |
| Engine Control | SL 3 | SL 2 (post-Phase 3) | Require vendor-supported access controls |
| Cargo Systems | SL 2 | SL 2 (post-Phase 2) | Compliant |
| IT Systems | SL 1-2 | SL 2 (post-Phase 2) | Compliant |

**Security Level Definitions**:
- **SL 1**: Protection against casual or coincidental violation
- **SL 2**: Protection against intentional violation using simple means (script kiddies)
- **SL 3**: Protection against intentional violation using sophisticated means (organized groups)
- **SL 4**: Protection against intentional violation using sophisticated means with extended resources (nation-states)

#### IMO Resolution MSC-FAL.1/Circ.3 Compliance

Address each pillar:

1. **Identify**: Phase 1 asset inventory, threat modeling ✓
2. **Protect**: Network segmentation, access controls, training ✓
3. **Detect**: IDS/IPS, SIEM, monitoring ✓
4. **Respond**: Incident response plan, playbooks ✓
5. **Recover**: Backup strategy, recovery procedures ✓

#### BIMCO Guidelines Compliance

- Assign shipboard responsibility (CSSO role) ✓
- Implement shipboard cyber risk management ✓
- Integrate cyber risks into safety management system ✓
- Conduct regular cyber drills and exercises ✓

### 12. Conclusions & Recommendations (1-2 pages)

Summarize the defense architecture and emphasize benefits.

**Key Takeaways**:
- Comprehensive defense-in-depth protects critical navigation and propulsion systems
- Phased implementation minimizes operational disruption
- Investment provides strong ROI through risk reduction
- Compliance with international standards achieved

**Success Factors**:
- Senior leadership support (Master, Fleet Manager)
- Crew engagement and training
- Vendor collaboration for OT system upgrades
- Continuous monitoring and improvement

**Future Enhancements** (post-12 months):
- Machine learning-based anomaly detection
- Shore-based Security Operations Center (SOC) integration
- Threat intelligence sharing with other vessels/fleet
- Advanced forensics capabilities

### 13. Appendices

**Appendix A: Firewall Rule Detailed Specifications**
Complete firewall rule set for all zones

**Appendix B: IDS Signature List**
Custom signatures for maritime protocols

**Appendix C: SIEM Correlation Rule Definitions**
Full correlation logic for threat detection

**Appendix D: Incident Response Contact List**
Emergency contacts (internal, external, vendors)

**Appendix E: Training Module Details**
Course outlines, quiz samples, assessment criteria

**Appendix F: Vendor Product Specifications**
Datasheets for recommended security products

### 14. References

Cite all sources, including:
- IEC 62443 series standards
- NIST SP 800-82, 800-61
- IMO and BIMCO guidelines
- Vendor documentation
- Maritime cyber threat reports

## Deliverable Submission

### Format Requirements

- **File Format**: PDF (primary) + editable diagrams (Visio, draw.io)
- **File Naming**: `TeamName_Phase3_2026-MM-DD.pdf`
- **Page Count**: 30-40 pages (excluding appendices)
- **Diagrams**: High-resolution, professional, color-coded
- **Tables**: Formatted consistently

### Submission Process

1. Submit PDF via course LMS by deadline (end of Week 12, 11:59 PM)
2. Push to GitHub repository with source files
3. Bring draft presentation slides to Week 12 check-in

### Late Policy

Same as previous phases.

## Grading Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| **Network Segmentation Design** | 25 | Comprehensive, secure, operationally feasible |
| **IDS/IPS Strategy** | 20 | Appropriate technology, placement, alert strategy |
| **Incident Response Plan** | 20 | Detailed, maritime-specific, actionable playbooks |
| **Implementation Roadmap** | 15 | Realistic, phased, addresses priorities |
| **Cost-Benefit Analysis** | 10 | Quantified benefits, justified investment |
| **Professional Quality** | 10 | Writing, diagrams, integration of components |

**Total**: 100 points (30% of project grade)

## Tips for Success

1. **Integration**: Phase 3 brings together Phases 1 and 2; ensure coherent narrative
2. **Realism**: Design must be implementable by vessel crew and vendors
3. **Safety First**: Never compromise vessel safety for security
4. **Justify Decisions**: Explain *why* you chose specific technologies, approaches
5. **Use Standards**: Reference IEC 62443, NIST, IMO throughout
6. **Visualize**: Diagrams are critical for communicating complex architecture
7. **Prepare for Phase 4**: Your Phase 3 document is the foundation for final presentation

## Resources

Same as previous phases, plus:
- IEC 62443-3-3: Security Levels for Zones and Conduits
- NIST SP 800-82: Guide to ICS Security
- SANS ICS Security Controls poster
- Sample network architecture diagrams

Good luck with Phase 3—this is the core of your capstone project!

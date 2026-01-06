---
title: "Phase 1: Reconnaissance & Threat Modeling"
phase: 1
duration: "Weeks 1-4"
weight: "20% of Project Grade"
deliverable: "Asset Inventory & Threat Model Document"
page_target: "15-25 pages"
---

# Phase 1: Reconnaissance & Threat Modeling

## Overview

In Phase 1, your team conducts reconnaissance on the M/V CyberSea's operational technology and IT systems. The goal is to develop a comprehensive understanding of the vessel's attack surface by documenting all assets, mapping network topology, and modeling potential threats.

This phase mirrors the **Identify** function of the NIST Cybersecurity Framework and establishes the foundation for all subsequent security work.

**Duration**: Weeks 1-4
**Deliverable**: Asset Inventory & Threat Model Document (15-25 pages)
**Due Date**: End of Week 4, 11:59 PM
**Weight**: 20% of total project grade

## Learning Objectives

By completing Phase 1, your team will:

- **Systematically identify** all OT and IT assets aboard a modern vessel
- **Document** network topology with appropriate notation and detail
- **Map** data flows between systems and external communications
- **Apply** structured threat modeling methodologies (STRIDE/ATT&CK)
- **Assess** threat actors relevant to maritime environments
- **Prioritize** assets based on criticality to vessel operations
- **Communicate** technical findings to stakeholders

## Phase Activities

### Week 1: Team Formation & Initial Research

**Tasks**:
1. Form teams and assign roles
2. Review M/V CyberSea scenario thoroughly
3. Research modern vessel system architectures
4. Begin asset inventory template
5. Schedule first team meeting with instructor

**Deliverables**:
- Team formation form submitted
- Initial meeting notes

### Week 2: Asset Inventory Development

**Tasks**:
1. Document all vessel systems (see Asset Categories below)
2. Research typical OT protocols (NMEA 2000, Modbus, CAN bus)
3. Identify data flows between systems
4. Create preliminary network diagram
5. Begin criticality assessment

**Deliverables**:
- Draft asset inventory spreadsheet
- Preliminary network diagram

### Week 3: Network Topology & Threat Actor Analysis

**Tasks**:
1. Finalize detailed network topology diagram
2. Document network zones and trust boundaries
3. Research maritime threat actors (nation-states, criminals, insiders)
4. Map threat actor capabilities and motivations
5. Identify external communication points (satellite, port, crew devices)

**Deliverables**:
- Detailed network topology diagram
- Threat actor profile matrix

### Week 4: Threat Modeling & Document Finalization

**Tasks**:
1. Apply STRIDE or ATT&CK methodology to each critical system
2. Document attack scenarios for high-priority threats
3. Complete asset criticality scoring
4. Write executive summary
5. Final document review and polish
6. Submit Phase 1 deliverable

**Deliverables**:
- Complete Asset Inventory & Threat Model Document
- Presentation-ready network diagrams

## Required Content

Your Phase 1 deliverable must include the following sections:

### 1. Executive Summary (1-2 pages)

A high-level overview for non-technical stakeholders covering:
- Number and types of systems identified
- Key network architecture characteristics
- Primary threat concerns
- Critical assets requiring protection
- Recommendations for Phase 2 focus areas

### 2. Vessel Asset Inventory (5-8 pages)

A comprehensive catalog of all OT and IT systems, organized by functional area:

#### Asset Categories

**Navigation Systems**:
- Integrated Navigation System (INS)
- Electronic Chart Display and Information System (ECDIS)
- Global Positioning System (GPS)
- Automatic Identification System (AIS)
- Radar systems (X-band, S-band)
- Gyrocompass and autopilot
- Voyage Data Recorder (VDR)
- Weather routing systems

**Engine & Propulsion Systems**:
- Engine Control System (ECS)
- Fuel management systems
- Ballast water management
- Emission monitoring systems
- Shaft power monitoring
- Engine room automation

**Cargo Management**:
- Container tracking system
- Refrigerated container (reefer) monitoring
- Cargo loading computer
- Lashing and securing monitors
- Dangerous goods tracking

**Communication Systems**:
- VSAT satellite communication
- Inmarsat systems (Fleet Xpress)
- VHF/UHF radios
- Global Maritime Distress and Safety System (GMDSS)
- Crew Wi-Fi network
- Email server

**Bridge & Control**:
- Ship Security Alert System (SSAS)
- Bridge alert management
- Machinery monitoring and control
- Fire detection and suppression
- Access control systems
- CCTV surveillance

**Enterprise IT**:
- Administrative workstations
- File servers
- Email servers
- Fleet management integration
- Electronic documentation systems

#### Asset Documentation Template

For each asset or asset category, document:

| Field | Description |
|-------|-------------|
| **Asset ID** | Unique identifier (e.g., NAV-001) |
| **Asset Name** | Common name |
| **Category** | Navigation, Engine, Cargo, etc. |
| **Vendor/Model** | Manufacturer and model number |
| **Function** | Primary operational purpose |
| **Network Zone** | Which network segment it resides in |
| **Protocols** | Communication protocols used (NMEA, Modbus, TCP/IP) |
| **External Connections** | Any connections outside vessel network |
| **Criticality** | High/Medium/Low (see scoring below) |
| **Dependencies** | Other systems it relies on |
| **Users** | Who interacts with the system |

#### Asset Criticality Scoring

Use the following criteria to assign criticality:

- **High**: Failure impacts vessel safety, regulatory compliance, or causes major operational disruption
  - Examples: Navigation systems, engine controls, SSAS

- **Medium**: Failure impacts operational efficiency or convenience but not safety
  - Examples: Cargo tracking, weather routing, crew Wi-Fi

- **Low**: Failure has minimal operational impact
  - Examples: Entertainment systems, non-critical administrative systems

### 3. Network Topology (3-5 pages)

#### Network Architecture Diagram

Create a detailed network diagram showing:
- All systems from asset inventory
- Network segments/zones (color-coded)
- Firewalls, routers, switches
- Trust boundaries (dashed lines)
- External communication paths
- Data flow directions (arrows with labels)

**Tools**: Use Visio, draw.io, Lucidchart, or similar professional diagramming tools.

**Notation**: Follow standard network diagram conventions:
- Rectangles for systems/devices
- Cylinders for databases
- Cloud shapes for external networks
- Firewall symbols for security boundaries
- Clear labels and legends

#### Network Zone Descriptions

Document each network zone:

**Example Zones**:
1. **Navigation Network** (OT Zone 1)
   - Purpose: Critical navigation and communication systems
   - Trust Level: High
   - Systems: ECDIS, GPS, AIS, Radar, INS
   - Isolation Requirements: Air-gapped or strictly firewalled from other zones

2. **Engine Control Network** (OT Zone 2)
   - Purpose: Propulsion and machinery control
   - Trust Level: High
   - Systems: ECS, fuel management, ballast control
   - Isolation Requirements: No direct internet access

3. **Cargo Network** (OT Zone 3)
   - Purpose: Cargo monitoring and management
   - Trust Level: Medium
   - Systems: Container tracking, reefer monitoring
   - Isolation Requirements: Limited integration with enterprise systems

4. **Enterprise IT Network** (IT Zone)
   - Purpose: Administrative and business operations
   - Trust Level: Medium
   - Systems: Office workstations, email, file servers
   - Isolation Requirements: Firewalled from OT zones

5. **Crew Welfare Network** (Guest Network)
   - Purpose: Crew internet access and personal devices
   - Trust Level: Low
   - Systems: Wi-Fi access points, entertainment
   - Isolation Requirements: Fully isolated from operational networks

6. **DMZ** (Demilitarized Zone)
   - Purpose: External communications and fleet integration
   - Trust Level: Low-Medium
   - Systems: Fleet management gateway, email relay
   - Isolation Requirements: Strict firewall rules, IDS monitoring

For each zone, document:
- Connected systems
- Communication protocols
- Firewall rules (conceptual at this stage)
- Data flows in/out of zone
- Security requirements

#### Data Flow Mapping

Create data flow diagrams for critical processes:
- Navigation data to VDR
- Engine telemetry to shore-based fleet management
- Cargo data to port authorities
- Crew internet traffic routing
- Software update delivery paths

Use Data Flow Diagram (DFD) notation:
- Circles for processes
- Arrows for data flows
- Rectangles for external entities
- Parallel lines for data stores

### 4. Threat Actor Analysis (3-4 pages)

Identify and profile threat actors relevant to maritime OT environments:

#### Threat Actor Categories

**Nation-State Actors**:
- **Motivation**: Espionage, disruption, strategic advantage
- **Capabilities**: Sophisticated, persistent, well-resourced
- **Relevant Groups**: APT groups targeting maritime infrastructure
- **Typical Targets**: Navigation data, vessel tracking, cargo manifests
- **Likelihood**: Low-Medium (depends on vessel routes, cargo types)

**Organized Cybercrime**:
- **Motivation**: Financial gain (ransomware, cargo theft, piracy facilitation)
- **Capabilities**: Moderate to high, commodity malware to custom tools
- **Relevant Groups**: Ransomware gangs, cargo theft rings
- **Typical Targets**: Enterprise IT systems, cargo data, payment systems
- **Likelihood**: Medium (maritime sector increasingly targeted)

**Insider Threats**:
- **Motivation**: Sabotage, theft, negligence, coercion
- **Capabilities**: High (authorized access, knowledge of systems)
- **Relevant Actors**: Crew members, contractors, port personnel
- **Typical Targets**: Any system with physical or logical access
- **Likelihood**: Medium (insider threats underreported)

**Hacktivists**:
- **Motivation**: Political statement, environmental protest
- **Capabilities**: Low to moderate
- **Relevant Groups**: Environmental activists, geopolitical protesters
- **Typical Targets**: Public-facing systems, AIS spoofing
- **Likelihood**: Low (opportunistic)

**Opportunistic Attackers**:
- **Motivation**: Challenge, curiosity, reputation
- **Capabilities**: Low to moderate
- **Relevant Actors**: Script kiddies, security researchers
- **Typical Targets**: Internet-exposed systems, default credentials
- **Likelihood**: Medium (ports and satellite links are attack vectors)

#### Threat Actor Matrix

Create a matrix summarizing:

| Threat Actor | Motivation | Capability | Intent | Likelihood | Impact |
|--------------|------------|------------|--------|------------|---------|
| Nation-State | Espionage | High | Targeted | Low | Critical |
| Cybercrime | Financial | Medium | Opportunistic | Medium | Major |
| Insider | Varies | High | Targeted | Medium | Major |
| Hacktivist | Political | Low-Med | Targeted | Low | Moderate |
| Opportunistic | Curiosity | Low | Opportunistic | Medium | Minor |

### 5. Threat Modeling (5-8 pages)

Apply a structured threat modeling methodology to identify potential attack scenarios.

#### Methodology Selection

Choose one of the following frameworks:

**Option A: STRIDE**

STRIDE categorizes threats by type:
- **S**poofing: Impersonating another entity
- **T**ampering: Modifying data or systems
- **R**epudiation: Denying actions occurred
- **I**nformation Disclosure: Exposing confidential information
- **D**enial of Service: Disrupting availability
- **E**levation of Privilege: Gaining unauthorized access

**Option B: MITRE ATT&CK for ICS**

ATT&CK maps adversary tactics and techniques:
- Initial Access
- Execution
- Persistence
- Evasion
- Discovery
- Lateral Movement
- Collection
- Command and Control
- Inhibit Response Function
- Impair Process Control
- Impact

**Recommendation**: Use STRIDE for comprehensive coverage, or ATT&CK if team prefers industry-standard framework.

#### Threat Modeling Process

For each **critical system** or **network zone**:

1. **Identify Entry Points**: Where can attackers gain access?
   - External: Satellite links, port networks, crew devices
   - Physical: USB ports, maintenance laptops, unauthorized devices
   - Internal: Compromised systems, insider access

2. **Enumerate Assets**: What valuable targets exist?
   - Data: Navigation routes, cargo manifests, operational data
   - Functionality: Steering control, engine control, safety systems
   - Availability: Critical systems that must remain operational

3. **Apply Threat Framework**: For each asset and entry point, identify threats
   - STRIDE example: "Spoofing GPS signals to mislead navigation (S)"
   - ATT&CK example: "Adversary exploits VNC on engineering workstation (Initial Access: T0886)"

4. **Document Attack Scenarios**: Write narrative descriptions of plausible attacks

#### Example Attack Scenarios

Provide 5-10 detailed attack scenarios covering:

**Example 1: Ransomware via Crew Wi-Fi**
- **Entry Point**: Crew member's infected laptop connects to crew Wi-Fi
- **Attack Path**: Malware spreads to enterprise IT network → pivots to DMZ → compromises fleet management gateway → deploys ransomware across administrative systems
- **Impact**: Loss of electronic documentation, email, cargo tracking; demand for ransom
- **Affected Systems**: Enterprise IT zone, partially DMZ
- **Threat Type**: STRIDE - Tampering, Denial of Service; ATT&CK - Initial Access, Lateral Movement, Impact
- **Likelihood**: Medium (common attack vector)
- **Severity**: Major (operational disruption, regulatory issues)

**Example 2: GPS Spoofing Attack**
- **Entry Point**: External RF interference near navigation antennas
- **Attack Path**: Adversary broadcasts stronger GPS signals with false position data → navigation systems accept spoofed data → vessel diverts from planned route
- **Impact**: Vessel misdirection, potential grounding, piracy risk
- **Affected Systems**: GPS, INS, autopilot
- **Threat Type**: STRIDE - Spoofing; ATT&CK - Impair Process Control
- **Likelihood**: Low (requires proximity and equipment)
- **Severity**: Critical (safety of navigation)

**Example 3: Insider Sabotage of Engine Control**
- **Entry Point**: Authorized crew member with physical access to engine control room
- **Attack Path**: Insider plugs malicious USB device into ECS maintenance port → malware modifies control parameters → engine operates at unsafe levels
- **Impact**: Engine damage, loss of propulsion, environmental incident
- **Affected Systems**: Engine Control System
- **Threat Type**: STRIDE - Tampering, Elevation of Privilege; ATT&CK - Execution, Impair Process Control
- **Likelihood**: Low (requires malicious insider)
- **Severity**: Critical (safety and environmental)

*Continue with additional scenarios covering AIS manipulation, ECDIS malware, VSAT interception, etc.*

#### Threat Prioritization

Create a matrix prioritizing threats by likelihood and impact:

```
         Low Impact    Medium Impact    High Impact    Critical Impact
High     [Threats]     [Threats]        [Threats]      [Threats]
Likely

Medium   [Threats]     [Threats]        [Threats]      [Threats]
Likely

Low      [Threats]     [Threats]        [Threats]      [Threats]
Likely
```

**Prioritization Guidance**:
- **Critical Impact + High Likelihood** = Immediate attention in Phase 2
- **Critical Impact + Any Likelihood** = Must be addressed
- **Low Impact + Low Likelihood** = Monitor but lower priority

### 6. Findings & Recommendations (2-3 pages)

Summarize Phase 1 insights:

**Key Findings**:
- Total number of identified assets
- Number of network zones
- Most critical systems
- Highest priority threats
- Notable security gaps observed

**Recommendations for Phase 2**:
- Which systems require deep vulnerability assessment
- External penetration testing considerations
- Configuration review priorities
- Third-party vendor security evaluations needed

### 7. References

Cite all sources used:
- M/V CyberSea scenario documentation
- Maritime cybersecurity standards (IMO, BIMCO)
- Threat intelligence reports
- Vendor documentation
- Academic papers on maritime OT security
- MITRE ATT&CK for ICS framework (if used)

Use IEEE or APA citation style consistently.

## Deliverable Submission

### Format Requirements

- **File Format**: PDF (primary submission)
- **File Naming**: `TeamName_Phase1_2026-MM-DD.pdf`
- **Page Count**: 15-25 pages (excluding cover, table of contents, appendices)
- **Font**: 11-12 pt, professional (Times New Roman, Arial, Calibri)
- **Margins**: 1 inch all sides
- **Figures**: High-resolution, properly labeled with captions
- **Tables**: Formatted consistently, numbered sequentially

### Submission Process

1. Submit PDF via course LMS by deadline (end of Week 4, 11:59 PM)
2. Optionally push to team GitHub repository
3. Bring one printed copy to instructor check-in (Week 4)

### Late Policy

- **Within 24 hours**: 5% deduction
- **24-48 hours**: 10% deduction
- **48-72 hours**: 20% deduction
- **Beyond 72 hours**: Not accepted without prior approval

Extensions granted only for documented emergencies; request at least 48 hours in advance when possible.

## Grading Rubric

Your Phase 1 deliverable will be evaluated on:

| Criterion | Points | Excellent (90-100%) | Good (80-89%) | Satisfactory (70-79%) | Needs Improvement (<70%) |
|-----------|--------|---------------------|---------------|-----------------------|--------------------------|
| **Asset Inventory Completeness** | 25 | All systems documented with comprehensive details | Most systems documented, minor gaps | Basic documentation, missing details | Significant gaps, superficial |
| **Network Topology Accuracy** | 20 | Professional, detailed, accurate diagrams; clear zones | Good diagrams, minor inaccuracies | Basic diagrams, clarity issues | Unclear or incorrect topology |
| **Threat Modeling Rigor** | 25 | Thorough application of methodology, diverse scenarios | Good methodology use, adequate coverage | Basic threat modeling, limited scenarios | Superficial or incorrect application |
| **Criticality Assessment** | 15 | Well-justified, consistent criteria, clear priorities | Reasonable assessments, minor inconsistencies | Basic prioritization, weak justification | Unclear or arbitrary priorities |
| **Professional Quality** | 10 | Excellent writing, formatting, visuals | Good quality, minor issues | Acceptable but needs polish | Poor quality, difficult to read |
| **Threat Actor Analysis** | 5 | Comprehensive, well-researched, relevant | Good coverage, minor gaps | Basic analysis | Superficial or inaccurate |

**Total**: 100 points (20% of project grade)

## Tips for Success

1. **Start with Research**: Understand modern vessel systems before diving in
2. **Use Templates**: Spreadsheets and diagram templates save time and ensure consistency
3. **Iterate Network Diagrams**: Start simple, add detail progressively
4. **Think Like an Attacker**: Challenge assumptions about security boundaries
5. **Leverage Course Materials**: Reference lab exercises and lecture notes
6. **Seek Feedback Early**: Use Week 2 check-in to validate approach
7. **Divide Tasks**: Parallel work on asset inventory, diagrams, and threat research
8. **Budget Time for Integration**: Final document requires synthesis, not just aggregation
9. **Proofread**: Technical accuracy matters, but so does clear communication

## Resources

### Recommended Reading

- IMO MSC-FAL.1/Circ.3: Guidelines on Maritime Cyber Risk Management
- BIMCO Guidelines on Cyber Security Onboard Ships
- NIST SP 800-82: Guide to Industrial Control Systems Security
- ENISA: Analysis of Cyber Security Aspects in the Maritime Sector
- MITRE ATT&CK for ICS: [https://attack.mitre.org/matrices/ics/](https://attack.mitre.org/matrices/ics/)

### Tools

- **Diagramming**: draw.io (free), Lucidchart, Microsoft Visio
- **Threat Modeling**: Microsoft Threat Modeling Tool, OWASP Threat Dragon
- **Documentation**: Markdown + Pandoc, LaTeX, Microsoft Word
- **Collaboration**: Google Docs, GitHub, Notion

### Sample Artifacts

Available on course LMS:
- Example asset inventory spreadsheet
- Network diagram templates
- STRIDE threat modeling worksheet
- Sample Phase 1 report (redacted from previous semester)

## Questions?

Reach out via:
- **Instructor Office Hours**: Tuesday/Thursday, 2-4 PM
- **Slack**: #phase1-questions channel
- **Email**: instructor@university.edu

Good luck with Phase 1!

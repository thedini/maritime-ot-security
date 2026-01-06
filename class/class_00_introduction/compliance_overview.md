---
title: Maritime Cybersecurity Regulatory Compliance Overview
module: Class 00 - Introduction
type: reference
audience: Maritime security professionals, vessel operators, compliance officers
last_updated: 2026-01-06
---

# Maritime Cybersecurity Regulatory Compliance Overview

## Introduction

Maritime cybersecurity has evolved from a voluntary practice to a regulatory requirement. This document provides an overview of the key regulations, guidelines, and standards that govern cybersecurity in the maritime industry, with particular focus on Operational Technology (OT) systems aboard vessels.

## International Maritime Organization (IMO) Requirements

### IMO Resolution MSC.428(98) - Maritime Cyber Risk Management in Safety Management Systems

**Adopted:** June 2017
**Effective:** January 1, 2021
**Status:** Mandatory

#### Key Requirements

- **Integration with ISM Code:** Cyber risk management must be integrated into existing Safety Management Systems (SMS) by the first annual Document of Compliance (DOC) verification after January 1, 2021
- **Scope:** Applies to all ships covered by the ISM Code (SOLAS vessels)
- **Risk Assessment:** Companies must identify cyber risks and implement safeguards
- **Documentation:** Cyber risk management procedures must be documented in the SMS

#### What This Means

All shipping companies operating SOLAS-regulated vessels must:
1. Conduct cyber risk assessments for their vessels
2. Document cyber risk management procedures
3. Implement protective measures
4. Train crew on cyber risks
5. Maintain records of cyber incidents and responses

### IMO MSC-FAL.1/Circ.3 - Guidelines on Maritime Cyber Risk Management

**Published:** July 2017
**Status:** Guidance (non-mandatory but widely adopted)

#### Core Principles

The guidelines are built on five functional elements:

1. **Identify:** Determine critical systems, data, and assets
2. **Protect:** Implement safeguards and protective measures
3. **Detect:** Develop anomaly detection capabilities
4. **Respond:** Plan and execute incident response
5. **Recover:** Restore systems and improve resilience

These align with the NIST Cybersecurity Framework.

#### Critical Systems Identified

The guidelines specifically highlight vulnerability of:
- Bridge systems (ECDIS, GPS, AIS, autopilot)
- Cargo handling and management systems
- Propulsion and machinery management
- Access control systems
- Passenger management systems
- Crew welfare systems (internet, email)
- Administrative and crew management systems

#### Risk Management Approach

- **Functional vs. Technical:** Focus on maintaining essential functions rather than specific technologies
- **Proportionate:** Risk management should be proportionate to vessel type and operations
- **Dynamic:** Continuous process, not one-time assessment
- **Integrated:** Must work with existing SMS frameworks

## United States Coast Guard (USCG) Cybersecurity Requirements

### USCG Navigation and Vessel Inspection Circular (NVIC) 01-20

**Published:** January 2020
**Status:** Guidance for compliance with MSC.428(98)

#### Key Provisions

- Provides U.S.-flagged vessels with detailed guidance on implementing IMO cyber risk requirements
- Specifies documentation expectations for SMS integration
- Outlines inspection procedures and compliance verification

### USCG Cyber Rules - 33 CFR Part 104 (Facility Security)

**Effective:** July 1, 2025
**Status:** Mandatory for MTSA-regulated facilities

#### Coverage

Applies to:
- Marine Terminal Operators (MTOs)
- Outer Continental Shelf (OCS) facilities
- Vessel-to-facility interface security

#### Requirements

- Cybersecurity assessments as part of Facility Security Assessments (FSA)
- Cyber incident reporting
- Cybersecurity measures in Facility Security Plans (FSP)
- Designated Cybersecurity Officer or point of contact
- Regular security drills including cyber scenarios

#### Vessel Interface Implications

While primarily focused on facilities, these rules affect vessels through:
- Shore-side connectivity requirements
- Data exchange security protocols
- Coordinated cyber incident response
- Supply chain cybersecurity

## NIST Cybersecurity Framework for Maritime

### Application to Maritime OT

The National Institute of Standards and Technology (NIST) Cybersecurity Framework (CSF) version 1.1 provides a flexible, risk-based approach applicable to maritime OT systems.

#### Framework Core Functions

1. **Identify (ID)**
   - Asset Management (ID.AM)
   - Business Environment (ID.BE)
   - Governance (ID.GV)
   - Risk Assessment (ID.RA)
   - Risk Management Strategy (ID.RM)

2. **Protect (PR)**
   - Access Control (PR.AC)
   - Awareness and Training (PR.AT)
   - Data Security (PR.DS)
   - Information Protection Processes (PR.IP)
   - Maintenance (PR.MA)
   - Protective Technology (PR.PT)

3. **Detect (DE)**
   - Anomalies and Events (DE.AE)
   - Security Continuous Monitoring (DE.CM)
   - Detection Processes (DE.DP)

4. **Respond (RS)**
   - Response Planning (RS.RP)
   - Communications (RS.CO)
   - Analysis (RS.AN)
   - Mitigation (RS.MI)
   - Improvements (RS.IM)

5. **Recover (RC)**
   - Recovery Planning (RC.RP)
   - Improvements (RC.IM)
   - Communications (RC.CO)

#### Maritime-Specific Implementation

See `/home/vessel/vessel_lstm/maritime-ot-security/resources/nist_csf_maritime_mapping.md` for detailed maritime applications.

**Key Differences from IT Security:**
- **Safety-Critical Systems:** OT failures can cause physical harm or environmental damage
- **Legacy Systems:** Many maritime systems run on outdated, unpatched operating systems
- **Network Segmentation:** Critical bridge systems should be isolated from crew internet access
- **Remote Monitoring:** Shore-based condition monitoring creates attack surfaces
- **Physical Access:** Vessels in port face insider threats from visitors, contractors, port workers

## BIMCO Guidelines on Cyber Security Onboard Ships

**Published:** February 2016 (5th edition: 2020)
**Status:** Industry best practice

### Key Features

The Baltic and International Maritime Council (BIMCO) guidelines provide practical, ship-operator-focused advice:

#### Organizational Measures

- Designate a Cyber Security Officer (CSO)
- Establish cyber security policies
- Conduct regular risk assessments
- Implement access control procedures
- Maintain awareness and training programs
- Plan incident response procedures

#### Technical Measures

- Network segmentation between critical systems
- Firewall configuration and maintenance
- Anti-malware protection
- Patch management procedures
- Backup and recovery procedures
- Secure remote access controls
- USB and removable media policies

#### Practical Tools

BIMCO provides:
- Cyber security clause for charter parties
- Checklist for shipboard procedures
- Incident reporting templates
- Training materials

### Industry Adoption

The BIMCO guidelines are widely adopted because:
- Written in operational language (not highly technical)
- Practical and cost-effective recommendations
- Compatible with ISM Code structure
- Supported by major industry stakeholders (ICS, INTERTANKO, INTERCARGO, INTERMANAGER)

## IEC 62443 - Industrial Automation and Control Systems Security

### Overview

IEC 62443 is a multi-part international standard series for securing Industrial Control Systems (ICS), applicable to maritime OT environments.

### Series Structure

- **IEC 62443-1-x:** General concepts, terminology, models
- **IEC 62443-2-x:** Policies and procedures (management level)
- **IEC 62443-3-x:** System requirements (technical level)
- **IEC 62443-4-x:** Component requirements (product development)

### Maritime Application

#### Relevant Parts for Vessel Operators

**IEC 62443-2-1: Security Program Requirements**
- Cybersecurity management system establishment
- Risk assessment methodology
- Security policies and procedures

**IEC 62443-3-3: System Security Requirements and Security Levels**
- Defines Security Levels (SL) 1-4
- Foundational requirements (FR):
  - FR1: Identification and Authentication Control
  - FR2: Use Control
  - FR3: System Integrity
  - FR4: Data Confidentiality
  - FR5: Restricted Data Flow
  - FR6: Timely Response to Events
  - FR7: Resource Availability

**IEC 62443-3-2: Security Risk Assessment**
- Zones and conduits methodology
- Threat modeling for ICS environments
- Security Level targeting

#### Security Zones for Maritime

Example zone architecture:
- **Zone 1 (Highest Security):** Navigation and steering systems
- **Zone 2:** Propulsion control systems
- **Zone 3:** Cargo management systems
- **Zone 4:** Administrative IT systems
- **Zone 5 (Lowest Security):** Guest/crew internet access

**Conduits:** Controlled interfaces between zones with specific security requirements.

### Implementation Challenges

- **Cost:** Full IEC 62443 compliance can be expensive
- **Legacy Systems:** Many vessel systems predate these standards
- **Complexity:** Standard is comprehensive but technically demanding
- **Certification:** Limited number of certified assessors in maritime sector

### Practical Approach

- Use IEC 62443 as a framework, not strict compliance target
- Focus on zone/conduit architecture principles
- Apply security levels proportionate to risk
- Prioritize high-criticality systems (navigation, propulsion)

## Classification Society Requirements

### Overview

Classification societies (class) have begun incorporating cybersecurity into their rules and notations. Compliance may be required for insurance and financing.

### Det Norske Veritas (DNV)

#### DNV Class Notation: CYBER

**Levels:**
- **CYBER-Secure:** Basic cyber risk management integrated in SMS
- **CYBER-Secure+:** Enhanced security for critical systems
- **CYBER-Resilient:** Advanced resilience and recovery capabilities

**Requirements:**
- Cyber risk assessment documented
- Network architecture with segmentation
- Access control and authentication
- Malware protection
- Patch management
- Backup and recovery procedures
- Incident response plan
- Cybersecurity training

**DNV-RP-0496: Recommended Practice for Cyber Security Resilience Management**
- Comprehensive guidance for maritime cyber resilience
- Aligned with IMO, NIST, IEC 62443
- Practical implementation guidance

### Lloyd's Register (LR)

#### LR Cyber Notations

**Cyber Descriptive Notes:**
- **Cyber AL1:** Awareness Level - Basic procedures in place
- **Cyber AL2:** Compliance Level - Meets regulatory requirements
- **Cyber AL3:** Advanced Level - Enhanced security measures
- **Cyber AL4:** Leading Level - Best-in-class security posture

**LR Cyber Safety and Security Certification (CySS)**
- Independent assessment and certification
- Based on risk assessment
- Regular surveillance and re-certification

**LR Code for Software Asset Management (SAM)**
- Focused on software inventory and lifecycle management
- Critical for patch management and vulnerability tracking

### American Bureau of Shipping (ABS)

#### ABS Cyber Safety Notations

**ABS CySafe:** Cybersecurity certification program

**Tiers:**
- **CySafe-Design:** Cyber considerations in design phase
- **CySafe-Build:** Cybersecurity during construction
- **CySafe-Operate:** Operational cybersecurity management

**ABS Guide for Cybersecurity Implementation for the Marine and Offshore Industries**
- Risk-based approach
- Aligned with NIST CSF, IEC 62443, IMO guidelines
- Specific guidance for shipyards, operators, equipment manufacturers

#### ABS Requirements

- Asset inventory and criticality assessment
- Network architecture documentation
- Security controls implementation
- Vulnerability management
- Incident response planning
- Training and awareness
- Third-party risk management

### Bureau Veritas (BV)

**BV Cyber Managed Notation:**
- Integration of cyber risk in safety management
- Technical and organizational measures
- Regular audits and surveillance

### Choosing a Cyber Notation

**Considerations:**
- **Insurance Requirements:** Some insurers mandate cyber certifications
- **Charter Requirements:** Charterers may specify cyber standards
- **Operational Profile:** Level of digital integration and connectivity
- **Budget:** Certification and ongoing compliance costs
- **Competitive Advantage:** Marketing benefit in some sectors

## Regional Requirements

### European Union (EU)

**NIS2 Directive (Directive (EU) 2022/2555)**
- Applies to entities in maritime transport sector
- Requirements for risk management, incident reporting, supply chain security
- Member state implementation varies
- Affects EU-flagged vessels and vessels calling at EU ports

**EU Maritime Security Strategy**
- Emphasizes cyber resilience for critical maritime infrastructure
- Coordination between maritime and cybersecurity authorities

### Singapore

**Maritime and Port Authority of Singapore (MPA) Cybersecurity Requirements**
- Cybersecurity requirements for ship registration
- Port cybersecurity standards
- Incident reporting to MPA

### Other Flag States

Many flag states defer to IMO requirements but may have additional specific requirements. Consult with flag state administration for vessel-specific requirements.

## Insurance and P&I Club Requirements

### Cyber Risk in Marine Insurance

**Hull & Machinery (H&M) Policies:**
- Increasingly include cyber exclusions or sublimits
- May require evidence of cyber risk management for full coverage

**Protection & Indemnity (P&I) Clubs:**
- Cyber incidents may affect coverage (e.g., pollution from cyber-caused incident)
- Some clubs offer cyber risk guidance and require risk assessments
- Incident reporting obligations

**Cyber-Specific Marine Insurance:**
- Emerging market for dedicated maritime cyber insurance
- Covers business interruption, data breach, system restoration
- Often requires compliance with standards (IMO, class notation, etc.)

### Key Requirements from Insurers

- Evidence of cyber risk assessment
- SMS integration per MSC.428(98)
- Documented cybersecurity procedures
- Incident response plan
- Regular training and drills
- Potentially: class notation or third-party certification

## Industry Guidelines and Best Practices

### Additional Resources

**International Chamber of Shipping (ICS):**
- Guidance on Cyber Security Onboard Ships (version 4, 2021)
- Practical checklists and procedures

**IUMI (International Union of Marine Insurance):**
- Cyber risk guidelines for shipowners and operators

**OCIMF (Oil Companies International Marine Forum):**
- Tanker Management and Self-Assessment (TMSA) includes cyber elements
- Ship Inspection Report Programme (SIRE) 2.0 includes cyber questions

**International Association of Ports and Harbors (IAPH):**
- Cybersecurity Guidelines for Ports
- Affects vessel-port interface security

**ISO/IEC 27001:**
- General information security management
- Applicable to shipping company shore-based operations
- Can be extended to vessel systems

## Compliance Roadmap

### For Vessel Operators

**Phase 1: Foundation (Months 1-3)**
1. Review IMO MSC-FAL.1/Circ.3 guidelines
2. Conduct initial cyber risk assessment
3. Document current cybersecurity measures in SMS
4. Designate Cyber Security Officer

**Phase 2: Implementation (Months 4-9)**
1. Implement priority security controls (network segmentation, access control)
2. Develop cybersecurity procedures and policies
3. Begin crew training program
4. Establish incident response plan
5. Conduct tabletop exercises

**Phase 3: Verification (Months 10-12)**
1. Internal audit of cyber risk management in SMS
2. External verification (flag state, class society, or third-party)
3. Document of Compliance (DOC) verification including cyber elements
4. Address any findings

**Phase 4: Continuous Improvement (Ongoing)**
1. Regular risk reassessments (annual minimum)
2. Update procedures based on incidents and lessons learned
3. Continuous monitoring and detection
4. Stay informed of regulatory changes
5. Engage with industry forums and information sharing

### Documentation Requirements

Maintain records of:
- Cyber risk assessments and updates
- Security policies and procedures
- Asset inventories and network diagrams
- Training records
- Incident logs
- Audit and inspection reports
- Lessons learned and improvements

## Key Takeaways

1. **Cybersecurity is Mandatory:** IMO MSC.428(98) makes cyber risk management a regulatory requirement, not optional.

2. **Integration, Not Addition:** Cyber risk management should be integrated into existing SMS, not treated as separate.

3. **Risk-Based Approach:** Focus resources on highest-risk systems and scenarios.

4. **Multi-Stakeholder:** Compliance requires coordination between ship operators, flag states, class societies, port authorities, and insurers.

5. **Operational Focus:** Maritime cyber regulations emphasize maintaining safety and operational continuity, not just IT security.

6. **Continuous Process:** Cyber risk management is dynamic; regular reassessment and improvement are essential.

7. **Training is Critical:** Human factors are the biggest vulnerability; crew awareness and training are foundational.

8. **Documentation Matters:** Demonstrable compliance requires thorough documentation and record-keeping.

## Further Reading

- IMO MSC-FAL.1/Circ.3: `/home/vessel/vessel_lstm/maritime-ot-security/resources/imo_guidelines_summary.md`
- NIST CSF Maritime Application: `/home/vessel/vessel_lstm/maritime-ot-security/resources/nist_csf_maritime_mapping.md`
- Compliance Checklist: `/home/vessel/vessel_lstm/maritime-ot-security/resources/compliance_checklist.md`

## References

- IMO Resolution MSC.428(98), 2017
- IMO MSC-FAL.1/Circ.3, Guidelines on Maritime Cyber Risk Management, 2017
- USCG NVIC 01-20, 2020
- NIST Cybersecurity Framework v1.1, 2018
- BIMCO Guidelines on Cyber Security Onboard Ships, 5th edition, 2020
- IEC 62443 series (various parts)
- DNV-RP-0496: Recommended Practice for Cyber Security Resilience Management
- ABS Guide for Cybersecurity Implementation for the Marine and Offshore Industries
- Lloyd's Register Code for Software Asset Management

---

*Document Version: 1.0*
*Last Updated: January 6, 2026*
*Next Review: July 2026*

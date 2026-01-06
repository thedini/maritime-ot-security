---
title: IMO Cyber Risk Management Guidelines - Detailed Summary
document_reference: IMO MSC-FAL.1/Circ.3
published_date: 2017-07-05
status: Guidance (Non-mandatory)
related_resolution: MSC.428(98)
type: reference
last_updated: 2026-01-06
---

# IMO Cyber Risk Management Guidelines - Detailed Summary

## Document Overview

**Full Title:** Guidelines on Maritime Cyber Risk Management
**Document Number:** MSC-FAL.1/Circ.3
**Published:** July 5, 2017
**Issuing Body:** International Maritime Organization (IMO)
**Legal Status:** Non-mandatory guidance supporting Resolution MSC.428(98)

## Purpose and Scope

### Primary Objectives

The guidelines aim to:
1. Provide high-level recommendations on maritime cyber risk management
2. Support implementation of Resolution MSC.428(98)
3. Protect shipping from current and emerging cyber threats
4. Safeguard maritime safety and security
5. Protect the marine environment

### Applicability

**Applies to:**
- All ships (emphasis on ships subject to ISM Code)
- Shipping companies
- Ship operators
- Shipyards (for newbuilds and retrofits)
- Port facilities
- Maritime service providers

**Systems Covered:**
- Shipboard operational technology (OT) systems
- Information technology (IT) systems connected to OT
- Shore-based systems that interface with ships
- Third-party systems with access to ship systems

## Key Definitions

### Cyber Risk
The measure of the extent to which a technology asset is threatened by a potential circumstance or event, combining:
- **Likelihood:** Probability of occurrence
- **Impact:** Consequences if it occurs

### Maritime Cyber Risk
Cyber risk specifically affecting:
- Safety of the ship
- Security of the ship and port facilities
- Marine environment
- Commercial operations

### Cyber Incident
An occurrence that:
- Jeopardizes cyber security
- May be caused by malicious, negligent, or accidental action
- Results in actual or potentially adverse consequences

## Risk Management Framework

The guidelines adopt a five-functional approach based on the NIST Cybersecurity Framework:

### 1. IDENTIFY

**Objective:** Develop understanding of cyber risks to systems, assets, data, and capabilities.

#### Activities

**Asset Identification:**
- Inventory all information and operational technology systems
- Identify critical systems essential for safety and operations
- Map dependencies between systems
- Document network architecture and connections

**Critical Systems Examples:**
- Bridge systems (ECDIS, radar, AIS, VHF DSC, autopilot, GPS/GNSS)
- Propulsion and machinery control systems
- Cargo handling and tank management systems
- Power management systems
- Safety systems (fire detection, bilge alarms)
- Security systems (CCTV, access control)

**Business Environment:**
- Understand operational context
- Identify stakeholder expectations (regulatory, commercial, reputational)
- Determine safety and environmental criticality

**Vulnerability Assessment:**
- Identify potential threat vectors (e.g., internet connections, USB drives, email, remote access)
- Recognize system vulnerabilities (outdated software, poor access controls, lack of segmentation)
- Consider human factors (insider threats, social engineering susceptibility)

**Risk Assessment:**
- Evaluate likelihood and impact of cyber incidents
- Prioritize risks based on safety, security, environmental, and commercial consequences
- Document risk register

#### Documentation

- Asset inventory with criticality ratings
- Network architecture diagrams
- Data flow diagrams
- Threat and vulnerability assessment
- Risk assessment report

### 2. PROTECT

**Objective:** Implement appropriate safeguards to ensure delivery of critical services.

#### Activities

**Access Control:**
- Implement role-based access control (RBAC)
- Use strong authentication (passwords, multi-factor where possible)
- Restrict physical access to critical systems
- Control remote access (shore-based monitoring, OEM support)
- Manage user accounts (creation, modification, deletion)

**Best Practices:**
- Change default passwords on all systems
- Use unique passwords for each system/user
- Implement password policies (complexity, expiration)
- Disable unused accounts (former crew, contractors)
- Log all access attempts

**Network Segmentation:**
- Separate critical operational systems from non-critical systems
- Isolate crew internet/email from navigation and engineering systems
- Use firewalls between network segments
- Implement VLANs or physical separation
- Control data flow between segments

**Example Architecture:**
```
[Critical Systems Zone] <--Firewall--> [Ship Operations Zone] <--Firewall--> [Crew/Guest Zone]
    - ECDIS                               - Admin systems                        - Crew WiFi
    - Autopilot                           - CCTV                                - Email
    - Engine control                      - Maintenance systems                 - Entertainment
    - Cargo systems
```

**Data Security:**
- Protect sensitive information (navigation plans, cargo details, crew data)
- Encrypt sensitive data in transit and at rest
- Control data transfers (USB drives, email attachments)
- Implement data backup procedures
- Secure deletion of data when systems are decommissioned

**Awareness and Training:**
- Conduct cybersecurity awareness training for all crew
- Provide role-specific training (officers, engineers, IT staff)
- Include cyber scenarios in drills and exercises
- Update training materials regularly
- Document training records

**Training Topics:**
- Recognizing phishing and social engineering
- Safe use of email and internet
- USB drive and removable media policies
- Password security
- Reporting suspicious activities
- Incident response procedures

**Maintenance:**
- Keep systems updated with security patches
- Document patch management procedures
- Test patches before deployment (where possible)
- Maintain antivirus/antimalware with updated signatures
- Perform regular system health checks

**Protective Technology:**
- Deploy firewalls with appropriate rule sets
- Implement antivirus/antimalware solutions
- Use intrusion detection/prevention systems (where appropriate)
- Disable unnecessary services and ports
- Implement secure configuration baselines

**Policies and Procedures:**
- Develop and document cybersecurity policies
- Create operational procedures for secure system use
- Establish clear lines of authority and responsibility
- Integrate cyber procedures into SMS
- Review and update procedures regularly

#### Documentation

- Cybersecurity policy document
- Access control procedures
- Network architecture with security controls
- Training records and materials
- Patch management logs
- Configuration baselines
- Backup schedules and verification logs

### 3. DETECT

**Objective:** Develop and implement capabilities to identify the occurrence of a cybersecurity event.

#### Activities

**Anomaly Detection:**
- Monitor for unusual system behavior
- Watch for unexpected network traffic
- Look for unauthorized access attempts
- Notice system performance degradation
- Identify unexpected system restarts or errors

**Warning Signs:**
- GPS position jumps or anomalies
- AIS displaying incorrect ship information
- ECDIS charts not updating or showing errors
- Steering or propulsion responding unexpectedly
- Unauthorized users or login attempts
- Unknown devices on network
- Unusual data transfers

**Continuous Monitoring:**
- Regularly review system logs
- Monitor network traffic patterns
- Check for unauthorized configuration changes
- Verify system integrity
- Conduct periodic vulnerability scans (where appropriate)

**Detection Processes:**
- Establish baseline of normal operations
- Define indicators of compromise (IoCs)
- Implement alerting mechanisms
- Assign monitoring responsibilities
- Document detection procedures

**Reporting:**
- Establish clear reporting channels
- Encourage crew to report suspicions without fear
- Document all potential incidents
- Escalate appropriately based on severity

#### Documentation

- Monitoring schedules and logs
- Baseline operational parameters
- Indicators of compromise (IoCs)
- Detection procedures
- Incident reporting forms

### 4. RESPOND

**Objective:** Develop and implement appropriate activities to take action regarding a detected cybersecurity incident.

#### Activities

**Response Planning:**
- Develop cyber incident response plan
- Define roles and responsibilities
- Establish communication protocols
- Identify decision-making authority
- Create response checklists

**Communications:**
- Notify appropriate personnel (Master, CSO, company DPA)
- Report to flag state administration (as required)
- Inform coast guard or port state (as required)
- Coordinate with class society
- Notify customers/stakeholders (as appropriate)
- Document all communications

**Analysis:**
- Assess incident scope and severity
- Determine affected systems
- Identify root cause (if possible)
- Evaluate impact on safety, security, operations
- Document findings

**Mitigation:**
- Contain the incident (isolate affected systems)
- Implement workarounds to maintain critical functions
- Eradicate threat (remove malware, block attacker access)
- Prioritize safety of ship and crew
- Document actions taken

**Incident Response Phases:**
1. **Detection and Reporting:** Incident identified and reported
2. **Assessment:** Determine severity and impact
3. **Containment:** Limit spread and damage
4. **Eradication:** Remove threat
5. **Recovery:** Restore normal operations
6. **Lessons Learned:** Document and improve

**Emergency Procedures:**
- Revert to manual operations if automated systems compromised
- Use backup navigation methods (paper charts, celestial navigation)
- Maintain situation awareness at all times
- Prioritize safe navigation and seamanship
- Consider safe haven or anchoring if necessary

#### Documentation

- Cyber incident response plan
- Emergency contact lists
- Response checklists
- Incident logs (timeline, actions, decisions)
- Communication records
- Post-incident report

### 5. RECOVER

**Objective:** Develop and implement appropriate activities to maintain resilience and restore any capabilities or services impaired by a cybersecurity incident.

#### Activities

**Recovery Planning:**
- Develop system recovery procedures
- Maintain system backups (regularly tested)
- Document recovery priorities
- Identify alternative methods (manual operations)
- Plan for external support (OEMs, cybersecurity consultants)

**Recovery Priorities:**
1. Safety-critical systems (navigation, steering, propulsion)
2. Security systems (access control, CCTV)
3. Environmental protection systems
4. Operational systems (cargo, communications)
5. Administrative systems

**System Restoration:**
- Verify threat has been eliminated before reconnection
- Restore from known-good backups
- Rebuild systems if necessary
- Revalidate system functionality
- Monitor for reoccurrence

**Testing:**
- Verify systems operate correctly after restoration
- Ensure security controls are functioning
- Confirm no residual compromise
- Conduct post-recovery testing

**Improvements:**
- Conduct post-incident review
- Identify lessons learned
- Update procedures based on experience
- Implement corrective actions
- Share lessons with fleet (maintaining confidentiality as needed)

**Communication:**
- Inform stakeholders of recovery status
- Update flag state and port state as required
- Document recovery timeline
- Report completion of recovery

#### Documentation

- Recovery procedures
- Backup and restoration logs
- System test results
- Lessons learned report
- Corrective action plan

## Safety Management System (SMS) Integration

### ISM Code Requirements

**Resolution MSC.428(98) Mandates:**
- Cyber risks must be appropriately addressed in existing SMS by the first annual DOC verification after January 1, 2021
- No separate documentation system required - integrate into current SMS structure

### Integration Points

**SMS Section** | **Cyber Risk Management Element**
---|---
Safety and Environmental Policy | Include commitment to cyber risk management
Company Responsibilities and Authority | Designate Cyber Security Officer or responsible person
Designated Person Ashore (DPA) | Include cyber incidents in DPA responsibilities
Master's Responsibility | Include cyber risk awareness and response
Resources and Personnel | Include cybersecurity training requirements
Shipboard Operations | Include cyber-secure operational procedures
Emergency Preparedness | Include cyber incident response procedures
Non-Conformity, Accidents, and Hazardous Situations | Include cyber incidents in reporting
Maintenance of Ship and Equipment | Include cyber-related maintenance (patches, updates)
Documentation | Include cyber risk assessment, procedures, records
Company Verification and Review | Include cyber risk management in internal audits
Certification and Verification | Expect cyber elements in DOC/SMC audits

### Practical Integration Steps

1. **Review Current SMS:** Identify where cyber elements fit within existing structure
2. **Update Policies:** Add cyber risk management to safety and environmental policy statements
3. **Revise Procedures:** Incorporate cyber considerations into relevant operational procedures
4. **Develop New Procedures:** Create procedures for cyber-specific activities (patch management, incident response)
5. **Update Training:** Integrate cyber awareness into SMS training programs
6. **Enhance Documentation:** Create forms and templates for cyber risk assessment, incident reporting
7. **Audit Integration:** Include cyber elements in internal audits

## Risk Assessment Requirements

### Conducting a Maritime Cyber Risk Assessment

#### Step 1: Define Scope

- Identify vessels or vessel types covered
- Determine systems to be assessed
- Set assessment boundaries (shipboard only, or including shore-based systems)
- Define time period and frequency of reassessment

#### Step 2: Identify Assets

- Create inventory of all IT and OT systems
- Document system functions and interdependencies
- Identify critical data and information
- Map network architecture and connections

**Asset Categories:**
- **Navigation Systems:** ECDIS, GPS, radar, AIS, autopilot, compass
- **Communication Systems:** VHF, GMDSS, satellite communications, email
- **Propulsion Systems:** Engine control, fuel management, propulsion control
- **Cargo Systems:** Tank management, cargo monitoring, ballast control
- **Safety Systems:** Fire detection, bilge alarms, emergency shutdown
- **Security Systems:** CCTV, access control, SSAS
- **Administrative Systems:** Crew management, payroll, voyage planning

#### Step 3: Identify Threats

**Threat Categories:**
- **Malware:** Viruses, worms, ransomware, trojans
- **Unauthorized Access:** Hacking, insider threats, physical intrusion
- **Denial of Service:** Network flooding, system overload
- **Data Breaches:** Theft of sensitive information
- **System Manipulation:** Spoofing, data injection, control system takeover

**Threat Actors:**
- **External:** Hackers, criminal organizations, nation-states, terrorists
- **Internal:** Disgruntled crew, negligent users, contractors

**Threat Vectors:**
- Internet/email connectivity
- Removable media (USB drives, CDs)
- Remote access (shore-based monitoring, OEM support)
- Supply chain (compromised equipment or software)
- Physical access (port visitors, contractors, stowaways)

#### Step 4: Identify Vulnerabilities

**Technical Vulnerabilities:**
- Outdated or unpatched software
- Default or weak passwords
- Lack of network segmentation
- Unnecessary services or ports enabled
- Lack of encryption
- Poor logging and monitoring

**Procedural Vulnerabilities:**
- Inadequate access controls
- Lack of cybersecurity policies
- Insufficient training
- Poor incident response capability
- Inadequate backup procedures

**Human Vulnerabilities:**
- Lack of cyber awareness
- Susceptibility to social engineering
- Negligent behavior (clicking suspicious links, using personal USB drives)

#### Step 5: Assess Likelihood

For each threat-vulnerability pair, estimate likelihood:
- **High:** Likely to occur within 1 year
- **Medium:** May occur within 1-3 years
- **Low:** Unlikely to occur within 3 years

Consider:
- Attractiveness of target (vessel type, cargo, route)
- Threat actor capability and motivation
- Effectiveness of existing controls
- Historical incidents (own vessel, fleet, industry)

#### Step 6: Assess Impact

For each threat scenario, estimate impact:
- **Safety:** Potential for injury, loss of life, loss of vessel
- **Environmental:** Potential for pollution or ecological damage
- **Security:** Potential for security breach, terrorism, piracy
- **Commercial:** Financial loss, reputational damage, contractual penalties
- **Regulatory:** Potential for non-compliance, fines, detention

**Impact Levels:**
- **Critical:** Catastrophic consequences (e.g., loss of navigation in confined waters)
- **High:** Severe consequences (e.g., cargo system failure causing delays)
- **Medium:** Moderate consequences (e.g., temporary loss of non-critical system)
- **Low:** Minor consequences (e.g., nuisance, easily mitigated)

#### Step 7: Evaluate Risk

Combine likelihood and impact to determine risk level:

| | Low Impact | Medium Impact | High Impact | Critical Impact |
|---|---|---|---|---|
| **High Likelihood** | Medium | High | High | Critical |
| **Medium Likelihood** | Low | Medium | High | Critical |
| **Low Likelihood** | Low | Low | Medium | High |

#### Step 8: Prioritize and Treat Risks

**Risk Treatment Options:**
- **Mitigate:** Implement controls to reduce likelihood or impact
- **Accept:** Acknowledge risk but take no action (for low risks)
- **Transfer:** Share risk (e.g., insurance, third-party services)
- **Avoid:** Eliminate activity causing risk (e.g., disable unnecessary connectivity)

**Prioritization:**
1. Address Critical and High risks immediately
2. Plan mitigation for Medium risks
3. Monitor Low risks for changes

#### Step 9: Document Assessment

Document:
- Scope and methodology
- Asset inventory
- Threats and vulnerabilities identified
- Likelihood and impact assessments
- Risk ratings and prioritization
- Treatment decisions and action plan
- Residual risks after treatment

#### Step 10: Review and Update

- Review risk assessment annually (minimum)
- Update after significant changes (new systems, incidents, operational changes)
- Update after industry-wide threats emerge
- Document review dates and changes

## Implementation Timeline

### Historical Context

- **June 2017:** IMO adopts Resolution MSC.428(98)
- **July 2017:** IMO publishes MSC-FAL.1/Circ.3 guidelines
- **January 1, 2021:** Deadline for integration into SMS
- **2021 onwards:** Cyber risk management expected during DOC/SMC audits

### Compliance Verification

**Flag State Audits:**
- Flag state inspectors verify cyber risk management during SMS audits
- Expect review of cyber risk assessment
- Expect evidence of procedures, training, incident records

**Port State Control:**
- Some PSC regimes include cyber questions in inspections
- Focus on SMS integration and Master's awareness
- Deficiencies can be issued for non-compliance

**Class Society Audits:**
- Class societies verify SMS compliance during surveys
- Cyber notations require additional assessment
- Annual audits review continued compliance

## Compliance Checklist

### Documentation Checklist

- [ ] Cyber risk assessment completed and documented
- [ ] Cyber risk management procedures integrated into SMS
- [ ] Cybersecurity policy statement in SMS
- [ ] Asset inventory with criticality ratings
- [ ] Network architecture diagram
- [ ] Access control procedures
- [ ] Patch management procedures
- [ ] Backup and recovery procedures
- [ ] Incident response plan
- [ ] Training program and records
- [ ] Audit records showing cyber elements reviewed
- [ ] Master and crew aware of cyber procedures

### Technical Controls Checklist

- [ ] Default passwords changed on all systems
- [ ] Strong password policy implemented
- [ ] Network segmentation between critical and non-critical systems
- [ ] Firewalls configured and maintained
- [ ] Antivirus/antimalware installed and updated
- [ ] Unnecessary services and ports disabled
- [ ] Remote access controlled and logged
- [ ] System logs reviewed regularly
- [ ] Backups performed and tested regularly
- [ ] Physical access controls for critical systems

### Organizational Controls Checklist

- [ ] Cyber Security Officer or responsible person designated
- [ ] Cybersecurity roles and responsibilities defined
- [ ] Crew trained on cyber risks and procedures
- [ ] Cyber incidents included in emergency drills
- [ ] Incident reporting procedures established
- [ ] Communication plan for cyber incidents
- [ ] Relationship with external support (OEMs, IT support) established
- [ ] Lessons learned from incidents documented and shared

### SMS Integration Checklist

- [ ] SMS policy includes cyber risk management
- [ ] DPA responsibilities include cyber incidents
- [ ] Master responsibilities include cyber risk awareness
- [ ] Training matrix includes cybersecurity
- [ ] Emergency preparedness includes cyber incidents
- [ ] Non-conformity reporting includes cyber incidents
- [ ] Internal audit program includes cyber elements
- [ ] Management review includes cyber risk

## Common Implementation Challenges

### Challenge 1: Legacy Systems

**Issue:** Many shipboard systems run outdated operating systems (Windows XP, Windows 7) that no longer receive security updates.

**Solutions:**
- Network isolation (air-gap or strict firewall rules)
- Virtual patching (network-based protection)
- Compensating controls (monitoring, physical security)
- Plan for system replacement in long-term

### Challenge 2: Cost

**Issue:** Implementing technical controls (firewalls, segmentation, security software) can be expensive.

**Solutions:**
- Prioritize high-risk systems
- Use cost-effective solutions (open-source tools, policy-based controls)
- Phase implementation over time
- Consider cyber risks in CAPEX planning for new equipment

### Challenge 3: Crew Awareness

**Issue:** Crew may not appreciate cyber risks or may see security measures as burdensome.

**Solutions:**
- Practical, scenario-based training
- Explain "why" behind procedures
- Involve crew in risk assessment
- Make procedures simple and clear
- Recognize and reward good cyber hygiene

### Challenge 4: Balancing Security and Operations

**Issue:** Security measures can interfere with operational efficiency.

**Solutions:**
- Involve operational personnel in procedure design
- Test procedures in realistic scenarios
- Provide flexibility where appropriate (e.g., emergency access procedures)
- Focus on risk-based approach, not blanket restrictions

### Challenge 5: Keeping Up with Threats

**Issue:** Cyber threat landscape evolves rapidly; assessments can become outdated.

**Solutions:**
- Subscribe to maritime cyber threat intelligence
- Participate in industry information sharing
- Conduct regular reassessments
- Stay informed of incidents in the industry
- Engage with class societies and industry associations

## Key Takeaways

1. **High-Level Guidance:** IMO MSC-FAL.1/Circ.3 provides principles, not prescriptive requirements
2. **Risk-Based:** Focus resources on highest-risk systems and scenarios
3. **Functional Approach:** Organize efforts around Identify, Protect, Detect, Respond, Recover
4. **SMS Integration:** Leverage existing safety management system structure
5. **Proportionate:** Measures should be appropriate to vessel type, operations, and risk level
6. **Continuous:** Cyber risk management is ongoing, not one-time
7. **Safety-Focused:** Emphasis is on maintaining safety, security, and environmental protection
8. **Practical:** Guidelines recognize maritime operational realities (legacy systems, cost, crew constraints)

## Additional Resources

**IMO Documents:**
- IMO Resolution MSC.428(98): Maritime cyber risk management in safety management systems
- IMO MSC-FAL.1/Circ.3: Guidelines on maritime cyber risk management (this document)
- IMO MSC.1/Circ.1526: Interim guidelines on maritime cyber risk management

**Related Course Materials:**
- Compliance Overview: `/home/vessel/vessel_lstm/maritime-ot-security/class/class_00_introduction/compliance_overview.md`
- NIST CSF Maritime Mapping: `/home/vessel/vessel_lstm/maritime-ot-security/resources/nist_csf_maritime_mapping.md`
- Compliance Checklist: `/home/vessel/vessel_lstm/maritime-ot-security/resources/compliance_checklist.md`

**External Resources:**
- BIMCO Guidelines on Cyber Security Onboard Ships
- ICS Guidance on Cyber Security Onboard Ships
- Classification society cyber guides (DNV, LR, ABS, BV)
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework

---

*Document Version: 1.0*
*Last Updated: January 6, 2026*
*Source: IMO MSC-FAL.1/Circ.3 (July 5, 2017)*

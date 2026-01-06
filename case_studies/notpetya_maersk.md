---
title: "NotPetya Attack on Maersk (2017)"
date: "June 27, 2017"
category: "Ransomware"
severity: "Critical"
estimated_losses: "$300+ million"
recovery_time: "10 days"
affected_systems: "IT infrastructure, container tracking, port operations"
attack_vector: "Supply chain compromise (M.E.Doc software)"
attribution: "Russian military intelligence (attributed by multiple governments)"
learning_objectives:
  - Understand supply chain attack vectors
  - Analyze cascading failures in maritime operations
  - Evaluate business continuity and disaster recovery
  - Assess the impact of IT/OT convergence vulnerabilities
---

# NotPetya Attack on Maersk (2017)

## Executive Summary

On June 27, 2017, the global shipping giant A.P. Moller-Maersk became one of the most prominent victims of the NotPetya cyberattack, suffering catastrophic disruption to its worldwide operations. The attack, which was not actually ransomware but a wiper disguised as such, encrypted systems across Maersk's global network, bringing container shipping operations to a near-complete halt. The incident resulted in losses exceeding $300 million and took 10 days to fully remediate, requiring the reinstallation of 4,000 servers and 45,000 PCs.

This case demonstrates the vulnerability of critical maritime infrastructure to cyberattacks and the cascading effects that can ripple through global supply chains when major shipping operations are disrupted.

## Background

### A.P. Moller-Maersk

- **World's largest container shipping company** (at the time)
- Operates approximately 600+ vessels
- Handles roughly 20% of global container traffic
- Employs 76,000+ people across 130 countries
- Revenue: ~$30 billion annually
- Owns APM Terminals (76+ port and terminal facilities worldwide)
- Integrated business includes shipping, port operations, and logistics

### Pre-Attack Context

In early 2017, Maersk's IT infrastructure consisted of:
- Highly interconnected global network
- Centralized IT systems for container tracking (GCSS - Global Container Shipping System)
- Integrated port terminal management systems
- Active Directory infrastructure spanning all operations
- Mix of IT and OT systems with increasing convergence

## Timeline of Events

### Day 0: June 27, 2017

**~14:30 UTC (10:30 AM EDT)**
- NotPetya malware begins spreading globally via compromised update to M.E.Doc tax accounting software
- M.E.Doc was widely used by Ukrainian companies for tax reporting
- Maersk's Ukrainian office in Odessa had M.E.Doc installed

**~14:45 UTC**
- NotPetya enters Maersk's network through the Odessa office
- Malware begins lateral movement across the global network
- Uses EternalBlue exploit (NSA-developed, leaked by Shadow Brokers)
- Also spreads via legitimate Windows management tools (PsExec, WMIC)

**~15:00-16:00 UTC**
- Encryption spreads exponentially across Maersk's global infrastructure
- Active Directory domain controllers begin failing
- Container tracking systems go offline
- Port terminal operations systems affected
- Total time from initial infection to near-complete network encryption: **~30 minutes**

**16:00+ UTC**
- Maersk realizes the severity of the attack
- Decision made to shut down all systems globally to contain spread
- All 17 container terminals and 76 port facilities affected
- Ships at sea lose connection to shore-side systems
- Booking systems, documentation, container tracking all offline

### Days 1-3: June 28-30, 2017

**June 28**
- Emergency response teams assembled across all regions
- Assessment reveals 4,000 servers and 45,000 PCs encrypted
- All domain controllers destroyed except one in Ghana (offline due to power outage)
- Manual operations begun at ports and terminals
- Booking taken via phone and email only
- Crisis communication initiated with customers

**June 29**
- Recovery strategy developed: complete rebuild of IT infrastructure
- Decision made to recreate Active Directory from Ghana domain controller
- Manual documentation for container movements
- Some terminals operating at reduced capacity with paper processes

**June 30**
- IT teams mobilized globally for infrastructure rebuild
- Hardware procurement accelerated
- Network segmentation planning begun

### Days 4-7: July 1-4, 2017

- Gradual restoration of systems by region
- Rebuilt Active Directory infrastructure
- Restored booking systems with reduced functionality
- Container tracking remains partially offline
- Backlog of containers and documentation growing
- Customer communication continues regarding delays

### Days 8-10: July 5-7, 2017

- Most critical systems restored
- Operations returning to normal capacity
- Container tracking systems back online
- Documentation backlog being processed
- Post-incident analysis begun

### Post-Recovery: July-December 2017

- Full financial impact assessed: $200-300 million in Q2/Q3 2017
- Lost revenue from unable-to-ship containers
- IT recovery costs (hardware, software, labor)
- Productivity losses across organization
- Long-term security improvements implemented

## Technical Analysis

### The NotPetya Malware

**Key Characteristics:**

1. **Not Actually Ransomware**
   - Disguised as Petya ransomware variant
   - Actually a wiper with no recovery mechanism
   - Encryption keys not properly stored; decryption impossible
   - Political/destructive motivation rather than financial

2. **Propagation Methods**
   - **Initial vector**: Supply chain compromise (M.E.Doc update)
   - **Lateral movement**:
     - EternalBlue (SMBv1 vulnerability - MS17-010)
     - EternalRomance (SMBv1 vulnerability)
     - Credential harvesting via Mimikatz
     - PSExec for remote execution
     - WMIC (Windows Management Instrumentation Command-line)

3. **Technical Mechanism**
   ```
   Attack Flow:
   1. M.E.Doc update downloads malicious DLL
   2. DLL drops NotPetya payload
   3. Payload harvests credentials from LSASS
   4. Spreads laterally using harvested credentials
   5. Exploits EternalBlue where credentials insufficient
   6. Encrypts Master File Table (MFT) and overwrites MBR
   7. Displays fake ransom note
   8. Renders system unbootable
   ```

4. **Why It Spread So Fast at Maersk**
   - Flat network architecture with limited segmentation
   - Domain administrator credentials cached on many systems
   - EternalBlue vulnerability present despite patch availability
   - High trust model between different business units
   - Interconnected global network topology

### Vulnerability Factors

**Organizational:**
- Global interconnected network without adequate segmentation
- Insufficient network monitoring and anomaly detection
- Delayed patching of critical vulnerabilities (MS17-010 released March 2017)
- Over-reliance on perimeter security
- Inadequate business continuity planning for complete IT failure

**Technical:**
- Unpatched SMBv1 vulnerabilities
- Weak network segmentation between business units
- Privileged credentials cached on multiple systems
- Single Active Directory forest spanning global operations
- Limited offline backups of critical systems

**Supply Chain:**
- Third-party software (M.E.Doc) used without adequate vendor security assessment
- No isolation of systems running third-party software
- Automatic updates enabled without security review

## Impact Assessment

### Operational Impact

**Immediate (Days 0-3):**
- Complete loss of container booking systems
- Loss of container tracking and documentation
- Port terminals operating at 20-50% capacity
- Ships unable to receive loading/unloading instructions
- Manual paper-based processes overwhelming staff
- Global supply chain disruptions for customers

**Short-term (Days 4-30):**
- Gradual restoration of systems
- Massive documentation backlog
- Containers misplaced or delayed
- Customer service overload
- Revenue loss from inability to accept new bookings
- Competitor gains as customers seek alternatives

**Long-term (Months 1-12):**
- Customer confidence impact
- Contractual penalties for delays
- Increased insurance premiums
- Market share loss
- Regulatory scrutiny

### Financial Impact

**Direct Costs:**
- IT recovery: $100-150 million (estimated)
  - 4,000 servers replaced/rebuilt
  - 45,000 PCs reinstalled
  - New hardware procurement
  - Emergency labor costs (24/7 operations)
  - Software licensing

**Revenue Loss:**
- Lost container bookings: $150-200 million (estimated)
- Contractual penalties
- Customer compensation

**Total Impact: $200-350 million** (Maersk officially reported $250-300M)

### Supply Chain Impact

- Disruption to global trade flows
- Delayed deliveries for thousands of customers
- Cascading effects on manufacturing (just-in-time inventory disrupted)
- Agricultural product spoilage (refrigerated containers delayed)
- Retail inventory shortages
- Port congestion at major terminals worldwide

### Reputational Impact

- Initial customer confidence decline
- Questions about cybersecurity preparedness
- Competitive disadvantage vs. unaffected competitors
- Increased scrutiny from regulators and insurers

## Recovery Process

### Emergency Response (Day 0-1)

1. **Containment**
   - Global system shutdown to prevent further spread
   - Network isolation of remaining uninfected systems
   - Disconnection from internet and customer networks

2. **Assessment**
   - Scope determination: ~4,000 servers, 45,000 PCs
   - Critical system inventory
   - Backup assessment (most backups also encrypted)

3. **Communication**
   - Internal stakeholder notification
   - Customer communication plan activated
   - Media response coordination

### Rebuilding Phase (Days 2-10)

1. **Active Directory Restoration**
   - Ghana domain controller (saved by power outage) located
   - Physical transport of hard drives to secure location
   - Rebuild of global AD infrastructure from this copy
   - "Hero moment" - Ghana DC became foundation of recovery

2. **Infrastructure Rebuild**
   - Servers rebuilt from scratch (4,000)
   - Clean OS installations
   - Application reinstallation
   - Data restoration from uncorrupted backups where available
   - Manual data recreation where backups unavailable

3. **Network Redesign**
   - Improved segmentation implemented during rebuild
   - Enhanced monitoring deployed
   - Zero-trust principles introduced

4. **Application Restoration Priority**
   - Container booking systems (highest priority)
   - Terminal operating systems
   - Documentation systems
   - Container tracking
   - Supporting business systems

### Lessons from Recovery

**What Worked:**
- Decisive leadership (CEO personally involved)
- Global coordination of IT teams
- Ghana domain controller providing recovery foundation
- Staff adaptability (manual processes)
- Vendor partnerships (accelerated hardware delivery)

**What Didn't Work:**
- Initial backup strategy (backups encrypted along with production)
- Incident response planning (insufficient for this scale)
- Communication systems (relied on compromised infrastructure)
- Business continuity plans (assumed partial, not total failure)

## Lessons Learned

### Technical Lessons

1. **Network Segmentation is Critical**
   - Flat networks enable rapid lateral movement
   - Business units should be isolated
   - IT/OT convergence requires careful security architecture
   - Micro-segmentation can limit blast radius

2. **Patch Management is Essential**
   - Critical patches must be prioritized (MS17-010 available 3 months prior)
   - Automated patching with testing protocols
   - Legacy system patching strategies needed

3. **Backup Strategy Must Be Resilient**
   - Offline/air-gapped backups essential
   - 3-2-1 rule: 3 copies, 2 media types, 1 offsite
   - Regular backup restoration testing
   - Immutable backups (cannot be encrypted by malware)

4. **Supply Chain Security**
   - Vendor security assessments mandatory
   - Third-party software isolation
   - Update verification mechanisms
   - Software Bill of Materials (SBOM) tracking

5. **Privileged Access Management**
   - Credential caching minimization
   - Privileged account segmentation
   - Just-in-time access models
   - Multi-factor authentication enforcement

### Organizational Lessons

1. **Business Continuity Planning**
   - Plan for complete system failure, not just partial
   - Manual fallback procedures documented and tested
   - Degraded operations plans
   - Regular disaster recovery exercises

2. **Incident Response**
   - Clear chain of command
   - Communication systems independent of primary infrastructure
   - Pre-established vendor relationships for emergency support
   - Regional response capabilities

3. **Cybersecurity Investment**
   - Security cannot be an afterthought
   - Board-level cybersecurity oversight
   - Adequate security staffing and tools
   - Continuous monitoring and threat detection

4. **Supply Chain Resilience**
   - Customers need alternatives during disruptions
   - Industry-wide collaboration on cyber threats
   - Regulatory compliance is minimum, not target

### Maritime-Specific Lessons

1. **IT/OT Convergence Risks**
   - Container tracking connects IT and physical operations
   - Port terminal systems increasingly IT-dependent
   - Vessel connectivity creates attack surface
   - Shipping is critical infrastructure requiring protection

2. **Global Operations Vulnerability**
   - Interconnected global networks amplify risk
   - Single point of compromise can affect worldwide operations
   - Regional isolation capabilities needed
   - Time zone challenges in incident response

3. **Just-in-Time Supply Chain Fragility**
   - Modern shipping enables lean inventory
   - Single-point failures have cascading effects
   - Buffer capacity needed for resilience
   - Multi-supplier strategies for redundancy

## Discussion Questions

### Technical Analysis

1. How could Maersk's network architecture have been designed to limit the spread of NotPetya? What specific segmentation strategies would have been most effective?

2. The EternalBlue vulnerability was patched 3 months before NotPetya. What organizational and technical factors might prevent timely patching in large maritime organizations? How can these be overcome?

3. Analyze the backup strategy failures in this incident. Design a comprehensive backup architecture for a global shipping company that would survive a similar attack.

4. NotPetya used multiple propagation methods (EternalBlue, PsExec, WMIC, credential theft). Which of these should have been preventable with proper configuration? How?

### Operational Considerations

5. Maersk's terminals operated at reduced capacity using manual processes during the outage. What critical functions should maritime organizations maintain manual backup procedures for? How do you balance operational efficiency with resilience?

6. The incident response required rebuilding 4,000 servers in 10 days. Is this timeframe acceptable for a critical infrastructure provider? What alternative approaches could reduce recovery time?

7. How should shipping lines balance the efficiency gains of global IT integration against the security risks demonstrated by this incident?

### Strategic Questions

8. The financial impact was $200-300 million, roughly 1% of annual revenue. How should organizations determine appropriate cybersecurity investment levels? What metrics should guide this decision?

9. NotPetya was attributed to nation-state actors with political motivations, not financial gain. How does this change the threat model for maritime organizations? What different defensive strategies are needed?

10. Maersk's competitors were unaffected and potentially gained market share during the outage. How should this competitive dynamic influence cybersecurity investment and incident response strategies?

### Policy and Governance

11. Should maritime critical infrastructure be subject to mandatory cybersecurity standards? What would effective regulation look like without stifling innovation?

12. The attack originated from compromised Ukrainian tax software. What responsibilities do software vendors have for supply chain security? How can buyers protect themselves?

13. What role should information sharing play in maritime cybersecurity? How can competitors share threat intelligence while maintaining business confidentiality?

### Scenario Planning

14. **Scenario**: You are the CISO of a major shipping line. Your CEO asks, "Could NotPetya happen to us?" How do you assess this? What questions do you ask? What assessments do you perform?

15. **Scenario**: Three hours into a suspected malware outbreak affecting 30% of your network, you must decide: continue containment efforts or shut down the entire global network. What factors influence this decision? What information do you need?

16. **Scenario**: You're the head of port operations during a complete IT failure. Container ships are arriving, but tracking systems are offline. How do you maintain operations? What systems need manual procedures defined in advance?

## Additional Resources

### Official Reports and Analysis

- Maersk Q2 2017 Earnings Report (Financial Impact Disclosure)
- Maersk Q3 2017 Earnings Report (Final Impact Assessment)
- WIRED Magazine: "The Untold Story of NotPetya" (Andy Greenberg)
- US Government Attribution Statement (February 2018)

### Technical References

- Microsoft Security Bulletin MS17-010 (EternalBlue Patch)
- MITRE ATT&CK: NotPetya/Petya Variants
- CISA Alert (TA17-181A): Petya Ransomware
- Cisco Talos NotPetya Technical Analysis

### Academic and Industry Analysis

- "Maritime Cyber Risk Management: An Experimental Ship Assessment" - BIMCO/CLIA/ICS/INTERTANKO/OCIMF/IUMI
- NIST Cybersecurity Framework Application to Maritime
- "The Cyber Dimension of Maritime Security" - Atlantic Council

### Related Case Studies

- 2020 CMA CGM Ransomware Attack
- 2017 Black Sea GPS Spoofing Incident
- 2018 COSCO Ransomware Attack
- 2011-2013 Port of Antwerp Hack

## Instructor Notes

### Key Teaching Points

1. **Scale and Speed**: Emphasize how quickly NotPetya spread (30 minutes) and the scale of impact (4,000 servers). This illustrates why prevention is critical - containment was nearly impossible.

2. **Unintended Consequences**: NotPetya was likely aimed at Ukrainian infrastructure but became a global pandemic. This demonstrates cyber weapons cannot be precisely targeted.

3. **The Ghana Domain Controller Story**: Use this as a case study in how randomness and luck play roles in disaster recovery, but also how preparation (having multiple domain controllers) created the opportunity for luck to help.

4. **IT/OT Convergence**: Maersk's case perfectly illustrates how IT attacks disrupt physical operations in modern maritime industry. Container ships couldn't be loaded/unloaded because IT systems were down.

5. **Supply Chain Ripple Effects**: Discuss how Maersk's customers were impacted, and their customers, showing the interconnectedness of global supply chains.

### Suggested Activities

1. **Red Team / Blue Team Exercise**: Have students role-play Maersk's security team defending against NotPetya-style attack, with another group attempting to breach and spread.

2. **Recovery Planning Workshop**: Groups design a disaster recovery plan for a shipping company that would survive NotPetya. Present and critique each plan.

3. **Cost-Benefit Analysis**: Calculate ROI of various cybersecurity investments (patching, segmentation, backups) based on NotPetya impact.

4. **Tabletop Exercise**: Simulate first 4 hours of NotPetya incident with students in different roles (CISO, CEO, Port Operations, IT, Communications).

### Assessment Ideas

- Technical report: Network architecture design preventing NotPetya spread
- Policy brief: Recommendations for maritime cybersecurity regulation
- Incident response plan: First 24 hours of similar attack
- Risk assessment: Evaluate organization's NotPetya readiness

### Time Allocation Suggestions

- **Lecture/Overview**: 45-60 minutes
- **Technical Deep Dive**: 30-45 minutes
- **Group Discussion**: 30 minutes
- **Hands-on Activity**: 60-90 minutes
- **Total**: 3-4 hours for comprehensive coverage

---

*This case study is designed for educational purposes in maritime cybersecurity curriculum. Information is compiled from public sources, industry reports, and security research publications.*

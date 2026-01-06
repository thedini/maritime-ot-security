---
title: "Black Sea GPS Spoofing Incident (2017)"
date: "June 22, 2017"
category: "GPS Spoofing / Navigation Warfare"
severity: "High"
affected_vessels: "20+"
location: "Black Sea, near Novorossiysk Port, Russia"
attack_vector: "GPS signal manipulation"
attributed_to: "Unknown (suspected state actor)"
learning_objectives:
  - Understand GPS spoofing techniques and vulnerabilities
  - Analyze impacts on maritime navigation safety
  - Evaluate detection methods for GNSS interference
  - Assess the convergence of cybersecurity and navigation systems
---

# Black Sea GPS Spoofing Incident (2017)

## Executive Summary

On June 22, 2017, approximately 20 vessels in the Black Sea near Russia's Novorossiysk Port reported GPS navigation anomalies indicating their positions were incorrectly displayed as being at an inland airport approximately 25 miles away. This incident, analyzed by researchers at the University of Texas at Austin's Radionavigation Laboratory, represented one of the first publicly documented cases of large-scale GPS spoofing affecting civilian maritime navigation.

Unlike GPS jamming (which simply blocks signals), this was GPS spoofing - the transmission of false GPS signals that caused receivers to calculate incorrect positions. The incident raised serious concerns about the vulnerability of maritime navigation systems to electronic warfare techniques and the potential for catastrophic navigation errors in congested or dangerous waters.

## Background

### Global Navigation Satellite Systems (GNSS)

**GPS Fundamentals:**
- GPS satellites broadcast timing signals from known positions
- Receivers calculate position by measuring time delay from 4+ satellites
- Accuracy: typically 5-10 meters for civilian signals
- No authentication or encryption on civilian GPS signals
- System designed in 1970s without adversarial threat model

**Maritime Dependence on GPS:**
- Primary navigation method for modern vessels
- Integrated with:
  - Electronic Chart Display and Information System (ECDIS)
  - Automatic Identification System (AIS)
  - Dynamic Positioning Systems (DP)
  - Collision avoidance systems
  - Automated docking systems
- Backup systems (gyrocompass, radar) often neglected in modern shipping
- Port operations increasingly automated using GPS timing

### GPS Vulnerabilities

**Jamming:**
- Transmission of noise on GPS frequencies
- Prevents receiver from acquiring satellite signals
- Obvious to operators (loss of signal)
- Requires minimal technical sophistication
- Readily available commercial jammers

**Spoofing:**
- Transmission of false GPS signals
- Causes receiver to calculate incorrect position/time
- Can be subtle and undetected
- Requires sophisticated equipment and knowledge
- Can be tailored to specific targets or effects

**Meaconing:**
- Rebroadcast of genuine GPS signals with delay
- Creates false position offset
- Simpler than full spoofing but less controllable

### Black Sea Geopolitical Context

**Strategic Importance:**
- Critical shipping route connecting Mediterranean and inland ports
- Major Russian naval presence (Black Sea Fleet)
- Novorossiysk: Russia's largest Black Sea port
- Recent conflicts: 2014 Crimean annexation, ongoing Ukraine tensions
- High military activity and electronic warfare capabilities deployed

**Known GPS Interference:**
- Multiple reports of GPS issues in Black Sea region (2016-2017)
- Suspected Russian electronic warfare systems (e.g., Krasukha, RB-341V "Leer-3")
- Both jamming and spoofing incidents reported
- Patterns suggesting territorial defense or test operations

## Timeline of Events

### June 22, 2017

**~Unknown Time (Approximate Morning/Afternoon)**
- Multiple vessels in Black Sea near Novorossiysk Port experience GPS anomalies
- Ship navigation systems indicate positions at Gelendzhik Airport
- Airport location: 37°24'50"N 38°00'48"E (approximately 25 nautical miles inland)
- At least 20 vessels affected simultaneously
- Vessels' actual positions: offshore in Black Sea

**Initial Observations:**
- GPS receivers showing "good" satellite lock (strong signals, normal indicators)
- No obvious signs of malfunction to operators
- Position displayed at impossible inland location
- Cross-checking with other navigation methods revealed discrepancy
- AIS broadcasts showing false positions to other vessels
- Time synchronization also affected (slight offset)

**Vessel Responses:**
- Navigation officers noticed impossible positions (ships "on land")
- Consultation with other vessels revealed widespread issue
- Reversion to traditional navigation methods (radar, visual, compass)
- Reports filed with maritime authorities
- Incidents logged in ships' records

### June 22-30, 2017

- Additional reports collected from vessels transiting the area
- Maritime safety bulletins issued warning of GPS unreliability
- Mariners advised to use backup navigation systems
- Data collection from affected vessels' GPS logs

### Late June - July 2017

**University of Texas Analysis:**
- Dr. Todd Humphreys and team at UT Austin Radionavigation Laboratory began investigation
- Analysis of GPS data logs from affected vessels
- Consultation with maritime industry sources
- Technical characterization of the spoofing signals

### August 2017

**Public Disclosure:**
- UT Austin researchers published initial findings
- Media coverage (New Scientist, MIT Technology Review)
- Industry awareness increased
- IMO (International Maritime Organization) notified

### Post-Incident (2017-Present)

- Continued GPS anomalies reported in Black Sea region
- Expanded documentation of GPS interference globally
- Development of spoofing detection capabilities
- Regulatory discussions on navigation system resilience

## Technical Analysis

### The Spoofing Attack

**Observed Characteristics:**

1. **False Position Injection**
   - All affected vessels reported positions at Gelendzhik Airport
   - Coordinates: approximately 37.41°N, 38.01°E
   - Actual vessel positions: various locations in Black Sea offshore
   - Position offset: ~25 nautical miles northeastward
   - Altitude: airport elevation (~100 meters) vs. sea level

2. **Signal Characteristics**
   - GPS receivers showed normal signal strength
   - Satellite geometry appeared normal
   - No alarms or fault indicators
   - Lock indicators showed "good" status
   - Multiple satellite vehicles (SVs) spoofed simultaneously

3. **Timing Anomalies**
   - GPS time showed slight offset from true UTC
   - Timing error: estimated several microseconds
   - Implications for systems dependent on GPS timing (port operations, network synchronization)

**Spoofing Methodology:**

The UT Austin analysis concluded this was **simplistic spoofing**:

```
Attack Vector:
1. Spoofer transmits false GPS signals
2. Signals overpowered legitimate satellite signals (near-field vs. far-field)
3. GPS receivers locked onto stronger false signals
4. Receivers calculated position based on false timing data
5. Position calculation yielded Gelendzhik Airport coordinates
6. No receiver authentication mechanism to detect falsification
```

**Characteristics suggesting relatively unsophisticated attack:**
- All vessels spoofed to same location (no target-specific tailoring)
- Obvious false position (airport vs. sea)
- No attempt to create believable maritime position
- Time offset detectable with proper monitoring
- Likely "spillover" from intended target (airport or military facilities?)

**More sophisticated spoofing would include:**
- Gradual position drift (harder to detect)
- Individualized false positions for each target
- Matched velocity vectors (movement consistency)
- Correct altitude for maritime operations
- Synchronized timing without offset

### Why Vessels Were Vulnerable

**Technical Factors:**

1. **No GPS Signal Authentication**
   - Civilian GPS signals are unauthenticated
   - Receivers accept strongest signal as genuine
   - No cryptographic verification
   - Military GPS (P(Y) code) has encryption, but not available to civilians

2. **Receiver Design Limitations**
   - Designed for benign interference environment
   - Optimize for signal acquisition and tracking
   - No anti-spoofing capabilities in commercial receivers
   - Trust GPS signal integrity implicitly

3. **Inadequate Sensor Fusion**
   - Modern vessels rely heavily on GPS
   - Backup systems (gyro, radar) not always monitored actively
   - Insufficient cross-checking between navigation sources
   - Alarms not triggered by implausible positions

4. **System Integration**
   - GPS feeds ECDIS, AIS, autopilot, dynamic positioning
   - False GPS propagates through multiple systems
   - Cascading effects across vessel operations
   - Difficult to override once locked on false signal

**Operational Factors:**

1. **Over-reliance on GPS**
   - Traditional navigation skills declining
   - Backup systems viewed as legacy/redundant
   - Economic pressure reduces redundant systems
   - Training emphasizes electronic navigation

2. **Lack of Awareness**
   - GPS spoofing relatively unknown in maritime industry (2017)
   - Mariners unprepared to recognize or respond
   - No standard operating procedures for GPS anomalies
   - Limited understanding of GPS vulnerabilities

3. **Inadequate Monitoring**
   - Position plausibility checks not routine
   - Cross-referencing with radar/visual infrequent
   - Alarm thresholds set for mechanical failures, not spoofing

### Detection Methods

**Indicators observed in Black Sea incident:**

1. **Impossible Position**
   - GPS showing vessel on land
   - Obvious to attentive navigator
   - Requires situational awareness and chart monitoring

2. **Cross-checking with Other Systems**
   - Gyrocompass direction vs. GPS course
   - Radar returns inconsistent with GPS position
   - Visual navigation marks don't match GPS location
   - Dead reckoning position significantly different

3. **Time Consistency Checks**
   - GPS time vs. other time sources (NTP, radio time signals)
   - Microsecond offsets detectable with precise timing equipment
   - Port synchronization systems may detect discrepancies

4. **Signal Analysis**
   - Abnormal signal strength (if monitoring equipment available)
   - Multiple satellites from impossible geometries
   - Doppler shift anomalies
   - Requires specialized monitoring equipment

**Advanced Detection Methods (not available to most vessels in 2017):**

- **Receiver Autonomous Integrity Monitoring (RAIM)**: Checks consistency across multiple satellites
- **Multi-antenna systems**: Detect spatially inconsistent signals
- **Inertial Navigation System (INS) integration**: Cross-check GPS with inertial measurements
- **GNSS authentication**: Cryptographic verification (not available for civilian GPS)
- **Signal direction finding**: Detect terrestrial signal source
- **Timing cross-checks**: Compare GPS time with independent atomic clocks

## Impact Assessment

### Immediate Navigational Safety Risks

**Collision Hazards:**
- Vessels operating on false position information
- AIS broadcasts showing incorrect positions to other ships
- Collision avoidance systems using bad data
- Traffic separation scheme navigation compromised
- Near-miss potential in high-traffic areas

**Grounding Risks:**
- False position could indicate safe water when vessel is near hazards
- Automatic route following could lead to danger
- Harbor approaches particularly vulnerable
- Dynamic positioning failures (offshore platforms, narrow channels)

**Specific Risks in Black Sea Context:**
- High vessel traffic density
- Complex coastal navigation
- Restricted waters and traffic separation schemes
- Political tensions increasing collision risks
- Potential for maritime incidents with international implications

### Operational Impacts

**Documented Effects (June 2017):**
- Navigation uncertainty requiring manual pilotage
- Reduced vessel speeds for safety
- Increased bridge manning and vigilance
- Delays in port approaches
- Additional fuel consumption (slower speeds, route deviations)

**Potential Cascading Effects:**
- Port operations disrupted (GPS timing used for automation)
- Search and rescue complications (false distress positions)
- Cargo delays
- Insurance implications (operating in compromised navigation environment)

### Strategic and Security Implications

**Anti-Access/Area Denial (A2/AD):**
- GPS spoofing as tool for territorial control
- Creates navigation uncertainty deterring vessel operations
- Plausibly deniable (no kinetic action)
- Asymmetric capability (low-cost defensive tool)
- Part of broader electronic warfare capabilities

**Escalation Risks:**
- Navigation errors could trigger international incidents
- False AIS data could be used for deceptive operations
- Attribution challenges complicate diplomatic responses
- Potential for spoofing to mask kinetic attacks

**Critical Infrastructure Vulnerability:**
- Ports dependent on GPS timing for automation
- Power grids use GPS for timing synchronization
- Financial systems rely on GPS timestamps
- Maritime GPS spoofing demonstrates broader vulnerability

### Economic Impacts

**Direct Costs:**
- Individual incident costs relatively low (delays, fuel)
- Insurance rate increases in affected regions
- Investment in backup navigation systems
- Training costs for navigation without GPS

**Indirect Costs:**
- Reduced confidence in maritime automation
- Delays in autonomous vessel development
- Potential for regional trade disruptions if spoofing widespread
- Strategic costs of vulnerable navigation infrastructure

### Broader GNSS Vulnerability

The Black Sea incident highlighted that GPS is vulnerable globally:
- Over 20,000 vessels worldwide rely primarily on GPS
- Port infrastructure increasingly GPS-dependent
- Aviation, rail, power, finance also vulnerable
- Single point of failure in critical infrastructure

## Attribution and Geopolitical Context

### Evidence and Theories

**Evidence Suggesting Russian Origin:**

1. **Geographic Proximity**
   - Incident near Russian port and military facilities
   - Known Russian electronic warfare deployments in region
   - Pattern of GPS interference near Russian strategic sites

2. **Technical Capabilities**
   - Russia acknowledged electronic warfare capabilities
   - Systems like Krasukha-4 (jamming) and GNSS spoofing platforms
   - Military doctrine includes radioelectronic combat

3. **Pattern of Incidents**
   - Multiple GPS anomalies near Russian borders (2016-2018)
   - Similar incidents in Syria, Arctic, Norway, Finland
   - Correlation with geopolitical tensions

4. **Strategic Logic**
   - Protection of critical infrastructure (port, naval base)
   - Deterrence and A2/AD strategy
   - Testing and capability demonstration

**Alternative Theories:**

1. **Unintentional Spillover**
   - Spoofing intended for airport/military target
   - Civilian vessels affected as collateral
   - Possible protection of VIP travel or military operations

2. **Testing/Training**
   - Military electronic warfare exercises
   - Capability testing without intent to disrupt shipping
   - Lack of coordination with maritime authorities

3. **Non-State Actor**
   - Sophisticated criminal or hacker group
   - Academic/research demonstration
   - Generally considered unlikely due to required resources

**Attribution Challenges:**

- No direct evidence of perpetrator
- Russia has not acknowledged responsibility
- Spoofing equipment could theoretically be deployed by others
- Plausible deniability inherent in electronic warfare
- International law and norms unclear for GPS spoofing

### Official Responses

**International Maritime Organization (IMO):**
- Increased awareness of GPS vulnerabilities
- Guidance on navigation system resilience
- Encouragement of backup systems
- No formal attribution or sanctions

**National Governments:**
- US acknowledged vulnerability and concern
- Enhanced GNSS resilience research programs
- Maritime safety bulletins issued
- Limited public diplomatic response

**Industry Response:**
- Increased awareness in maritime community
- Development of spoofing detection technologies
- Training updates for navigation officers
- Renewed emphasis on backup navigation systems

## Defensive Measures and Mitigation

### Immediate Operational Responses

**Navigation Best Practices:**

1. **Continuous Cross-checking**
   - Compare GPS with gyrocompass, radar, visual bearings
   - Maintain manual position plotting
   - Regular position sanity checks (am I where GPS says?)
   - Monitor multiple navigation sources simultaneously

2. **Backup System Utilization**
   - Maintain operational gyrocompass
   - Use radar for position fixing
   - Visual navigation in coastal waters
   - Dead reckoning cross-checks
   - Maintain traditional navigation skills

3. **Anomaly Recognition**
   - Train crew to recognize GPS anomalies
   - Position plausibility checks
   - Velocity/acceleration consistency checks
   - Time consistency monitoring
   - Suspicious signal characteristics

4. **Response Procedures**
   - Switch to backup navigation immediately
   - Report anomalies to authorities
   - Increase bridge vigilance
   - Reduce speed if necessary for safe navigation
   - Avoid reliance on automated systems during anomalies

### Technical Countermeasures

**Short-term Solutions:**

1. **Enhanced Monitoring**
   - GPS signal quality monitoring equipment
   - Multi-GNSS receivers (GPS, GLONASS, Galileo, BeiDou)
   - Comparison across GNSS systems
   - Signal strength and satellite geometry monitoring

2. **Sensor Fusion**
   - Integration of GPS with INS (Inertial Navigation Systems)
   - Kalman filtering for multi-sensor integration
   - Cross-validation between independent systems
   - Automated anomaly detection algorithms

3. **Position Verification**
   - Automatic plausibility checks (land vs. water)
   - Velocity/acceleration bounds checking
   - Route consistency verification
   - Database of known interference zones

**Long-term Solutions:**

1. **GNSS Authentication**
   - **Galileo OSNMA (Open Service Navigation Message Authentication)**: Provides cryptographic authentication for civilian signals (operational 2023+)
   - GPS is developing similar capabilities for civilian use
   - Prevents spoofing by verifying signal authenticity
   - Requires receiver upgrades

2. **Multi-Antenna Systems**
   - Multiple GPS antennas on vessel
   - Detect spatially inconsistent signals
   - Direction finding for signal source
   - Commercial systems becoming available

3. **Alternative PNT (Positioning, Navigation, Timing)**
   - **eLoran**: Enhanced Long-Range Navigation (terrestrial radio-navigation)
   - **R-Mode**: Ranging Mode using existing marine beacons
   - **STL (Satellite Time and Location)**: LEO satellite constellations
   - **Inertial systems**: High-grade INS with GPS independence
   - **5G/Terrestrial networks**: Positioning using cellular signals

4. **Receiver-Level Countermeasures**
   - Anti-spoofing algorithms in receivers
   - Signal direction discrimination
   - Power-level anomaly detection
   - Consistency checking across measurements

### Regulatory and Policy Measures

**IMO Actions:**

1. **Resolution MSC.401(95) - ECDIS Performance Standards**
   - Requirements for position sensor backup
   - Integrity monitoring recommendations
   - Alarm requirements for position inconsistencies

2. **SN.1/Circ.344 - GNSS Vulnerability Guidance**
   - Awareness of jamming and spoofing
   - Recommendations for mariners
   - Backup system utilization

3. **Ongoing Work:**
   - Enhanced navigation system standards
   - Resilient PNT requirements
   - Cybersecurity integration with navigation systems

**National Initiatives:**

**United States:**
- **DHS Maritime Security Directive**: Awareness and preparedness
- **DOT PNT Backup Studies**: Evaluating eLoran, R-Mode, other alternatives
- **DOD GPS Modernization**: L1C signal with authentication capability

**European Union:**
- **Galileo OSNMA Deployment**: Authentication service operational
- **E-LORAN Evaluation**: Some member states studying terrestrial backup
- **EU Maritime Cybersecurity Directive**: Including navigation resilience

**Industry Standards:**
- BIMCO/IMO cybersecurity guidelines incorporating GNSS resilience
- Classification society rules for navigation system redundancy
- Port state control potentially including GNSS integrity checks

## Lessons Learned

### Technical Lessons

1. **GPS Is Vulnerable and Not Trustworthy Alone**
   - Civilian GPS signals are unauthenticated and easily spoofed
   - Receivers cannot distinguish genuine from false signals
   - Single-source navigation is inadequate for safety-critical operations
   - Over-reliance on GPS has created systemic vulnerability

2. **Detection Requires Multi-Source Verification**
   - Cross-checking between independent systems is essential
   - Automated consistency checks can identify anomalies
   - Diversity of sensors provides resilience
   - Operator awareness and training crucial for anomaly recognition

3. **Spoofing is More Dangerous Than Jamming**
   - Jamming is obvious (loss of signal); spoofing is subtle
   - False information can lead to unsafe actions; no information leads to caution
   - Sophisticated spoofing may be undetectable without specialized equipment
   - Threat model must include intelligent adversaries, not just noise

4. **Navigation Systems Require Defense-in-Depth**
   - No single countermeasure is sufficient
   - Layered defenses: detection, verification, backup systems, procedures
   - Resilience requires technical, operational, and organizational measures
   - Redundancy and diversity are key principles

### Operational Lessons

5. **Traditional Navigation Skills Remain Essential**
   - Electronic systems can fail or be compromised
   - Manual navigation provides critical backup
   - Training must maintain proficiency in non-GPS navigation
   - "Lost art" of navigation needs preservation

6. **Procedures Must Account for GPS Failure**
   - Transition to backup navigation must be practiced
   - Decision-making under uncertainty requires preparation
   - Bridge resource management includes anomaly response
   - Reporting mechanisms for GPS issues needed

7. **Automation Requires Monitoring**
   - Automated systems depend on sensor integrity
   - "Trust but verify" principle for navigation automation
   - Human oversight remains critical safety layer
   - Automation complacency is a significant risk

### Strategic Lessons

8. **GPS Is Critical Infrastructure with Systemic Risk**
   - Single point of failure across multiple sectors
   - Maritime, aviation, power, finance, communications all affected
   - National and economic security implications
   - Resilience investments needed at infrastructure level

9. **Electronic Warfare Is a Maritime Threat**
   - Cyber and electromagnetic spectrum operations are converging
   - Non-kinetic attacks can disrupt maritime operations
   - A2/AD strategies employ GNSS interference
   - Maritime security must include EW preparedness

10. **Attribution and Response Are Challenging**
    - Difficulty determining attacker complicates response
    - Plausible deniability enables aggression below conflict threshold
    - International law and norms for GNSS interference unclear
    - Deterrence requires detection and attribution capabilities

### Policy and Governance Lessons

11. **International Cooperation Required**
    - GPS spoofing is a transnational threat
    - Information sharing between nations and industry essential
    - Coordinated response and standards needed
    - IMO and other international bodies play key role

12. **Regulation Must Balance Safety and Innovation**
    - Requirements for resilience may increase costs
    - Prescriptive standards may limit technology advancement
    - Performance-based standards allow flexibility
    - Regulatory lag behind threats requires agility

13. **Public-Private Partnership Needed**
    - Government provides GNSS infrastructure
    - Private sector operates vulnerable systems
    - Shared responsibility for resilience
    - Information exchange mechanisms needed

## Discussion Questions

### Technical Understanding

1. Explain the difference between GPS jamming and GPS spoofing. Why is spoofing generally considered more dangerous for maritime navigation?

2. The Black Sea spoofing was described as "unsophisticated" because all vessels were spoofed to the same location. Design a more sophisticated spoofing attack that would be harder to detect. What would make it more dangerous?

3. How could a vessel's GPS receiver be modified or augmented to detect spoofing? What additional sensors, algorithms, or data sources would help?

4. What are the advantages and disadvantages of using multiple GNSS constellations (GPS, GLONASS, Galileo, BeiDou) for spoofing resistance?

### Operational Analysis

5. You are the officer on watch when you notice your GPS position shows the vessel is 2 nautical miles inland. Walk through your immediate actions and decision-making process. What systems do you check? What course of action do you take?

6. Evaluate the trade-off between navigation efficiency (automation, optimal routing, just-in-time port arrival) and resilience (backup systems, manual navigation, redundancy). Where should the balance be?

7. How should training for bridge officers change to account for GPS spoofing threats? What skills and knowledge are most important?

### Strategic Considerations

8. Analyze the Black Sea incident from a geopolitical perspective. If Russia was responsible, what were the likely objectives? Was this effective strategy?

9. GPS is provided free to the world by the US government. What are the strategic implications of global dependence on US-controlled infrastructure? Should other nations develop independent PNT systems?

10. How should the international community respond to GPS spoofing incidents? What mechanisms exist for attribution, accountability, and deterrence?

### Risk Assessment

11. **Scenario**: You are conducting a risk assessment for a shipping company. How do you evaluate the risk of GPS spoofing? What factors determine risk level (geography, vessel type, operations, etc.)? What risk mitigation strategies do you recommend?

12. Compare the cyber risk of GPS spoofing with other maritime cyber threats (malware, hacking of ship systems, ransomware). How should resources be allocated across different threat categories?

13. What are the potential cascading effects if GPS spoofing became widespread in a major shipping route (e.g., Strait of Malacca, Suez Canal)? How would global supply chains be affected?

### Technical Mitigation

14. **Design Challenge**: Design a backup Position, Navigation, and Timing (PNT) system for vessels that is independent of GNSS. What technologies would you use? What are the trade-offs in cost, accuracy, and complexity?

15. Evaluate the following countermeasures for cost-effectiveness: (a) multi-antenna GPS systems, (b) GPS/INS integration, (c) eLoran receivers, (d) operator training, (e) multiple GNSS constellations. Which provide the best return on investment?

16. Galileo's OSNMA provides authentication for civilian GNSS signals. Research this technology and explain how it prevents spoofing. What are the limitations? Why isn't GPS offering equivalent capability?

### Policy and Regulation

17. Should GPS spoofing be considered an act of aggression under international law? What about if it causes a maritime incident with casualties? How does this compare to kinetic attacks?

18. Develop a proposed set of international regulations for maritime GNSS resilience. What requirements would you mandate? How would they be enforced? What are the implementation challenges?

19. Who should bear the cost of GNSS resilience - vessel operators, governments, technology providers? Justify your answer from economic and policy perspectives.

### Future Scenarios

20. **Scenario**: It is 2030, and GPS spoofing has become common in contested waters. How has the maritime industry adapted? What technologies and procedures are standard? What has changed about navigation?

21. **Scenario**: A GPS spoofing incident in a major port results in a collision with significant casualties and environmental damage. As the port authority director, what is your response? What changes do you implement?

22. **Tabletop Exercise**: Your vessel is transiting the Taiwan Strait when GPS systems begin showing erratic positions. You suspect spoofing. Various systems (autopilot, ECDIS, AIS) are affected. Conduct a tabletop exercise simulating the bridge team's response over the first 2 hours of the incident.

## Additional Resources

### Primary Sources and Technical Reports

- **University of Texas at Austin Radionavigation Laboratory**: "GPS Lie Detectors" research and publications (Dr. Todd Humphreys)
- **US Department of Homeland Security**: "2017 Federal Radionavigation Plan"
- **C4ADS Report**: "Above Us Only Stars" - Unauthorized use of GPS signal interference and spoofing

### Academic Research

- Humphreys, T. E., et al., "The GPS Assimilation Attack" - Journal of GPS Solutions
- Psiaki, M. L. and Humphreys, T. E., "GNSS Spoofing and Detection" - Proceedings of IEEE
- Shepard, D. P., et al., "Evaluation of Smart Grid and Civilian UAV Vulnerability to GPS Spoofing Attacks"

### Standards and Guidance

- **IMO Resolution MSC.401(95)**: Performance Standards for Multi-System Shipborne Radionavigation Receivers
- **IMO SN.1/Circ.344**: Promulgation of Maritime Safety Information on the Unavailability of GNSS
- **IEC 61108 Series**: Maritime navigation and radiocommunication equipment and systems

### News and Analysis

- "Twenty Ships in Black Sea Placed at Inland Airport" - *New Scientist* (August 2017)
- "GPS Spoofing in the Black Sea Sends Ships' Systems Haywire" - *MIT Technology Review*
- "Suspected Russian Spoofing of GPS Signals Spreads" - *Wired*

### Industry Reports

- **BIMCO Maritime Cyber Security Resources**: Including GPS resilience guidance
- **Royal Institute of Navigation**: Publications on PNT resilience
- **USCG Navigation Center**: GPS Problem Reporting database and analysis

### Technical References

- **GPS.gov**: Official US Government GPS information
- **European GNSS Agency**: Galileo and EGNOS information including OSNMA
- **International Committee on GNSS (ICG)**: Information on all GNSS systems worldwide

### Related Incidents

- **Norwegian GPS Disruption (2018)**: Jamming during NATO exercises attributed to Russia
- **Finnish GPS Disruption (2018-2019)**: Interference in Lapland region
- **Port of Shanghai GPS Anomalies (2019)**: Suspected spoofing near major Chinese port
- **Dover Strait Incidents (2020)**: Multiple GPS anomaly reports

### Emerging Technologies

- **Galileo OSNMA**: Authentication service for civilian users
- **LEO-PNT**: Low Earth Orbit satellite positioning systems (e.g., Iridium STL, Xona Space)
- **R-Mode**: Ranging mode using terrestrial maritime beacons
- **Quantum Timing**: Chip-scale atomic clocks for precise timing without GNSS

## Instructor Notes

### Key Teaching Points

1. **Invisible Threat**: Unlike jamming, spoofing can be completely undetectable without proper monitoring. Emphasize the danger of invisible threats that cause incorrect actions rather than inaction.

2. **Systemic Vulnerability**: GPS spoofing demonstrates how dependence on a single system creates systemic risk. Use this to discuss critical infrastructure protection and single points of failure.

3. **Cyber-Physical Convergence**: This incident shows how cyber attacks (false data injection) directly affect physical safety (navigation). Important for understanding modern maritime cyber threats.

4. **Attribution Difficulty**: Use the uncertain attribution to discuss challenges in responding to cyber and electronic attacks. Plausible deniability enables aggression below traditional conflict thresholds.

5. **Operational Reality**: Many mariners in 2017 were unaware GPS could be spoofed. Discuss the gap between theoretical vulnerabilities and operational awareness.

### Suggested Activities

1. **GPS Spoofing Simulation**:
   - Use maritime simulator to inject GPS errors
   - Have students navigate while GPS shows false position
   - Debrief on detection methods and response

2. **Detection Algorithm Development**:
   - Provide multi-sensor data from a vessel (GPS, gyro, radar, AIS)
   - Have students develop algorithm to detect spoofing
   - Compare approaches and effectiveness

3. **System Design Exercise**:
   - Groups design resilient PNT architecture for new vessel class
   - Present designs and critique trade-offs
   - Cost-benefit analysis of different approaches

4. **Policy Debate**:
   - Assign roles: shipping company, regulator, GPS provider, nation-state
   - Debate responsibility for GNSS resilience and who pays for solutions
   - Develop consensus recommendations

5. **Geopolitical Analysis**:
   - Map GPS interference incidents globally (2016-present)
   - Analyze patterns and correlate with geopolitical events
   - Discuss strategic use of electronic warfare

### Demonstration Ideas

**If resources available:**

- **Live GPS Spoofing** (controlled environment): Demonstrate how easily GPS receivers can be fooled using USRP software-defined radio (NOTE: requires proper authorization and RF shielding)
- **Multi-GNSS Monitoring**: Show real-time GPS/GLONASS/Galileo/BeiDou signals and demonstrate how monitoring multiple systems provides resilience
- **OSNMA Authentication**: Demonstrate Galileo authentication on compatible receivers

### Assessment Ideas

- **Technical Report**: Design a GPS spoofing detection system for a specific vessel type
- **Incident Response Plan**: Develop procedures for bridge team when spoofing suspected
- **Risk Analysis**: Evaluate GPS spoofing risk for shipping routes and propose mitigation
- **Policy Brief**: Recommend national-level policies for maritime GNSS resilience
- **Capstone Project**: Integrate GPS spoofing detection with anomaly detection system (connects to vessel LSTM project)

### Connections to Broader Curriculum

**Integration with Other Topics:**

- **CAN Bus Security**: Both involve false data injection into trusted systems
- **Network Segmentation**: Principles of defense-in-depth apply to navigation systems
- **Anomaly Detection**: GPS spoofing detection uses similar concepts to LSTM anomaly detection
- **Incident Response**: Navigation anomalies require similar response frameworks
- **Risk Assessment**: Evaluating GPS spoofing risk uses same methodologies as cyber risk

**Capstone Project Integration:**

The GPS spoofing case study can connect to the vessel LSTM anomaly detection project:
- GPS data can be input to LSTM model
- Anomalous position changes could be detected
- Sensor fusion with other navigation systems
- Real-world application of ML to safety-critical systems

### Time Allocation Suggestions

- **Lecture/Overview**: 45 minutes
- **Technical Deep Dive**: 45 minutes (GPS fundamentals, spoofing techniques)
- **Geopolitical Context**: 30 minutes
- **Mitigation Strategies**: 30 minutes
- **Hands-on Activity**: 60-90 minutes
- **Discussion/Debrief**: 30 minutes
- **Total**: 3.5-4.5 hours for comprehensive coverage

### Prerequisites

Students should have basic understanding of:
- GPS/GNSS fundamentals
- Maritime navigation basics
- Signal processing concepts (helpful but not required)
- Cyber-physical systems

### Advanced Topics for Deep Dives

- Signal processing: How GPS receivers work at RF level
- Cryptography: Authentication mechanisms like OSNMA
- Kalman filtering: Sensor fusion algorithms
- International law: Law of the sea and peacetime electronic warfare
- Game theory: Deterrence and escalation dynamics

---

*This case study is designed for educational purposes in maritime cybersecurity curriculum. Information is compiled from public sources, academic research, and security publications. GPS spoofing demonstrations require proper authorization and should only be conducted in controlled, shielded environments.*

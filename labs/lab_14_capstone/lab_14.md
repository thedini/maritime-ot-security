---
title: "Lab 14"
subtitle: "Capstone - Red Team / Blue Team Exercise"
author: "Constantine Macris"
date: "2026"
titlepage: true
titlepage-color: "1E3A5F"
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "FFFFFF"
titlepage-rule-height: 2
book: true
classoption: oneside
code-block-font-size: \scriptsize
description: |
    Final capstone exercise with red team attacks and blue team defense
---

# Lab 14 -- Capstone: Red Team / Blue Team Exercise

## Lab Overview

**Duration**: 3 hours
**Prerequisites**: All labs completed
**Materials Required**:
- Complete ensemble IDS from Lab 13
- All attack tools from Labs 06-08
- Test network access
- Team assignments

## Exercise Structure

| Phase | Duration | Activity |
|-------|----------|----------|
| 1 | 30 min | Team setup and planning |
| 2 | 45 min | Red team attacks / Blue team defends |
| 3 | 15 min | Role swap preparation |
| 4 | 45 min | Second round (swapped) |
| 5 | 30 min | Analysis and debrief |
| 6 | 15 min | Presentation preparation |

## Team Assignments

Teams will be assigned by instructor. Each team operates as both attacker and defender.

**Team A**: _________________ (Start as Red Team)
**Team B**: _________________ (Start as Blue Team)

## Phase 1: Planning (30 minutes)

### Red Team Planning

As Red Team, plan attacks to evade detection:

1. **Review detection methods available to Blue Team:**
   - Frequency monitoring
   - Entropy analysis
   - ML anomaly detection
   - Device fingerprinting

2. **Select attack strategies:**

| Attack | Evasion Technique | Expected Detection |
|--------|-------------------|-------------------|
| Position spoof | Rate-matched | Fingerprint only |
| DoS | Low-rate (50%) | May evade frequency |
| Replay | Old data injection | Entropy/ML |
| Engine alarm | Normal values | None (value spoof) |

3. **Create attack timeline:**

```
00:00 - 05:00: Reconnaissance
05:00 - 15:00: Position spoofing (gradual drift)
15:00 - 25:00: Engine data manipulation
25:00 - 35:00: DoS attempt
35:00 - 45:00: Combined attack
```

### Blue Team Planning

As Blue Team, prepare defense:

1. **Configure ensemble IDS:**
   - Set appropriate thresholds
   - Enable all detection methods
   - Configure logging

2. **Establish monitoring procedures:**
   - Dashboard refresh rate
   - Alert escalation process
   - Manual verification steps

3. **Document baseline:**
   - Normal message rates
   - Active devices
   - Expected values

## Phase 2: First Attack Round (45 minutes)

### Red Team Execution

Execute your attack plan. Document each action:

```markdown
# Red Team Attack Log

| Time | Attack | Parameters | Observed Effect |
|------|--------|------------|-----------------|
| 00:00 | Started recon | monitor mode | |
| 05:00 | Position drift | +0.01° lat/min | |
| | | | |
```

### Blue Team Defense

Monitor and respond to attacks. Document observations:

```markdown
# Blue Team Defense Log

| Time | Alert | Detector | Action Taken | Confirmed? |
|------|-------|----------|--------------|------------|
| 05:32 | Position anomaly | Freq | Verified GPS | False alarm |
| 08:15 | Fingerprint mismatch | FP | Investigated | TRUE ATTACK |
| | | | | |
```

### Scoring System

| Event | Red Team Points | Blue Team Points |
|-------|-----------------|------------------|
| Attack executed undetected (5 min) | +10 | |
| Attack detected within 30 sec | | +10 |
| Attack detected within 2 min | | +5 |
| False alarm triggered | +5 | -5 |
| Correct attack identification | | +5 |

## Phase 3: Role Swap (15 minutes)

- Red team becomes Blue team
- Blue team becomes Red team
- Exchange any learned insights
- Adjust strategies based on first round

## Phase 4: Second Attack Round (45 minutes)

Repeat with swapped roles.

### Attack Scenarios (Suggestions for Red Team)

**Scenario A: Stealthy Position Manipulation**
```python
# Gradual drift: 0.0005° every 10 seconds
# Total drift over 45 min: ~0.135° (~8nm)
# Rate matches baseline
# May evade frequency detection
```

**Scenario B: Intermittent DoS**
```python
# 5-second bursts every minute
# May evade sustained rate detection
# Look for burst detection gaps
```

**Scenario C: Multi-Device Spoof**
```python
# Spoof from multiple source addresses
# Spread attack across devices
# Harder to correlate
```

**Scenario D: Data-Only Attack**
```python
# Match all timing perfectly
# Only modify data values slightly
# Hardest to detect
```

## Phase 5: Analysis (30 minutes)

### Individual Analysis

Complete the following analysis for both rounds:

#### Detection Effectiveness

| Attack Type | Round 1 Detected? | Round 2 Detected? | Detection Method |
|-------------|-------------------|-------------------|------------------|
| Position spoof | | | |
| Heading spoof | | | |
| Engine spoof | | | |
| DoS | | | |
| Replay | | | |

#### False Positive Analysis

| False Positive | Cause | Suggested Fix |
|----------------|-------|---------------|
| | | |
| | | |

#### Evasion Techniques Effectiveness

| Technique | Effectiveness (1-5) | Why? |
|-----------|---------------------|------|
| Rate matching | | |
| Gradual changes | | |
| Multi-source | | |
| Timing sync | | |

### Team Discussion

Discuss with your team:

1. Which detection methods were most effective?
2. Which attacks were hardest to detect?
3. What improvements would you recommend?
4. What did you learn as attacker vs defender?

### Calculate Final Scores

**Round 1:**
- Red Team (Team A): ______ points
- Blue Team (Team B): ______ points

**Round 2:**
- Red Team (Team B): ______ points
- Blue Team (Team A): ______ points

**Total:**
- Team A: ______ points
- Team B: ______ points

## Phase 6: Presentation Preparation (15 minutes)

Prepare a 5-minute team presentation covering:

1. **Attack strategy** (Red team phase)
   - What attacks did you attempt?
   - What evasion techniques worked?

2. **Defense performance** (Blue team phase)
   - What did you detect?
   - What did you miss?

3. **Key learnings**
   - Most effective detection method
   - Biggest vulnerability discovered
   - Recommended improvements

4. **Demonstration**
   - Show one successful detection
   - Show one evaded attack (if any)

## Capstone Report Requirements

Submit individual report (3-5 pages) including:

### 1. Executive Summary
- Exercise overview
- Key findings
- Final scores

### 2. Attack Analysis
- Attacks attempted and results
- Evasion techniques used
- What worked / didn't work

### 3. Defense Analysis
- Detection coverage
- False positive rate
- Response effectiveness

### 4. Lessons Learned
- Technical insights
- Operational insights
- Recommendations

### 5. System Improvements
- Specific detection improvements
- Configuration changes
- Architecture recommendations

### 6. Appendix
- Attack log
- Defense log
- Score breakdown

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Participation in exercise | 20 |
| Attack strategy and execution | 20 |
| Defense effectiveness | 20 |
| Analysis quality | 20 |
| Presentation | 10 |
| Report quality | 10 |
| **Total** | **100** |

## Bonus Challenges

For extra credit (up to 10 points):

1. **Develop novel attack** (+5)
   - Attack not covered in labs
   - Must document and explain

2. **Improve detection** (+5)
   - Propose and test new detection method
   - Show improved performance

3. **Automate response** (+5)
   - Create automated response script
   - Demonstrate blocking attack

## Ethics Reminder

This exercise demonstrates real attack techniques.

**Remember:**
- These skills are for DEFENSE
- Only use on authorized systems
- Real attacks cause real harm
- Professional responsibility

## Course Completion Checklist

Before leaving:

- [ ] Attack log submitted
- [ ] Defense log submitted
- [ ] Score sheet completed
- [ ] Presentation delivered
- [ ] Capstone report submitted
- [ ] Equipment returned
- [ ] Course evaluation completed

## Final Words

Congratulations on completing the Maritime OT Security course!

You have learned:
- CAN bus and NMEA 2000 fundamentals
- Attack techniques (for understanding threats)
- Detection methods (frequency, entropy, ML, fingerprinting)
- Defense architecture and ensemble systems

**Use these skills responsibly to protect maritime systems and lives at sea.**

## References

- Course syllabus and all lab materials
- [Maritime Cybersecurity Best Practices]
- [NIST Cybersecurity Framework]
- [IMO Maritime Cyber Security Guidelines]

[Maritime Cybersecurity Best Practices]:https://www.uscg.mil/cyber
[NIST Cybersecurity Framework]:https://www.nist.gov/cyberframework
[IMO Maritime Cyber Security Guidelines]:https://www.imo.org

---

**Thank you for your participation!**

Questions? Contact: [instructor email]

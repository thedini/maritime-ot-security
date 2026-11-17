# Maritime OT Security Course

**Maritime Operational Technology Security on the NEMO platform**

A 14-week course teaching maritime cybersecurity using NEMO (NMEA 2000 Education and Maritime Operations), an open-source platform designed by James Campbell. NEMO versions 1.0.0 and 1.0.1 are supported.

## Overview

This course provides hands-on experience with maritime operational technology (OT) security. Students learn CAN bus and NMEA 2000 protocols, build low-cost hardware interfaces (~$50), analyze vessel network traffic, implement attack scenarios, and develop anomaly detection systems.

## Course Structure

```
maritime-ot-security/
├── class/                    # Weekly lecture content
│   ├── class_00_introduction/
│   ├── class_01_can_protocol/
│   └── ...
├── labs/                     # Hands-on lab exercises
│   ├── lab_01_network_recon/
│   ├── lab_02_can_decode/
│   └── ...
├── datasets/                 # Synthetic captures + generator (see datasets/README.md)
├── assessments/              # Quizzes
├── capstone/                 # Four-phase team project
├── case_studies/             # Maritime incident case studies
├── docs/                     # Instructor guide, prerequisites, technology requirements
├── templates/                # Build templates
├── syllabus.md              # Course syllabus
├── build.py                 # Build script for PDF/HTML
└── README.md                # This file
```

## Content Format

All content is written in Markdown with:
- YAML frontmatter for metadata
- HTML comments (`<!-- -->`) for instructor notes
- Reference-style links at document end

### Building Content

```bash
# Install dependencies
pip install pypandoc gitpython

# Build all formats
python build.py class/ output/ false

# Build website
python build.py class/ output/ true
```

## Hardware Requirements

| Component | Cost |
|-----------|------|
| NEMO board (Teensy 4.0, SH1106 OLED, 2x TJA1050, pots, buttons, connector) | about $50 |
| Micro USB data cable | $5 |
| Listen-only CAN capture interface (shared per bench) | instructor |
| **Total per student** | **about $55** |

## Software Requirements

- VS Code with PlatformIO, and Teensyduino (for NEMO firmware)
- Python 3.x (numpy, pandas, scikit-learn, pytorch)
- can-utils (Linux)
- NEMO firmware (https://github.com/thedini/NEMO)

## Learning Outcomes

Upon completion, students will be able to:

1. Explain CAN bus protocol vulnerabilities and maritime implications
2. Decode and construct NMEA 2000 PGN messages
3. Build and program a Teensy-based CAN interface
4. Perform reconnaissance on maritime CAN networks
5. Execute and detect spoofing, replay, and DoS attacks
6. Implement frequency-based and entropy-based anomaly detection
7. Apply machine learning techniques to intrusion detection
8. Analyze clock skew for device fingerprinting
9. Design defense-in-depth architectures for vessel networks

## NICE Framework Alignment

- **Cyber Defense Analyst (PR-CDA-001)**: Network traffic analysis
- **Security Architect (SP-ARC-001)**: Security architecture design
- **Vulnerability Assessment Analyst (PR-VAM-001)**: Vulnerability analysis

## License

This work is licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

## Contributing

Contributions are welcome! Please submit pull requests with improvements or corrections.

## Author

Constantine Macris
University of Rhode Island
cmacris@uri.edu

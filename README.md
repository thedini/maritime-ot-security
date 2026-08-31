# Maritime OT Security Course

**OpenBridge: Maritime Operational Technology Security**

A 14-week course teaching maritime cybersecurity using the open-source OpenBridge platform.

## Overview

This course provides hands-on experience with maritime operational technology (OT) security. Students learn CAN bus and NMEA 2000 protocols, build the open-source [NEMO](https://github.com/Soups71/NEMO) dual-bus hardware interface (~$50), analyze vessel network traffic, implement attack scenarios, and develop anomaly detection systems.

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
├── images/                   # Diagrams and figures
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

Students build the **NEMO** dual-bus NMEA 2000 board. The Teensy 4.0's two native FlexCAN controllers provide one transmit/inject bus and one passive monitor bus simultaneously — no external CAN controller needed.

| Component | Cost | Qty |
|-----------|------|-----|
| Teensy 4.0 | $23 | 1 |
| TJA1050 CAN Transceiver | $1.50 | 2 |
| SH1106 128×64 OLED (I2C) | $5 | 1 |
| 10kΩ Potentiometer | $0.50 | 3 |
| Tactile Push Button | $0.20 | 4 |
| NMEA 2000 M12 Connector | $8–$15 | 1 |
| 3-Pin Screw Terminal Block | $0.50 | 1 |
| Custom NEMO PCB (JLCPCB) | $2–$5 | 1 |
| **Total** | **~$42–$55** | |

KiCad design files, 3D-printable case STLs, and firmware live in the [NEMO repository](https://github.com/Soups71/NEMO). For programs without soldering capacity, pre-built boards can be requested at `nemo@jamescampbell.org`.

## Software Requirements

- Arduino IDE with Teensyduino
- Python 3.x (numpy, pandas, scikit-learn, pytorch)
- can-utils (Linux)
- OpenBridge firmware

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

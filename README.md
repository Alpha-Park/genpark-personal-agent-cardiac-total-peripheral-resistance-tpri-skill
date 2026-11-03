# Cardiac Total Peripheral Resistance Index (TPRI) Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Systemic Vascular Resistance (SVR) and Total Peripheral Resistance Index (TPRI) Quantitative Analyzer. Evaluates left-ventricular afterload and peripheral vascular compliance.

```mermaid
flowchart TD
    A[SBP, DBP, and Central Venous Pressure] --> B[Calculate MAP = DBP + SBP - DBP / 3]
    C[Height & Weight] --> D[Mosteller BSA Formula]
    B & E[Cardiac Output CO] --> F[SVR = 80 * MAP - CVP / CO]
    F & D --> G[TPRI = SVR * BSA]
    G --> H[Autonomic Vascular Afterload Evaluation]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Standard Cardiovascular Hemodynamics**: Evaluates SVR in dyn*s/cm^5 and indexed TPRI in dyn*s*cm^-5*m^2.
- **Precision Anthropometry**: Incorporates Mosteller body surface area adjustment.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0

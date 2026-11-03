---
name: genpark-personal-agent-cardiac-total-peripheral-resistance-tpri-skill
description: Total Peripheral Resistance Index (TPRI) and Systemic Vascular Resistance (SVR) analyzer. Computes Mean Arterial Pressure, Mosteller Body Surface Area, and vascular impedance to assess autonomic tone and afterload.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - cardiovascular
  - hemodynamics
  - blood-pressure
  - svr
  - tpri
  - openclaw
  - genpark
  - mcp
---

# Cardiac Total Peripheral Resistance Index (TPRI) Skill

## Overview
This skill calculates hemodynamic impedance parameters of the systemic circulation:
- **Mean Arterial Pressure (MAP)**: Geometric mean perfusion pressure derived from systolic and diastolic measurements.
- **Systemic Vascular Resistance (SVR)**: Total downstream frictional resistance in dynes $\cdot$ s / cm$^5$.
- **Total Peripheral Resistance Index (TPRI)**: SVR indexed to body surface area ($m^2$) using the Mosteller formula.
- **Clinical Hemodynamic State**: Discriminates vasodilatory shock / exercise vasodilation from severe sympathetic vasoconstrictive afterload stress.

## Mathematical Formulation
1. **Mean Arterial Pressure**:
   $$\text{MAP} = \text{DBP} + \frac{\text{SBP} - \text{DBP}}{3}$$
2. **Body Surface Area (Mosteller)**:
   $$\text{BSA} = \sqrt{\frac{\text{Height (cm)} \times \text{Weight (kg)}}{3600}}$$
3. **Systemic Vascular Resistance (SVR)**:
   $$\text{SVR} = \frac{80 \times (\text{MAP} - \text{CVP})}{\text{CO}} \quad [\text{dyn} \cdot \text{s} \cdot \text{cm}^{-5}]$$
4. **Total Peripheral Resistance Index (TPRI)**:
   $$\text{TPRI} = \text{SVR} \times \text{BSA} \quad [\text{dyn} \cdot \text{s} \cdot \text{cm}^{-5} \cdot m^2]$$

## Usage
```python
from client import TotalPeripheralResistanceClient

client = TotalPeripheralResistanceClient()
res = client.evaluate_hemodynamics(
    systolic_bp_mmhg=120.0,
    diastolic_bp_mmhg=80.0,
    cardiac_output_l_min=5.0
)
print(res["evaluation"]["classification"])
```

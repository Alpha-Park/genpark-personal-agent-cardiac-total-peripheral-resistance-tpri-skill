"""
Example usage of Cardiac Total Peripheral Resistance Index (TPRI) Skill.
Demonstrates normal systemic resistance vs hyperdynamic vasodilatation vs severe vasoconstrictive stress.
"""

import json
from client import TotalPeripheralResistanceClient


def main():
    print("=== Testing Cardiac Total Peripheral Resistance Index (TPRI) Skill ===")
    client = TotalPeripheralResistanceClient()

    # 1. Normal adult resting hemodynamics (SBP=120, DBP=80, CO=5.0 L/min, CVP=4 mmHg, H=175cm, W=70kg)
    res_normal = client.evaluate_hemodynamics(
        systolic_bp_mmhg=120.0,
        diastolic_bp_mmhg=80.0,
        cardiac_output_l_min=5.0,
        central_venous_pressure_mmhg=4.0,
        height_cm=175.0,
        weight_kg=70.0
    )
    print("\n[Case 1: Normal Systemic Vascular Resistance]")
    print(json.dumps(res_normal, indent=2))

    # 2. Hyperdynamic / Vasodilatory state (e.g. post-exercise heat dissipation, high CO=8.5 L/min, BP=110/60)
    res_vasodilated = client.evaluate_hemodynamics(
        systolic_bp_mmhg=110.0,
        diastolic_bp_mmhg=60.0,
        cardiac_output_l_min=8.5,
        central_venous_pressure_mmhg=3.0,
        height_cm=180.0,
        weight_kg=75.0
    )
    print("\n[Case 2: Vasodilatory / Hyperdynamic State]")
    print(json.dumps(res_vasodilated, indent=2))

    # 3. Severe hypertensive vasoconstriction / high afterload (BP=170/105, low CO=3.6 L/min)
    res_constricted = client.evaluate_hemodynamics(
        systolic_bp_mmhg=170.0,
        diastolic_bp_mmhg=105.0,
        cardiac_output_l_min=3.6,
        central_venous_pressure_mmhg=6.0,
        height_cm=170.0,
        weight_kg=80.0
    )
    print("\n[Case 3: High Afterload / Vasoconstrictive Stress]")
    print(json.dumps(res_constricted, indent=2))

    # Assertions
    assert res_normal["status"] == "success"
    assert res_vasodilated["svr_dyn_s_cm5"] < res_normal["svr_dyn_s_cm5"]
    assert res_constricted["svr_dyn_s_cm5"] > res_normal["svr_dyn_s_cm5"]
    print("\n[SUCCESS] All Total Peripheral Resistance test cases passed!")


if __name__ == "__main__":
    main()

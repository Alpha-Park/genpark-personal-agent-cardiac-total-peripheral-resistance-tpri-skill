"""
Cardiac Total Peripheral Resistance Index (TPRI) & Systemic Vascular Resistance (SVR) Client.
Zero-mock pure Python standard library implementation.
Calculates Mean Arterial Pressure (MAP), Body Surface Area (BSA), Systemic Vascular Resistance (SVR),
and Total Peripheral Resistance Index (TPRI) to evaluate autonomic afterload and vascular compliance.
"""

import math
from typing import Dict, Any, Optional


class TotalPeripheralResistanceClient:
    """
    Computes SVR (dyn * s / cm^5) and TPRI (dyn * s * cm^-5 * m^2)
    using Poiseuille-hemodynamic modeling and Mosteller BSA formula.
    """

    def __init__(self):
        pass

    def _calculate_bsa_mosteller(self, height_cm: float, weight_kg: float) -> float:
        """
        Mosteller formula for Body Surface Area (BSA):
        BSA (m^2) = sqrt((height_cm * weight_kg) / 3600)
        """
        return math.sqrt((height_cm * weight_kg) / 3600.0)

    def evaluate_hemodynamics(
        self,
        systolic_bp_mmhg: float,
        diastolic_bp_mmhg: float,
        cardiac_output_l_min: float,
        central_venous_pressure_mmhg: float = 4.0,
        height_cm: Optional[float] = 175.0,
        weight_kg: Optional[float] = 70.0
    ) -> Dict[str, Any]:
        """
        Calculates SVR, TPRI, Cardiac Index (CI), and systemic vascular impedance.
        systolic_bp_mmhg: SBP (mmHg).
        diastolic_bp_mmhg: DBP (mmHg).
        cardiac_output_l_min: Cardiac output (L/min).
        central_venous_pressure_mmhg: CVP or right atrial pressure (default: 4.0 mmHg).
        height_cm: Body height in cm.
        weight_kg: Body weight in kg.
        """
        if systolic_bp_mmhg <= diastolic_bp_mmhg or diastolic_bp_mmhg <= 0:
            raise ValueError("Systolic BP must be strictly greater than Diastolic BP, and both positive.")
        if cardiac_output_l_min <= 0:
            raise ValueError("Cardiac output must be strictly positive.")

        # Mean Arterial Pressure (MAP) = DBP + (SBP - DBP) / 3
        pulse_pressure = systolic_bp_mmhg - diastolic_bp_mmhg
        map_mmhg = diastolic_bp_mmhg + (pulse_pressure / 3.0)

        # Perfusion pressure across systemic capillary bed = MAP - CVP
        perfusion_pressure = max(1.0, map_mmhg - central_venous_pressure_mmhg)

        # SVR (dyn * s / cm^5) = 80 * (MAP - CVP) / CO
        svr_dyn_s_cm5 = (80.0 * perfusion_pressure) / cardiac_output_l_min

        bsa_m2 = None
        tpri_dyn_s_cm5_m2 = None
        cardiac_index = None

        if height_cm is not None and weight_kg is not None and height_cm > 0 and weight_kg > 0:
            bsa_m2 = self._calculate_bsa_mosteller(height_cm, weight_kg)
            tpri_dyn_s_cm5_m2 = svr_dyn_s_cm5 * bsa_m2
            cardiac_index = cardiac_output_l_min / bsa_m2

        # Clinical evaluation:
        # Normal SVR: 800 - 1200 dyn * s / cm^5
        # Normal TPRI: 1600 - 2400 dyn * s * cm^-5 * m^2
        # Normal Cardiac Index: 2.5 - 4.0 L/min/m^2
        target_val = tpri_dyn_s_cm5_m2 if tpri_dyn_s_cm5_m2 is not None else svr_dyn_s_cm5
        threshold_low = 1600.0 if tpri_dyn_s_cm5_m2 is not None else 800.0
        threshold_high = 2400.0 if tpri_dyn_s_cm5_m2 is not None else 1200.0

        if target_val < threshold_low:
            classification = "Vasodilatory / Hyperdynamic State"
            pathophysiology = "Low systemic vascular resistance. Commonly observed in aerobic heat dissipation, early sepsis, or high-output states."
            afterload_status = "Reduced Afterload"
        elif target_val <= threshold_high:
            classification = "Normal Systemic Vascular Resistance"
            pathophysiology = "Well-balanced autonomic vascular tone and arteriolar caliber."
            afterload_status = "Optimal Afterload"
        elif target_val <= threshold_high * 1.4:
            classification = "Elevated Vascular Resistance / Vasoconstrictive Stress"
            pathophysiology = "Sympathetic arteriolar constriction elevating left ventricular afterload."
            afterload_status = "Elevated Afterload"
        else:
            classification = "Severe Hypertensive Vasospasm / Extreme Resistance"
            pathophysiology = "Pronounced systemic impedance significantly impeding cardiac stroke volume."
            afterload_status = "Critical High Afterload"

        return {
            "status": "success",
            "map_mmhg": round(map_mmhg, 1),
            "pulse_pressure_mmhg": round(pulse_pressure, 1),
            "svr_dyn_s_cm5": round(svr_dyn_s_cm5, 1),
            "tpri_dyn_s_cm5_m2": round(tpri_dyn_s_cm5_m2, 1) if tpri_dyn_s_cm5_m2 is not None else None,
            "bsa_m2": round(bsa_m2, 2) if bsa_m2 is not None else None,
            "cardiac_index_l_min_m2": round(cardiac_index, 2) if cardiac_index is not None else None,
            "evaluation": {
                "classification": classification,
                "afterload_status": afterload_status,
                "pathophysiology": pathophysiology
            }
        }

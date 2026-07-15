
"""
carbonate.py

Carbonate chemistry calculations for WWTP forcing.

Uses PyCO2SYS to estimate DIC from:

- alkalinity
- pH
- temperature

Author:
Abdoul Tall
"""

import numpy as np
import PyCO2SYS as pyco2

from .constants import *

# DIC

def estimate_DIC(
    alkalinity,
    pH,
    temperature,
    salinity=SALINITY,
    silicate=TOTAL_SILICATE,
    phosphate=TOTAL_PHOSPHATE,
):
    """
    Estimate Dissolved Inorganic Carbon (DIC, mmol/m3) from alkalinity (mmol/m3), pH, and temperature (degC)
    and salinity (PSU).
    """

    alkalinity = np.asarray(alkalinity, dtype=float)

    pH = np.asarray(pH, dtype=float)

    temperature = np.asarray(temperature, dtype=float)

    if len(alkalinity) != 12:
        raise ValueError("alkalinity must contain 12 months")

    if len(pH) != 12:
        raise ValueError("pH must contain 12 months")

    if len(temperature) != 12:
        raise ValueError("temperature must contain 12 months")

    kwargs = dict(

        par1_type=1,
        par1=alkalinity,

        par2_type=3,
        par2=pH,

        salinity=salinity,

        temperature=temperature,

        pressure=0,

        total_silicate=silicate,

        total_phosphate=phosphate,

        opt_pH_scale=4,

        opt_k_carbonic=8,

        opt_k_bisulfate=1,

        opt_total_borate=1,

    )

    results = pyco2.sys(**kwargs)

    dic = results["dic"]

    return np.asarray(dic)


# Carbonate summary

def carbonate_summary(dic):

    print()

    print("Carbonate chemistry")

    print("-------------------")

    print(f"Mean DIC : {np.mean(dic):.1f} mmol/m3")

    print(f"Minimum  : {np.min(dic):.1f}")

    print(f"Maximum  : {np.max(dic):.1f}")

    print()


# Simple QC

def check_dic(dic):

    if np.any(np.isnan(dic)):
        raise ValueError("NaN detected in DIC")

    if np.any(dic < 0):
        raise ValueError("Negative DIC values detected")

    return True


"""
conversions.py

Unit conversions and empirical relationships for WWTP forcing.

All returned values follow SalishSeaCast conventions.
"""

import numpy as np
import gsw

from .constants import *


# Temperature

def conservative_temperature(temp):
    """
    Convert potential temperature (degC) to Conservative Temperature.
    """

    temp = np.asarray(temp, dtype=float)

    return gsw.CT_from_pt(0, temp)


# Flow

def flow_to_flux(flow_m3_day, cell_area):
    """
    Convert WWTP flow (m3/day) to flux (kg m-2 s-1)
    """

    flow = np.asarray(flow_m3_day)

    return flow * RHO / (cell_area * SECONDS_PER_DAY)

# NH3

def ammonia_to_mmol(ammonia_mgL):
    """
    mg/L NH3  ->. mmol/m3
    """

    ammonia = np.asarray(ammonia_mgL)

    return ammonia * 1000 / MW_NH3


# NO3

def nitrate_to_mmol(nitrate_mgL):
    """
    mg/L NO3. ->. mmol/m3
    """

    nitrate = np.asarray(nitrate_mgL)

    return nitrate * 1000 / MW_NO3

# Oxygen

def oxygen_to_mmol(oxygen_mgL):
    """
    mg/L O2 -> mmol/m3
    """

    oxygen = np.asarray(oxygen_mgL)

    return oxygen * 1000 / MW_O2


# Alkalinity

def alkalinity_to_mmol(alk_mgL):
    """
    mg/L as CaCO3 -> mmol/m3
    """

    alk = np.asarray(alk_mgL)

    return alk * 1000 / MW_CACO3 * 2


# Turbidity

def turbidity_from_tss(tss):
    """
    Estimate turbidity (FAU) from TSS (mg/L)
    """

    tss = np.asarray(tss)

    turbidity_fau = (tss - 7.0) / 0.89

    return np.maximum(turbidity_fau, 0.5)


# Organic Nitrogen

def bod_to_PON_DON(bod):
    """
    Estimate PON and DON from cBOD.
    """

    bod = np.asarray(bod)

    boc = bod * 1000 / 32 * 106 / 138

    poc = boc / (1 + DOC_TO_POC)

    doc = poc * DOC_TO_POC

    pon = poc / C_TO_N

    don = doc / C_TO_N

    return pon, don

# Missing biology

def zero_biology():

    """
    Variables not available
    """

    return np.zeros(12)


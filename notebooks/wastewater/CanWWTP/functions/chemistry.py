"""
chemistry.py

Compute all SalishSeaCast WWTP forcing variables
from raw wastewater observations.

Author:
Abdoul Tall
"""

import numpy as np

from .conversions import (
    conservative_temperature,
    flow_to_flux,
    ammonia_to_mmol,
    nitrate_to_mmol,
    oxygen_to_mmol,
    alkalinity_to_mmol,
    turbidity_from_tss,
    bod_to_PON_DON,
)

from .carbonate import estimate_DIC


# Main routine

def compute_all_variables(station, cell_area):
    """
    Compute all model variables from raw observations.

    Parameters
    ----------
    station : Station

    cell_area : float
        Grid-cell area (m²)

    Returns
    -------
    Station
    """

    raw = station.raw

    derived = station.derived

    # Temperature

    derived["temperature"] = conservative_temperature(
        raw["temperature"]
    )

    station.flags["temperature"] = "calculated"

    # Flux

    derived["flux"] = flow_to_flux(
        raw["flow"],
        cell_area,
    )

    station.flags["flux"] = "calculated"

    # NH3

    derived["NH3"] = ammonia_to_mmol(
        raw["ammonia"]
    )

    station.flags["NH3"] = "calculated"

    # NO3

    if "nitrate" in raw:

        derived["NO3"] = nitrate_to_mmol(
            raw["nitrate"]
        )

        station.flags["NO3"] = "calculated"

    # Oxygen

    if "oxygen" in raw:

        derived["oxygen"] = oxygen_to_mmol(
            raw["oxygen"]
        )

        station.flags["oxygen"] = "calculated"

    # Alkalinity

    if "alkalinity" in raw:

        derived["alkalinity"] = alkalinity_to_mmol(
            raw["alkalinity"]
        )

        station.flags["alkalinity"] = "calculated"

    # PON / DON

    if "bod" in raw:

        pon, don = bod_to_PON_DON(
            raw["bod"]
        )

        derived["PON"] = pon
        derived["DON"] = don

        station.flags["PON"] = "calculated"
        station.flags["DON"] = "calculated"

    # Turbidity

    if "tss" in raw:

        derived["turb"] = turbidity_from_tss(
            raw["tss"]
        )

        station.flags["turb"] = "calculated"

    # DIC

    if (
        "alkalinity" in derived
        and
        "pH" in raw
    ):

        derived["DIC"] = estimate_DIC(

            alkalinity=derived["alkalinity"],

            pH=raw["pH"],

            temperature=raw["temperature"],

        )

        station.flags["DIC"] = "calculated"

    # Variables unavailable

    zeros = np.zeros(12)

    for var in [

        "dSi",

        "diatoms",

        "nanoflagellates",

        "Z1",

        "bSi",

    ]:

        derived[var] = zeros.copy()

        station.flags[var] = "default"

    return station
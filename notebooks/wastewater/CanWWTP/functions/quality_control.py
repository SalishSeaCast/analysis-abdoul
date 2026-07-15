"""
quality_control.py

Quality-control checks for WWTP database.

Author:
Abdoul Tall
"""

import numpy as np


def check_length(values, variable, station):
    """Check that a variable has 12 monthly values."""

    values = np.asarray(values)

    if len(values) != 12:
        raise ValueError(
            f"{station}: '{variable}' has {len(values)} values (expected 12)."
        )


def check_nan(values, variable, station):
    """Check for NaN values."""

    values = np.asarray(values)

    if np.any(np.isnan(values)):
        print(f"WARNING: {station} - {variable} contains NaN values.")


def check_negative(values, variable, station):
    """Check for negative values."""

    values = np.asarray(values)

    if np.any(values < 0):
        print(f"WARNING: {station} - {variable} contains negative values.")


def check_range(values, variable, station, minimum=None, maximum=None):
    """Generic range check."""

    values = np.asarray(values)

    if minimum is not None and np.any(values < minimum):
        print(
            f"WARNING: {station} - {variable} below minimum ({minimum})."
        )

    if maximum is not None and np.any(values > maximum):
        print(
            f"WARNING: {station} - {variable} above maximum ({maximum})."
        )


def qc_station(station):
    """
    Run QC checks on one station.
    """

    variables = {}

    variables.update(station.raw)
    variables.update(station.derived)

    for var, values in variables.items():

        check_length(values, var, station.name)

        check_nan(values, var, station.name)

        check_negative(values, var, station.name)

    # Typical ranges for wastewater treatment plant effluent

    if "temperature" in station.raw:
        check_range(station.raw["temperature"], "temperature",
                    station.name, 0, 40)

    if "flow" in station.raw:
        check_range(station.raw["flow"], "flow",
                    station.name, 0, 1e8)

    if "pH" in station.raw:
        check_range(station.raw["pH"], "pH",
                    station.name, 5.5, 9.5)

    if "oxygen" in station.raw:
        check_range(station.raw["oxygen"], "oxygen",
                    station.name, 0, 20)

    if "ammonia" in station.raw:
        check_range(station.raw["ammonia"], "ammonia",
                    station.name, 0, 1e4)

    if "nitrate" in station.raw:
        check_range(station.raw["nitrate"], "nitrate",
                    station.name, 0, 1e4)


def qc_database(database):
    """
    Run QC on all stations.
    """

    print()

    print("=" * 70)
    print("QUALITY CONTROL")
    print("=" * 70)

    for station in database:
        qc_station(station)

    print()
    print("QC completed.")
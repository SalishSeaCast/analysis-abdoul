"""
reader.py

Read one WWTP Excel and return a station object.

Structure: 
Metadata sheet: "Information"
2020
2021
2022
...

Each yearly sheet contains:

Month | Flow | Temperature | Ammonia | BOD | TSS | Alkalinity | pH | Nitrate | Oxygen
"""

import numpy as np
import pandas as pd

from .station import Station


def read_station(filename):
    """
    Read one WWTP Excel.

    Parameters
    ----------
    filename : str or Path

    Returns
    -------
    Station
    """

    # Information sheet

    info = pd.read_excel(
        filename,
        sheet_name="Information",
    )

    station = Station(
        name=info.loc[0, "Value"],
        authority=info.loc[1, "Value"],
        j=int(info.loc[2, "Value"]),
        i=int(info.loc[3, "Value"]),
        source=info.loc[4, "Value"],
    )

    # Read workbook

    workbook = pd.ExcelFile(filename)

    year_sheets = [
        sheet
        for sheet in workbook.sheet_names
        if sheet != "Information"
    ]

    # Variables to read

    variable_map = {

        "Temperature": "temperature",

        "Flow": "flow",

        "Ammonia": "ammonia",

        "BOD": "bod",

        "TSS": "tss",

        "Alkalinity": "alkalinity",

        "Oxygen": "oxygen",

        "Nitrate": "nitrate",

        "pH": "pH",

    }

    # Compute monthly averages

    for excel_name, station_name in variable_map.items():

        yearly_arrays = []

        for sheet in year_sheets:

            df = pd.read_excel(
                filename,
                sheet_name=sheet,
            )

            if excel_name not in df.columns:
                continue

            values = df[excel_name].to_numpy(dtype=float)

            if len(values) != 12:
                continue

            yearly_arrays.append(values)

        if len(yearly_arrays) == 0:
            continue

        yearly_arrays = np.array(yearly_arrays)

        monthly_mean = np.nanmean(
            yearly_arrays,
            axis=0,
        )

        if np.isnan(monthly_mean).all():
            continue

        station.add_raw_variable(
            station_name,
            monthly_mean,
        )

    return station
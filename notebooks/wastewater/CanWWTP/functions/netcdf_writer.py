"""
netcdf_writer.py

Write WWTP forcing NetCDF
from WWTPDatabase.

Author:
Abdoul Tall
"""

import numpy as np
import xarray as xr
from functions.constants import WWTP_VARIABLES


class NetCDFWriter:

    def __init__(self, template_file):

        self.ds = xr.open_dataset(template_file)

        self.ds.attrs.update({

            "title":
                "British Columbia Wastewater Treatment Plant Climatology for SalishSeaCast",

            "summary":
                "Monthly climatology of wastewater discharge and water quality variables for British Columbia wastewater treatment plants.",

            "creator_name":
                "Abdoul Tall",

            "creator_email":
                "atall@eoas.ubc.ca",

            "institution":
                "University of British Columbia",

            "institution_fullname":
                "Department of Earth, Ocean and Atmospheric Sciences, University of British Columbia",

            "acknowledgements":
                "Compiled from annual WWTP monitoring reports, Metro Vancouver, Capital Regional District, Regional District of Nanaimo, Rich Pawlowicz, and other publicly available sources.",

            "source":
                "Monthly climatologies derived from annual monitoring reports and reference-station infilling.",

            "comment":
                "Missing water-quality variables were filled using nearby reference WWTPs; measured flow was retained for every facility.",

            "history":
                "[2026-07-15] Created with build_WWTP_database.py"

        })        

    def clear_variables(self):

        variables = WWTP_VARIABLES

        for var in variables:

            self.ds[var][:] = 0.0

    def write_station(self, station):

        j = station.j
        i = station.i

        for var in station.derived:

            self.ds[var][:, j, i] = station.derived[var]

    def write_database(self, database):

        for station in database:

            self.write_station(station)

    def save(self, filename):
        self.ds.load()
        self.ds.to_netcdf(filename)
        self.ds.close()

        print()

        print("Saved")

        print(filename)
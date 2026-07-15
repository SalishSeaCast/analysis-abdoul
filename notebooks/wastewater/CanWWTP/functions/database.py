"""
database.py

Database of WWTP stations.

This class stores all stations and provides methods for:

- adding stations
- searching stations
- computing variables
- checking quality
- exporting to NetCDF

Author:
Abdoul Tall
"""

import pickle
import numpy as np

from .chemistry import compute_all_variables


class WWTPDatabase:

    def __init__(self):

        self.stations = {}

    # Add station

    def add_station(self, station):

        if station.name in self.stations:

            raise ValueError(
                f"{station.name} already exists."
            )

        self.stations[station.name] = station


    def remove_station(self, name):

        del self.stations[name]

    def get(self, name):

        return self.stations[name]

    def names(self):

        return sorted(self.stations.keys())

    def __len__(self):

        return len(self.stations)

    # Compute everything

    def compute_all(self, ds_mask):

        for station in self.stations.values():

            cell_area = (

                ds_mask.e1t[0, station.j, station.i].values

                *

                ds_mask.e2t[0, station.j, station.i].values

            )

            compute_all_variables(

                station,

                cell_area,

            )

    # Summary

    def summary(self):

        print()

        print("=" * 70)

        print("WWTP DATABASE")

        print("=" * 70)

        print()

        print(f"Number of stations : {len(self)}")

        print()

        for station in self.stations.values():

            print(

                f"{station.name:35s}"

                f"({station.j:4d}, {station.i:4d})"

            )

    # Missing variables

    def missing_report(self):

        print()

        print("=" * 70)

        print("Missing Variables")

        print("=" * 70)

        print()

        for station in self.stations.values():

            missing = station.missing_raw()

            if len(missing):

                print()

                print(station.name)

                print("-" * len(station.name))

                for var in missing:

                    print(var)

    # Save

    def save(self, filename):

        with open(filename, "wb") as f:

            pickle.dump(self, f)

    # Load

    @staticmethod
    def load(filename):

        with open(filename, "rb") as f:

            return pickle.load(f)

    # Iterator

    def __iter__(self):

        return iter(self.stations.values())
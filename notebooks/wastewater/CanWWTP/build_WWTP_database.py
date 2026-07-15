#!/usr/bin/env python

"""
Build WWTP NetCDF forcing file.

Pipeline

Excel
    ↓
Station objects
    ↓
Fill missing data
    ↓
Compute chemistry
    ↓
Quality control
    ↓
NetCDF
"""

from pathlib import Path

import xarray as xr

from functions.database import WWTPDatabase
from functions.reader import read_station
from functions.fill_missing import fill_missing
from functions.quality_control import qc_database
from functions.netcdf_writer import NetCDFWriter


# Paths

ROOT = Path(__file__).parent

DATA_DIR = ROOT / "data"

STATION_DIR = DATA_DIR / "stations"

OUTPUT_DIR = DATA_DIR / "output"

DATABASE_FILE = OUTPUT_DIR / "CanWWTP_20260715.pkl"

OUTPUT_NETCDF = OUTPUT_DIR / "CanWWTP_20260715.nc"

TEMPLATE = "/ocean/atall/MOAD/Obs/PugetSound/WWTP/wwtp_20260617.nc"

MESH_MASK = "/ocean/atall/MOAD/grid/mesh_mask202605.nc"


# Read mesh
mesh = xr.open_dataset(MESH_MASK)

# Read stations
db = WWTPDatabase()

files = sorted(STATION_DIR.glob("*.xlsx"))

print()

print("=" * 70)
print("READING STATIONS")
print("=" * 70)

for file in files:

    print(file.name)

    station = read_station(file)

    db.add_station(station)

print()

print(f"{len(db)} stations loaded.")

# Fill missing observations

print()

print("=" * 70)
print("FILLING MISSING VARIABLES")
print("=" * 70)

fill_missing(db)

# Compute chemistry

print()

print("=" * 70)
print("COMPUTING VARIABLES")
print("=" * 70)

db.compute_all(mesh)

# Quality control

qc_database(db)

# Save database

DATABASE_FILE.parent.mkdir(exist_ok=True)

db.save(DATABASE_FILE)

# Write NetCDF

writer = NetCDFWriter(TEMPLATE)

writer.clear_variables()

writer.write_database(db)

writer.save(OUTPUT_NETCDF)

print()

print("=" * 70)
print("DONE")
print("=" * 70)

print()

print(f"Database : {DATABASE_FILE}")

print(f"NetCDF   : {OUTPUT_NETCDF}")
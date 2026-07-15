# Molecular weights (g/mol)
MW_NH3 = 17.031
MW_NO3 = 62.0
MW_O2 = 32.0
MW_CACO3 = 100.0869

# Water density (kg/m3)
RHO = 1000.0

# Time conversion
SECONDS_PER_DAY = 86400

# Organic matter assumptions
DOC_TO_POC = 0.8
C_TO_N = 34

# Carbonate system assumptions
SALINITY = 0.4
TOTAL_SILICATE = 137
TOTAL_PHOSPHATE = 0

# WWTP variables written to the NetCDF

WWTP_VARIABLES = [
    "flux",
    "temperature",
    "NO3",
    "NH3",
    "dSi",
    "diatoms",
    "nanoflagellates",
    "Z1",
    "PON",
    "DON",
    "bSi",
    "oxygen",
    "alkalinity",
    "DIC",
    "turb",
]

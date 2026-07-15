"""
fill_missing.py

Fill missing WWTP variables.

Strategy:
1. Complete the partially observed ("gold") stations using nearby reference stations.

2. Use the completed gold stations to fill stations that only have measured flow.
"""

# Variables that can be copied (flow is never copied)

RAW_VARIABLES = [

    "temperature",

    "ammonia",

    "bod",

    "tss",

    "alkalinity",

    "oxygen",

    "nitrate",

    "pH",

]

# PASS 1
# Complete the stations that already contain observations
PARTIAL_STATIONS = {

    "Annacis": [
        "Lulu",
        "Lions Gate",
    ],

    "Lulu": [
        "Annacis",
        "Lions Gate",
    ],

    "Lions Gate": [
        "Annacis",
        "Lulu",
    ],

    "McLoughlin Point": [
        "Saanich Peninsula",
        "Magic Lake",
    ],

    "Saanich Peninsula": [
        "McLoughlin Point",
        "Magic Lake",
    ],

    "Magic Lake": [
        "Saanich Peninsula",
        "McLoughlin Point",
    ],

    "Greater Nanaimo": [
        "French Creek",
        "Nanoose Bay",
        "Duke Point",
    ],

    "French Creek": [
        "Greater Nanaimo",
        "Nanoose Bay",
        "Duke Point",
    ],

    "Nanoose Bay": [
        "French Creek",
        "Greater Nanaimo",
        "Duke Point",
    ],

    "Duke Point": [
        "Greater Nanaimo",
        "French Creek",
        "Nanoose Bay",
    ],

}

# PASS 2
# Stations with only flow

FLOW_ONLY_STATIONS = {

    # Metro Vancouver
    "Riverport": "Annacis",

    # Capital Regional District
    "Clover Point": "McLoughlin Point",
    "Macaulay Point": "McLoughlin Point",
    "William Head": "McLoughlin Point",

    # Vancouver Island
    "Campbell River STP": "French Creek",
    "Cumberland": "French Creek",
    "Comox": "French Creek",
    "Sooke": "McLoughlin Point",

    # Sunshine Coast
    "Town of Gibsons": "Lions Gate",
    "Squamish": "Lions Gate",
    "Sechelt Water Resource Centre": "Greater Nanaimo",

    # qathet
    "Westview": "French Creek",
    "Powell River Townsite": "Westview",
    "Lund": "Westview",
    "Wildwood": "Westview",
    "Gillies Bay": "Westview",
    "Van Anda": "Westview",

    # Small districts
    "Snug Cove": "Lions Gate",
    "Citrus Wynd": "Lions Gate",
    "Sundowner": "Greater Nanaimo",
    "Quathiaski Cove": "French Creek",

    # First Nations
    "Sliammon": "Westview",
    "Nanoose FN": "Nanoose Bay",
    "Tsawout": "Saanich Peninsula",
    "SnawnNaw-As": "Nanoose Bay",
    "Cape Mudge Band": "French Creek",
    "Tsawwassen": "Annacis",

    # Federal
    "Rocky Point": "McLoughlin Point",
    "BC Ferries Terminals": "French Creek",

}


def copy_missing_variables(station, reference):

    """
    Copy only variables that are missing.
    """

    for variable in RAW_VARIABLES:

        if variable in station.raw:
            continue

        if variable not in reference.raw:
            continue

        station.raw[variable] = reference.raw[variable].copy()

        station.flags[variable] = f"Copied from {reference.name}"


# Main function

def fill_missing(database):

    print()
    print("Completing reference stations...")

    # PASS 1

    for station_name, references in PARTIAL_STATIONS.items():

        station = database.get(station_name)

        for ref_name in references:

            reference = database.get(ref_name)

            copy_missing_variables(station, reference)

    print("Reference stations completed.")

    print()
    print("Filling flow-only stations...")

    # PASS 2

    for station_name, ref_name in FLOW_ONLY_STATIONS.items():

        station = database.get(station_name)

        reference = database.get(ref_name)

        copy_missing_variables(station, reference)

    print("Missing variables filled.")

    return database
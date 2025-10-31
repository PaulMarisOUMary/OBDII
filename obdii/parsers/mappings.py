from .pids import EnumeratedPIDS


FUEL_SYSTEM_STATUS = EnumeratedPIDS(
    {
        0: "The motor is off",
        1: "Open loop due to insufficient engine temperature",
        2: "Closed loop, using oxygen sensor feedback to determine fuel mix",
        4: "Open loop due to engine load OR fuel cut due to deceleration",
        8: "Open loop due to system failure",
        16: "Closed loop, using at least one oxygen sensor but there is a fault in the feedback system",
    }
)

SECONDARY_AIR_STATUS = EnumeratedPIDS(
    {
        1: "Upstream",
        2: "Downstream of catalytic converter",
        4: "From the outside atmosphere or off",
        8: "Pump commanded on for diagnostics",
    }
)

VEHICLE_STANDARDS = EnumeratedPIDS(
    {
        1: "OBD-II as defined by the CARB",
        2: "OBD as defined by the EPA",
        3: "OBD and OBD-II",
        4: "OBD-I",
        5: "Not OBD compliant",
        6: "EOBD (Europe)",
        7: "EOBD and OBD-II",
        8: "EOBD and OBD",
        9: "EOBD, OBD and OBD II",
        10: "JOBD (Japan)",
        11: "JOBD and OBD II",
        12: "JOBD and EOBD",
        13: "JOBD, EOBD, and OBD II",
        14: "Reserved",
        15: "Reserved",
        16: "Reserved",
        17: "Engine Manufacturer Diagnostics (EMD)",
        18: "Engine Manufacturer Diagnostics Enhanced (EMD+)",
        19: "Heavy Duty On-Board Diagnostics (Child/Partial) (HD OBD-C)",
        20: "Heavy Duty On-Board Diagnostics (HD OBD)",
        21: "World Wide Harmonized OBD (WWH OBD)",
        22: "Reserved",
        23: "Heavy Duty Euro OBD Stage I without NOx control (HD EOBD-I)",
        24: "Heavy Duty Euro OBD Stage I with NOx control (HD EOBD-I N)",
        25: "Heavy Duty Euro OBD Stage II without NOx control (HD EOBD-II)",
        26: "Heavy Duty Euro OBD Stage II with NOx control (HD EOBD-II N)",
        27: "Reserved",
        28: "Brazil OBD Phase 1 (OBDBr-1)",
        29: "Brazil OBD Phase 2 (OBDBr-2)",
        30: "Korean OBD (KOBD)",
        31: "India OBD I (IOBD I)",
        32: "India OBD II (IOBD II)",
        33: "Heavy Duty Euro OBD Stage VI (HD EOBD-IV)",
        range(34, 250): "Reserved",
        range(251, 255): "Not available for assignment (SAE J1939 special meaning)",
    }
)

FUEL_TYPE_CODING = EnumeratedPIDS(
    {
        0: "Not available",
        1: "Gasoline",
        2: "Methanol",
        3: "Ethanol",
        4: "Diesel",
        5: "LPG",
        6: "CNG",
        7: "Propane",
        8: "Electric",
        9: "Bifuel running Gasoline",
        10: "Bifuel running Methanol",
        11: "Bifuel running Ethanol",
        12: "Bifuel running LPG",
        13: "Bifuel running CNG",
        14: "Bifuel running Propane",
        15: "Bifuel running Electricity",
        16: "Bifuel running electric and combustion engine",
        17: "Hybrid gasoline",
        18: "Hybrid Ethanol",
        19: "Hybrid Diesel",
        20: "Hybrid Electric",
        21: "Hybrid running electric and combustion engine",
        22: "Hybrid Regenerative",
        23: "Bifuel running diesel",
    }
)

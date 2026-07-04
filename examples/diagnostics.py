from obdii import Connection, commands

description = """Read Diagnostic Trouble Codes (DTCs) from the vehicle."""

# Replace this with your actual port
PORT = "/dev/ttyUSB0"

# Connect to the adapter
with Connection(PORT) as conn:
    # Query vehicle's DTCs
    response = conn.query(commands.GET_DTC)

    dtcs = response.value
    if not dtcs:
        print("No DTCs found.")
    else:
        print(f"Found {len(dtcs)} DTC(s):")
        for dtc in dtcs:
            print(f"DTC: {dtc.code} | {dtc.category} {dtc.scope} {dtc.system}")

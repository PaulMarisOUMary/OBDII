from obdii import Connection, at_commands, commands

description = """Basic connection and query example."""

# Replace this with your actual port
PORT = "COM5"

# Connect to the adapter
with Connection(PORT) as conn:
    # Query adapter firmware version
    version = conn.query(at_commands.VERSION_ID)
    print(f"Version: {version.value}")

    # Query vehicle's engine speed (rpm)
    response = conn.query(commands.ENGINE_SPEED)
    print(f"Engine Speed: {response.value} {response.units}")

from obdii import Connection, at_commands, commands

description = """Simple interaction with an OBD device.
Demonstrates different approaches to query commands."""


# Establish a connection to the serial port (e.g., COM5)
conn = Connection("COM5")


# Query the ELM327 version using an AT command
version = conn.query(at_commands.VERSION_ID)

print(f"Version: {version.value}")


# Different ways to request data
# 1. Using a command directly
response = conn.query(commands.ENGINE_SPEED)
print(f"1. Base command: {response.value} {response.units} (Engine speed)")

# 2. Using the command name
response = conn.query(commands["ENGINE_SPEED"])
print(f"2. Command name: {response.value} {response.units} (Engine speed)")

# 3. Using the Mode and PID
response = conn.query(commands[1][0x0C])
print(f"3. Mode and PID: {response.value} {response.units} (Engine speed)")


# Close the connection
conn.close()
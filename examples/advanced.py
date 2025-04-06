from csv import DictWriter
from datetime import datetime
from logging import FileHandler, DEBUG, getLogger
from time import time, sleep

from obdii import Connection, Protocol, at_commands, commands
from obdii.errors import InvalidCommandError

description = """ Connects to an OBD device through serial port, using custom and advanced startup.
Fetch and log a batch of specified commands every second in a CSV."""


# File logging
file_handler = FileHandler("obdii.log")
obdii_logger = getLogger("obdii")

port = "COM5"  # Replace with the actual serial port

# Commands to log every second
batch_cmd = [
    commands.ENGINE_SPEED,
    commands.VEHICLE_SPEED,
    commands.ENGINE_OIL_TEMP,
    commands.ENGINE_COOLANT_TEMP,
]
max_runtime = 15
csv_file = "obd_data.csv"

with Connection(
        port=port,
        protocol = Protocol.ISO_15765_4_CAN,
        auto_connect = False,
        early_return = True,

        log_handler = file_handler,
        log_level = DEBUG,
    ) as conn:
    # Override the default init_sequence
    conn.init_sequence = [
        at_commands.RESET,
        at_commands.ECHO_OFF,
        at_commands.HEADERS_ON,
        at_commands.MEMORY_OFF,
        at_commands.SET_PROTOCOL(0), # Usage of command argument(s)
        conn._auto_protocol, # Detect and set required protocol if available
    ]

    # Advanced use of the connect method
    conn.connect(
        baudrate = 38400,
        timeout = 10,
    )

    # Write in a csv cmds values within the max_runtime
    with open(csv_file, 'w', newline='') as file:
        cmd_keys = [cmd.name for cmd in batch_cmd]
        fieldnames = ["timestamp"] + cmd_keys
        writer = DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        start_time = time()
        while conn.is_connected() and (time() - start_time) < max_runtime:
            log_entry = dict.fromkeys(cmd_keys, None)
            log_entry["timestamp"] = datetime.now().isoformat()

            for cmd in batch_cmd:
                try:
                    response = conn.query(cmd)
                    log_entry[cmd.name] = response.value
                except InvalidCommandError:
                    obdii_logger.warning(f"{cmd.name} seems not to be supported.")

            writer.writerow(log_entry)
            sleep(1)
.. title:: Usage

.. meta::
    :description: Basic usage of the py-obdii library.
    :keywords: py-obdii, py-obd2, obdii, obd2, quickstart, setup
    :robots: index, follow

.. _usage:

Basic Usage
===========

Scan for devices
----------------

Find your OBDII devices before you start. It could be connected via serial or WiFi.  
The :mod:`obdii.utils.scan` module makes this easy by scanning for available devices.

.. note::

    Not sure which function to use ? Check :ref:`port-guide`.

.. code-block:: python
    :caption: main.py
    :linenos:

    from obdii.utils.scan import scan_ports, scan_wifi

    # Scan for devices connected via serial ports
    ports = scan_ports()
    print("Available OBDII devices:", ports)

    # Scan for devices connected via WiFi
    wifi_devices = scan_wifi()
    print("Available OBDII WiFi devices:", wifi_devices)

AT Commands
-----------

AT commands are special commands you send directly to the OBDII adapter.
They let you configure it or retrieve information for/from the adapter.

.. code-block:: python
    :caption: main.py
    :linenos:

    from obdii import at_commands

    # AT Command example, get the version ID of the adapter
    at_commands.VERSION_ID

Commands
--------

Commands are predefined instructions to request data from the vehicle, like engine speed, coolant temperature, DTC, etc.
There are three different ways of using commands.

.. code-block:: python
    :caption: main.py
    :linenos:

    from obdii import commands

    # 1. Using a command directly
    commands.ENGINE_SPEED

    # 2. Using the command name
    commands["ENGINE_SPEED"]

    # 3. Using the Mode and PID
    commands[0x01][0x0C]

    # These three lines are equivalent
    # and all return the same command object:
    # <Command Mode.REQUEST 0C ENGINE_SPEED []>

Query data
----------

To read real-time data, you need an :class:`obdii.Connection` to the device.
Once connected, you can send commands and get responses from your car.

.. code-block:: python
    :caption: main.py
    :linenos:

    from obdii import Connection, at_commands, commands
    from obdii.utils.scan import scan_ports

    # Find first available OBDII device connected via serial
    ports = scan_ports(return_first=True)
    if not ports:
        raise ValueError("No OBDII devices found.")

    # Connect to the device and query engine speed
    with Connection(ports[0]) as conn:
        version = conn.query(at_commands.VERSION_ID)
        print(f"Version: {version.value}")

        response = conn.query(commands.ENGINE_SPEED)
        print(f"Engine Speed: {response.value} {response.unit}")
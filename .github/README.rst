OBDII
=====

.. image:: https://img.shields.io/pypi/v/py-obdii?label=pypi&logo=pypi&logoColor=white&link=https%3A%2F%2Fpypi.org%2Fproject%2Fpy-obdii
    :target: https://pypi.org/project/py-obdii
    :alt: PyPI version
.. image:: https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FPaulMarisOUMary%2FOBDII%2Fmain%2Fpyproject.toml&logo=python&logoColor=white&label=python
    :target: https://pypi.org/project/py-obdii
    :alt: Python Version from PEP 621 TOML
.. image:: https://img.shields.io/github/actions/workflow/status/PaulMarisOUMary/OBDII/ci-pytest.yml?branch=main&label=tests&logoColor=white&logo=pytest
    :target: https://github.com/PaulMarisOUMary/OBDII/actions/workflows/ci-pytest.yml
    :alt: PyTest CI status
.. image:: https://img.shields.io/readthedocs/py-obdii/latest?logo=readthedocs&logoColor=white&label=docs&link=https%3A%2F%2Fpy-obdii.rtfd.io
    :target: https://py-obdii.rtfd.io/en/latest
    :alt: Documentation Status (ReadTheDocs)
.. image:: https://img.shields.io/discord/1437417392144912467?logo=discord&logoColor=white&label=discord&color=%235865f2&link=https%3A%2F%2Fdiscord.gg%2Fvn9bHUxeYB
    :target: https://discord.gg/vn9bHUxeYB
    :alt: Discord Support Server invite

Overview
--------

Connect to any vehicle through its `OBDII <https://en.wikipedia.org/wiki/On-board_diagnostics#OBD-II>`_ port and start reading real-time data from Python in a few lines of code.

Plug in a USB, Bluetooth, WiFi or Ethernet adapter, then query engine speed, fault codes, fuel level, VIN, and much more.

Whether you're building a diagnostic tool, a performance data logger, a custom dashboard, a smart home integration, or just learning how vehicles communicate, this library handles the complexity of vehicle communication, so you don't have to.

Usage Example
-------------

.. code-block:: python

    from obdii import Connection, at_commands, commands
    from obdii.utils.scan import scan_ports

    # Find first available OBDII device connected via serial
    ports = scan_ports(return_first=True)
    if not ports:
        raise ValueError("No OBDII devices found.")

    # Connect to the adapter
    with Connection(ports[0]) as conn:
        # Query adapter firmware version
        version = conn.query(at_commands.VERSION_ID)
        print(f"Version: {version.value}")

        # Query vehicle's engine speed (rpm)
        response = conn.query(commands.ENGINE_SPEED)
        print(f"Engine Speed: {response.value} {response.units}")

More examples in the `examples folder <https://github.com/PaulMarisOUMary/OBDII/tree/main/examples>`_ and `Usage Guide <https://py-obdii.readthedocs.io/en/latest/usage.html>`_.

Installation
------------

Python 3.8 or higher is required.

Install from PyPI using pip:

.. code-block:: console

    pip install py-obdii

For more installation options, see the `Installation Guide <https://py-obdii.readthedocs.io/en/latest/installation.html>`_.

Emulator Support
----------------

You don't need a physical OBDII device to start developing.

You can use the `ELM327-Emulator <https://pypi.org/project/ELM327-emulator>`_ library to simulate an OBDII adapter and vehicle responses.

Setting Up the ELM327-Emulator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Install the library with the ``sim`` extra options:

    .. code-block:: console

        pip install py-obdii[sim]

#. Start the ELM327-Emulator:

    .. code-block:: console

        python -m elm -p "REPLACE_WITH_PORT" -s car --baudrate 38400

    .. note::

        Replace ``REPLACE_WITH_PORT`` with the serial port of your choice

For platform-specific instructions, see the `Emulating a Vehicle <https://py-obdii.readthedocs.io/en/latest/emulator.html>`_ guide.

Hardware Requirements
---------------------

For real-world usage, an ELM327-compatible OBDII adapter is required to connect to your vehicle.

- **USB**: reliable, plug and play
- **Ethernet**: reliable, low latency
- **Bluetooth**: wireless, convenient
- **WiFi**: wireless, mobile compatible

More information on connecting to different adapter types can be found in the `Connection Guide <https://py-obdii.readthedocs.io/en/latest/connection.html>`_.

Compatibility
-------------

All ELM327 protocols are supported, covering vehicles from the
mid-1990s through today.

Protocol Support
^^^^^^^^^^^^^^^^

===== ================ ========================
ID    Protocol         Specifications          
===== ================ ========================
0x01  SAE J1850 PWM    41.6 Kbaud              
0x02  SAE J1850 VPW    10.4 Kbaud              
0x03  ISO 9141-2       5 baud init, 10.4 Kbaud 
0x04  ISO 14230-4 KWP  5 baud init, 10.4 Kbaud 
0x05  ISO 14230-4 KWP  fast init, 10.4 Kbaud   
0x06  ISO 15765-4 CAN  11 bit ID, 500 Kbaud    
0x07  ISO 15765-4 CAN  29 bit ID, 500 Kbaud    
0x08  ISO 15765-4 CAN  11 bit ID, 250 Kbaud    
0x09  ISO 15765-4 CAN  29 bit ID, 250 Kbaud    
0x0A  SAE J1939 CAN    29 bit ID, 250 Kbaud    
0x0B  USER1 CAN        11 bit ID, 125 Kbaud    
0x0C  USER2 CAN        11 bit ID, 50 Kbaud     
===== ================ ========================

Support & Contact
-----------------

Found a bug?

- `Open an Issue <https://github.com/PaulMarisOUMary/OBDII/issues>`_

Have a question?

- `Join the Discussion <https://github.com/PaulMarisOUMary/OBDII/discussions>`_
- `Discord Support Server <https://discord.gg/vn9bHUxeYB>`_

Your feedback is greatly appreciated and helps improve this project.

-------

Follow our updates by leaving a star to this repository!
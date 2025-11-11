.. title:: Connection Guide

.. meta::
    :description: Connection Guide for py-obdii.
    :keywords: py-obdii, py-obd2, obdii, obd2, quickstart, setup
    :robots: index, follow

.. |contribute-button| replace::

    Untested, help us improve this part of the documentation. :bdg-link-success:`Contribute <https://github.com/PaulMarisOUMary/OBDII/edit/main/docs/source/connection.rst>`

.. _connection:

Connection
==========

This guide explains how to connect the library to different types of OBDII adapters and start communicating with your vehicle.

Understanding Adapters
----------------------

An OBDII adapter is a small physical device that acts as a bridge between your vehicle's diagnostic port and your computer, Raspberry Pi, smartphone, etc..

It plugs into the vehicle's OBDII diagnostic port (female connector), usually found under the dashboard or near the steering wheel, you can check online for your vehicle's exact location.

It converts the car's data signals into a standard format that our library can read.

The image below shows a male OBDII connector, which is the adapter side that plugs into your vehicle's diagnostic port.

.. image:: assets/adapters/obdii-connector.webp
    :alt: OBDII male connector
    :scale: 50%
    :align: center

Connect your Adapter
--------------------

The library can connect to adapters via several methods, including:

- **Serial**: :ref:`USB <conn-usb>` and :ref:`Bluetooth <conn-bluetooth>`
- **Network**: :ref:`WiFi <conn-network>` and :ref:`Ethernet <conn-network>`

.. _conn-usb:

Connecting via USB
^^^^^^^^^^^^^^^^^^

Use this method if your adapter connects via USB cable.

.. tab-set::
    :sync-group: os

    .. tab-item:: Linux
        :sync: linux

        #. Identify the USB serial port:

            .. code-block:: console

                $ dmesg | grep tty

            .. note::

                You can also list available USB serial devices with:

                .. code-block:: console

                    $ ls /dev/ttyUSB*

        #. Chose the correct port from the output (e.g., ``/dev/ttyUSB0``).

        #. Use this port for connecting.
        
            .. dropdown:: Connection example
                :open:
                :chevron: down-up
                :icon: quote

                .. code-block:: python
                    :caption: main.py
                    :linenos:
                    :emphasize-lines: 3

                    from obdii import Connection, at_commands

                    with Connection("/dev/ttyUSB0") as conn:
                        version = conn.query(at_commands.VERSION_ID)
                        print(f"Adapter Version: {version.value}")

    .. tab-item:: Windows
        :sync: windows

        |contribute-button|
    
    .. tab-item:: macOS
        :sync: macos

        |contribute-button|

.. _conn-bluetooth:

Connecting via Bluetooth
^^^^^^^^^^^^^^^^^^^^^^^^

Use this method if your adapter communicates wirelessly over Bluetooth.

.. tab-set::
    :sync-group: os

    .. tab-item:: Linux
        :sync: linux

        #. Open the Bluetooth control terminal:

            .. code-block:: console

                $ bluetoothctl

        #. Power on Bluetooth, and pair with the adapter:

            .. code-block:: console

                power on
                agent on
                default-agent
                scan on
                pair 00:00:00:00:00:00
                trust 00:00:00:00:00:00
                exit

        #. Bind the adapter to an RFCOMM port:

            .. code-block:: console

                $ rfcomm bind /dev/rfcomm0 00:00:00:00:00:00
            
            .. note::
                Replace ``00:00:00:00:00:00`` with the MAC address of the adapter, which should appear after running ``scan on``.
        
        #. Use the ``/dev/rfcomm0`` port for connecting.

            .. dropdown:: Connection example
                :open:
                :chevron: down-up
                :icon: quote

                .. code-block:: python
                    :caption: main.py
                    :linenos:
                    :emphasize-lines: 3

                    from obdii import Connection, at_commands

                    with Connection("/dev/rfcomm0") as conn:
                        version = conn.query(at_commands.VERSION_ID)
                        print(f"Adapter Version: {version.value}")

    .. tab-item:: Windows
        :sync: windows

        |contribute-button|
    
    .. tab-item:: macOS
        :sync: macos

        |contribute-button|

.. _conn-network:

Connecting via Network (WiFi/Ethernet)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use this method if your adapter connects over a network.  
WiFi and Ethernet adapters use the same network transport.

.. tab-set::
    :sync-group: os

    .. tab-item:: Linux
        :sync: linux

        #. Connect to the adapter's WiFi network or plug in via Ethernet.

        #. Determine the adapter's IP address and port.
        
            Common default IP address and port combinations:

            .. table::
                :widths: 33 33 33
                :align: left

                =================  ========== ===============
                Address            Port       Device
                =================  ========== ===============
                ``192.168.0.10``   ``35000``  Generic
                ``192.168.1.10``   ``35000``  Clones
                =================  ========== ===============

            .. note::
                These values may vary depending on the adapter. Refer to the adapter's documentation for the correct IP address and port.
        
        #. Use the IP address and port for connecting.

            .. dropdown:: Connection example
                :open:
                :chevron: down-up
                :icon: quote

                .. code-block:: python
                    :caption: main.py
                    :linenos:
                    :emphasize-lines: 3

                    from obdii import Connection, at_commands

                    with Connection(("192.168.0.10", 35000)) as conn:
                        version = conn.query(at_commands.VERSION_ID)
                        print(f"Adapter Version: {version.value}")

    .. tab-item:: Windows
        :sync: windows

        |contribute-button|

    .. tab-item:: macOS
        :sync: macos

        |contribute-button|
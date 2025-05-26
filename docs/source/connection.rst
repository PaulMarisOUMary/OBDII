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

.. _conn-usb:

Connecting via USB
^^^^^^^^^^^^^^^^^^

.. tab-set::
    :sync-group: os

    .. tab-item:: Linux
        :sync: linux

        - To identify the USB serial port, run:

            .. code-block:: console

                $ dmesg | grep tty

        - You can also list available USB serial devices with:

            .. code-block:: console

                $ ls /dev/ttyUSB*

        Multiple ports may appear in the output of these commands, the serial port to use for the connection will be one of them.

        .. dropdown:: Connection example
            :open:
            :chevron: down-up
            :icon: quote

            .. code-block:: python
                :caption: main.py
                :linenos:
                :emphasize-lines: 3

                from obdii import Connection

                conn = Connection("/dev/ttyUSB0")

    .. tab-item:: Windows
        :sync: windows

        |contribute-button|

.. _conn-bluetooth:

Connecting via Bluetooth
^^^^^^^^^^^^^^^^^^^^^^^^

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

        #. Bind the RFCOMM port:

            .. code-block:: console

                $ rfcomm bind /dev/rfcomm0 00:00:00:00:00:00
            
            .. note::
                Replace ``00:00:00:00:00:00`` with the MAC address of the adapter, which should appear after running ``scan on``.
        
        #. The connection is now available at ``/dev/rfcomm0``. Use this port for connecting.

        .. dropdown:: Connection example
            :open:
            :chevron: down-up
            :icon: quote

            .. code-block:: python
                :caption: main.py
                :linenos:
                :emphasize-lines: 3

                from obdii import Connection

                conn = Connection("/dev/rfcomm0")

    .. tab-item:: Windows
        :sync: windows

        |contribute-button|

.. _conn-wifi:

Connecting via WiFi
^^^^^^^^^^^^^^^^^^^

.. tab-set::
    :sync-group: os

    .. tab-item:: Linux
        :sync: linux

        #. Turn on the WiFi adapter and connect to its WiFi network.

        #. Common default IP address and port combinations:
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
        
        .. dropdown:: Connection example
            :open:
            :chevron: down-up
            :icon: quote

            .. code-block:: python
                :caption: main.py
                :linenos:
                :emphasize-lines: 3

                from obdii import Connection

                conn = Connection(("192.168.0.10", 35000))

    .. tab-item:: Windows
        :sync: windows

        |contribute-button|
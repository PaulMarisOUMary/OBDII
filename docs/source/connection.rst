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
        
        #. The connection is now available at ``/dev/rfcomm0``. Use this port for connecting.
        
        .. note::
            Replace ``00:00:00:00:00:00`` with the MAC address of the adapter, which should appear after running ``scan on``.

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

        |contribute-button|

    .. tab-item:: Windows
        :sync: windows

        |contribute-button|
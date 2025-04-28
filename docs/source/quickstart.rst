.. title:: Quickstart

.. meta::
    :description: Quickstart instructions for py-obdii.
    :keywords: py-obdii, py-obd2, obdii, obd2, quickstart, setup
    :robots: index, follow

.. _quickstart:

Quickstart
==========

This page provides a quick introduction to the library.
It assumes you have the library installed, if not check the :ref:`installation` section.

.. _minimal-example:

Minimal Example
---------------

.. code-block:: python
    :caption: main.py
    :linenos:
    :emphasize-lines: 3

    from obdii import at_commands, commands, Connection

    conn = Connection("PORT")

    response = conn.query(commands.VEHICLE_SPEED)
    print(f"Vehicle Speed: {response.value} {response.units}")

    conn.close()

.. note::
    Replace ``"PORT"`` with the appropriate port.
    Refer to the :ref:`port-guide` section below.

You can find more detailed examples and usage scenarios in the `repository <https://github.com/PaulMarisOUMary/OBDII/tree/main/examples>`_.

.. _port-guide:

Determining Your Port
---------------------

Scenario 1: With a Car and OBDII Adapter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:bdg-success-line:`Car` + :bdg-success-line:`OBDII Adapter`

If you're connecting to a real vehicle, you'll need to find the port your adapter is using (Bluetooth, USB, or WiFi).

Refer to the :ref:`connection` page for detailed instructions.

Scenario 2: Without a Car or OBDII Adapter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:bdg-secondary-line:`No Car` • :bdg-secondary-line:`No Adapter`

You can emulate an OBDII environment using an emulator.

Refer to the :ref:`emulator` page for setup instructions and usage details.
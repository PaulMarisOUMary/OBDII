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

    from obdii import commands, Connection

    with Connection("PORT") as conn:
        response = conn.query(commands.ENGINE_SPEED)
        print(f"Engine Speed: {response.value} {response.units}")

.. note::
    Replace ``"PORT"`` with the appropriate port.
    Refer to the :ref:`port-guide` section below.

You can find more detailed examples and usage scenarios in the `repository <https://github.com/PaulMarisOUMary/OBDII/tree/main/examples>`_.

.. _port-guide:

Determining Your Port
---------------------

Scenario 1: :bdg-secondary-line:`No Car` or :bdg-secondary-line:`No Adapter`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you don't have access to a car or an OBDII adapter, or simply want to develop
without having to be in your car, you can simulate an OBDII environment using an emulator.

Refer to the :ref:`emulator` page for setup instructions and usage details.

Scenario 2: :bdg-success-line:`Car` and :bdg-success-line:`OBDII Adapter`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To connect to a real vehicle, make sure you have both a car and a compatible OBDII adapter.
Next, you'll need to find the port your adapter is using (Bluetooth, USB, or WiFi).

Refer to the :ref:`connection` page for detailed instructions.
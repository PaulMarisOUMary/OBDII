.. title:: Quickstart

.. meta::
    :description: Quickstart instructions for py-obdii.
    :keywords: py-obdii, py-obd2, obdii, obd2, quickstart, setup
    :robots: index, follow

.. _quickstart:

Quickstart
==========

This page helps you get started quickly with the library.
It assumes the library is already installed, if not check the :ref:`installation` section.

Overview
--------

This library can operate in two main scenarios:

#. :ref:`Simulated Environment <scenario-1>`: No car or adapter needed, ideal for development and testing.

#. :ref:`Real Vehicle Connection <scenario-2>`: Connects to an actual car using an OBDII adapter.

Internally, both scenarios works the same way, your code remains the same, so you can switch between scenarios seamlessly. The only difference is the port you provide when establishing the connection.

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
    See :ref:`port-guide` section below.

You can find more detailed examples and usage scenarios in the `repository <https://github.com/PaulMarisOUMary/OBDII/tree/main/examples>`_.

.. _port-guide:

Determining Your Port
---------------------

.. _scenario-1:

Scenario 1: :bdg-secondary-line:`No Car` or :bdg-secondary-line:`No Adapter`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This scenario is ideal for development, it doesn't require any physical OBDII adapter or vehicle.

Refer to the :ref:`emulator` page for setup instructions and usage details.

.. _scenario-2:

Scenario 2: :bdg-success-line:`Car` and :bdg-success-line:`OBDII Adapter`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This scenario is ideal for real-world applications, it connects to an actual vehicle via a physical OBDII adapter.

As mentioned, you will need:

#. A vehicle with an OBDII port (most vehicles manufactured after 1996 have one).
#. An OBDII adapter.

Refer to the :ref:`connection` page for detailed instructions and more information on adapters.
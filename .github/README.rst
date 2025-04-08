OBDII
=====

.. image:: https://img.shields.io/pypi/v/py-obdii?label=pypi&logo=pypi&logoColor=white&link=https%3A%2F%2Fpypi.org%2Fproject%2Fpy-obdii
    :target: https://pypi.org/project/py-obdii/
    :alt: PyPI version
.. image:: https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FPaulMarisOUMary%2FOBDII%2Fmain%2Fpyproject.toml&logo=python&logoColor=white&label=python
    :target: https://pypi.org/project/py-obdii/
    :alt: Python Version from PEP 621 TOML
.. image:: https://img.shields.io/github/actions/workflow/status/PaulMarisOUMary/OBDII/ci-pytest.yml?branch=main&label=pytest&logoColor=white&logo=pytest
    :target: https://pypi.org/project/py-obdii/
    :alt: PyTest

A modern, easy to use, Python ≥3.8 library for interacting with OBDII devices.

Installing
----------

Python 3.8 or higher is required.

A `Virtual Environment <https://docs.python.org/3/library/venv.html>`_ is recommended to install the library.

.. code-block:: bash

    # Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate

    # Windows
    py -3 -m venv .venv
    .venv\Scripts\activate

Install from PyPI
^^^^^^^^^^^^^^^^^

.. code-block:: bash

    pip install py-obdii

Install the development version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # From Github
    pip install git+https://github.com/PaulMarisOUMary/OBDII@main[dev,test]

    # From local source
    git clone https://github.com/PaulMarisOUMary/OBDII
    cd OBDII
    pip install .[dev,test]

    # From test.pypi.org
    pip install -i https://test.pypi.org/simple/ py-obdii

Usage Example
-------------

.. important::

    This library is still in the design phase and may change in the future.

.. code-block:: python

    from obdii import at_commands, commands, Connection

    conn = Connection("COM5")

    version = conn.query(at_commands.VERSION_ID)
    print(f"Version: {version.value}")

    response = conn.query(commands.VEHICLE_SPEED)
    print(f"Vehicle Speed: {response.value} {response.units}")

    conn.close()

You can find more detailed examples and usage scenarios in the `examples folder <https://github.com/PaulMarisOUMary/OBDII/tree/main/examples>`_ of this repository.

Using the Library Without a Physical Device
-------------------------------------------

To streamline the development process, you can use the `ELM327-Emulator <https://pypi.org/project/ELM327-emulator>`_ library. This allows you to simulate an OBDII connection without needing a physical device.

Setting Up the ELM327-Emulator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Install the library with "dev" extra options**:

    .. code-block:: bash

        pip install py-obdii[dev]

2. **Start the ELM327-Emulator**:

    .. code-block:: bash

        python -m elm -p "REPLACE_WITH_PORT" -s car --baudrate 38400

.. note::

    Replace ``REPLACE_WITH_PORT`` with the serial port of your choice

Use Virtual Ports on Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For Windows users, you can use `com0com <https://com0com.sourceforge.net>`_ to create virtual serial ports and connect the ELM327-Emulator to your Python code.

1. **Install com0com** and create two virtual serial ports, (e.g. ``COM5`` and ``COM6``).

2. In the **ELM327-Emulator**, set the port to ``COM6``.

3. In your **Python code**, set the connection port to ``COM5``.

Contributing & Development
--------------------------

The development of this library follows the `ELM327 PDF </docs/ELM327.PDF>`_ provided by Elm Electronics, with the goal of implementing most features and commands as outlined, starting from page 6 of the document.

This library aims to deliver robust error handling, comprehensive logging, complete type hinting support, and follow best practices to create a reliable tool.

Please, feel free to contribute and share your feedback !

Testing the Library with Pytest
-------------------------------

This library uses `pytest <https://docs.pytest.org/>`_ for testing. To run the tests, you need to install the library with the ``[test]`` extra option.

1. **Install the library with "test" extra options**:

    .. code-block:: bash

        pip install py-obdii[test]

2. **Run tests**:

    .. code-block:: bash

        pytest

Support & Contact
-----------------

For questions or support, open an issue or start a discussion on GitHub.
Your feedback and questions are greatly appreciated and will help improve this project !

- `Open an Issue <https://github.com/PaulMarisOUMary/OBDII/issues>`_
- `Join the Discussion <https://github.com/PaulMarisOUMary/OBDII/discussions>`_

-------

Thank you for using or contributing to this project.
Follow our updates by leaving a star to this repository !
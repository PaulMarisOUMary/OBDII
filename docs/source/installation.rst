.. title:: Installation Guide

.. meta::
    :description: Installation instructions for py-obdii.
    :keywords: py-obdii, py-obd2, obdii, obd2, installation, setup, requirements, virtual environment, dependencies, extras
    :robots: index, follow

.. _installation:

Installation
============

Welcome to the installation guide for this library !
This guide will help you set up the library on your system.

Setup
-----

Prepare your environment and ensure all requirements are met before installing the library.

.. _requirements:

Requirements
^^^^^^^^^^^^

* Python 3.8 or higher

.. _venv:

Virtual Environment
^^^^^^^^^^^^^^^^^^^

A `Virtual Environment <https://docs.python.org/3/library/venv.html>`_ is always recommended as it keeps your projects dependencies isolated from other Python projects. This helps to avoid conflicts with other packages or libraries.

.. tab-set::
    :sync-group: os

    .. tab-item:: Linux/macOS
        :sync: unix

        .. code-block:: console

            $ python3 -m venv .venv
            $ source .venv/bin/activate

    .. tab-item:: Windows
        :sync: windows

        .. code-block:: console

            py -3 -m venv .venv
            .venv\Scripts\activate

.. tip::
    To deactivate the virtual environment later, simply run ``deactivate`` in your terminal.

.. _installing:

Install the Library
-------------------

You can install the library from multiple sources. Choose the option that best fits your needs.

If unsure, you'll likely want to install it from PyPI.

From PyPI :bdg-success-line:`Recommended`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The easiest and recommended way to install the library, as it ensures you get the latest stable release.

.. code-block:: console

    pip install py-obdii

From GitHub
^^^^^^^^^^^

To get the latest features and bug fixes that haven't been released yet.

.. code-block:: console

    pip install git+https://github.com/PaulMarisOUMary/OBDII@main

From Source
^^^^^^^^^^^

If you want to contribute to the library or modify the source code.

.. code-block:: console

    git clone https://github.com/PaulMarisOUMary/OBDII
    cd OBDII
    pip install -e .

The ``-e`` flag installs the library in editable mode to modify the source code directly (ideal for contributors).

From PyPI Pre-release
^^^^^^^^^^^^^^^^^^^^^

To install the official latest pre-release version (beta, alpha, release candidate) from PyPI.

.. code-block:: console

    pip install --upgrade --pre py-obdii

From TestPyPI
^^^^^^^^^^^^^

To test pre-release versions before they're officially published on PyPI.

.. code-block:: console

    pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple py-obdii

.. _extras:

Optional Dependencies
---------------------

Depending on your use case, you may want to install additional dependencies to emulate vehicles, run tests, develop the library, or build documentation.

This is why this library provides extra sets of dependencies group for different use cases.

Available extras:

.. tab-set::

    .. tab-item:: sim

        Installs the `ELM327-Emulator <https://pypi.org/project/ELM327-emulator>`_ library and dependencies for data mocking and vehicle emulation.

        .. code-block:: console

            pip install py-obdii[sim]

    .. tab-item:: dev

        Installs development dependencies, including linters, formatters, and type checkers.

        .. code-block:: console

            pip install py-obdii[dev]

    .. tab-item:: test

        Required if you want to run unit tests or integration tests.

        .. code-block:: console

            pip install py-obdii[test]
    
    .. tab-item:: docs

        Useful if you plan to build the documentation with Sphinx or contribute to the docs.

        .. code-block:: console

            pip install py-obdii[docs]
    
    .. tab-item:: all

        Installs all extras at once.

        .. code-block:: console
    
            pip install py-obdii[sim,dev,test,docs]

Verify Installation
-------------------

After installation, you can verify that the library is installed correctly by running:

.. code-block:: console

    python -c "import obdii; print(obdii.__version__)"

This should print the version of the library you have installed, e.g. ``0.8.0b``.

Upgrade the Library
-------------------

To upgrade to the latest version of the library, use:

.. code-block:: console

    pip install --upgrade py-obdii
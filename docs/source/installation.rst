.. title:: Installation Guide

.. meta::
    :description: Installation instructions for py-obdii.
    :keywords: py-obdii, py-obd2, obdii, obd2, installation, setup, requirements, virtual environment, dependencies, extras
    :robots: index, follow

.. _installation:

Installation
============

Welcome to the installation guide of this library !
This document will help you set up the library on your system.

.. _requirements:

Requirements
------------

* Python 3.8 or higher

.. _venv:

Virtual Environment
-------------------

A `Virtual Environment <https://docs.python.org/3/library/venv.html>`_ is always recommended to avoid conflicts with other packages or libraries.

.. tab-set::
    :sync-group: os

    .. tab-item:: Linux
        :sync: linux

        .. code-block:: console

            $ python3 -m venv .venv
            $ source .venv/bin/activate

    .. tab-item:: Windows
        :sync: windows

        .. code-block:: console

            py -3 -m venv .venv
            .venv\Scripts\activate

.. _installing:

Installing the Library
----------------------

You can install the library from multiple sources. Choose the option that best fits your needs.

From PyPI :bdg-success-line:`Recommended`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The latest stable version can be installed from PyPI:

.. code-block:: console

    pip install py-obdii

From GitHub
^^^^^^^^^^^

Install the latest development version directly from GitHub:

.. code-block:: console

    pip install git+https://github.com/PaulMarisOUMary/OBDII@main

From Source
^^^^^^^^^^^

Alternatively, you can install the library directly from the source: 

.. code-block:: console

    git clone https://github.com/PaulMarisOUMary/OBDII
    cd OBDII
    pip install .

From TestPyPI
^^^^^^^^^^^^^

To try a pre-release or a test version, install from TestPyPI:

.. code-block:: console

    pip install -i https://test.pypi.org/simple py-obdii

.. _extras:

Optional Extras
---------------

This library provides extra sets of dependencies for specific tasks such as development, testing, and building the documentation.

To install additional dependencies, simply add ``[extra_here]`` after the method used to install the library, as mentioned in the :ref:`installing` section.

Available extras:

.. tab-set::

    .. tab-item:: dev

        Installs the `ELM327-Emulator <https://pypi.org/project/ELM327-emulator>`_ library and dependencies for development.

        .. code-block:: console

            pip install py-obdii[dev]
    
    .. tab-item:: test

        Required if you want to run unit tests or integration tests locally.

        .. code-block:: console

            pip install py-obdii[test]
    
    .. tab-item:: docs

        Useful if you plan to build the documentation with Sphinx or contribute to the docs.

        .. code-block:: console

            pip install py-obdii[docs]
    
    .. tab-item:: all

        Installs all extras at once.

        .. code-block:: console
    
            pip install py-obdii[dev,test,docs]
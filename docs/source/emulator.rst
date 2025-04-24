.. title:: Emulator

Simulated Vehicle Environment
=============================

Let's be honest, developing OBDII tools directly from your car isn't the most practical setup. For convenience (and comfort), we use a vehicle emulator during development. It lets you simulate real car responses from your desk, so you can test and build features without needing to be plugged into an actual vehicle every time.

This is especially handy when you're iterating quickly, writing tests, or just don't want to sit in the driveway with a laptop balanced on your knees.

.. card:: Prerequisites

    To simulate a vehicle without needing a real car, you can use the `ELM327-Emulator <https://pypi.org/project/ELM327-emulator>`_, a third-party tool included automatically when you install the library with the `dev` extra:

    .. code-block:: bash

        pip install py-obdii[dev]

    This emulator simulates a vehicle's responses and can be connected to just like a real car through a virtual serial port.

.. tab-set::

    .. tab-item:: Linux
    
        Run and use the emulator on Linux.

        #. Install the library with development dependencies

        #. Start the ELM327 Emulator.

            .. code-block:: bash

                python -m elm -s car --baudrate 38400
            
            The emulator will display the virtual port (e.g., /dev/pts/1) to use for connection.

        #. Connect your Python code to the emulator (e.g., /dev/pts/1):

            .. code-block:: python

                from obdii import Connection

                with Connection("/dev/pts/1", baudrate=38400) as conn:
                    # Your code here

    .. tab-item:: Windows

        To run and use the emulator on Windows, you will need to create virtual serial ports.

        #. Install the library with development dependencies

        #. Use a kernel-mode virtual serial port driver like `com0com <https://com0com.sourceforge.net>`_ to create virtual COM ports.

        #. Create a virtual COM port pair (e.g., COM5 ↔ COM6). These act like a physical cable between two serial devices.

        #. Start the ELM327 Emulator on one end of the virtual connection (e.g., COM6):

            .. code-block:: bash

                python -m elm -p COM6 -s car --baudrate 38400

            This command launches the emulator in *car simulation* mode on COM6.

        #. Connect your Python code to the other end of the virtual pair (e.g., COM5):

            .. code-block:: python

                from obdii import Connection

                with Connection("COM5", baudrate=38400) as conn:
                    # Your code here
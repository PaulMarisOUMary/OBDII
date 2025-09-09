Contributing
============

Thanks for considering contributing !

The following is a set of guidelines for contributing to the repository. These are guidelines, not hard rules.

Contribution of all kind are welcome: bug reports, new features, documentation improvements, tests, examples, etc.

Questions
---------

Generally questions are better suited in `GitHub Discussions <https://github.com/PaulMarisOUMary/OBDII/discussions/categories/q-a>`_.

Please do not use issues for questions. Most of them don't belong there unless they provide value to a larger audience.

Reference Documentation
-----------------------

When implementing features, you can refer to the official `ELM327 PDF </docs/ELM327.PDF>`_, starting from page 8.   
This document outlines standard behaviors, AT commands, protocols, etc.

Other technical references exist, but are behind paywalls and are not currently available. See `this <https://github.com/users/PaulMarisOUMary/projects/9?pane=issue&itemId=113877896>`_ and `this <https://github.com/users/PaulMarisOUMary/projects/9?pane=issue&itemId=114252340>`_ for more details.

Don't know where to start ?
---------------------------

If you want to contribute but aren't sure how to begin, here are some ways to get involved:

- Visit `Issues <https://github.com/PaulMarisOUMary/OBDII/issues>`_ to reproduce bugs, provide additional details, or suggest fixes.
- Review `Pull Requests <https://github.com/PaulMarisOUMary/OBDII/pulls>`_ to help with code reviews, testing, and feedback.
- Participate in `Discussions <https://github.com/PaulMarisOUMary/OBDII/discussions>`_.
- Improve existing documentation, add examples, or clarify explanations.
- Add new scripts in ``examples/`` to showcase library usage.
- Write tests for untested features and increase coverage.
- Implement new features or small improvements.
- Refactor code, improve type hints, and maintain consistency.

You can also check ongoing work and ideas in the `Repository Projects <https://github.com/PaulMarisOUMary/OBDII/projects>`_.

Starting with small contributions is encouraged, every little improvement helps.

Getting Started
---------------

#. Fork the repository.

#. Clone your fork locally:

    .. code-block:: console

        git clone https://github.com/<your-username>/OBDII
        cd OBDII

#. Create a new branch for your work:

    .. code-block:: console

        git checkout -b my-feature-branch

#. Create a `Virtual Environment <https://docs.python.org/3/library/venv.html>`_ (recommended):

    Linux/macOS

    .. code-block:: console

        python3 -m venv .venv
        source .venv/bin/activate

    Windows

    .. code-block:: console

        py -3 -m venv .venv
        .venv\Scripts\activate

#. Install the library with the ``[dev,test,docs]`` extra options:

    .. code-block:: console

        pip install -e .[dev,test,docs]

Bug Reports
-----------

Report bugs via `Issues <https://github.com/PaulMarisOUMary/OBDII/issues>`_.

Include the following to help us resolve them quickly:

- Search for existing issues to avoid duplicates.
- Provide a clear and descriptive title.
- Describe the steps to reproduce the issue, ideally with a minimal code snippet.
- Expected vs. actual behavior, what you thought would happen vs. what happened.
- Environment details, Python version, OS, OBDII device model, and install method.
- Full traceback and/or logs if applicable.

Incomplete bug reports may require follow-up questions and could be closed if not clarified.

Pull Requests
-------------

Before opening a pull request, please make sure that:

- Keep each PR focused on a single issue or feature.
- Reference related issues (e.g., "Fix #123").
- Ideally the code follows the existing style.

Commit Messages
---------------

- Use clear, descriptive commit messages in present tense (e.g., "Add feature X", not "Added feature X").
- Group related changes into single commits.
- Reference related issues in the description when applicable (e.g., "Fix #123").

Testing
-------

This library uses `pytest <https://docs.pytest.org/>`_ for testing.

Tests are located in the ``tests/`` folder.

Before opening a pull request, make sure that all tests pass:

.. code-block:: console

    pytest

Project Documentation
-------------

This library uses `Sphinx <https://www.sphinx-doc.org/>`_ for documentation.
If you add or change features, please updates the documentation accordingly.

Sources are located in ``docs/source/``.

To build and view the documentation locally, run:

.. code-block:: console

    sphinx-build -b html -j auto -a -n -T --keep-going docs/source docs/build/html

    python -m http.server --directory docs/build/html

-------

Your contributions make OBDII better and more reliable for everyone !
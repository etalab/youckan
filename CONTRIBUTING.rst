Contributing
============

YouCKAN is open-source and very open to contributions.

Submitting issues
-----------------

Issues are contributions in a way so don't hesitate
to submit reports on the `official bugtracker`_.

Provide as much informations as possible to specify the issues:

- the YouCKAN version used
- a stacktrace
- installed applications list
- ...


Submitting patches (bugfix, features, ...)
------------------------------------------

If you want to contribute some code:

1. fork the `official YouCKAN repository`_
2. create a branch with an explicit name (like ``my-new-feature`` or ``issue-XX``)
3. do your work in it
4. rebase it on the master branch from the official repository (cleanup your history by performing an interactive rebase)
5. submit your pull-request

There are some rules to follow:

- your contribution should be documented (if needed)
- your contribution should be tested and the test suite should pass successfully
- your code should be mostly PEP8 compatible with a 120 characters line length
- your contribution should support both Python 2 and 3 (use ``tox`` to test)

You need to install some dependencies to hack on YouCKAN:

.. code-block:: bash

    $ pip install -r requirements/all.pip

A fabfile is provided to simplify the common tasks:

.. code-block:: bash

    $ fab -l
    Available commands:

    coverage    Run the test suite with coverage
    datamig     Generate a south data migration for an application
    debug       Run Development server.
    dist        Build a source distribution
    doc         Generate the documentation.
    gdist       Build a source distribution with git version
    i18n        Generate translation files (.mo)
    i18n_build  Compile translation files (.po)
    init        Initialize database and user.
    mig         Generate a south migration for an application
    pep8        Run the PEP8 report
    pylint      Run the pylint report
    serve       Run Development server.
    sso         Run Development server.
    syncdb      Synchronize database and generate changesets
    test        Run only project tests (exclude those from Django and third-party applications).
    test_all    Run all tests (including those from Django and third-party applications).
    update      Update all dependencies and database
    update_js   Update javascript dependencies
    update_py   Update python dependencies.
    work        Run the development worker


To ensure everything is fine before submission, use ``tox``.
It will run the test suite on all the supported Python version
and ensure the documentation is generating.

.. code-block:: bash

    $ pip install tox
    $ tox

You also need to ensure your code is PEP8 compliant (following the project rules: see ``pep8.rc`` file):

.. code-block:: bash

    $ fab pep8


**Don't forget client-side code and tests.**

You can run the javascript test suite in the browser (http://localhost:8000/tests).

.. note::

    minification use ``yuglify`` so you need to install it before: ``npm install -g yuglify``


.. _official YouCKAN repository: https://github.com/etalab/youckan
.. _official bugtracker: https://github.com/etalab/youckan/issues

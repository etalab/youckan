Deployment
==========


Environment creation
--------------------

.. code-block:: bash

    $ mkdir -p $YOUCKAN_HOME
    $ cd $YOUCKAN_HOME
    $ virtualenv .
    $ source bin/activate
    $ pip install youckan
    $ mkdir media

As a postgresql administrator:

.. code-block:: bash

    $ createuser youckan -P
    $ createdb youckan -O youckan -E UTF8


Configuration
-------------

.. code-block:: bash

    $ youckan genconf --ini
    $ vim youckan.ini


Initialisation
--------------

.. code-block:: bash

    $ youckan init [--noinput]

If ``--noinput`` is specified, no questions will be asked and the initialization will run in unattended mode.

You can create a super user at anytime with:

.. code-block:: bash

    $ youckan createsuperuser

Upgrade
-------

Upgrading is as easy as upgrading the youckan package and rerunning the initialization:

.. code-block:: bash

    $ pip install -U youckan
    $ youckan init --noinput


NGinx + uWSGI
-------------

.. code-block:: bash

    $ youckan genconf --nginx
    # or
    $ youckan genconf --nginx --uwsgi


Apache 2 + mod
--------------

.. code-block:: bash

    $ youckan genconf --apache
    # or
    $ youckan genconf --apache --uwsgi



Configuration
=============

YouCKAN use a single ini file for its configuration

Sample
------

You can generate a sample configuration by running:

.. code-block:: bash

    $ youckan genconf
    # or
    $ youckan-auth genconf

You will be asked some questions and have as a result the following ini file:

.. code-block:: ini

    [site]
    debug = false
    secret = +hant#30d^df=1$vbolo3p+6t6xdio5312@a63-8b^96q3n-u@
    allowed_hosts =
    admins =
    language = fr
    timezone = Europe/Paris

    [db]
    default = sqlite://youckan.sqlite
    ckan = postgres://ckan_default:ckan_default@localhost/ckan_default

    [email]
    webmaster = webmaster@youckan
    admin = admin@youckan

    [etalab]
    domain = my-domain.com
    ckan_url = http://ckan.{domain}
    home_url = http://www.{domain}
    wiki_url = http://wiki.{domain}
    wiki_api_url = http://wiki.{domain}/api.php
    questions_url = http://questions.{domain}

    [path]
    static = staticroot
    static_url = /static/
    media = media
    media_url = /media/

    [social:twitter]
    key =
    secret =

    [social:google]
    key =
    secret =

    [social:linkedin]
    key =
    secret =

    [log]
    level = warning
    file = {name}.log

    [celery]
    broker = django://
    backend = database

Feel free to customize it for your needs.


Advanced customization
----------------------

YouCKAN configuration is extensible as its only standard django configuration.

You can either extend an existing configuration:

.. code-block:: python

    from youckan.settings import *

    MY_OVERRIDEN_SETTING = 'my.value'

or start a new one from scratch.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from youckan.settings import *  # pylint: disable=W0614,W0401

PROJECT_APPS = (
    'youckan',
    'youckan.apps.accounts',
    'youckan.apps.ckan',
    'youckan.apps.sso',
)

INSTALLED_APPS = PROJECT_APPS + THIRD_PARTY_APPS + DJANGO_APPS

ROOT_URLCONF = 'youckan.apps.sso.urls_standalone'

# WSGI_APPLICATION = 'youckan.apps.sso.wsgi.application'

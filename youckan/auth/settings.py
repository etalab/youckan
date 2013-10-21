# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from youckan.settings import *  # pylint: disable=W0614,W0401

PROJECT_APPS = (
    'youckan',
    'youckan.auth',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

ROOT_URLCONF = 'youckan.auth.urls_standalone'

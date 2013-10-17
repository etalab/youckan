# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys

from django.core.management import execute_from_command_line


def manage():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youckan.settings")
    execute_from_command_line(sys.argv)


def manage_auth():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youckan.auth.settings")
    execute_from_command_line(sys.argv)

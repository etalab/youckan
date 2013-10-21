# -*- coding: utf-8 -*-
import os
import sys

sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'youckan.settings'

from youckan.wsgi import application

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import requests

from celery import task

from youckan.auth.models import YouckanUser

logger = logging.getLogger(__name__)


@task
def sync_users(email):
    user = YouckanUser.objects.get(email=email)
    sync_ckan_user(user)


def sync_ckan_user(user):
    logger.info('Creating CKAN user %s', user.email)

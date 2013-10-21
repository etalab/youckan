# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import requests

from django.conf import settings

from celery import task

from youckan.auth.models import YouckanUser

logger = logging.getLogger(__name__)


@task
def sync_users(email):
    logger.info('Synchronizing user %s', email)
    try:
        user = YouckanUser.objects.get(email=email)
    except YouckanUser.DoesNotExists:
        logger.error('User %s does not exists', email)
        return
    if not user.is_active:
        logger.debug('Skipping inactive user %s', user.email)
    sync_ckan_user(user)


def sync_ckan_user(user):
    logger.info('Creating CKAN user %s', user.email)

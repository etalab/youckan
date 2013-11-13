# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from requests.exceptions import HTTPError

from celery import task

from youckan.models import User
from youckan.apps.ckan import client

logger = logging.getLogger(__name__)


@task
def sync_ckan_user(email):
    logger.info('Synchronizing user %s with CKAN', email)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExists:
        logger.error('User %s does not exists', email)
        return

    if not user.is_active:
        logger.debug('Skipping inactive user %s', user.email)

    ckan_user_id = None
    try:
        response = client.action('user_show', {'id': user.slug})
        if response['success']:
            ckan_user_id = response['result']['id']
    except HTTPError as error:
        if not error.response.status_code == 404:
            raise

    if ckan_user_id:
        response = client.action('user_update', {
            'id': ckan_user_id,
            'name': user.slug,
            'email': user.email,
            'fullname': user.full_name,
            'about': user.profile.about,
            'sysadmin': user.is_superuser,
        })
    else:
        response = client.action('user_create', {
            'name': user.slug,
            'email': user.email,
            'password': 'not used',
            'fullname': user.full_name,
            'about': user.profile.about,
            'sysadmin': user.is_superuser,
        })

    if response['success']:
        logger.info('Synchronized CKAN user %s', user.slug)
    else:
        logger.error('Failed to synchre CKAN user %s: %s', user.slug, response['error']['message'])
        raise Exception(response['error']['message'])

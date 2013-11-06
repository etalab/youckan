# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import requests

from django.conf import settings

logger = logging.getLogger(__name__)

TIMEOUT = 3


def call_ckan(url, data=None, method='post'):
    '''Call CKAN API url'''
    data = data or {}
    headers = {
        'content-type': 'application/json',
        'Authorization': settings.CKAN_API_KEY,
    }

    func = getattr(requests, method.lower(), 'get')

    try:
        response = func(url, data=json.dumps(data), headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException:
        logger.exception('Unable to fetch URL "%s"', url)
        raise
    return response.json()


def action(name, data=None, method='post'):
    '''Call a CKAN API v3 action'''
    logger.info('CKAN API: %s %s', name, data)
    url = '{0}/api/3/action/{1}'.format(settings.CKAN_URL, name)
    return call_ckan(url, data, method)


def weckan(name, data=None, method='get'):
    '''Call a WeCKAN API action'''
    logger.info('WeCKAN API: %s %s', name, data)
    url = '{0}/api/weckan/{1}'.format(settings.HOME_URL, name)
    return call_ckan(url, data, method)


def connector(name, data=None, method='get'):
    '''Call a WeCKAN API action'''
    logger.info('YouCKAN Connector: %s %s', name, data)
    url = '{0}/youckan/{1}'.format(settings.HOME_URL, name)
    return call_ckan(url, data, method)

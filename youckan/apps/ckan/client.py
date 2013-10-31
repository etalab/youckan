# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import requests

from django.conf import settings

logger = logging.getLogger(__name__)

TIMEOUT = 3


def action(name, data=None):
    data = data or {}
    url = '{0}/api/3/action/{1}'.format(settings.CKAN_URL, name)
    headers = {
        'content-type': 'application/json',
        'Authorization': settings.CKAN_API_KEY,
    }

    logger.debug('action: %s %s', name, data)

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException:
        logger.exception('Unable to perform action "%s": %s', name)
        raise
    return response.json()

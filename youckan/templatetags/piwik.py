# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.conf import settings


register = template.Library()


@register.inclusion_tag('widgets/piwik.html')
def piwik_tracking():
    if settings.DEBUG and not (hasattr(settings, 'PIWIK_IN_DEBUG') and settings.PIWIK_IN_DEBUG):
        return {
            'error': 'Piwik is disable in DEBUG mode unless PIWIK_IN_DEBUG is set',
        }
    elif not hasattr(settings, 'PIWIK_URL') and hasattr(settings, 'PIWIK_SITE_ID'):
        return {
            'error': 'Piwik is missing configuration',
        }
    else:
        return {
            'url': settings.PIWIK_URL.replace('http://', '').replace('https://', '').rstrip('/'),
            'site_id': settings.PIWIK_SITE_ID,
            'domain': settings.PIWIK_DOMAIN,
        }

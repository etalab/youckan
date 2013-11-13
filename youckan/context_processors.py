# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.template.defaultfilters import slugify


def etalab_config(request):
    '''
    Inject custom Etalab configuration into templates
    '''
    return {
        'etalab': {
            'DOMAIN': settings.DOMAIN,
            'HOME_URL': settings.HOME_URL,
            'WIKI_URL': settings.WIKI_URL,
            'WIKI_API_URL': settings.WIKI_API_URL,
            'QUESTIONS_URL': settings.QUESTIONS_URL,
            'MENU_TOPICS': [
                {'title': topic['title'], 'url': topic['url'].format(
                    wiki=settings.WIKI_URL,
                    group='{0}/{1}/groups'.format(settings.HOME_URL, request.LANGUAGE_CODE),
                )}
                for topic in settings.MENU_TOPICS
            ],
        }
    }

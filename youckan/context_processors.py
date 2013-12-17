# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings


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
                {'title': topic['title'], 'url': '{home}/{lang}/group/{name}'.format(
                    home=settings.HOME_URL, lang=request.LANGUAGE_CODE, name=topic['name']
                )}
                for topic in settings.MENU_TOPICS
            ],
        }
    }

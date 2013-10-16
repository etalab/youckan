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
                (title, icon, url.format(wiki=settings.WIKI_URL) if url else slugify(title))
                for title, icon, url in settings.MENU_TOPICS
            ],
        }
    }

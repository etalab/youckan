# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.dateparse import parse_datetime

from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter('format')
@stringfilter
def string_format(string, params):
    if isinstance(params, dict):
        return string.format(**params)
    elif isinstance(params, (list, tuple)):
        return string.format(*params)
    else:
        return string.format(params)


@register.filter
def default_static(url, default):
    return url or staticfiles_storage.url(default)


@register.filter
@stringfilter
def flag_url(language_code):
    code = (language_code or settings.LANGUAGE_CODE).split('-')[0]
    filename = 'img/flags/{0}.png'.format(code.lower())
    return staticfiles_storage.url(filename)


@register.filter
@stringfilter
def dtparse(string):
    try:
        return parse_datetime(string)
    except:
        return string


@register.filter(is_safe=True)
def alert_class(message):
    if 'error' in message.tags:
        return 'alert-error'
    elif 'warning' in message.tags:
        return 'alert-warning'
    elif 'success' in message.tags:
        return 'alert-success'
    else:
        return 'alert-info'

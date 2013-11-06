# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.dateparse import parse_datetime

from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import Truncator

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
@stringfilter
def markdown(source):
    '''Render Markdown to HTML'''
    import markdown as md
    if (source is None) or (source.strip() == ''):
        return ''
    return mark_safe(md.markdown(force_unicode(source), safe_mode=True, enable_attributes=False))


@register.filter(is_safe=True)
@stringfilter
def truncate_markdown(source, length=0):
    ''' return the plain text representation of markdown encoded text.  That
    is the texted without any html tags.  If ``length`` is 0 then it
    will not be truncated.'''
    try:
        length = int(length)
    except ValueError:  # invalid literal for int()
        return source  # Fail silently.
    return Truncator(markdown(source)).words(length, html=True, truncate=' ...')


@register.filter(is_safe=True)
@stringfilter
def strip_markdown(source, length=0):
    try:
        length = int(length)
    except ValueError:  # invalid literal for int()
        return source  # Fail silently.
    rendered = strip_tags(markdown(source))
    if length:
        return Truncator(rendered).chars(length, truncate=' ...')
    return rendered


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

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.utils.html import strip_tags

register = template.Library()


@register.filter
@stringfilter
def format(string, params):
    if isinstance(params, dict):
        return string.format(**params)
    elif isinstance(params, (list, tuple)):
        return string.format(*params)
    else:
        return string.format(params)


@register.filter
def default_static(url, default):
    from django.templatetags.static import static
    return url or static(default)


@register.filter
@stringfilter
def flag_url(language_code):
    from django.conf import settings
    from django.templatetags.static import static
    code = (language_code or settings.LANGUAGE_CODE).split('-')[0]
    filename = 'images/flags/{0}.png'.format(code.lower())
    return static(filename)


@register.filter(is_safe=True)
@stringfilter
def markdown(source):
    '''Render Markdown to HTML'''
    import markdown
    if (source is None) or (source.strip() == ''):
        return ''
    return mark_safe(markdown.markdown(force_unicode(source), safe_mode=True, enable_attributes=False))


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

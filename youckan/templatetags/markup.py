# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import bleach
import markdown as md

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import Truncator


register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def markdown(source):
    '''Render Markdown to HTML'''
    if (source is None) or (source.strip() == ''):
        return ''
    return mark_safe(md.markdown(
        bleach.clean(source),
        output_format='html5'
    ))


@register.filter(is_safe=True)
@stringfilter
def truncate_markdown(source, length=0):
    ''' return the plain text representation of markdown encoded text.  That
    is the texted without any html tags.  If ``length`` is 0 then it
    will not be truncated.'''
    try:
        length = int(length)
    except ValueError:  # invalid literal for int()
        return bleach.clean(source)  # Fail silently.
    return mark_safe(Truncator(markdown(source)).words(length, html=True, truncate=' ...'))


@register.filter(is_safe=True)
@stringfilter
def strip_markdown(source, length=0):
    try:
        length = int(length)
    except ValueError:  # invalid literal for int()
        return bleach.clean(source)  # Fail silently.
    rendered = strip_tags(markdown(source))
    if length:
        return mark_safe(Truncator(rendered).chars(length, truncate=' ...'))
    return mark_safe(rendered)

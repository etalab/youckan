# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.contrib.auth import get_user_model

register = template.Library()


@register.inclusion_tag('widgets/avatar.html')
def avatar(param, size=32, editable=False, button=False):
    if isinstance(param, get_user_model()) and hasattr(param, 'avatar'):
        field = getattr(param, 'avatar')
    else:
        field = param
    return {
        'avatar': field,
        'size': size,
        'editable': editable,
        'button': button,
    }


@register.inclusion_tag('widgets/avatar.html')
def avatar_field(field, size=32):
    return {
        'size': size,
        'editable': True,
    }

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.contrib.auth import get_user_model

from django_gravatar.helpers import get_gravatar_url

register = template.Library()


@register.inclusion_tag('widgets/avatar.html')
def avatar(user, size=32):
    if not isinstance(user, get_user_model()):
        raise ValueError('Should have an user as parameter')
    if user.avatar:
        avatar_url = user.avatar.url
    else:
        avatar_url = get_gravatar_url(user.email)
    return {
        'avatar_url': avatar_url,
        'size': size
    }


@register.inclusion_tag('widgets/avatar_field.html')
def avatar_field(field, size=32):
    return {
        'field': field,
        'size': size,
    }

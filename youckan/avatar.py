# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_gravatar.helpers import get_gravatar_url


def get_avatar_url(user, size=100):
    '''Get the avatar URL for a given user'''
    return user.profile.avatar.url if user.profile.avatar else get_gravatar_url(user.email, size or 100)

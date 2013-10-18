# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib2

from urlparse import urlparse

from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from social.pipeline.partial import partial
from social.exceptions import AuthAlreadyAssociated

from youckan.auth.mail import send_confirmation

USER_FIELDS = ['username', 'email', 'first_name', 'last_name']


@partial
def register_form(strategy, backend, details, user, avatar_url, *args, **kwargs):
    '''Display the registeration form'''
    if user:
        return

    if strategy.session_get('new_user'):
        user = strategy.session_pop('new_user')
        avatar_url = avatar_url if strategy.session_pop('use_avatar') else None
        return {
            'user': user,
            'is_new': True,
            'avatar_url': avatar_url,
        }
    else:
        fields = dict(
            (name, kwargs.get(name) or details.get(name))
            for name in strategy.setting('USER_FIELDS', USER_FIELDS)
        )
        strategy.session_set('userfields', fields)
        strategy.session_set('backend', backend.name)

        return redirect('register')


def new_registeration_only(strategy, response, user=None, social=None, *args, **kwargs):
    '''Don't let already registered user to log with their social account'''
    print 'new only'
    if user or hasattr(social, 'user'):
        msg = _('This {0} account is already in use. Please login with your password').format(strategy.backend.name)
        raise AuthAlreadyAssociated(strategy.backend, msg)


def get_avatar_url(request, backend, response, *args, **kwargs):
    ''' fetch the avatar URL'''
    from social.backends.google import GoogleOAuth2
    from social.backends.twitter import TwitterOAuth
    from social.backends.linkedin import LinkedinOAuth2
    avatar_url = None
    if isinstance(backend, TwitterOAuth):
        avatar_url = response.get('profile_image_url', '').replace('_normal', '')
    elif isinstance(backend, GoogleOAuth2):
        avatar_url = response.get('picture')
    elif isinstance(backend, LinkedinOAuth2):
        avatar_url = response.get('pictureUrls', {}).get('values', [None])[0]
        if not avatar_url:
            avatar_url = response.get('pictureUrl')
    request.session['avatar_url'] = avatar_url
    return {'avatar_url': avatar_url}


def fetch_avatar(request, backend, user, avatar_url=None, *args, **kwargs):
    '''Fetch and store the avatar picture'''
    if not avatar_url:
        return

    filename = urlparse(avatar_url).path.split('/')[-1]
    content = ContentFile(urllib2.urlopen(avatar_url).read())
    user.avatar.save(filename, content, save=True)


def activate_user(strategy, user, *args, **kwargs):
    '''Activate the user and send a confirmation email'''
    if not user:
        return
    user.is_active = True
    user.save()
    send_confirmation(strategy, user)

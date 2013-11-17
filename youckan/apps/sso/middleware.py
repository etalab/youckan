# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import hashlib

from django.conf import settings
from django.contrib.auth import logout

log = logging.getLogger(__name__)


class YouckanAuthCookieMiddleware(object):
    separator = '::'

    def process_request(self, request):
        '''Verify cookie signature and logout if it doesn't match'''
        if self.cookie_name in request.COOKIES:
            cookie = request.COOKIES[self.cookie_name]
            user = request.user
            session = request.session
            if not self.verify_cookie(cookie, user, session):
                log.error('Bad cookie for user %s', user.email)
                logout(request)


    def process_response(self, request, response):
        '''Set domain auth cookie if user is logged in else delete it if exists'''
        if hasattr(request, 'user') and request.user.is_authenticated():
            content = self.build_cookie(request.user, request.session)
            response.set_cookie(self.cookie_name, content, domain=self.domain)
        elif not hasattr(request, 'user') or not request.user.is_authenticated():
            response.delete_cookie(self.cookie_name, domain=self.domain)
        return response

    def build_cookie(self, user, session):
        return self.separator.join([
            self.sign(user.slug, session.session_key),
            user.slug,
        ])

    def verify_cookie(self, cookie, user, session):
        try:
            signature, slug = cookie.split(self.separator)
            assert slug == user.slug
            assert signature == self.sign(slug, session.session_key)
            return True
        except:
            return False

    @property
    def cookie_name(self):
        return getattr(settings, 'YOUCKAN_AUTH_COOKIE', 'youckan.auth')

    @property
    def domain(self):
        domain = getattr(settings, 'YOUCKAN_DOMAIN', settings.SESSION_COOKIE_DOMAIN)
        if not domain.startswith('.'):
            domain = '.' + domain
        return domain

    def sign(self, message, salt):
        return hashlib.sha256(settings.SECRET_KEY + salt + message).hexdigest()

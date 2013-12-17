# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.contrib.auth import logout
from django.core import signing

log = logging.getLogger(__name__)


class YouckanAuthCookieMiddleware(object):
    def process_request(self, request):
        '''Verify cookie signature and logout if it doesn't match'''
        if self.cookie_name not in request.COOKIES:
            return
        cookie = request.COOKIES[self.cookie_name]
        user = request.user
        session = request.session
        try:
            if user.is_authenticated() and signing.loads(cookie, salt=session.session_key) == user.slug:
                return
        except signing.BadSignature:
            if hasattr(user, 'email'):
                log.error('Bad cookie for user %s', user.email)
            else:
                log.error('Bad cookie for session %s', session.session_key)
        logout(request)
        return

    def process_response(self, request, response):
        '''Set domain auth cookie if user is logged in else delete it if exists'''
        if hasattr(request, 'user') and request.user.is_authenticated():
            session_key = request.session.session_key
            content = signing.dumps(request.user.slug, salt=session_key)
            response.set_cookie(self.cookie_name, content, domain=self.domain, secure=settings.HTTPS)
            if settings.HTTPS:
                response.set_cookie(self.logged_cookie_name, '', domain=self.domain)
        elif not hasattr(request, 'user') or not request.user.is_authenticated():
            response.delete_cookie(self.cookie_name, domain=self.domain)
            if settings.HTTPS:
                response.delete_cookie(self.logged_cookie_name, domain=self.domain)
        return response

    @property
    def cookie_name(self):
        return getattr(settings, 'YOUCKAN_AUTH_COOKIE', 'youckan.auth')

    @property
    def logged_cookie_name(self):
        return '{0}.logged'.format(self.cookie_name)

    @property
    def domain(self):
        domain = getattr(settings, 'YOUCKAN_DOMAIN', settings.SESSION_COOKIE_DOMAIN)
        if not domain.startswith('.'):
            domain = '.' + domain
        return domain

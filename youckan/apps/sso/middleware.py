# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib

from django.conf import settings


class YouckanAuthCookieMiddleware(object):
    def process_response(self, request, response):
        cookie_name = getattr(settings, 'YOUCKAN_AUTH_COOKIE', 'youckan.auth')
        domain = getattr(settings, 'YOUCKAN_DOMAIN', settings.SESSION_COOKIE_DOMAIN)
        if not domain.startswith('.'):
            domain = '.' + domain

        if hasattr(request, 'user') and request.user.is_authenticated():
            cookie_hash = self.get_cookie_hash(request.user, request.session.session_key)
            response.set_cookie(cookie_name, cookie_hash, domain=domain)
        elif not hasattr(request, 'user') or not request.user.is_authenticated():
            response.delete_cookie(cookie_name, domain=domain)
        return response

    def get_cookie_hash(self, user, salt):
        signature = hashlib.sha256(settings.SECRET_KEY + salt + user.slug).hexdigest()
        return '::'.join([signature, user.slug])

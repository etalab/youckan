# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from social.backends.base import BaseAuth


class NoSocialAuth(BaseAuth):
    name = 'no-social'
    ID_KEY = 'email'

    def get_user_id(self, details, response):
        return details.get(self.ID_KEY) or response.get(self.ID_KEY)

    def auth_url(self):
        return None

    def auth_complete(self, *args, **kwargs):
        response = kwargs.get('response') or {}
        kwargs.update({'response': response, 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)

    def get_user_details(self, response):
        return {}

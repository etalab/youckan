# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from social.backends.base import BaseAuth


class NoSocialAuth(BaseAuth):
    name = 'no-social'

    def auth_url(self):
        return None

    def auth_complete(self, *args, **kwargs):
        response = kwargs.get('response') or {}
        kwargs.update({'response': response, 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)

    def get_user_details(self, *args, **kwargs):
        return {
            # 'username': username,
            # 'email': '',
            # 'fullname': fullname,
            # 'first_name': first_name,
            # 'last_name': last_name
        }

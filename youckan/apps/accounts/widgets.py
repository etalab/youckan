# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


class ProfileWidget(object):
    name = None
    template_name = None

    def __init__(self, user):
        if not self.name:
            raise ValueError('Name is required')

        if not self.template_name:
            raise ValueError('Template name is required')

        self.user = user

    def fill_context(self, context):
        pass

    def can_display(self, user):
        '''Conditionnal inclusion'''
        return True


class BadgesWidget(ProfileWidget):
    name = _('Badges')
    template_name = 'accounts/widgets/badges.html'

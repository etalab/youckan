# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.utils.translation import ugettext_lazy as _

from youckan.apps.accounts.widgets import ProfileWidget
from youckan.apps.ckan import client as ckan

log = logging.getLogger(__name__)


class DatasetsWidget(ProfileWidget):
    name = _('Datasets')
    template_name = 'ckan/widgets/datasets.html'

    def fill_context(self, context):
        try:
            context['datasets'] = ckan.connector('/'.join(['profile', self.user.slug, 'datasets']))
        except:
            log.exception('Unable to fetch datasets for %s', self.user.slug)
            pass


class UsefulsWidget(ProfileWidget):
    name = _('Usefuls')
    template_name = 'ckan/widgets/usefuls.html'

    def fill_context(self, context):
        try:
            context['usefuls'] = ckan.connector('/'.join(['profile', self.user.slug, 'usefuls']))
        except:
            log.exception('Unable to fetch usefuls for %s', self.user.slug)
            pass


class ReusesWidget(ProfileWidget):
    name = _('Reuses')
    template_name = 'ckan/widgets/reuses.html'

    def fill_context(self, context):
        try:
            context['reuses'] = ckan.connector('/'.join(['profile', self.user.slug, 'reuses']))
        except:
            log.exception('Unable to fetch reuses for %s', self.user.slug)
            pass


class OrganizationsWidget(ProfileWidget):
    name = _('Organizations')
    template_name = 'ckan/widgets/organizations.html'

    def fill_context(self, context):
        try:
            context['organizations'] = ckan.connector('/'.join(['profile', self.user.slug, 'organizations']))
        except:
            log.exception('Unable to fetch orgnizations for %s', self.user.slug)
            pass


class PrivateDatasetsWidget(ProfileWidget):
    name = _('Privates')
    template_name = 'ckan/widgets/privates.html'

    def fill_context(self, context):
        try:
            context['privates'] = ckan.connector('/'.join(['profile', self.user.slug, 'privates']))
        except:
            log.exception('Unable to fetch private datasets for %s', self.user.slug)
            pass

    def can_display(self, user):
        return user.is_superuser or user is self.user

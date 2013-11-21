# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from youckan.apps.accounts.widgets import ProfileWidget
from youckan.apps.ckan import client as ckan


class DatasetsWidget(ProfileWidget):
    name = _('Datasets')
    template_name = 'ckan/widgets/datasets.html'

    def fill_context(self, context):
        try:
            context['datasets'] = ckan.connector('/'.join(['profile', self.user.slug, 'datasets']))
        except:
            pass


class UsefulsWidget(ProfileWidget):
    name = _('Usefuls')
    template_name = 'ckan/widgets/usefuls.html'

    def fill_context(self, context):
        try:
            context['usefuls'] = ckan.connector('/'.join(['profile', self.user.slug, 'usefuls']))
        except:
            pass


class ValorizationsWidget(ProfileWidget):
    name = _('Valorizations')
    template_name = 'ckan/widgets/valorizations.html'

    def fill_context(self, context):
        try:
            context['valorizations'] = ckan.connector('/'.join(['profile', self.user.slug, 'valorizations']))
        except:
            pass


class OrganizationsWidget(ProfileWidget):
    name = _('Organizations')
    template_name = 'ckan/widgets/organizations.html'

    def fill_context(self, context):
        try:
            context['organizations'] = ckan.connector('/'.join(['profile', self.user.slug, 'organizations']))
        except:
            pass


class PrivateDatasetsWidget(ProfileWidget):
    name = _('Privates')
    template_name = 'ckan/widgets/privates.html'

    def fill_context(self, context):
        try:
            context['datasets'] = ckan.connector('/'.join(['profile', self.user.slug, 'privates']))
        except:
            pass

    def can_display(self, user):
        return user.is_superuser or user is self.user

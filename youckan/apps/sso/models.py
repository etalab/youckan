# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from oauth2_provider.models import AbstractApplication


@python_2_unicode_compatible
class OAuth2Application(AbstractApplication):
    is_internal = models.BooleanField(_('Is an internal application'), default=False)

    class Meta:
        verbose_name = _('OAuth2 Application')
        verbose_name_plural = _('OAuth2 Applications')

    def __str__(self):
        return self.name or self.client_id

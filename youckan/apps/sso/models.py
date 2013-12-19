# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from oauth2_provider.models import AbstractApplication

from simple_email_confirmation.signals import email_confirmed, unconfirmed_email_created

from youckan.apps.sso import mail


@python_2_unicode_compatible
class OAuth2Application(AbstractApplication):
    is_internal = models.BooleanField(_('Is an internal application'), default=False)

    class Meta:
        verbose_name = _('OAuth2 Application')
        verbose_name_plural = _('OAuth2 Applications')

    def __str__(self):
        return self.name or self.client_id


@receiver(unconfirmed_email_created)
def send_validation_mail(sender, email, **kwargs):
    mail.send_validation(sender)


@receiver(email_confirmed)
def send_confirmation_mail(sender, email, **kwargs):
    if sender.email == email and not sender.is_active:
        sender.is_active = True
        sender.save()
        mail.send_confirmation(sender)

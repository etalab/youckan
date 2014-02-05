# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _

from youckan import mail


def send_validation(user):
    mail.send(user, _('Validate your account'), 'mails/validation',
        url=mail.absolute_url('register-confirm', key=user.confirmation_key),
        user=user
    )


def send_confirmation(user):
    site = Site.objects.get_current()
    mail.send(user, _('Welcome on {site}').format(site=site.name), 'mails/confirmation',
        user=user, profile_url=mail.absolute_url('profile', slug=user.slug))


def reset_password(user):
    context = mail.get_context(
        email=user.email,
        uid=urlsafe_base64_encode(force_bytes(user.pk)),
        user=user,
        token=default_token_generator.make_token(user),
    )
    subject = loader.render_to_string('registration/password_reset_subject.txt', context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    email = loader.render_to_string('registration/password_reset_email.html', context)
    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email])

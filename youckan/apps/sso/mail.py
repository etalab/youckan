# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext as _

from youckan import mail


def absolute_url(name, *args, **kwargs):
    return "{protocol}://{domain}{path}".format(
        protocol='https' if settings.HTTPS else 'http',
        domain=Site.objects.get_current().domain,
        path=reverse(name, args=args, kwargs=kwargs)
    )


def get_mail_context(**kwargs):
    site = Site.objects.get_current()
    context = {
        'domain': site.domain,
        'site_name': site.name,
        'protocol': 'https' if settings.HTTPS else 'http',
    }
    context.update(kwargs)
    return Context(context)


def send_validation(user):
    mail.send(user, _('Validate your account'), 'mails/validation',
        url=mail.absolute_url('register-confirm', key=user.confirmation_key),
        user=user
    )


def send_confirmation(user):
    mail.send(user, _('Account creation confirmation'), 'mails/confirmation',
        user=user, profile_url=absolute_url('profile', slug=user.slug))


def reset_password(user):
    site = Site.objects.get_current()
    context = {
        'email': user.email,
        'domain': site.domain,
        'site_name': site.name,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': default_token_generator.make_token(user),
        'protocol': 'https' if settings.HTTPS else 'http',
    }
    subject = loader.render_to_string('registration/password_reset_subject.txt', context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    email = loader.render_to_string('registration/password_reset_email.html', context)
    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email])

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import render_to_string


def absolute_url(name, *args, **kwargs):
    return "{protocol}://{domain}{path}".format(
        protocol='https' if settings.HTTPS else 'http',
        domain=Site.objects.get_current().domain,
        path=reverse(name, args=args, kwargs=kwargs)
    )


def get_mail_context(**kwargs):
    '''Prefill the a mail context with common data'''
    site = Site.objects.get_current()
    context = {
        'domain': site.domain,
        'site_name': site.name,
        'protocol': 'https' if settings.HTTPS else 'http',
    }
    context.update(kwargs)
    return Context(context)


def send(recipients, subject, template_base, **kwargs):
    context = get_mail_context(**kwargs)

    if isinstance(recipients, get_user_model()):
        recipients = [recipients]
    emails = [recipient.email for recipient in recipients]

    mail = EmailMultiAlternatives(subject,
        render_to_string('{0}.txt'.format(template_base), context),
        to=emails
    )
    mail.attach_alternative(render_to_string('{0}.html'.format(template_base), context), 'text/html')
    mail.send(fail_silently=False)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext as _


def send_validation(strategy, code):
    url = strategy.build_absolute_uri('?'.join([
        reverse('social:complete', args=[strategy.backend_name]),
        'verification_code={0}'.format(code.code)
    ]))
    user = strategy.storage.user.get_users_by_email(code.email)[0]

    template = loader.get_template('mails/validation.html')
    context = Context({
        'url': url,
        'code': code,
        'user': user,
    })

    email = EmailMultiAlternatives(_('Validate your account'),
        _('Validate your account {0}').format(url),
        to=[code.email]
    )
    email.attach_alternative(template.render(context), 'text/html')
    email.send(fail_silently=False)


def send_confirmation(strategy, user):
    profile_url = strategy.build_absolute_uri(user.get_absolute_url())
    template = loader.get_template('mails/confirmation.html')
    context = Context({
        'user': user,
        'profile_url': profile_url,
    })

    email = EmailMultiAlternatives(_('Account creation confirmation'),
        _('Your account has been created'),
        to=[user.email]
    )
    email.attach_alternative(template.render(context), 'text/html')
    email.send(fail_silently=False)


def reset_password(user, use_https=False, domain='youckan.org', site='YouCKAN',
    subject_template_name='registration/password_reset_subject.txt',
    email_template_name='registration/password_reset_email.html'):
    context = {
        'email': user.email,
        'domain': domain,
        'site_name': site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': default_token_generator.make_token(user),
        'protocol': 'https' if use_https else 'http',
    }
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    email = loader.render_to_string(email_template_name, context)
    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email])

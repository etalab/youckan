# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _


def send_validation(strategy, code):
    url = strategy.build_absolute_uri('?'.join([
        reverse('social:complete', args=[strategy.backend_name]),
        'code={0}'.format(code.code)
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


def send_confirmation(user):
    template = loader.get_template('mails/confirmation.html')
    context = Context({'user': user})

    email = EmailMultiAlternatives(_('Account creation confirmation'),
        _('Your account has been created'),
        to=[user.email]
    )
    email.attach_alternative(template.render(context), 'text/html')
    email.send(fail_silently=False)

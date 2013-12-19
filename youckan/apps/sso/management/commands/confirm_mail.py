# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.models.signals import post_save

from simple_email_confirmation.signals import email_confirmed, unconfirmed_email_created

from youckan.apps.ckan.models import sync_ckan_on_save
from youckan.apps.sso.models import send_validation_mail, send_confirmation_mail
from youckan.models import User


class Command(BaseCommand):
    help = 'Fix and reinitialize mail confirmations'
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Update CKAN users to match imported users'
        ),
    )

    def handle(self, *args, **options):
        # Prevent user to be automatically created
        post_save.disconnect(sync_ckan_on_save, sender=User, dispatch_uid="youckan.ckan.sync_user")

        if options['all']:
            for user in User.objects.all():
                self.fix_user(user)
        else:
            email = args[0]
            user = User.objects.get(email=email)
            self.fix_user(user)

    def fix_user(self, user):
        if user.is_active and not user.is_confirmed:
            self.stdout.write('Marking user {0} as already confirmed'.format(user.email))
            # Disconnect signals
            unconfirmed_email_created.disconnect(send_validation_mail)
            email_confirmed.disconnect(send_confirmation_mail)
            # Confirm user
            user.add_unconfirmed_email(user.email)
            user.confirm_email(user.confirmation_key)
            # Reconnect signals
            unconfirmed_email_created.connect(send_validation_mail)
            email_confirmed.connect(send_confirmation_mail)
        elif not user.is_active and user.email not in user.unconfirmed_emails:
            self.stdout.write('Sending email confirmation mail to {0}'.format(user.email))
            user.add_unconfirmed_email(user.email)
        else:
            self.stdout.write('Nothing to do for {0}'.format(user.email))

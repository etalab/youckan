# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.models.signals import post_save

from youckan.apps.ckan.models import sync_ckan_on_save
from youckan.apps.sso import mail
from youckan.models import User


class Command(BaseCommand):
    help = 'Reset a user password'
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Update CKAN users to match imported users'
        ),
        make_option('-s', '--https',
            action='store_true',
            dest='https',
            help='Use HTTPS'
        ),
        make_option('-d', '--domain',
            action='store',
            dest='domain',
            help='Domain name to use'
        ),
        make_option('--site',
            action='store',
            dest='site',
            default='Etalab2.fr',
            help='Site name to use'
        ),
    )

    def handle(self, *args, **options):
        # Prevent user to be automatically created
        post_save.disconnect(sync_ckan_on_save, sender=User, dispatch_uid="youckan.ckan.sync_user")

        if options['all']:
            for user in User.object.all():
                self.stdout.write('Sending reset password mail to {0}'.format(user.email))
                mail.reset_password(user,
                    use_https=options['https'],
                    domain=options['domain'],
                    site=options['site'],
                )
        else:
            email = args[0]
            user = User.objects.get(email=email)
            self.stdout.write('Sending reset password mail to {0}'.format(user.email))
            mail.reset_password(user,
                use_https=options['https'],
                domain=options['domain'],
                site=options['site'],
            )

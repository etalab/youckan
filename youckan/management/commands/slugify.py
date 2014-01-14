# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from django.core.management.base import BaseCommand


from youckan.models import User

HAS_CKAN = 'youckan.apps.ckan' in settings.INSTALLED_APPS

if HAS_CKAN:
    from django.db.models.signals import post_save
    from youckan.apps.ckan import client
    from youckan.apps.ckan.models import sync_ckan_on_save


class Command(BaseCommand):
    args = '<slug slug ...>'
    help = 'Rebuild user slug'

    def handle(self, *args, **options):
        verbose = int(options['verbosity']) > 1
        if HAS_CKAN:  # Prevent user to be automatically created
            post_save.disconnect(sync_ckan_on_save, sender=User, dispatch_uid="youckan.ckan.sync_user")

        users = User.objects.filter(slug__in=args) if args else User.objects.all()
        if verbose:
            self.stdout.write('{0} user(s) to process'.format(users.count()))
        for user in users:
            if verbose:
                self.stdout.write('-> Processing user "{0}"'.format(user.full_name))
            if HAS_CKAN:  # Store CKAN id before slug change
                try:
                    response = client.action('user_show', {'id': user.slug})
                except:
                    self.stderr.write('Unable to fetch CKAN user for "{0}"'.format(user.full_name))
                    continue
                if not response.get('success'):
                    self.stderr.write('Unable to fetch CKAN user for "{0}"'.format(user.full_name))
                    continue
                ckan_user_id = response['result']['id']

            # Trigger slug update
            user.slug = None
            user.save()

            if HAS_CKAN:
                response = client.action('user_update', {
                    'id': ckan_user_id,
                    'name': user.slug,
                    'email': user.email,
                    'fullname': user.full_name,
                    'about': user.profile.about,
                    'sysadmin': user.is_superuser,
                })

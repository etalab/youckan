# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.db.models.signals import post_save
from django.utils.dateparse import parse_datetime


from youckan.apps.ckan import client
from youckan.models import User, sync_on_save


class Command(BaseCommand):
    help = 'Import CKAN users from CKAN API'

    def handle(self, *args, **options):
        # Prevent user to be automatically created
        post_save.disconnect(sync_on_save, sender=User, dispatch_uid="youckan.sync_users")

        response = client.action('user_list')
        for userdata in response['result']:
            try:
                user = self.create_user(userdata)
            except Exception as e:
                self.stdout.write('Error creating user {0}: {1}'.format(userdata['id'], e))
                user = None
            ckan_id = userdata['id']
            if not user:
                self.stdout.write('Skipping user {id}'.format(**userdata))
                continue
            self.update_ckan_user(user, ckan_id)
            self.notify_user(user, ckan_id)

    def create_user(self, userdata):
        fullname = userdata['fullname']
        email = userdata['email']

        if not (email and fullname):
            self.stdout.write('Missing email or fullname for user {id}'.format(**userdata))
            return None

        self.stdout.write('Processing {fullname} ({email})'.format(**userdata))
        first_name, last_name = fullname.split(' ', 1) if ' ' in fullname else (fullname, '')

        if User.objects.filter(email=userdata['email']).exists():
            self.stdout.write('User {email} already exists'.format(**userdata))
            return None

        return User.objects.create(
            email=userdata['email'],
            first_name=first_name,
            last_name=last_name,
            is_staff=userdata['sysadmin'],
            is_superuser=userdata['sysadmin'],
            date_joined=parse_datetime(userdata['created']),
        )

    def update_profile(self, user, userdata):
        user.profile.about = userdata['about']
        user.profile.save()

    def update_ckan_user(self, user, ckan_id):
        response = client.action('user_update', {
            'id': ckan_id,
            'name': user.slug,
            'email': user.email,
        })
        return response['success']

    def notify_user(self, user, ckan_id):
        self.stdout.write('Sending email to {email}'.format(**user.__dict__))

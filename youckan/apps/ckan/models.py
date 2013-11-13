# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from youckan.models import User


@receiver(post_save, sender=User, dispatch_uid="youckan.ckan.sync_user")
def sync_ckan_on_save(sender, instance, created, **kwargs):
    from youckan.apps.ckan.tasks import sync_ckan_user
    sync_ckan_user.delay(instance.email)

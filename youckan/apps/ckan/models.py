# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from youckan.models import User


logger = logging.getLogger(__name__)


@receiver(post_save, sender=User, dispatch_uid="youckan.ckan.sync_user")
def sync_ckan_on_save(sender, instance, created, **kwargs):
    if settings.TESTING:
        logger.debug('Skipping CKAN synchronization for user %s while testing', instance.email)
        return
    from youckan.apps.ckan.tasks import sync_ckan_user
    sync_ckan_user.delay(instance.email)

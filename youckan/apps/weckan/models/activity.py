# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

User = get_user_model()


class ActivityManager(models.Manager):
    pass


class Activity(models.Model):
    id = models.TextField(primary_key=True)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(get_user_model())
    # object_id = models.TextField()
    # user_id text,
    # object_id text,
    # revision_id text,
    type = models.TextField(db_column='activity_type')
    data = models.TextField()

    objects = ActivityManager().db_manager('ckan')

    class Meta:
        db_table = 'activity'
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
        managed = False
        abstract = True

    def __unicode__(self):
        pass

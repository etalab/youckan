# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _


class Related(models.Model):
    id = models.TextField(primary_key=True)
    type = models.TextField(default='idea')
    title = models.TextField()
    description = models.TextField()
    image = models.URLField()
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    # sa.Column('title', types.UnicodeText),
    # sa.Column('description', types.UnicodeText),
    # sa.Column('image_url', types.UnicodeText),
    # sa.Column('url', types.UnicodeText),
    # sa.Column('created', types.DateTime, default=datetime.datetime.now),
    # sa.Column('owner_id', types.UnicodeText),
    # sa.Column('view_count', types.Integer, default=0),
    # sa.Column('featured', types.Integer, default=0)

    objects = models.Manager().db_manager('ckan')

    class Meta:
        db_table = 'related'
        managed = False
        verbose_name = _('Related')
        verbose_name_plural = _('Relateds')

    def __unicode__(self):
        return self.title

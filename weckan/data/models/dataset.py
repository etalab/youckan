# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _

from weckan.data.models.activity import Activity
from weckan.data.models.related import Related


class DatasetManager(models.Manager):
    pass


class Dataset(models.Model):
    id = models.TextField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    title = models.TextField()
    url = models.URLField()
    notes = models.TextField()
    # license_id text,
    # revision_id text,
    # author text,
    author = models.TextField()
    # author_email text,
    author_email = models.TextField()
    # maintainer text,
    maintainer = models.TextField()
    # maintainer_email text,
    maintainer_email = models.TextField()
    # state text,
    state = models.TextField()
    # type text,
    # owner_org text,
    # private boolean DEFAULT false,
    private = models.BooleanField(default=False)
    # CONSTRAINT package_pkey PRIMARY KEY (id),
    # CONSTRAINT package_revision_id_fkey FOREIGN KEY (revision_id)
    #   REFERENCES revision (id) MATCH SIMPLE
    #   ON UPDATE NO ACTION ON DELETE NO ACTION,
    # CONSTRAINT package_name_key UNIQUE (name)

    relateds = models.ManyToManyField(Related, through='RelatedDataset')

    objects = DatasetManager().db_manager('ckan')

    class Meta:
        db_table = 'package'
        verbose_name = _('Dataset')
        verbose_name_plural = _('Datasets')

    def __unicode__(self):
        return self.display_name

    @property
    def display_name(self):
        return self.title or self.name


class DatasetActivity(Activity):
    object = models.ForeignKey(Dataset, related_name='activities')
    objects = models.Manager().db_manager('ckan')

    class Meta:
        db_table = 'activity'
        managed = False


class RelatedDataset(models.Model):
    id = models.TextField(primary_key=True)
    related = models.ForeignKey(Related)
    dataset = models.ForeignKey(Dataset)
    status = models.TextField()

    objects = models.Manager().db_manager('ckan')

    class Meta:
        db_table = 'related_dataset'
        managed = False

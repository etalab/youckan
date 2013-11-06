# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Max, Count
from django.views.generic import TemplateView

from youckan.apps.weckan.models.dataset import Dataset


class HomeView(TemplateView):
    template_name = 'home.html'
    nb_datasets = 8

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HomeView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['last_datasets'] = self.last_datasets()
        context['popular_datasets'] = self.popular_datasets()
        return context

    def last_datasets(self):
        '''Get the ``num`` latest created datasets'''
        queryset = Dataset.objects.filter(private=False, state='active')
        queryset = queryset.filter(activities__type='new package')
        queryset = queryset.annotate(timestamp=Max('activities__timestamp'))
        queryset = queryset.order_by('-timestamp')
        return queryset[:self.nb_datasets]

    def popular_datasets(self):
        '''Get the ``num`` most popular (ie. with the most related) datasets'''
        queryset = Dataset.objects.filter(private=False, state='active')
        queryset = queryset.filter(relateddataset__status='active')
        queryset = queryset.annotate(nb_related=Count('relateddataset'))
        queryset = queryset.annotate(timestamp=Max('activities__timestamp'))
        queryset = queryset.order_by('-nb_related', '-timestamp')
        return queryset[:self.nb_datasets]

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from youckan.apps.ckan.views import HomeView, DatasetView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^dataset/(?P<slug>[\w\d_-]+)/$', DatasetView.as_view(), name='dataset'),
)

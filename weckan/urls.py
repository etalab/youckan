# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url('', include('weckan.auth.urls')),
    # url('', include('weckan.data.urls')),

    url(r'^js/', include('djangojs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

# For debug
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

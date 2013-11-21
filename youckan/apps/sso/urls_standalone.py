# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

admin.autodiscover()

handler500 = 'youckan.views.server_error'

redirect_url = reverse_lazy('users') if settings.DEBUG else settings.HOME_URL

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=redirect_url)),
    url('', include('youckan.apps.accounts.urls')),
    url('', include('youckan.apps.sso.urls')),
    # url('', include('youckan.data.urls')),
    url(r'^api/', include('youckan.api')),

    url(r'^js/', include('djangojs.urls')),

    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^admin/', include(admin.site.urls)),
)

# For debug
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'youckan.views.server_error'),
    )

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

admin.autodiscover()

redirect_url = reverse_lazy('users')
# redirect_url = reverse_lazy('users') if settings.DEBUG else settings.ETALAB_HOME

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

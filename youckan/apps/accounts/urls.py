from django.conf.urls import patterns, include, url

from youckan.apps.accounts.views import ProfileView, ProfileEditView

urlpatterns = patterns('',

    url(r'^user/(?P<pk>\d+)/$', ProfileView.as_view(), name='profile'),

    url(r'^my/profile$', ProfileEditView.as_view(), name='profile-edit'),
    url(r'^my/password$', ProfileEditView.as_view(), name='password-change'),
)

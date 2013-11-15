from django.conf.urls import patterns, include, url

from youckan.apps.accounts.views import UserListView, ProfileView, ProfileEditView, AvatarView, AvatarEditView

urlpatterns = patterns('',

    url(r'^users/$', UserListView.as_view(), name='users'),
    url(r'^u/(?P<slug>[\d\w_-]+)/$', ProfileView.as_view(), name='profile'),
    url(r'^u/(?P<slug>[\d\w_-]+)/avatar$', AvatarView.as_view(), name='avatar'),

    url(r'^my/profile/$', ProfileEditView.as_view(), name='profile-edit'),
    url(r'^my/avatar/$', AvatarEditView.as_view(), name='avatar-edit'),
    url(r'^my/password/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'accounts/password_change.html', 'post_change_redirect': 'password-change-done'},
        name='password-change'),
    url(r'^my/password/done$', 'django.contrib.auth.views.password_change',
        {'template_name': 'accounts/password_change_done.html', 'post_change_redirect': 'password-change-done'},
        name='password-change-done'),
)

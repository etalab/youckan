from django.conf.urls import patterns, include, url

from youckan.apps.sso.views import RegisterView, RegisterMailView, RegisterDoneView, login, OAuthAuthorizationView
from oauth2_provider.views import TokenView

urlpatterns = patterns('',
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'sso/logout.html'}, name='logout'),

    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register/mail/$', RegisterMailView.as_view(), name='register-mail'),
    url(r'^register/done/$', RegisterDoneView.as_view(), name='register-done'),

    url(r'^oauth2/authorize/$', OAuthAuthorizationView.as_view(), name="authorize"),
    url(r'^oauth2/token/$', TokenView.as_view(), name="token"),

    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/password/reset/done/', 'template_name': 'sso/password_reset_form.html'},
        name="password-reset"),
    url(r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'sso/password_reset_done.html'}),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/password/done/', 'template_name': 'sso/password_reset_confirm.html'}),
    url(r'^password/done/$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'sso/password_reset_complete.html'}),

    url('', include('social.apps.django_app.urls', namespace='social')),
)

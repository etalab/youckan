from django.conf.urls import patterns, include, url

from youckan.auth.views import ProfileView, ProfileEditView, RegisterView, RegisterMailView, RegisterDoneView, login

urlpatterns = patterns('',
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),

    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register/mail$', RegisterMailView.as_view(), name='register-mail'),
    url(r'^register/done$', RegisterDoneView.as_view(), name='register-done'),

    url(r'^user/(?P<pk>\d+)/$', ProfileView.as_view(), name='profile'),
    url(r'^user/(?P<pk>\d+)/edit$', ProfileEditView.as_view(), name='profile-edit'),


    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    url('', include('social.apps.django_app.urls', namespace='social')),
)

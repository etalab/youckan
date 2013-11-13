# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib.auth.views import login as default_login
from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView

from oauth2_provider.exceptions import OAuthToolkitError
from oauth2_provider.models import get_application_model
from oauth2_provider.views import AuthorizationView

from youckan.apps.sso.forms import LoginForm, RegisterForm

Application = get_application_model()

log = logging.getLogger(__name__)

NEXT_URL_BLACKLIST = (
    reverse_lazy('login'),
    reverse_lazy('logout'),
    reverse_lazy('register'),
)
BLACKLIST_CACHE_KEY = 'NEXT_URL_BLACKLIST'


def get_next_blacklist():
    blacklist = cache.get(BLACKLIST_CACHE_KEY)
    if not blacklist:
        blacklist = [bytes(url) for url in NEXT_URL_BLACKLIST]
        cache.set(BLACKLIST_CACHE_KEY, blacklist)
    return blacklist


def login(request, *args, **kwargs):
    redirect_field_name = 'next'
    if request.method == 'POST':
        if not request.POST.get('remember_me'):
            request.session.set_expiry(0)
    else:
        request.session.pop('partial_pipeline', None)
        redirect_field_name = 'none'
        next_url = request.GET.get('next', '')

        # Hackish way to implement a redirect blacklist
        if next_url in get_next_blacklist():
            redirect_field_name = 'none'
        else:
            request.session['next'] = next_url

    return default_login(request, template_name='sso/login.html', authentication_form=LoginForm,
        redirect_field_name=redirect_field_name, *args, **kwargs)


class RegisterView(CreateView):
    template_name = 'sso/register.html'
    form_class = RegisterForm

    def get_initial(self):
        initial = {}
        if 'userfields' in self.request.session:
            fields = self.request.session['userfields']
            for field_name in 'email', 'first_name', 'last_name':
                if field_name in fields:
                    initial[field_name] = fields[field_name]

        return initial

    def form_valid(self, form):
        response = super(RegisterView, self).form_valid(form)
        self.request.session['new_user'] = self.object
        self.request.session['use_avatar'] = 'use_avatar' in self.request.POST
        return response

    def get_success_url(self):
        backend = self.request.session['partial_pipeline']['backend']
        return reverse('social:complete', kwargs={'backend': backend})


class RegisterDoneView(TemplateView):
    template_name = 'sso/register_done.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterDoneView, self).get_context_data(**kwargs)
        context['next'] = self.request.session.get('next')
        return context


class RegisterMailView(TemplateView):
    template_name = 'sso/register_mail.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterMailView, self).get_context_data(**kwargs)
        context['email'] = self.request.session.get('email_validation_address')
        return context


class OAuthAuthorizationView(AuthorizationView):
    '''
    An OAuth2 authorization view that do not prompt user for validation for internal applications.
    '''

    def get(self, request, *args, **kwargs):
        try:
            scopes, credentials = self.validate_authorization_request(request)

            application = Application.objects.get(client_id=credentials['client_id'])

            if not application.is_internal:
                return super(OAuthAuthorizationView, self).get(request, *args, **kwargs)

            uri, headers, body, status = self.create_authorization_response(
                request=self.request, scopes=' '.join(scopes), credentials=credentials, allow=True)

            return HttpResponseRedirect(uri)

        except OAuthToolkitError as error:
            return self.error_response(error)

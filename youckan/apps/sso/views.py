# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.contrib.auth import login as auth_login, REDIRECT_FIELD_NAME
from django.contrib.sites.models import get_current_site
from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
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


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, current_app=None, extra_context=None, *args, **kwargs):
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    if redirect_to in get_next_blacklist():
        redirect_to = ''

    if request.method == "POST":
        if not request.POST.get('remember_me'):
            request.session.set_expiry(0)

        form = LoginForm(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not redirect_to:
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = LoginForm(request)
        request.session.pop('partial_pipeline', None)
        request.session[REDIRECT_FIELD_NAME] = redirect_to

    current_site = get_current_site(request)

    context = {
        'form': form,
        REDIRECT_FIELD_NAME: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'social_exception_message': request.GET.get('message')
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, 'sso/login.html', context, current_app=current_app)


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
        context['next'] = self.request.session.get(REDIRECT_FIELD_NAME)
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

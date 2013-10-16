# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.views import login as default_login
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView

from youckan.auth.forms import LoginForm, RegisterForm
from youckan.auth.models import YouckanUser


def login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me'):
            request.session.set_expiry(0)
    return default_login(request, template_name='login.html', authentication_form=LoginForm, *args, **kwargs)


class ProfileView(DetailView):
    template_name = 'profile.html'
    model = YouckanUser
    context_object_name = 'user_profile'


class ProfileEditView(UpdateView):
    template_name = 'profile_edit.html'
    model = YouckanUser
    context_object_name = 'user_profile'


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register-done')

    def get_initial(self):
        initial = {}
        if 'email' in self.request.session:
            initial['email'] = self.request.session['email']
        if 'userfields' in self.request.session:
            fields = self.request.session['userfields']
            for field_name in 'first_name', 'last_name':
                if field_name in fields:
                    initial[field_name] = fields[field_name]

        return initial

    def form_valid(self, form):
        response = super(RegisterView, self).form_valid(form)
        self.request.session['new_user'] = self.object
        return response

    def get_success_url(self):
        backend = self.request.session['partial_pipeline']['backend']
        return reverse('social:complete', kwargs={'backend': backend})

    # def get_form_kwargs(self, **kwargs):
    #     kwargs = super(RegisterView, self).get_form_kwargs(**kwargs)
    #     # kwargs['user'] = self.request.user
    #     # kwargs['board'] = ...
    #     # kwargs['post'] = ...
    #     return kwargs


class RegisterDoneView(TemplateView):
    template_name = 'register-done.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterDoneView, self).get_context_data(**kwargs)
        context['next'] = self.request.session.get('next')
        return context


class RegisterMailView(TemplateView):
    template_name = 'register-mail.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterMailView, self).get_context_data(**kwargs)
        context['email'] = self.request.session.get('email_validation_address')
        return context

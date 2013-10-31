# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView, UpdateView

from braces.views import LoginRequiredMixin

from youckan.apps.accounts.forms import UserForm, ProfileFormset
from youckan.models import User
from youckan.views import FormsetsMixin


class ProfileView(DetailView):
    template_name = 'accounts/profile.html'
    model = User
    context_object_name = 'user_profile'


class UserViewMixin(object):
    def get_object(self):
        return self.request.user


class ProfileEditView(LoginRequiredMixin, FormsetsMixin, UserViewMixin, UpdateView):
    template_name = 'accounts/profile_edit.html'
    model = User
    form_class = UserForm

    formsets = {
        'profile': ProfileFormset,
    }

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory

from youckan.models import User, UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'avatar',
            'city',
            'about',
            'website',
        )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


ProfileFormset = inlineformset_factory(User, UserProfile, UserProfileForm, can_delete=False)

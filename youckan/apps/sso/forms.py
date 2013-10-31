# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from youckan.models import User


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].required = True
        self.fields['password'].required = True


class RegisterForm(forms.ModelForm):
    raw_password = forms.CharField(label=_('Password'),
        widget=forms.PasswordInput(attrs={'id': 'raw-password'}))
    password_confirm = forms.CharField(label=_('Confirm password'),
        widget=forms.PasswordInput(attrs={'equalTo': '#raw-password'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': forms.TextInput(attrs={'type': 'email'}),
        }

    def clean_password_confirm(self):
        raw_password = self.cleaned_data.get("raw_password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if raw_password and password_confirm and raw_password != password_confirm:
            raise forms.ValidationError(_("Passwords don't match"))
        return password_confirm

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["raw_password"])
        user.is_active = False
        if commit:
            user.save()
        return user

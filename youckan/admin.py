# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf.urls import patterns, url
from django.core.exceptions import PermissionDenied
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from youckan.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_staff']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(DjangoUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()

    def reset_password(self, request, user_id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.model, pk=user_id)

        form = PasswordResetForm(data={'email': user.email})
        if form.is_valid():
            form.save()
            change_message = self.construct_change_message(request, form, None)
            self.log_change(request, request.user, change_message)
            msg = _('A reset password mail has been sent.')
            messages.success(request, msg)
        return HttpResponseRedirect('..')

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()

        my_urls = patterns('',
            url(r'^(\d+)/reset-password/$',
                self.admin_site.admin_view(self.reset_password),
                name='reset-user-password'
            ),
        )
        return my_urls + urls

admin.site.register(User, UserAdmin)

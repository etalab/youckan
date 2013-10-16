# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os.path import splitext

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from user_avatar.fields import AvatarField

def avatar_file_name(user, filename):
    return '/'.join(['avatars', user.id, filename])

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        '''
        Creates and saves a User with the given email and password.
        '''
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class WeckanUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    avatar = AvatarField(_('Avatar'), blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def full_name(self):
        return '{first_name} {last_name}'.format(**self.__dict__)

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.pk})

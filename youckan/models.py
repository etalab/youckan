# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from autoslug.fields import AutoSlugField
from awesome_avatar.fields import AvatarField
from south.modelsinspector import add_introspection_rules


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


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), max_length=150, unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=64)
    last_name = models.CharField(_('last name'), max_length=64)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    slug = AutoSlugField(editable=False, max_length=150,
            populate_from=lambda instance: instance.email.replace('@', '-at-').replace('.', '-dot-'))

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
        return reverse('profile', kwargs={'slug': self.slug})


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    avatar = AvatarField(_('avatar'), blank=True, null=True)
    city = models.CharField(_('city'), max_length=64, blank=True, null=True)
    about = models.TextField(_('about'), blank=True, null=True)
    website = models.URLField(_('website'), blank=True, null=True)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __unicode__(self):
        return '{0} profile'.format(self.user)


@receiver(post_save, sender=User, dispatch_uid="youckan.sync_users")
def sync_on_save(sender, instance, created, **kwargs):
    from youckan.tasks import sync_users
    sync_users.delay(instance.email)


@receiver(post_save, sender=User, dispatch_uid="youckan.create_profile")
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


add_introspection_rules([
    (
        [AvatarField],  # Class(es) these apply to
        [],         # Positional arguments (not used)
        {           # Keyword argument
            "width": ["width", {}],
            "height": ["height", {}],
        },
    ),
], ["^awesome_avatar\.fields\.AvatarField"])

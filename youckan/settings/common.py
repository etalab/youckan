# -*- coding: utf-8 -*-
'''
Common settings shared between all settings
'''
from __future__ import unicode_literals

import codecs
import pkg_resources
import sys
import os

import dj_database_url

from ConfigParser import RawConfigParser as ConfigParser

from os.path import join, dirname, exists, abspath
from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _


PACKAGE_ROOT = abspath(join(dirname(__file__), '..'))


def _merge_config(into, filename):
    '''Read and merge a config file into a given dictionnary'''
    config = ConfigParser()
    with codecs.open(filename, encoding='utf8') as fp:
        config.readfp(fp)
    for section in config.sections():
        if not section in into:
            into[section] = {}
        into[section].update(config.items(section))


conf = {}
_merge_config(conf, pkg_resources.resource_filename(__name__, 'default.ini'))

# Loads config from environment variable or current directory
if 'YOUCKAN_CONF' in os.environ:
    _merge_config(conf, os.environ['YOUCKAN_CONF'])
elif exists('youckan.ini'):
    _merge_config(conf, 'youckan.ini')


TESTING = 'test' in sys.argv
DEBUG = TESTING or conf['site']['debug'] == 'true'
TEMPLATE_DEBUG = DEBUG

if conf['site'].get('admins'):
    ADMINS = [row.split(',') for row in conf['site']['admins'].split('\n') if row]
else:
    ADMINS = []

MANAGERS = ADMINS

DATABASES = {
    'default': dj_database_url.parse(conf['db']['default']),
    # 'ckan': dj_database_url.parse(conf['db']['ckan']),
}


DEFAULT_FROM_EMAIL = conf['email']['webmaster']
SERVER_EMAIL = conf['email']['admin']

if conf['email'].get('host'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = conf['email']['host']
    EMAIL_PORT = int(conf['email'].get('port', 0)) or global_settings.EMAIL_PORT
    EMAIL_HOST_USER = conf['email'].get('user', global_settings.EMAIL_HOST_USER)
    EMAIL_HOST_PASSWORD = conf['email'].get('password', global_settings.EMAIL_HOST_PASSWORD)
    EMAIL_USE_TLS = conf['email'].get('tls') == 'true' if 'tls' in conf['email'] else global_settings.EMAIL_USE_TLS
    EMAIL_SUBJECT_PREFIX = conf['email'].get('prefix', '[youckan]')
    if not EMAIL_SUBJECT_PREFIX.endswith(' '):
        EMAIL_SUBJECT_PREFIX += ' '
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ALLOWED_HOSTS += [host.strip() for host in conf['site']['allowed_hosts'].split('\n') if host.strip()]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = conf['site']['timezone']

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = conf['site']['language']

LANGUAGES = (
    ('fr', 'Français'),
    ('en', 'English'),
    ('de', 'Deutsch'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = conf['site']['secret']

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'youckan.context_processors.etalab_config',
)

JS_CONTEXT_PROCESSOR = 'youckan.context_serializer.YouckanContextSerializer'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'youckan.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'youckan.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

import djcelery
djcelery.setup_loader()
BROKER_URL = conf['celery']['broker']
CELERY_RESULT_BACKEND = conf['celery']['backend']

PROJECT_APPS = (
    'youckan',
    'youckan.apps.accounts',
    'youckan.apps.ckan',
    'youckan.apps.sso',
)

THIRD_PARTY_APPS = (
    'south',
    'pipeline',
    'djangojs',
    'rest_framework',
    'django_gravatar',
    'awesome_avatar',
    # 'avatar',
    'social.apps.django_app.default',
    'oauth2_provider',
    'corsheaders',
    'djcelery',
    'suit',
)

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

INSTALLED_APPS = PROJECT_APPS + THIRD_PARTY_APPS + DJANGO_APPS


PROFILE_WIDGETS = (
    'youckan.apps.ckan.profile.OrganizationsWidget',
    'youckan.apps.ckan.profile.DatasetsWidget',
    'youckan.apps.ckan.profile.ValorizationsWidget',
    'youckan.apps.ckan.profile.UsefulsWidget',
    # 'youckan.apps.accounts.widgets.BadgesWidget',
)


SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'YouCKAN',
    # 'MENU_EXCLUDE': ('sites.site',),
    'MENU': (
        bytes('sites'),
        {'label': _('Authentication'), 'icon': 'icon-lock', 'models': (
            bytes('youckan.user'),
            bytes('auth.group'),
        )},
        {'label': _('OAuth2'), 'icon': 'icon-certificate', 'models': (
            bytes('sso.oauth2application'),
            bytes('oauth2_provider.accesstoken'),
            bytes('oauth2_provider.refreshtoken'),
            bytes('oauth2_provider.grant'),
        )},
        {'label': _('Social'), 'icon': 'icon-globe', 'models': (
            bytes('default.usersocialauth'),
            bytes('default.association'),
            bytes('default.nonce'),
        )},
        {'label': _('Tasks'), 'icon': 'icon-cog', 'models': (
            bytes('djcelery.taskstate'),
            bytes('djcelery.workerstate'),
            bytes('djcelery.periodictask'),
            bytes('djcelery.intervalschedule'),
            bytes('djcelery.crontabsschedule'),
        )},
    ),
}

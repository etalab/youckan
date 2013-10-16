# -*- coding: utf-8 -*-
# Django settings for youckan project.
from os.path import join, dirname
from django.core.urlresolvers import reverse_lazy

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


PACKAGE_ROOT = dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'youckan.sqlite',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    },
    'ckan': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ckan',
        'USER': 'ckan',
        'PASSWORD': 'ckan',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

DEFAULT_FROM_EMAIL = 'webmaster@etalab2.fr'
EMAIL_BACKEND = 'django_sendmail_backend.backends.EmailBackend'

DOMAIN = 'etalab.dev'
HOME_URL = 'http://www.etalab.dev'
WIKI_URL = 'http://wiki.etalab.dev'
WIKI_API_URL = 'http://wiki.etalab.dev/api.php'
QUESTIONS_URL = 'http://questions.etalab.dev'
MENU_TOPICS = (
    (u'Culture et communication', 'culture', None),
    (u'Développement durable', 'wind', '{wiki}/Le_D%C3%A9veloppement_Durable'),
    (u'Éducation et recherche', 'education', None),
    (u'État et collectivités', 'france', None),
    (u'Europe', 'europe', None),
    (u'Justice', 'justice', None),
    (u'Monde', 'world', None),
    (u'Santé et solidarité', 'heart', None),
    (u'Sécurité et défense', 'shield', None),
    (u'Société', 'people', None),
    (u'Travail, économie, emploi', 'case', None),
)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr'

LANGUAGES = (
    ('fr', 'Français'),
    ('en', 'English'),
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

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = 'media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = 'staticroot'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ('fonts', join(PACKAGE_ROOT, 'static', 'bower', 'bootstrap', 'fonts')),
    ('fonts', join(PACKAGE_ROOT, 'static', 'bower', 'etalab-assets', 'fonts')),
    ('images/flags', join(PACKAGE_ROOT, 'static', 'bower', 'flags', 'flags', 'flags-iso', 'shiny', '16')),
    ('images', join(PACKAGE_ROOT, 'static', 'bower', 'etalab-assets', 'img')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+hant#30d^df=1$vbolo3p+6t6xdio5312@a63-8b^96q3n-u@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
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
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTH_USER_MODEL = 'auth.YouckanUser'

AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.linkedin.LinkedinOAuth2',
    'youckan.auth.backends.NoSocialAuth',
    'django.contrib.auth.backends.ModelBackend',
)


LOGIN_REDIRECT_URL = HOME_URL
LOGIN_ERROR_URL = reverse_lazy('login')
LOGIN_URL = reverse_lazy('login')

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_FORCE_EMAIL_VALIDATION = True
SOCIAL_AUTH_SANITIZE_REDIRECTS = False

SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'youckan.auth.mail.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = reverse_lazy('register-mail')

# SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# Used to redirect new registered users, will be used in place of SOCIAL_AUTH_LOGIN_REDIRECT_URL if defined.
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = reverse_lazy('register-done')
# Like SOCIAL_AUTH_NEW_USER_REDIRECT_URL but for new associated accounts (user is already logged in). Used in place of SOCIAL_AUTH_LOGIN_REDIRECT_URL
# SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'
# The user will be redirected to this URL when a social account is disconnected
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = reverse_lazy('logout')
# SOCIAL_AUTH_INACTIVE_USER_URL = '/inactive-user/'
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '263896935856.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'pky5p4zZcq1t-xlOQNfOJPfU'

SOCIAL_AUTH_TWITTER_KEY = 'IBTTJfsInsbMbxBVD7ymw'
SOCIAL_AUTH_TWITTER_SECRET = '8fUgUpN0To13G4EXE6de7W1eGZF4aEcHangJoEuPs'

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = 'hcaxcat3jlbq'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = 'FSXMMbJw42OeKbWM'
# https://developer.linkedin.com/documents/authentication#granting
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress', 'r_contactinfo']
# http://developer.linkedin.com/documents/profile-fields
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = [
    'email-address',
    'first-name',
    'last-name',
    'picture-url',
    'picture-urls::(original)',
]
# Arrange to add the fields to UserSocialAuth.extra_data
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    ('id', 'id'),
    ('first-name', 'first_name'),
    ('last-name', 'last_name'),
    ('email-address', 'email_address'),
]

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'youckan.auth.pipeline.new_registeration_only',
    'social.pipeline.user.get_username',
    # 'social.pipeline.user.create_user',
    # 'social.pipeline.social_auth.load_extra_data',
    # 'social.pipeline.user.user_details'
    'youckan.auth.pipeline.get_avatar_url',
    'youckan.auth.pipeline.register_form',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.social_auth.associate_user',
    'youckan.auth.pipeline.fetch_avatar',
    'youckan.auth.pipeline.activate_user',
)

ROOT_URLCONF = 'youckan.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'youckan.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

PROJECT_APPS = (
    'youckan',
    'youckan.auth'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

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
) + PROJECT_APPS

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)

LESS_INCLUDE_PATHS = (
    'bower/etalab-assets/less',
    'bower/bootstrap/less',
)

_less_include_path = (join(PACKAGE_ROOT, 'static', path) for path in LESS_INCLUDE_PATHS)
PIPELINE_LESS_ARGUMENTS = '--include-path=%s' % ':'.join(_less_include_path)

# PIPELINE_CSS_COMPRESSOR = 'webnotes.compressors.CSSMinCompressor'

PIPELINE_CSS = {
    'youckan': {
        'source_filenames': (
            'less/youckan.less',
        ),
        'output_filename': 'css/weckab.min.css',
    },
}

# PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'

PIPELINE_JS = {
    'modernizr': {
        'source_filenames': (
            'bower/modernizr/modernizr.js',
            'bower/respond/respond.src.js',
        ),
        'output_filename': 'js/modernizr.min.js',
    },
    'jquery': {
        'source_filenames': {
            'bower/jquery/jquery.js',
        },
        'output_filename': 'js/jquery.min.js',
    },
    'jquery-legacy': {
        'source_filenames': {
            'bower/jquery-legacy/index.js',
        },
        'output_filename': 'js/jquery-legacy.min.js',
    },
    'youckan-common': {
        'source_filenames': (
            'bower/bootstrap/dist/js/bootstrap.js',
            'bower/jquery.cookie/jquery.cookie.js',
            'bower/jquery.validation/jquery.validate.js',
            'bower/typeahead.js/dist/typeahead.js',
            'bower/swig/index.js',
            'bower/etalab-assets/js/etalab-site.js',
            'js/djangojs/django.js',
            'js/common.js',
        ),
        'output_filename': 'js/youckan.min.js'
    },
    'home': {
        'source_filenames': (
            'js/home.js'
        ),
        'output_filename': 'js/home.min.js',
    },

}


# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


try:
    import debug_toolbar
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = ('127.0.0.1',)
except:
    pass

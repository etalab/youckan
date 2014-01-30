# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy

from youckan.settings.common import conf, DEBUG, HTTPS
from youckan.settings.etalab import HOME_URL, DOMAIN

SESSION_COOKIE_DOMAIN = '.{0}'.format(DOMAIN)
SESSION_COOKIE_NAME = 'youckan.session'

# SESSION_SERIALIZER = 'redis_sessions_fork.serializers.UjsonSerializer',
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SESSION_ENGINE = 'redis_sessions_fork.session'
SESSION_REDIS_PREFIX = 'session'
# TODO: tune redis config


CSRF_COOKIE_SECURE = HTTPS

AUTH_USER_MODEL = 'youckan.User'

AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.linkedin.LinkedinOAuth2',
    'youckan.apps.sso.backends.NoSocialAuth',
    'django.contrib.auth.backends.ModelBackend',
)


LOGIN_REDIRECT_URL = HOME_URL
LOGIN_ERROR_URL = reverse_lazy('login')
LOGIN_URL = reverse_lazy('login')

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
# SOCIAL_AUTH_FORCE_EMAIL_VALIDATION = True
SOCIAL_AUTH_SANITIZE_REDIRECTS = False

# SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'youckan.apps.sso.mail.send_validation'
# SOCIAL_AUTH_EMAIL_VALIDATION_URL = reverse_lazy('register-mail')

# SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# Used to redirect new registered users, will be used in place of SOCIAL_AUTH_LOGIN_REDIRECT_URL if defined.
# SOCIAL_AUTH_NEW_USER_REDIRECT_URL = reverse_lazy('register-mail')
SOCIAL_AUTH_INACTIVE_USER_URL = reverse_lazy('register-mail')
# Like SOCIAL_AUTH_NEW_USER_REDIRECT_URL but for new associated accounts (user is already logged in).
# Used in place of SOCIAL_AUTH_LOGIN_REDIRECT_URL
# SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'
# The user will be redirected to this URL when a social account is disconnected
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = reverse_lazy('logout')
# SOCIAL_AUTH_INACTIVE_USER_URL = '/inactive-user/'
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email']

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = conf['social:google']['key']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = conf['social:google']['secret']

SOCIAL_AUTH_TWITTER_KEY = conf['social:twitter']['key']
SOCIAL_AUTH_TWITTER_SECRET = conf['social:twitter']['secret']

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = conf['social:linkedin']['key']
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = conf['social:linkedin']['secret']
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
    'youckan.apps.sso.pipeline.new_registeration_only',
    'social.pipeline.user.get_username',
    'youckan.apps.sso.pipeline.get_avatar_url',
    'youckan.apps.sso.pipeline.register_form',
    'youckan.apps.sso.pipeline.fix_no_social_auth',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'youckan.apps.sso.pipeline.fetch_avatar',
    'youckan.apps.sso.pipeline.prepare_mail_validation',
)

OAUTH2_PROVIDER = {
    'SCOPES': {
        'profile': 'Read profile',
    },
    'APPLICATION_MODEL': 'sso.OAuth2Application',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# CORS_ORIGIN_WHITELIST = (
#     DOMAIN,
# )

CORS_ORIGIN_REGEX_WHITELIST = (
    r'^https?://(\w+\.)?{0}$'.format(DOMAIN.replace('.', '\.')),
)

CORS_ALLOW_CREDENTIALS = True
CORS_URLS_REGEX = r'^/api/.*$'


if DEBUG:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += (
        'rest_framework.authentication.BasicAuthentication',
    )

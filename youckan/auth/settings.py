from youckan.settings import *

PROJECT_APPS = (
    'youckan',
    'youckan.auth',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

ROOT_URLCONF = 'youckan.auth.urls_standalone'

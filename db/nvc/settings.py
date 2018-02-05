"""
Django settings for nvc project.

Based on the Django 1.9 template, with wq-specific modifications noted as such.
Generated by 'wq start' 1.0.0.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/

For more information about wq.db's Django settings see
http://wq.io/docs/settings

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from .local_settings import SECRET_KEY, DEBUG

# wq: extra dirname() to account for db/ folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# wq: SECRET_KEY and DEBUG are defined in local_settings.py
SECRET_KEY = SECRET_KEY

ALLOWED_HOSTS = [
    "medullaskyline.com",
    "localhost",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    # Uncomment to enable python-social-auth
    # 'social.apps.django_app.default',
    'wq.db.rest',
    'wq.db.rest.auth',
    'smart_selects',
    # added to try the relate pattern
    'wq.db.patterns.relate',

    # Project apps
    'entries',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nvc.urls'

# wq: Recommended settings for Django, rest_framework, and social auth
from wq.db.default_settings import (
    TEMPLATES,
    SESSION_COOKIE_HTTPONLY,
    REST_FRAMEWORK,
    SOCIAL_AUTH_PIPELINE,
)

TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'master_templates')]
TEMPLATES[1]['DIRS'] = [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'master_templates')]

# wq: Recommended settings unique to wq.db
from wq.db.default_settings import (
    ANONYMOUS_PERMISSIONS,
    SRID,
    DEFAULT_AUTH_GROUP,
)

WSGI_APPLICATION = 'nvc.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# wq: DATABASES is defined in local_settings.py

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# wq: Put social auth backends here (see http://psa.matiasaguirre.net/docs/backends/)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
LOGIN_REDIRECT_URL = '/login'

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# wq: Configure paths for default project layout
STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
VERSION_TXT = os.path.join(BASE_DIR, 'version.txt')
MEDIA_URL = '/media/'

# wq: Import local settings
try:
    from .local_settings import *
except ImportError:
    pass

# wq: Determine if we are running off django's testing server
import sys

DEBUG_WITH_RUNSERVER = 'manage.py' in sys.argv[0]

JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js'

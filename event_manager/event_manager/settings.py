"""
Django settings for event_manager project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*arvy=e9d^nk!-cb&*9irda1e=cj5ssbi$-k#ih+doon#u4+9e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users',
    'visit',
    'management',
    'api',
    'mail_templated',
    'widget_tweaks',
    'betterforms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'event_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'event_manager.wsgi.application'
AUTH_USER_MODEL = 'users.User'

LOGIN_REDIRECT_URL = '/home'
LOGOUT_REDIRECT_URL = '/home'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SINGLE_VISITOR = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.environ.get('EM_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EM_EMAIL_HOST_PASSWORD')

EM_DEFAULT_COMPANY_NAME = os.environ.get('EM_DEFAULT_COMPANY_NAME', 'Holmes Home')
EM_DEFAULT_COMPANY_ADD_1 = os.environ.get('EM_DEFAULT_COMPANY_ADD_1', '221B Baker Street')
EM_DEFAULT_COMPANY_ADD_2 = os.environ.get('EM_DEFAULT_COMPANY_ADD_2', None)
EM_DEFAULT_COMPANY_ZIP_CODE = os.environ.get('EM_DEFAULT_COMPANY_ZIP_CODE', 'NW1 6XE')
EM_DEFAULT_COMPANY_CITY = os.environ.get('EM_DEFAULT_COMPANY_CITY', 'London')
EM_DEFAULT_COMPANY_COUNTRY = os.environ.get('EM_DEFAULT_COMPANY_COUNTRY', 'England')

DEFAULT_OFFICE_ADDRESS = {
    'name': EM_DEFAULT_COMPANY_NAME,
    'add1': EM_DEFAULT_COMPANY_ADD_1,
    'add2': EM_DEFAULT_COMPANY_ADD_2,
    'zip': EM_DEFAULT_COMPANY_ZIP_CODE,
    'city': EM_DEFAULT_COMPANY_CITY,
    'country': EM_DEFAULT_COMPANY_COUNTRY
}

ALLOW_EMAILS = True

# AUTHENTICATION_BACKENDS = ('users.auth_backend.PasswordlessAuthBackend',
#                            'django.contrib.auth.backends.ModelBackend',)

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

HOST_REPR = 'employee'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

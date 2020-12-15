"""
Django settings for ecommerce_site project.
Generated by 'django-admin startproject' using Django 3.0.7.
For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
from django.contrib import messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+#q+csvjzmt7!lh&#db&e9)(c4=62h4c^p2^599o0@=(u$sn-^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'users',
    # third-party apps
    'crispy_forms',
    'django_summernote',
    'widget_tweaks',
    'phonenumber_field',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',
    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'order.apps.OrderConfig',
    'coupons.apps.CouponsConfig',
    'sell',
    'marketing',
    'achironet_admin'
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

ROOT_URLCONF = 'ecommerce_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ecommerce_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'achironetmarketplace',
        'USER': 'achironetmarketplace',
        'PASSWORD': '@random#2019LDAP',
        'HOST': '45.79.127.228',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Tweak the messages dictionary tags to match bootstrap classes
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
AWS_ACCESS_KEY_ID = 'AKIAUJG4P2TTMUWJPMPW'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'achironetmarketplace'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.af-south-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'ecommerce_site.settings.storage_backends.MediaStorage'


# Crispy templates for form rendering
CRISPY_TEMPLATE_PACK = 'bootstrap4'

CART_SESSION_ID = 'cart'

# Authentication custom user
AUTH_USER_MODEL = 'users.User'

# django-allauth settings
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = "/users/choose"

# the site name
ECOMMERCE_SITE_NAME = 'Ecommerce'
STRIPE_SECRET_KEY = 'sk_test_AtEc25PGFsh4lksCjP17kS2H'

# Set X_FRAME_OPTIONS
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Specify the email backend
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

AMDINS = [
    ('Patrice', 'chaulapsx@gmail.com'), ('Robert', 'robertechiduku@gmail.com')
]

# USED when testing
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

# configure summer-note
SUMMERNOTE_CONFIG = {
    'width': '100%'
}

TIME_ZONE = "Africa/Harare"

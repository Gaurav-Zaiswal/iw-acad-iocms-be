from pathlib import Path
import os

from .env import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# DEBUG = False

# ALLOWED_HOSTS = ["gauravjaiswal.pythonanywhere.com", "aithonclass.heroku.com", "localhost", "127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'classroom',
    'assignment',
    'feed',
    'search',
    'attendance',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
     'django_elasticsearch_dsl'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware'
]

ROOT_URLCONF = 'iocms.urls'

# CORS_ALLOWED_ORIGINS = [
#     *
# ]
CORS_ORIGIN_ALLOW_ALL = True

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

WSGI_APPLICATION = 'iocms.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': os.path.join(BASE_DIR, './database.cnf'),
#         },
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'users.User'
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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     BASE_DIR / "static",
#     # '/var/www/static/',
# ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


######################################
#        extra settings here        ##
######################################

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5
}

# DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
# STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'

DEFAULT_FILE_STORAGE = 'iocms.custom_azure.AzureMediaStorage'
STATICFILES_STORAGE = 'iocms.custom_azure.AzureStaticStorage'

AZURE_ACCOUNT_NAME = 'aithonimages'
AZURE_ACCOUNT_KEY = '6DOaVUjMpn7XYQvXPw66tIgiejKeMoqy5YF0BzoyfR1mPM7kWrPkvVC+sXtYzLrVSe/oLHJfh9Oe+AStmcY5/A=='
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net' 

STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'

# Elastic search configs
# connect to instance of elasticsearch ALREADY RUNNING at localhost:9200
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://127.0.0.1:9200',
        'requestTimeout': 60000 
    },
}

import os

"""
Django settings for blango project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from configurations import Configuration
from configurations import values
import dj_database_url


class Dev(Configuration):
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-+sn%dpa!086+g+%44z9*^j^q-u4n!j(#wl)x9a%_1op@zz2+1-'

    ALLOWED_HOSTS = values.ListValue(["localhost", "0.0.0.0", ".codio.io"])
    X_FRAME_OPTIONS = 'ALLOW-FROM ' + os.environ.get('CODIO_HOSTNAME') + '-8000.codio.io'
    CSRF_COOKIE_SAMESITE = None
    CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('CODIO_HOSTNAME') + '-8000.codio.io']
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SAMESITE = 'None'


    # Application definition
    INSTALLED_APPS = [

        'blango_auth', # prioritized over django admin
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        # django-allauth
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.google',
        #
        'django.contrib.staticfiles',
        'crispy_forms',
        'crispy_bootstrap5',
        'blog',
        'debug_toolbar',
        'rest_framework',
        'rest_framework.authtoken',
        'drf_yasg',

    ]

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        #'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    # For Codio platform only, TBR
    INTERNAL_IPS = ["192.168.10.93"]

    # Tests email registration in terminal
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    
    AUTH_USER_MODEL = "blango_auth.User"
    ACCOUNT_ACTIVATION_DAYS = 7
    REGISTRATION_OPEN = True
    
    # Django Allauth
    SITE_ID = 1
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_AUTHENTICATION_METHOD = "email"

    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.Argon2PasswordHasher', # recommended (pip3 install django[argon2])
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
        'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    ]

    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
    CRISPY_TEMPLATE_PACK = "bootstrap5"

    ROOT_URLCONF = 'blango.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
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

    WSGI_APPLICATION = 'blango.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/3.2/ref/settings/#databases

    # Three slashes after the schema indicates the empty hostname.
    #DATABASES = values.DatabaseURLValue(f"sqlite:///{BASE_DIR}/db.sqlite3")
    DATABASES = {
      "default": dj_database_url.config(default=f"sqlite:///{BASE_DIR}/db.sqlite3"),
      "alternative": dj_database_url.config(
        "ALTERNATIVE_DATABASE_URL",
        default=f"sqlite:///{BASE_DIR}/alternative_db.sqlite3",
      ),
    }  
# DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': BASE_DIR / 'db.sqlite3',
    #     }
    # }

    # Password validation
    # https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/3.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = values.Value("UTC")
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/

    STATIC_URL = '/static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # Logging
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
        },
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "verbose",
            },
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
                "filters": ["require_debug_false"],
            },
        },
        "loggers": {
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    }
    
    # DRF
    from rest_framework import authentication
    from rest_framework import permissions
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.BasicAuthentication",
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.TokenAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            # APIs only accessible with authentication
            #"rest_framework.permissions.IsAuthenticated",
            "rest_framework.permissions.IsAuthenticatedOrReadOnly"
        ],
    }

    SWAGGER_SETTINGS = {
        "SECURITY_DEFINITIONS": {
            "Token": {"type": "apiKey", "name": "Authorization", "in": "header"},
            "Basic": {"type": "basic"},
        }
    }

class Prod(Dev):
    DEBUG = values.BooleanValue(False)
    SECRET_KEY = values.SecretValue()

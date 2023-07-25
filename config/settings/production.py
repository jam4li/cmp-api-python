# -----------------------------------------------------------------------------
# This file contains settings specific to the production environment,
# such as disabling debug mode, configuring the production database,
# and other production-related settings.
# -----------------------------------------------------------------------------

import os
from .base import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update this to match your domain(s)
ALLOWED_HOSTS = [
    'cm-enterprise.net',
    'www.cm-enterprise.net',
    'backend.cm-enterprise.net',
]

INSTALLED_APPS += [
    'corsheaders',
]

MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware',)

# Use a more secure secret key in production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Add any other production-specific settings here

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'https://cm-enterprise.net',
)

# Sentry config

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

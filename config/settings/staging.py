# -----------------------------------------------------------------------------
# This file contains settings specific to the staging environment,
# which is a testing environment that closely mirrors the production environment.
# -----------------------------------------------------------------------------

import os
from .base import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update this to match your domain(s)
ALLOWED_HOSTS = ['staging.cloudminepro.com']

# Use a more secure secret key in staging
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Add any other staging-specific settings here
# For example, you may want to configure HTTPS settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

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

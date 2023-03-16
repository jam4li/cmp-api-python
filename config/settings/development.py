# -----------------------------------------------------------------------------
# This file contains settings specific to the development environment,
# such as enabling debug mode, using a local database, and
# configuring other development-related settings.
# -----------------------------------------------------------------------------

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Add any other development-specific settings here
# For example, if you want to enable Django Debug Toolbar in development
# 1. Install the package: pip install django-debug-toolbar
# 2. Add the following lines to your development.py settings
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
# INTERNAL_IPS = ['127.0.0.1']

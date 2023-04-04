# -----------------------------------------------------------------------------
# This file contains settings specific to the development environment,
# such as enabling debug mode, using a local database, and
# configuring other development-related settings.
# -----------------------------------------------------------------------------

from .base import *


def get_docker_host_ip():
    import socket
    return socket.gethostbyname(socket.gethostname())


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Django debug toolbar config

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

DEBUG_TOOLBAR_CONFIG = {
    'ENABLE_STACKTRACES': True,
    'HIDE_DJANGO_SQL': False,
    'HIDE_TEMPLATE_LOADERS': False,
    'SHOW_COLLAPSED': True,
    'SQL_WARNING_THRESHOLD': 100,
}

# cmp_api_python/celery.py
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

app = Celery("cmp_api_python")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

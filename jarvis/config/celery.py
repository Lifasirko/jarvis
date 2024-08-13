from __future__ import absolute_import, unicode_literals
from django.conf import settings
import os

from celery import Celery

import sys
print(sys.path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jarvis.config.settings')

app = Celery('jarvis.config', broker=settings.CELERY_BROKER_URL)

app.conf.broker_connection_retry_on_startup = True

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
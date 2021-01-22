from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CeleryRedis.settings')

app = Celery('CeleryRedis')
app.conf.broker_heartbeat = 0



app.config_from_object('django.conf:settings', namespace='CELERY')



app.autodiscover_tasks()

from celery.schedules import crontab
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'sum',
        'schedule': 30.0,
        'args': (10, 10)
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
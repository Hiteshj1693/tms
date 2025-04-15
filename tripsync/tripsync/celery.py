import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tripsync.settings')

app = Celery('tripsync')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.schedules import crontab

# Task Scheduling
app.conf.beat_schedule = {
    'add-every-60-seconds': {
        'task': 'apps.trips.tasks.delete_blacklisted_tokens',   
        'schedule': crontab(minute='*/1'),
    },
}
app.conf.timezone = 'UTC'



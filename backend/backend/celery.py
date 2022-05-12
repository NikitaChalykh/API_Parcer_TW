import os

from celery import Celery
from celery.schedules import crontab

from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery(
    'backend',
    broker=os.getenv('BROKER')
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = os.getenv('BROKER_URL')

app.conf.timezone = 'Europe/Moscow'

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-hour-parcing': {
        'task': 'api.tasks.get_data',
        'schedule': crontab(minute='*/1')
    },
}

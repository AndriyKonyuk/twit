from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from celery.task import periodic_task
# from twitter_monitoring.models import User, Followers
from datetime import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twit.settings')

app = Celery('twit', backend='amqp',broker='amqp://guest@localhost//')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# @periodic_task(run_every=timedelta(seconds=10))
# def update_tweets():
#     print('Hello world!')
#     # u = User.objects.get(username='Admin')
#     # q = Followers(screen_name='poroshenko', name_foll='Петро Порошенко', id_foll=2423747006, user_id=u.id)
#     # q.save()

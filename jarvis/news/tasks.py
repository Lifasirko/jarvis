from celery import shared_task
from jarvis.config.celery import app
from django.core.management import call_command

@shared_task
def update_news_task():
    call_command('update_news')

@shared_task
def up():
    print('2')

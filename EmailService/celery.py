import os 
from celery import Celery 
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmailService.settings') 

app = Celery('EmailService') 
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks() 

app.conf.beat_schedule = {
    'update_telegram_chats': {
        'task': 'telegram_sender.tasks.update_telegram_chats_task',
        'schedule': crontab(hour=0, minute=0),  
    }, 
    'check_email_data_correctness': {
        'task': 'main.tasks.check_email_data_correctness',
        'schedule': crontab(hour=0, minute=0),  
    }
}
import os 
from celery import Celery 


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmailService.settings') 

app = Celery('EmailService') 
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks() 
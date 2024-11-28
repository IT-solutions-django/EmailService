from django.urls import path
from .views import *


app_name = 'main' 


urlpatterns = [
    path('send-email/', SendEmailView.as_view(), name='send_email'),
]
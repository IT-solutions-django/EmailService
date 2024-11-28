from django.core.mail import EmailMessage
from django.core.mail import send_mail, get_connection  
from dotenv import load_dotenv
from celery import shared_task 
import os


load_dotenv()



@shared_task(bind=True, max_retries=5)
def send_email_task(
    self, 
    sender: str, 
    host: str,
    password: str,
    recipient: str, 
    subject: str, 
    content: str, 
) -> None:     
    connection = get_connection(
        host=host,
        port=587,
        username=sender,
        password=password,
        use_tls=True,
        use_ssl=False,
    )
    send_mail(
        subject=subject, 
        message=content, 
        from_email=sender, 
        recipient_list=[recipient], 
        connection=connection
    )

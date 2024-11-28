from django.core.mail import send_mail, get_connection  
from dotenv import load_dotenv
from celery import shared_task 
from smtplib import SMTPException, SMTPAuthenticationError, SMTPConnectError
from loguru import logger
import os


load_dotenv()



@shared_task(bind=True, max_retries=3)
def send_email_task(
    self, 
    sender: str, 
    host: str,
    password: str,
    recipient: str, 
    subject: str, 
    content: str, 
) -> None:     
    try:
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
    except SMTPAuthenticationError as e:
        logger.error(f'Ошибка авторизации. Отправитель: {sender}, получатель: {recipient}. Тема: {subject}')
    except SMTPConnectError as e:
        if self.request.retries >= self.max_retries:
            logger.error(
                f'Ошибка подключения: {e}. Отправитель: {sender}, получатель: {recipient}. Тема: {subject}'
            )
        self.retry(exc=e, countdown=20)  
    except SMTPException as e:
        self.retry(exc=e, countdown=20) 
    except Exception as e:
        if self.request.retries >= self.max_retries:
            logger.error(f'Непредвиденная ошибка: {e}. Отправитель: {sender}, получатель: {recipient}. Тема: {subject}')
        raise self.retry(exc=e, countdown=20)
    
    logger.info(f'Письмо было успешно отправлено. Отправитель: {sender}, получатель: {recipient}. Тема: {subject}')


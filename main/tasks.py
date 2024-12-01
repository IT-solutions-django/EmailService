from django.core.mail import send_mail, get_connection  
from dotenv import load_dotenv
from celery import shared_task 
from smtplib import SMTPException, SMTPAuthenticationError, SMTPConnectError
from loguru import logger
from telegram_sender.tasks import send_telegram_message_for_all_task


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
    context_log_info = f'Отправитель: {sender}, получатель: {recipient}, тема: {subject}'
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
        log_text = f'Ошибка авторизации. {context_log_info}'
        logger.error(log_text)
        send_telegram_message_for_all_task.delay(message=log_text)
        return

    except SMTPConnectError as e:
        if self.request.retries >= self.max_retries:
            log_text = f'Ошибка подключения: {e}. {context_log_info}'
            logger.error(log_text)
            send_telegram_message_for_all_task.delay(message=log_text)
        self.retry(exc=e, countdown=20)  

    except SMTPException as e:
        if self.request.retries >= self.max_retries:
            log_text = f'Ошибка: {e}. {context_log_info}'
            logger.error(log_text)
            send_telegram_message_for_all_task.delay(message=log_text)
        self.retry(exc=e, countdown=20) 
        
    except Exception as e:
        if self.request.retries >= self.max_retries:
            log_text = f'Непредвиденная ошибка: {e}. {context_log_info}'
            logger.error(log_text)
            send_telegram_message_for_all_task.delay(message=log_text)
        raise self.retry(exc=e, countdown=20)
    
    logger.info(f'Письмо было успешно отправлено. {context_log_info}')
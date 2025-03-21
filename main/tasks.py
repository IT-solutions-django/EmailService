from django.core.mail import send_mail, get_connection  
from dotenv import load_dotenv
from celery import shared_task 
from smtplib import SMTPException, SMTPAuthenticationError, SMTPConnectError
from loguru import logger
from telegram_sender.tasks import send_telegram_message_for_all_task
from .models import IpAddress


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


@shared_task(bind=True, max_retries=3)
def check_email_data_correctness(self): 
    """Проверка того, что данные по всем серверам валидны. Отправка писем на тестовую почту"""
    ips = IpAddress.objects.all() 
    for ip in ips: 
        context_log_info = f'Отправитель: {ip.email}, получатель: sendmail.regular.check@gmail.com, тема: Проверка корректности работы'
        try:
            connection = get_connection(
                host=ip.host,
                port=587,
                username=ip.email,
                password=ip.password,
                use_tls=True,
                use_ssl=False,
            )
            send_mail(
                subject='Проверка корректности работы', 
                message='Проверка корректности работы', 
                from_email=ip.email, 
                recipient_list=['sendmail.regular.check@gmail.com'], 
                connection=connection
            )
        except SMTPAuthenticationError as e:
            log_text = f'Ошибка авторизации при проверке корректности данных. {context_log_info}'
            logger.error(log_text)
            send_telegram_message_for_all_task.delay(message=log_text)
            return

        except SMTPConnectError as e:
            if self.request.retries >= self.max_retries:
                log_text = f'Ошибка подключения при проверке корректности данных: {e}. {context_log_info}'
                logger.error(log_text)
                send_telegram_message_for_all_task.delay(message=log_text)
            self.retry(exc=e, countdown=20)  

        except SMTPException as e:
            if self.request.retries >= self.max_retries:
                log_text = f'Ошибка при проверке корректности данных: {e}. {context_log_info}'
                logger.error(log_text)
                send_telegram_message_for_all_task.delay(message=log_text)
            self.retry(exc=e, countdown=20) 
            
        except Exception as e:
            if self.request.retries >= self.max_retries:
                log_text = f'Непредвиденная ошибка при проверке корректности данных: {e}. {context_log_info}'
                logger.error(log_text)
                send_telegram_message_for_all_task.delay(message=log_text)
            raise self.retry(exc=e, countdown=20)
        
        logger.info(f'Проверка прошла успешно, данные {ip.email} корректны. {context_log_info}')
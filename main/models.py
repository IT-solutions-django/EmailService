from django.db import models
from smtplib import SMTPException, SMTPAuthenticationError, SMTPConnectError
from django.core.mail import send_mail, get_connection  
from loguru import logger
from .exceptions import WrongEmailDataError


class IpAddress(models.Model): 
    ip = models.GenericIPAddressField('IP') 
    email = models.EmailField('Электронная почта', max_length=100) 
    password = models.CharField('Пароль приложения', max_length=50)
    host = models.CharField('SMTP-сервер', max_length=100)

    class Meta: 
        verbose_name = 'IP-адрес'
        verbose_name_plural = 'Разрешённые IP адреса'

    def __str__(self) -> str: 
        return f'{self.email} | {self.ip}'
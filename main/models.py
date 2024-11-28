from django.db import models



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
from django.db import models



class IpAddress(models.Model): 
    ip = models.GenericIPAddressField('IP') 

    class Meta: 
        verbose_name = 'IP-адрес'
        verbose_name_plural = 'Разрешённые IP адреса'

    def __str__(self) -> str: 
        return self.ip
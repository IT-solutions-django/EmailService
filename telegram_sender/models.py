from django.db import models


class Chat(models.Model):
    chat_id = models.CharField(max_length=20, verbose_name='ID чата')

    def __str__(self):
        return self.chat_id

    class Meta:
        verbose_name = 'Telegram-чат'
        verbose_name_plural = 'Telegram-чаты'
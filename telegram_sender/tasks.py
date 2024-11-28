from celery import shared_task 
from .services import update_telegram_chats


@shared_task()
def update_telegram_chats_task() -> None: 
    update_telegram_chats()
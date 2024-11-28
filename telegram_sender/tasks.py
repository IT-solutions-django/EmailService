from celery import shared_task 
from .services import (
    update_telegram_chats, 
    send_telegram_message_for_all
)


@shared_task()
def update_telegram_chats_task() -> None: 
    update_telegram_chats()


@shared_task()
def send_telegram_message_for_all_task(message: str) -> None: 
    send_telegram_message_for_all(message)
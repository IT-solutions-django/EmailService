import requests
import os
from dotenv import load_dotenv
from .models import Chat


load_dotenv()


TELEGRAM_BOT_API_KEY = os.getenv('TELEGRAM_BOT_API_KEY')


def update_telegram_chats():
    res = requests.get(
        f'https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/getUpdates'
    ).json()

    for message in res['result']:
        if message.get('message'):
            if message['message']['text'] == '/start':
                Chat.objects.get_or_create(chat_id=message['message']['chat']['id'])


def send_telegram_message_for_all(message: str) -> None: 
    chats_ids = Chat.objects.all()
    for chat in chats_ids:
        requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendMessage',
            json={
                'chat_id': chat.chat_id,
                'text': message,
            }
        )

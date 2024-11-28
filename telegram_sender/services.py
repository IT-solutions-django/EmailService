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


def telegram_send_file_for_all(path_to_report: str):
    chats_ids = Chat.objects.all()
    with open(path_to_report, 'rb') as file:
        files = {'document': file}
        for chat_id in chats_ids:
            requests.post(f'https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendDocument?chat_id={chat_id}', files=files)
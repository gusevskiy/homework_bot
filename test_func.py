import os
from pprint import pprint
import json
import requests
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup
from dotenv import load_dotenv

class NoTokenInVenv(Exception):
    pass

load_dotenv()

practicum_token = os.getenv('PRACTICUM_TOKEN')
telegram_token = os.getenv('TELEGRAM_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {practicum_token}'}


def check_tokens():
    if None in (practicum_token, telegram_token, telegram_chat_id):
        raise NoTokenInVenv("need a token, check the instructions .env.example")
    
    
def get_api_answer(timestamp):
    homework_statuses = requests.get(
        ENDPOINT, headers=HEADERS, params=timestamp
    )
    return homework_statuses.json()
    
    
    
    
    
if __name__ == '__main__':
    payload = {'from_date': 1549962000}
    a = get_api_answer(payload)
    print(type(a))
    # print(json.loads(a))
import os
from pprint import pprint
import logging
import json
import requests
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup
from dotenv import load_dotenv
from http import HTTPStatus

logging.basicConfig(
    filename='log_bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf8',
)


load_dotenv()

practicum_token = os.getenv('PRACTICUM_TOKEN')
telegram_token = os.getenv('TELEGRAM_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {practicum_token}'}


def check_tokens():
    if None in (practicum_token, telegram_token, telegram_chat_id):
        logging.warning("need a token, check instructions .env.example")
    
    
def get_api_answer(timestamp):
    homework_statuses = requests.get(
            ENDPOINT, headers=HEADERS, params=timestamp
        )
    if homework_statuses.status_code == HTTPStatus.OK:
        return homework_statuses.json()
    logging.error("No connect API")
    raise ConnectionError("No connect API")
    
def check_response(response):
    if type(response) is not dict:
        logging.error("need")
        
def parse_status(homework):
    homework_name = homework['homeworks'][0]['homework_name']
    verdict = homework['homeworks'][0]['reviewer_comment']

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'
        
def send_message(bot, message):
    bot.send_message(telegram_chat_id, message)
    
if __name__ == '__main__':
    # check_tokens()
    
    payload = {'from_date': 1549962000}
    print(get_api_answer(payload))
    # pprint(type(a))
    # # print(json.loads(a))
    
    # check_response(get_api_answer(payload))
    
    # print(parse_status(get_api_answer(payload)))
    
    # send_message('1111')
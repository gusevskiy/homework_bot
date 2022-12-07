from http import HTTPStatus
import os
from pprint import pprint
import logging
import requests
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup
from dotenv import load_dotenv
import telegram
import time

logging.basicConfig(
    filename='log_bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

load_dotenv()

practicum_token = os.getenv('PRACTICUM_TOKEN')
telegram_token = os.getenv('TELEGRAM_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {practicum_token}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

def check_tokens():
    """Проверяет переменные в .env"""
    if None in (practicum_token, telegram_token, telegram_chat_id):
        logging.warning("need a token, check the instructions .env.example")
        raise Exception("need a token, check the instructions .env.example")

def send_message(bot, message):
    """Отправляет сообщение в telegram"""
    bot.send_message(telegram_chat_id, message)


def get_api_answer(timestamp):
    """Получает json() от API ресурса ENDPOINT"""
    homework_statuses = requests.get(
            ENDPOINT, headers=HEADERS, params=timestamp
        )
    if homework_statuses.status_code == HTTPStatus.OK:
        return homework_statuses.json()
    logging.error("No connect API")
    raise ConnectionError("No connect API")


def check_response(response):
    """Проверяет структуру данных, словарь или нет"""
    if type(response) is not dict:
        logging.error("need a dict")
        raise ValueError("need a dict")


def parse_status(homework):
    """Извлекает из всего API последнию работу и возвращвет ее статус"""
    if "homeworks" in homework.keys():
        homework_sort = sorted(
            homework["homeworks"], key=lambda d: d['date_updated']
        )[::-1]
        homework_name = homework_sort[0]['homework_name']
        verdict = HOMEWORK_VERDICTS[homework_sort[0]['status']]
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    logging.error("No keys in json")
    raise ValueError("No keys in json")


def main():
    """Основная логика работы бота."""
    check_tokens()
    while True:
        try:
            timestamp = int(time.time())- 1296000 - 1296000
            payload = {'from_date': timestamp} 
            dict_api = get_api_answer(payload)
            message = parse_status(dict_api)
            bot = telegram.Bot(telegram_token)  # type: ignore
            send_message(bot, message)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
        time.sleep(RETRY_PERIOD)

if __name__ == '__main__':
    main()
    

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

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

url = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
headers = {'Authorization': 'OAuth y0_AgAAAAAOuQYrAAYckQAAAADV9tf_y0pLexNrSzWiaIx6Av2f2KGaoh0'}
timestamp = int(time.time())- 1296000 - 1296000
payload = {'from_date': timestamp}

def get_api_answer(timestamp):  
    homework_statuses = requests.get(url, headers=headers, params=payload).json()
    return homework_statuses


def check_response(response):
    logging.debug('Начало проверки')
    if not isinstance(response, dict):
        raise TypeError('Ошибка в типе ответа API')
    if 'homeworks' not in response or 'current_date' not in response:
        raise Exception('Пустой ответ от API')
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise TypeError('homeworks не является списком')
    return homeworks[0]

def parse_status(homework):
    """Извлекает из всего API последнию работу и возвращвет ее статус"""
    if 'homework_name' not in homework:
        raise KeyError('В ответе отсутсвует ключ homework_name')
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status not in HOMEWORK_VERDICTS:
        raise ValueError(f'Неизвестный статус работы - {homework_status}')
    return(
        'Изменился статус проверки работы "{homework_name}" {verdict}'
    ).format(
        homework_name=homework_name,
        verdict=HOMEWORK_VERDICTS[homework_status]
    )


if __name__ == '__main__':
    pprint(get_api_answer(payload))
    
    data = (check_response(get_api_answer(payload)))
    
    # print(data[0])
    
    print(parse_status(data))
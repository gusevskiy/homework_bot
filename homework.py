from http import HTTPStatus
import os
import logging
import requests
from dotenv import load_dotenv
import telegram
import time

logging.basicConfig(
    filename='log_bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    encoding='utf8',
    filemode='w'
)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

def check_tokens():
    """Проверяет переменные в .env"""
    if None in (PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID):
        logging.critical("need a token, check the instructions .env.example")
        raise Exception("need a token, check the instructions .env.example")
    logging.info("check_tokens = True")

def send_message(bot, message):
    """Отправляет сообщение в telegram"""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.debug("Сообщение отправлено")
    except Exception as e:
        logging.error("Сообщение не отправилось")


def get_api_answer(timestamp):
    """Получает json() от API ресурса ENDPOINT
    возвращает json() file"""
    try:
        homework_statuses = requests.get(
            ENDPOINT, headers=HEADERS, params=timestamp
        )
        if homework_statuses.status_code == HTTPStatus.OK:
            logging.info("get_api_answer = True")
            return homework_statuses.json()
    except requests.exceptions.RequestException as e:
        logging.error(e, "нет данных")
        raise ConnectionError(e, "JSON не соответствие")
    if homework_statuses.status_code != HTTPStatus.OK:
        status_code = homework_statuses.status_code
        logging.error(f'Ошибка {status_code}')
        raise Exception(f'Ошибка {status_code}')

def check_response(response):
    """Проверяет структуру данных, словарь с ключом key(homeworks) и
    наличие списка в values([list]),
    возвращает значение первый элемент словаря"""
    if not isinstance(response, dict):
        raise TypeError('Ошибка в типе ответа API')
    if 'homeworks' not in response or 'current_date' not in response:
        raise Exception('Пустой ответ от API')
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise TypeError('homeworks не является списком')
    logging.debug('check_response')
    return homeworks[0]


def parse_status(homework):
    """Извлекает из всего API последнию работу и возвращвет ее статус"""
    if 'homework_name' not in homework:
        logging.error('В ответе отсутсвует ключ homework_name')
        raise KeyError('В ответе отсутсвует ключ homework_name')
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status not in HOMEWORK_VERDICTS:
        logging.error(f'Неизвестный статус работы - {homework_status}')
        raise ValueError(f'Неизвестный статус работы - {homework_status}')
    logging.info('func - parse_status = True')
    return(
        'Изменился статус проверки работы "{homework_name}" {verdict}'
    ).format(
        homework_name=homework_name,
        verdict=HOMEWORK_VERDICTS[homework_status]
    )


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)  # type: ignore
    minus_three_weeks = 3888000
    timestamp = int(time.time()) - minus_three_weeks
    payload = {'from_date': timestamp}
    check_tokens()
    while True:
        try:
            response = get_api_answer(payload)
            data = check_response(response)
            message = parse_status(data)
            send_message(bot, message)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
        time.sleep(RETRY_PERIOD)

if __name__ == '__main__':
    main()

from http import HTTPStatus
import os
import re
import sys
import time
import logging
import requests

from dotenv import load_dotenv
import telegram
from exceptions import (
    RequeststError,
    StatusNot200Error,
    DataNotDictError,
    NotKeyError,
    DataNotLictError,
)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

UNIT_WEEK = 1296000

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens() -> bool:
    """Check variables(TOKENS) в env."""
    logging.info("Start bot")
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def send_message(bot: telegram.bot.Bot, message: str) -> None:
    """Send message in telegram."""
    try:
        logging.info("Bot started")
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.debug("Status message: sent.")
    except telegram.error.TelegramError as e:
        logging.error(f"Status message: not sent. Error: {e}")


def get_api_answer(timestamp: int) -> dict:
    """Receives json() from API resource ENDPOINT return json() file."""
    timestamp = timestamp or int(time.time())
    try:
        response = requests.get(
            ENDPOINT, headers=HEADERS, params={'from_date': timestamp}
        )
        if response.status_code != HTTPStatus.OK:
            status_code = response.status_code
            raise StatusNot200Error(f'Error reason {status_code}')
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RequeststError(f"Error in json() {e}")


def check_response(response: dict) -> list:
    """
    Check structure data.
    Dictionary with key(homeworks).
    List in values().
    Return first element dictionary.
    """
    if not isinstance(response, dict):
        raise DataNotDictError(
            'Error in type API', 'received = ', type(response)
        )
    if 'homeworks' not in response or 'current_date' not in response:
        raise NotKeyError('In API no necessary key')
    homeworks = response.get('homeworks')
    # pytest просит это?
    if not isinstance(homeworks, list):
        raise DataNotLictError(
            'homeworks not a list', 'received = ', type(homeworks)
        )
    return homeworks


def parse_status(homework: dict) -> str:
    """Retrieves the latest work from the entire API and returns its status."""
    if 'homework_name' not in homework:
        raise NotKeyError('In response no key(homework_name)')
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status not in HOMEWORK_VERDICTS:
        raise NotKeyError(f'Unknown job status - {homework_status}')
    result = (
        'Изменился статус проверки работы "{homework_name}" {verdict}'
    ).format(
        homework_name=homework_name,
        verdict=(HOMEWORK_VERDICTS[homework_status])  # type: ignore
    )
    return result


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        with open('.env', 'r', encoding='utf8') as f:
            tex = f.read()
            reg = r"\b[A-Z]+_[A-Z]+\b|\b[A-Z]+_[A-Z]+_[A-Z]+"
            logging.critical(f'Check tokens: {(re.findall(reg, tex))}')
            sys.exit()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)  # type: ignore
    timestamp = int(time.time() - (UNIT_WEEK * 3))
    prev_massage = ''
    while True:
        try:
            response = get_api_answer(timestamp)
            data = check_response(response)
            if data:
                message = parse_status(data[0])
            else:
                message = "Статус работы прежний"
            if message != prev_massage:
                send_message(bot, message)
                prev_massage = message
            else:
                logging.info(message)

        except Exception as e:
            message = f'The program does not work: {e}, view log_bot.log'
            logging.error(message, exc_info=True)
            if message != prev_massage:
                send_message(bot, message)
                prev_massage = message
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
    logging.basicConfig(
        filename='log_bot.log',
        format=FORMAT,
        level=logging.DEBUG,
        encoding='utf8',
        filemode='w',
    )

    main()

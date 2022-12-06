import os
from dotenv import load_dotenv

class NoTokenInVenv(Exception):
    pass

load_dotenv()

practicum_token = os.getenv('PRACTICUM_TOKEN')
telegram_token = os.getenv('TELEGRAM_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

# print(telegram_chat_id)


# print(bool(practicum_token))
# print(bool(telegram_token))
# print(telegram_chat_id.isnumeric())


def check_tokens():
    if None in (practicum_token, telegram_token, telegram_chat_id):
        raise NoTokenInVenv("need a token, check the instructions .env.example")
    
check_tokens()
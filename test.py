"""
import os
from dotenv import load_dotenv
load_dotenv()

# PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
# TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def check_tokens():
    PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    dd = locals().items()
    my_dict = (dict((y, x) for y, x in dd))
    for i in my_dict:
        if my_dict[i] == '':
            print(i)
        print(i, '= True')
    
check_tokens()
"""
import re 


with open('.env', 'r', encoding='utf8') as f:
    tex = f.read()
    reg = r"\b[A-Z]+_[A-Z]+\b|\b[A-Z]+_[A-Z]+_[A-Z]+"
    print(re.findall(reg, tex))
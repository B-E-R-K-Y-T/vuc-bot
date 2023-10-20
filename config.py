import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GOD_ID = int(os.getenv('GOD_ID'))


class Message:
    WELCOME = 'Приветствую Вас! Я бот ВУЦ РТУ МИРЭА который помогает в учебе! Чтобы начать регистрацию введите /reg'
    ACCESS_DENIED = 'Вы не имеете доступ! Попробуйте пройти регистрацию'


class Commands:
    START = 'start'
    HELP = 'help'

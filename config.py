import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# Просто мой дебаг айди, чтобы у меня были все права на бота
# TODO: Потом удалить
GOD_ID = int(os.getenv('GOD_ID'))


class Commands:
    START = 'start'
    HELP = 'help'
    REG = 'reg'
    SELF = 'self'


class Message:
    WELCOME = (f'Приветствую Вас! Я бот ВУЦ РТУ МИРЭА который помогает в учебе! Чтобы начать регистрацию введите '
               f'{Commands.REG}')
    ACCESS_DENIED = f'Вы не имеете доступ! Попробуйте пройти регистрацию: {Commands.REG}'
    DEFAULT = 'Я не понимаю Вас.'

    class Registration:
        WARNING = 'Отправляя данные, Вы даете согласие на их обработку, хранение и анализ.'
        NAME = 'Введите ФИО: '
        DATE_OF_BIRTH = 'Введите Вашу дату рождения: '
        PHONE_NUMBER = 'Введите номер телефона: '
        MAIL = 'Введите электронную почту: '
        ADDRESS = 'Введите адрес проживания: '
        INSTITUTE = 'Введите наименование Вашего института: '
        COURSE_NUMBER = 'Введите номер курса: '
        VUS = 'Введите ваш ВУС*: \n\n*Военно-учетная специальность'
        FINAL = 'Регистрация окончена. Сохраняю данные'
import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# telegram id админов
ADMINS_ID = tuple(int(t_id) for t_id in os.getenv('GOD_ID').split(',') if t_id.isnumeric())
# Минимальный возраст поступления на военную кафедру
MINIUM_AGE_ENTRANCE = 18
LEN_TOKEN = 25
MAX_AMOUNT_TOKEN = 100


class Commands:
    START = 'start'
    HELP = 'help'
    REG = 'reg'
    SELF = 'self'
    GET_TOKEN = 'get_token'
    STOP_PROCESS = 'stop_process'


class Message:
    WELCOME = (f'Приветствую Вас! Я бот ВУЦ РТУ МИРЭА который помогает в учебе! Чтобы начать регистрацию введите '
               f'/{Commands.REG}')
    ACCESS_DENIED = f'Вы не имеете доступ! Попробуйте пройти регистрацию: /{Commands.REG}'
    DEFAULT = 'Я не понимаю Вас.'
    STOP_PROCESS = 'Вы вышли из процесса.'

    class Registration:
        WARNING = 'Отправляя данные, Вы даете согласие на их обработку, хранение и анализ.'
        NAME = 'Введите ФИО: '
        DATE_OF_BIRTH = 'Введите Вашу дату рождения: '
        PHONE_NUMBER = 'Введите номер телефона: '
        MAIL = 'Введите электронную почту: '
        ADDRESS = 'Введите адрес проживания: '
        INSTITUTE = 'Введите наименование Вашего института: '
        DIRECTION_OF_STUDY = 'Введите Ваше направление обучения: '
        GROUP_STUDY = 'Введите Вашу учебную группу: '
        COURSE_NUMBER = 'Введите номер курса: '
        VUS = 'Введите ваш ВУС*: \n\n*Военно-учетная специальность'
        FINAL = 'Регистрация окончена. Сохраняю данные'

    class GetToken:
        AMOUNT_TOKEN = 'Сколько токенов сгенерировать?'
        FINAL = 'Токены готовы!'

    class Error:
        NAME = 'Не правильный ввод! Формат ввода такой: ИМЯ ФАМИЛИЯ ОТЧЕСТВО'
        NAME_DIGIT = 'Не правильный ввод! Фамилия имя или отчество не может состоять только из цифр'
        DATE = 'Дата недействительна! Формат ввода: ДЕНЬ.МЕСЯЦ.ГОД'
        PHONE = 'Ошибка ввода!'
        MAIL = 'Ошибка ввода!'
        INSTITUTE = 'Название института не может состоять только из цифр или знаков пунктуации!'
        DIRECTION_OF_STUDY = 'Направление обучения не может состоять только из цифр и знаков пунктуации!'
        GROUP_STUDY = 'Учебная группа не может состоять только из цифр и знаков пунктуации!'
        ADDRESS = 'Адрес не может состоять только из цифр и знаков пунктуации!'
        COURSE_NUMBER = 'Номер курса должен состоять из цифр, а также должен быть в промежутке от 1 до 8!'
        VUS = 'ВУС должен состоять из цифр!'
        AMOUNT_TOKEN = 'Введите количество токенов цифрой!'
        AMOUNT_TOKEN_MAX = f'Можно указать только от 1 до {MAX_AMOUNT_TOKEN} токенов!'

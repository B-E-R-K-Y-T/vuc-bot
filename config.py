import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GOD_ID = os.getenv('GOD_ID')
# telegram id админов
ADMINS_ID = tuple(int(t_id) for t_id in os.getenv('ADMINS_ID').split(',') if t_id.isnumeric())
# Минимальный возраст поступления на военную кафедру
MINIUM_AGE_ENTRANCE = int(os.getenv('MINIUM_AGE_ENTRANCE'))
# Максимальная длина токена(Больше ставить не рекомендуется)
LEN_TOKEN = int(os.getenv('LEN_TOKEN'))
# Максимальное кол-во токенов(Больше ставить не рекомендуется)
MAX_AMOUNT_TOKEN = int(os.getenv('MAX_AMOUNT_TOKEN'))
# Если False, то бот, не будет записывать в логи то, что пишет пользователь
LOG_MODE = True
# Максимальный размер логов (для отдельного юзера!) (Если указать -1, то размер будет бесконечным)
MAX_SIZE_KB_LOG = int(os.getenv('MAX_SIZE_KB_LOG'))
PATH_TO_LOG_DIR = os.getenv('PATH_TO_LOG_DIR')
ENUM_TYPE_TOKEN = ('Командир отделения', 'Командир взвода', 'Студент')
# Режим дебага. Никаких ролей и безопасности
DEBUG = True
CRUD_ADDRESS = 'http://127.0.0.1:5000'


class Commands:
    START = 'start'
    HELP = 'help'
    REG = 'reg'
    SELF = 'self'
    GET_TOKEN = 'token'
    ROLLBACK_PROCESS = 'rollback'
    # Пока что не реализованы
    LATE = 'late'
    ADD_ADMIN = 'add_admin'
    DELETE_ADMIN = 'del_admin'
    LOGIN = 'login'


class Message:
    WELCOME = (f'Приветствую Вас! Я бот ВУЦ РТУ МИРЭА который помогает в учебе! Чтобы начать регистрацию введите '
               f'/{Commands.REG}')
    ACCESS_DENIED = f'Вы не имеете доступ! Попробуйте получить токен у администратора!'
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
        PLATOON = 'Введите номер Вашего взвода: '
        SQUAD = 'Введите номер Вашего отделения: '
        FINAL = 'Регистрация окончена. Сохраняю данные'

    class GetToken:
        TYPE_TOKEN = f'Для кого Вы хотите сгенерировать токены?\n\n{ENUM_TYPE_TOKEN}'
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
        PLATOON = 'Номер взвода должен состоять из цифр и должен иметь длину три символа!'
        SQUAD = 'Номер отделения должен состоять из цифр, а также должен быть в промежутке от 1 до 3'
        AMOUNT_TOKEN = 'Введите количество токенов цифрой!'
        AMOUNT_TOKEN_MAX = f'Можно указать только от 1 до {MAX_AMOUNT_TOKEN} токенов!'
        TYPE_TOKEN = f'Тип токена может быть только таким: {ENUM_TYPE_TOKEN}'

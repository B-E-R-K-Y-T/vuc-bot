import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GOD_ID = os.getenv('GOD_ID')
# telegram id админов
ADMINS_ID = tuple(int(t_id) for t_id in os.getenv('ADMINS_ID').split(',') if t_id.isnumeric())
# Минимальный возраст поступления на военную кафедру
MINIUM_AGE_ENTRANCE = int(os.getenv('MINIUM_AGE_ENTRANCE'))
# Максимальное кол-во токенов(Больше ставить не рекомендуется)
MAX_AMOUNT_TOKEN = int(os.getenv('MAX_AMOUNT_TOKEN'))
# Если False, то бот, не будет записывать в логи то, что пишет пользователь
LOG_MODE = True
# Максимальный размер логов (для отдельного юзера!) (Если указать -1, то размер будет бесконечным)
MAX_SIZE_KB_LOG = int(os.getenv('MAX_SIZE_KB_LOG'))
PATH_TO_LOG_DIR = os.getenv('PATH_TO_LOG_DIR')
ENUM_TYPE_TOKEN = ('Студент', 'Командир отделения', 'Командир взвода')
# Режим дебага. Никаких ролей и безопасности(Если True, то он включен)
DEBUG = False
CRUD_ADDRESS = os.getenv('CRUD_ADDRESS')


class Role:
    STUDENT = ENUM_TYPE_TOKEN[0]
    COMMANDER_SQUAD = ENUM_TYPE_TOKEN[1]
    COMMANDER_PLATOON = ENUM_TYPE_TOKEN[2]


class Commands:
    START = 'start'
    HELP = 'help'
    REG = 'reg'
    SELF = 'self'
    GET_TOKEN = 'token'
    ROLLBACK_PROCESS = 'rollback'
    CANCEL_STEP_PROCESS = 'cancel'
    LOGIN = 'login'
    BAN_USER = 'ban_user'
    GET_ROLE = 'get_role'
    GET_PLATOON = 'get_platoon'
    # TODO: Реализовать!
    LATE = 'late'
    ADD_ADMIN = 'add_admin'
    DELETE_ADMIN = 'del_admin'

    class Events:
        GET_PLATOON_EVENT = 'get_platoon_e'
        GET_SQUAD_1 = 'get_squad_1_e'
        GET_SQUAD_2 = 'get_squad_2_e'
        GET_SQUAD_3 = 'get_squad_3_e'

        class EditUser:
            SQUAD = 'edit_squad'
            # TODO: Реализовать!
            ROLE = 'edit_role'

    class Flags:
        class Ban:
            USER = '-u'


class Message:
    WELCOME = (f'Приветствую Вас! Я бот ВУЦ РТУ МИРЭА который помогает в учебе! Если Вы тут впервые, расскажу, '
               f'как начать со мной работать: '
               f'\n\nДля начала введите токен: /{Commands.LOGIN}'
               f'\nА теперь пройдите регистрацию: /{Commands.REG}')
    ACCESS_DENIED = f'Вы не имеете доступ! Попробуйте получить токен у администратора!'
    DEFAULT = 'Я не понимаю Вас.'
    EXIT_PROCESS = 'Вы вышли из процесса.'
    CANCEL_STEP_PROCESS = 'Действие отменено.'
    SUCCESSFUL = 'Успешно!'
    SELECT_SQUAD = 'Выберете отделение: '

    class EditUser:
        MAIN = 'Какой параметр Вы хотите поменять?'
        SQUAD = 'Отделение'
        ROLE = 'Должность'

    class EditSquadUserState:
        EDIT = 'Введите номер отделения цифрой: '
        FINAL = 'Обновляю атрибут...'

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
        FINAL = 'Регистрация окончена. Сохраняю данные...'

    class GetToken:
        TYPE_TOKEN = f'Для кого Вы хотите сгенерировать токены?\n\n{ENUM_TYPE_TOKEN}'
        AMOUNT_TOKEN = ('Сколько токенов сгенерировать?'
                        '\n\nЖелательно генерировать строго под кол-во людей во взводе, чтобы не было путаницы.')
        FINAL = 'Токены готовы!'

    class Login:
        LOGIN = 'Введите токен: '
        FINAL = 'Проверяю токен...'

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
        NOTHING_CANCEL_STEP_PROCESS = f'Нечего отменять.'
        DEFAULT_ERROR = 'Ошибка!'
        PLATOON_COMMANDER_ERROR = 'У данного взвода уже есть командир!'
        ERROR_LEN_TOKEN = 'Длина токена должна быть: '  # Потом я конкатенирую сюда длину
        INVALID_TOKEN = 'Токен недействителен!'
        CONNECTION_ERROR = 'Нет соединения с сервером!'
        USER_ALREADY_EXISTS = 'Вы уже зарегистрированы!'


class EndPoint:
    TEST = '/test'
    GET_TOKEN = '/get_token'
    GET_FREE_TOKEN = '/get_free_token'
    GET_LOGINS = '/get_login_users'
    GET_ADMINS = '/get_admins_users'
    LOGIN = '/login'
    ATTACH_TOKEN = '/attach_token'
    BAN_USER = '/ban_user'
    GET_LEN_TOKEN = '/get_len_token'
    SAVE_USER = '/save_user'
    CHECK_EXIST_USER = '/check_exist_user'
    GET_ROLE = '/get_role'
    DELETE_USER = '/del_user'
    GET_USER = '/get_user'
    GET_PLATOON_COMMANDER = '/get_platoon_commander'
    GET_PLATOON = '/get_platoon'
    GET_COUNT_PLATOON_SQUAD = '/get_count_squad_in_platoon'
    SET_PLATOON_SQUAD_OF_USER = '/set_squad_in_platoon_of_user'

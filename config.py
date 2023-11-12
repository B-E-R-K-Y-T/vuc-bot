import os

from utils.tools import auto_event_id

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

# Режим дебага. Никаких ролей и безопасности(Если True, то он включен)
DEBUG = False
PRINT_DEBUG = True
CRUD_ADDRESS = os.getenv('CRUD_ADDRESS')

ROLES = ('Студент', 'Командир отделения', 'Командир взвода')


class Role:
    STUDENT = ROLES[0]
    COMMANDER_SQUAD = ROLES[1]
    COMMANDER_PLATOON = ROLES[2]
    ADMIN = 'Admin'


class UserAttribute:
    NAME = 'ФИО'
    DOB = 'Дата рождения'
    PHONE_NUMBER = 'Номер телефона'
    MAIL = 'Почта'
    ADDRESS = 'Адрес'
    INSTITUTE = 'Институт'
    DOS = 'Направление'
    GROUP_STUDY = 'Группа'
    # COURSE_NUMBER = 'Номер курса'
    VUS = 'ВУС'
    PLATOON = 'Взвод'
    SQUAD = 'Отделение'
    COMMANDER = 'Командир'


class MenuButtons:
    class Text:
        BACK = 'Назад'
        EDIT = 'Изменить'
        EVALUATION = 'Оценка'
        ATTENDANCE = 'Посещаемость'
        PERSONAL_DATA = 'Перс данные'
        SQUAD = 'Отделения'
        MENU = 'Меню'
        STUDENT_MENU = 'Меню студента'
        PLATOON_COMMANDER_MENU = 'Меню командира взвода'
        SQUAD_COMMANDER_MENU = 'Меню командира отделения'
        ADMIN_COMMANDER_MENU = 'Меню администратора'
        ADD_STUDENT = 'Добавить студента'
        SQUADS_LIST_MENU = 'Меню отделений'


class _MenuGetEvent:
    MENU_EVENT = auto_event_id()
    STUDENT_EVALUATION = auto_event_id()
    STUDENT_ATTENDANCE = auto_event_id()
    STUDENT_PERSONAL_DATA = auto_event_id()
    COMMANDER_PLATOON_ATTENDANCE = auto_event_id()
    ADMIN_PLATOONS = auto_event_id()
    PLATOON_TESTS = auto_event_id()
    PLATOON_ATTENDANCE = auto_event_id()
    PLATOON_PERSONNEL = auto_event_id()
    PLATOON_COMMANDERS = auto_event_id()
    STUDENT_MENU = auto_event_id()
    PLATOON_COMMANDER_MENU = auto_event_id()
    SQUAD_COMMANDER_MENU = auto_event_id()
    ADMIN_COMMANDER_MENU = auto_event_id()
    ADD_STUDENT = auto_event_id()
    SQUADS_LIST_MENU = auto_event_id()


class MenuEvent:
    STUDENT_MENU = _MenuGetEvent.STUDENT_MENU
    PLATOON_COMMANDER_MENU = _MenuGetEvent.PLATOON_COMMANDER_MENU
    SQUAD_COMMANDER_MENU = _MenuGetEvent.SQUAD_COMMANDER_MENU
    ADMIN_COMMANDER_MENU = _MenuGetEvent.ADMIN_COMMANDER_MENU
    MAIN_MENU = _MenuGetEvent.MENU_EVENT

    class Student:
        EVALUATION = _MenuGetEvent.STUDENT_EVALUATION
        ATTENDANCE = _MenuGetEvent.STUDENT_ATTENDANCE
        PERSONAL_DATA = _MenuGetEvent.STUDENT_PERSONAL_DATA
        BACK = _MenuGetEvent.MENU_EVENT

        class PersonalData:
            EDIT = auto_event_id()
            BACK = _MenuGetEvent.STUDENT_MENU

        class Evaluation:
            BACK = _MenuGetEvent.STUDENT_MENU

    class CommanderSquad:
        BACK = _MenuGetEvent.MENU_EVENT

        class Evaluation:
            BACK = _MenuGetEvent.SQUAD_COMMANDER_MENU

    class CommanderPlatoon:
        ADD_STUDENT = _MenuGetEvent.ADD_STUDENT
        SQUADS_LIST_MENU = _MenuGetEvent.SQUADS_LIST_MENU
        BACK = _MenuGetEvent.MENU_EVENT

    class Admin:
        PLATOONS = _MenuGetEvent.ADMIN_PLATOONS

        class Platoon:
            TESTS = _MenuGetEvent.PLATOON_TESTS
            ATTENDANCE = _MenuGetEvent.PLATOON_ATTENDANCE
            PERSONNEL = _MenuGetEvent.PLATOON_PERSONNEL
            COMMANDERS = _MenuGetEvent.PLATOON_COMMANDERS
            BACK = _MenuGetEvent.MENU_EVENT


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
    GET_PLATOON = 'get_platoon'
    ATTEND = 'attend'
    UPLOAD_PLATOON = 'upload_platoon'
    MENU = 'menu'
    # TODO: Реализовать!
    LATE = 'late'
    GET_ROLE = 'get_role'
    ADD_ADMIN = 'add_admin'
    DELETE_ADMIN = 'del_admin'

    class Events:
        GET_PLATOON_EVENT = 'get_platoon_e'

        GET_SQUAD_1 = 'get_squad_1_e'
        GET_SQUAD_2 = 'get_squad_2_e'
        GET_SQUAD_3 = 'get_squad_3_e'

        SET_SQUAD_1 = 'set_squad_1_e'
        SET_SQUAD_2 = 'set_squad_2_e'
        SET_SQUAD_3 = 'set_squad_3_e'

        class EditUser:
            SQUAD = 'edit_squad'
            ATTEND = 'edit_attend'
            ATTEND_NO = 'edit_attend_no'
            ATTEND_YES = 'edit_attend_yes'
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
    ATTRS_PLATOON = 'Введите данные по взводу: Номер взвода, ВУС, семестр(в ВУЦ)'

    class EditUser:
        MAIN = 'Какой параметр Вы хотите поменять?'
        SQUAD = 'Отделение'
        ATTEND = 'Присутствие'
        ATTEND_NO = 'Отсутствует'
        ATTEND_YES = 'Присутствует'
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
        TYPE_TOKEN = f'Для кого Вы хотите сгенерировать токены?\n\n{ROLES}'
        AMOUNT_TOKEN = ('Сколько токенов сгенерировать?'
                        '\n\nЖелательно генерировать строго под кол-во людей во взводе, чтобы не было путаницы.')
        FINAL = 'Токены готовы!'

    class Login:
        LOGIN = 'Введите токен: '
        FINAL = 'Проверяю токен...'

    class UploadPlatoon:
        UPLOAD = 'Загрузите файл: '
        FINAL = 'Сканирую...'

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
        TYPE_TOKEN = f'Тип токена может быть только таким: {ROLES}'
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
    AUTH = '/auth'
    LOGIN = '/login'
    ADD_PLATOON = '/add_platoon'
    ATTACH_TOKEN = '/attach_token'
    BAN_USER = '/ban_user'
    GET_LEN_TOKEN = '/get_len_token'
    SAVE_USER = '/save_user'
    CHECK_EXIST_USER = '/check_exist_user'
    GET_ROLE = '/get_role'
    DELETE_USER = '/del_user'
    GET_USER = '/get_user'
    GET_USER_TG = '/get_user_tg'
    GET_PLATOON_COMMANDER = '/get_platoon_commander'
    GET_PLATOON = '/get_platoon'
    GET_COUNT_PLATOON_SQUAD = '/get_count_squad_in_platoon'
    SET_PLATOON_SQUAD_OF_USER = '/set_squad_in_platoon_of_user'
    ATTACH_USER_ATTENDANCE = '/attach_user_to_attendance'
    UPDATE_ATTENDANCE_USER = '/add_visit_user'

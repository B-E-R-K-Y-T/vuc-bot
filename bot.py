"""
Переменные:
- TELEGRAM_BOT_TOKEN: Токен для доступа к Telegram API.
- bot: Объект TeleBot для взаимодействия с ботом Telegram.
- security: Объект Security для реализации функций безопасности.
- fsm_worker: Объект FSMContainer для управления конечными автоматами.
- token_handler: Объект TokenHandler для обработки токенов.
- edit_users: Словарь для хранения пользователей, редактирующих данные.
- listener_edit_user: Объект ListenerEditUser для отслеживания изменений пользователя.

Обработчики команд:
1. send_welcome: Обработчик команды START и HELP, отправляет приветственное сообщение пользователю.
2. command_get_platoon: Обработчик команды GET_PLATOON, отправляет пользователю клавиатуру с кнопками для выбора взвода.
3. command_reg: Обработчик команды REG, запускает процесс регистрации пользователя.
4. command_get_token: Обработчик команды GET_TOKEN, запускает процесс получения токена.
5. command_stop_process: Обработчик команды ROLLBACK_PROCESS, останавливает текущий процесс.
6. command_self: Обработчик команды SELF, отображает информацию о текущем пользователе.
7. command_ban_user: Обработчик команды BAN_USER, блокирует пользователя.
8. command_cancel: Обработчик команды CANCEL_STEP_PROCESS, отменяет текущий шаг процесса.
9. command_login: Обработчик команды LOGIN, запускает процесс входа пользователя.
10. handler_message_loging_process: Обработчик сообщений для процесса входа пользователя.
11. handler_message: Обработчик сообщений пользователя.
12. squad_1, squad_2, squad_3: Обработчики выбора отряда.
13. attend, attend_no: Обработчики выбора посещения пользователя.

Функции-обработчики:
- handler_edit_user: Обработчик редактирования пользователя.
- handler_registration: Обработчик процесса регистрации пользователя.
- handler_get_token: Обработчик процесса получения

"""

import pandas as pd
import datetime
import telebot

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TELEGRAM_BOT_TOKEN, Message, Commands, Role, UserAttribute
from utils.fsm.upload.upload_fsm import FiniteStateMachineUpload
from utils.fsm.upload.states import UPLOAD_PLATOON_MSG_STATES
from utils.fsm.upload.validators import UPLOAD_VALIDATORS
from utils.fsm.edit_squad_user.states import EditSquadUserState, EDIT_SQUAD_USER_MSG_STATES
from utils.fsm.edit_squad_user.validators import EDIT_SQUAD_USER_VALIDATORS
from utils.fsm.fsm_container import FSMContainer
from utils.fsm.login.login_fsm import FiniteStateMachineLogin
from utils.fsm.login.states import LoginState, LOGIN_MSG_STATES
from utils.fsm.registrarion.states import REGISTRATION_MSG_STATES, RegistrationStates
from utils.fsm.upload.states import UploadState
from utils.security.security import Security
from utils.logger import log, debug
from utils.server_worker.server_worker import ServerWorker, Status, check_connection_with_server
from utils.user_worker.edit_user import ListenerEditUser
from utils.user_worker.user import save_user, get_telegram_id, get_user
from utils.fsm.registrarion.registration_fsm import FiniteStateMachineRegistration
from utils.fsm.registrarion.validators import REGISTRATION_VALIDATORS
from utils.fsm.login.validators import LOGIN_VALIDATORS
from utils.exceptions import MainException
from utils.fsm.get_token.get_token_fsm import FiniteStateMachineGetToken
from utils.fsm.get_token.states import GET_TOKEN_MSG_STATES, GetTokenState
from utils.fsm.get_token.validators import GET_TOKEN_VALIDATORS
from utils.handlers.token import TokenHandler

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)
security = Security(bot=bot)
fsm_worker = FSMContainer()
token_handler = TokenHandler()
edit_users = {}
listener_edit_user = ListenerEditUser()


@bot.message_handler(commands=[Commands.START, Commands.HELP])
@log
@save_user
def send_welcome(message):
    """
    Функция `send_welcome` является обработчиком команды START и HELP. Она выполняет следующие действия:

    1. Принимает сообщение от пользователя через объект `message`.
    2. Отправляет приветственное сообщение Message.WELCOME пользователю с помощью метода `bot.send_message`.
    3. Ведет журналирование выполнения команды с помощью декоратора `@log`.
    4. Сохраняет информацию о пользователе с помощью декоратора `@save_user`.
    """

    bot.send_message(message.chat.id, Message.WELCOME)


@bot.message_handler(commands=[Commands.GET_PLATOON])
@log
@check_connection_with_server(bot=bot)
@save_user
@security.is_login
def command_get_platoon(message: types.Message):
    """Функция `command_get_platoon` является обработчиком команды GET_PLATOON. Она выполняет следующие действия:

1. Принимает сообщение от пользователя через объект `message`.
2. Проверяет подключение к серверу с помощью декоратора `@check_connection_with_server`.
3. Сохраняет информацию о пользователе с помощью декоратора `@save_user`.
4. Проверяет, авторизован ли пользователь с помощью декоратора `@security.is_login`.
5. Создает объект `InlineKeyboardMarkup` для разметки клавиатуры.
6. Получает информацию о пользователе с помощью функции `get_user` и его Telegram ID из объекта `message`.
7. Если пользователь имеет роль COMMANDER_PLATOON или COMMANDER_SQUAD:
   - Получает номер взвода `platoon_number` пользователя.
   - Получает количество отрядов `count_squad` в взводе с помощью метода `get_count_platoon_squad` из объекта `ServerWorker`.
   - Создает события `events` для каждого отряда.
   - Добавляет кнопки для каждого отряда в разметку клавиатуры с помощью метода `markup.add`.
   - Отправляет сообщение с текстом Message.SELECT_SQUAD и клавиатурой reply_markup пользователю с помощью метода `bot.send_message`.
8. В противном случае, если пользователь не имеет доступа к команде:
   - Отправляет ответное сообщение Message.ACCESS_DENIED пользователю с помощью метода `bot.reply_to`.
"""
    markup = InlineKeyboardMarkup()
    user = get_user(get_telegram_id(message))

    if user.get_role() in [Role.COMMANDER_PLATOON, Role.COMMANDER_SQUAD]:
        platoon_number = user.platoon
        count_squad = ServerWorker().get_count_platoon_squad(platoon_number)

        events = [Commands.Events.GET_SQUAD_1, Commands.Events.GET_SQUAD_2, Commands.Events.GET_SQUAD_3]

        for squad_num in range(count_squad):
            markup.add(InlineKeyboardButton(squad_num + 1, callback_data=events[squad_num]))

        bot.send_message(chat_id=message.chat.id, text=Message.SELECT_SQUAD, reply_markup=markup)
    else:
        bot.reply_to(message, Message.ACCESS_DENIED)


@bot.message_handler(commands=[Commands.REG])
@log
@check_connection_with_server(bot=bot)
@save_user
@security.is_login # мы пытаемся зарегать пользователя, откуда у него токен?
def command_reg(message):
    """Функция `command_reg` является обработчиком команды REG. Она выполняет следующие действия:

1. Принимает сообщение от пользователя через объект `message`.
2. Проверяет подключение к серверу с помощью декоратора `@check_connection_with_server`.
3. Сохраняет информацию о пользователе с помощью декоратора `@save_user`.
4. Проверяет, авторизован ли пользователь с помощью декоратора `@security.is_login`.
5. Отправляет ответное сообщение Message.Registration.WARNING пользователю с помощью метода `bot.reply_to`, предупреждая о начале процесса регистрации.
6. Отправляет сообщение с текстом Message.Registration.NAME пользователю с помощью метода `bot.send_message`, запрашивая имя пользователя.
7. Создает экземпляр `FiniteStateMachineRegistration` и передает ему информацию о пользователе из функции `get_user` с Telegram ID из объекта `message`.
8. Очищает список данных пользователя с помощью `get_user(get_telegram_id(message)).writer.data = []`.
9. Устанавливает объект конечного автомата в `fsm_worker` с помощью `fsm_worker.set_fsm_obj(get_telegram_id(message), state)`.
"""
    bot.reply_to(message, Message.Registration.WARNING)
    bot.send_message(message.chat.id, Message.Registration.NAME)

    state = FiniteStateMachineRegistration(get_user(get_telegram_id(message)))
    # state.next_state()

    get_user(get_telegram_id(message)).writer.data = []

    fsm_worker.set_fsm_obj(get_telegram_id(message), state)


@bot.message_handler(commands=[Commands.GET_TOKEN])
@log
@check_connection_with_server(bot=bot)
@save_user
@security.is_login
@security.is_admin
def command_get_token(message):
    """Функция `command_get_token` является обработчиком команды GET_TOKEN. Она выполняет следующие действия:

1. Принимает сообщение от пользователя через объект `message`.
2. Проверяет подключение к серверу с помощью декоратора `@check_connection_with_server`.
3. Сохраняет информацию о пользователе с помощью декоратора `@save_user`.
4. Проверяет, авторизован ли пользователь с помощью декоратора `@security.is_login`.
5. Проверяет, является ли пользователь администратором с помощью декоратора `@security.is_admin`.
6. Отправляет сообщение с текстом Message.GetToken.TYPE_TOKEN пользователю с помощью метода `bot.send_message`, запрашивая тип токена.
7. Создает экземпляр `FiniteStateMachineGetToken` и передает ему информацию о пользователе из функции `get_user` с Telegram ID из объекта `message`.
8. Устанавливает объект конечного автомата в `fsm_worker` с помощью `fsm_worker.set_fsm_obj(get_telegram_id(message), state)`.

"""
    bot.send_message(message.chat.id, Message.GetToken.TYPE_TOKEN)
    state = FiniteStateMachineGetToken(get_user(get_telegram_id(message)))

    fsm_worker.set_fsm_obj(get_telegram_id(message), state)


@bot.message_handler(commands=[Commands.ROLLBACK_PROCESS])
@log
@check_connection_with_server(bot=bot)
@save_user
@security.is_login
def command_stop_process(message):
    """Функция `command_stop_process` является обработчиком команды ROLLBACK_PROCESS. Она выполняет следующие действия:

1. Принимает сообщение от пользователя через объект `message`.
2. Проверяет подключение к серверу с помощью декоратора `@check_connection_with_server`.
3. Сохраняет информацию о пользователе с помощью декоратора `@save_user`.
4. Проверяет, авторизован ли пользователь с помощью декоратора `@security.is_login`.
5. Устанавливает состояние пользователя (`state`) в значение `None`, чтобы остановить выполняющийся процесс.
6. Отправляет ответное сообщение Message.EXIT_PROCESS пользователю с помощью метода `bot.reply_to`, чтобы сообщить о завершении процесса.
"""
    get_user(get_telegram_id(message)).state = None

    bot.reply_to(message, Message.EXIT_PROCESS)


@bot.message_handler(commands=[Commands.SELF])
@log
@check_connection_with_server(bot=bot)
@save_user
@security.is_login
def command_self(message):
    bot.reply_to(message, get_user(get_telegram_id(message)))


@bot.message_handler(commands=[Commands.BAN_USER])
@log
@check_connection_with_server(bot=bot)
@save_user
@security.is_login
@security.is_admin
def command_ban_user(message):
    """
    Эта функция выполняет команду бана пользователя, с предварительной обработкой сообщения и проверкой различных условий,
    включая подключение к серверу, аутентификацию пользователя и проверку его прав доступа, после чего вызывается метод
    серверного воркера для выполнения бана, и в зависимости от результата отправляется соответствующее сообщение
    об успехе или ошибке.

    :param message:
    :return:
    """
    try:
        _, user_id = message.text.split(Commands.Flags.Ban.USER)
        res = ServerWorker().ban_user(user_id)

        if res == Status.OK:
            bot.reply_to(message, Message.SUCCESSFUL)
        else:
            bot.reply_to(message, Message.Error.DEFAULT_ERROR)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(commands=[Commands.CANCEL_STEP_PROCESS])
@log
@check_connection_with_server(bot=bot)
@save_user
@security.is_login
def command_cancel(message):
    """В этом коде происходит проверка состояния пользователя и выполнение логики отмены текущего шага процесса. Если пользователь имеет непустое состояние (`fsm_attr_user.step > -1`), то происходит переход к предыдущему состоянию (`fsm_attr_user.old_state()`), и отправляется сообщение о успешной отмене шага (`Message.CANCEL_STEP_PROCESS`).

Если пользователь не имеет состояния или его состояние пустое, то у пользователя сбрасывается состояние (`user.state = None`), и отправляется сообщение об ошибке, что нечего отменять (`Message.Error.NOTHING_CANCEL_STEP_PROCESS`).

Если пользователь не найден (`fsm_attr_user is None`), также отправляется сообщение об ошибке о том, что нечего отменять (`Message.Error.NOTHING_CANCEL_STEP_PROCESS`).
"""
    fsm_attr_user = fsm_worker.get_fsm_obj(get_telegram_id(message))
    user = get_user(get_telegram_id(message))

    if fsm_attr_user is not None:
        if fsm_attr_user.step > -1:
            fsm_attr_user.old_state()

            bot.reply_to(message, Message.CANCEL_STEP_PROCESS)
        else:
            user.state = None
            bot.reply_to(message, Message.Error.NOTHING_CANCEL_STEP_PROCESS)
    else:
        bot.reply_to(message, Message.Error.NOTHING_CANCEL_STEP_PROCESS)


@bot.message_handler(commands=[Commands.LOGIN])
@log
@check_connection_with_server(bot=bot)
@save_user
def command_login(message):
    bot.send_message(message.chat.id, Message.Login.LOGIN)

    state = FiniteStateMachineLogin(get_user(get_telegram_id(message)))

    fsm_worker.set_fsm_obj(get_telegram_id(message), state)


@bot.message_handler(commands=[Commands.UPLOAD_PLATOON])
@log
@check_connection_with_server(bot=bot)
@save_user
@security.is_login
@security.is_admin
def command_upload_platoon(message):
    bot.send_message(message.chat.id, Message.UploadPlatoon.UPLOAD)

    state = FiniteStateMachineUpload(get_user(get_telegram_id(message)))

    fsm_worker.set_fsm_obj(get_telegram_id(message), state)


@bot.message_handler(func=lambda m: True)
@log
@check_connection_with_server(bot=bot)
@save_user
def handler_message_loging_process(message):
    """В этом коде происходит проверка состояния пользователя и выполнение соответствующих действий в зависимости от
    этого состояния.

Если состояние пользователя является экземпляром класса `LoginState`, то вызывается функция `handler_login(user, message)`,
которая обрабатывает действия связанные с процессом входа в систему.

В противном случае, вызывается функция `security.is_login(handler_message)(message)`, которая проверяет, авторизован ли
 пользователь, и в случае, если пользователь авторизован, передает управление функции `handler_message(message)`
  для обработки входящего сообщения.

Обратите внимание, что `security.is_login` и `handler_message` являются функциями или методами, которые должны быть определены где-то в коде, поскольку они вызываются через скобки `()`.
"""
    user = get_user(get_telegram_id(message))

    if isinstance(user.state, LoginState):
        handler_login(user, message)
    else:
        security.is_login(handler_message)(message)


@bot.message_handler(func=lambda m: True)
@check_connection_with_server(bot=bot)
@save_user
# @security.is_login
def handler_message(message):
    """
    Обрабатывает сообщения пользователя и выполняет соответствующие действия в зависимости от состояния пользователя.

    Аргументы:
    - message: объект сообщения от пользователя

    Возвращаемое значение: нет

    Исключения: нет
    """

    # Получение объекта пользователя по Telegram ID сообщения
    user = get_user(get_telegram_id(message))

    # Вывод текущего состояния пользователя
    print(f'{user.state=}')

    # Обработка различных состояний пользователя
    if isinstance(user.state, RegistrationStates):
        # Обработка регистрации пользователя
        handler_registration(user, message)
    elif isinstance(user.state, GetTokenState):
        # Обработка получения токена пользователя
        handler_get_token(user, message)
    elif isinstance(user.state, EditSquadUserState):
        # Обработка редактирования информации о пользователе
        handler_edit_squad_user(user, message)
    elif isinstance(user.state, UploadState):
        # Обработка редактирования файла взвода
        handler_upload_platoon(user, message)
    else:
        # Ответ по умолчанию от бота
        bot.reply_to(message, Message.DEFAULT)


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.GET_SQUAD_1)
@check_connection_with_server(bot=bot)
def squad_1(call: types.CallbackQuery):
    handler_select_squad(call, '1')


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.GET_SQUAD_2)
@check_connection_with_server(bot=bot)
def squad_2(call: types.CallbackQuery):
    handler_select_squad(call, '2')


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.GET_SQUAD_3)
@check_connection_with_server(bot=bot)
def squad_3(call: types.CallbackQuery):
    handler_select_squad(call, '3')


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.EditUser.ATTEND)
@check_connection_with_server(bot=bot)
def attend(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(Message.EditUser.ATTEND_NO, callback_data=Commands.Events.EditUser.ATTEND_NO))
    markup.add(InlineKeyboardButton(Message.EditUser.ATTEND_YES, callback_data=Commands.Events.EditUser.ATTEND_YES))

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.EditUser.ATTEND_NO)
@check_connection_with_server(bot=bot)
def attend_no(call: types.CallbackQuery):
    res = ServerWorker().add_visit_user(datetime.date.today(), 0,
                                        listener_edit_user[get_telegram_id(call.message)])

    bot.delete_message(call.message.chat.id, call.message.id)

    if res == Status.OK:
        bot.send_message(get_telegram_id(message=call.message), Message.SUCCESSFUL)
    else:
        bot.send_message(get_telegram_id(message=call.message), Message.Error.DEFAULT_ERROR)


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.EditUser.ATTEND_YES)
@check_connection_with_server(bot=bot)
def attend_yes(call: types.CallbackQuery):
    res = ServerWorker().add_visit_user(datetime.date.today(), 1,
                                        listener_edit_user[get_telegram_id(call.message)])

    bot.delete_message(call.message.chat.id, call.message.id)

    if res == Status.OK:
        bot.send_message(get_telegram_id(message=call.message), Message.SUCCESSFUL)
    else:
        bot.send_message(get_telegram_id(message=call.message), Message.Error.DEFAULT_ERROR)


@bot.callback_query_handler(func=lambda call: call.data in [Commands.Events.SET_SQUAD_1,
                                                            Commands.Events.SET_SQUAD_2,
                                                            Commands.Events.SET_SQUAD_3])
@check_connection_with_server(bot=bot)
def set_squads(call: types.CallbackQuery):
    handlers_edit_squad = {
        Commands.Events.SET_SQUAD_1: (ServerWorker().set_squad, 1),
        Commands.Events.SET_SQUAD_2: (ServerWorker().set_squad, 2),
        Commands.Events.SET_SQUAD_3: (ServerWorker().set_squad, 3),
    }

    func, num = handlers_edit_squad[call.data]

    res = func(num, listener_edit_user[get_telegram_id(call.message)])

    bot.delete_message(get_telegram_id(call.message), call.message.message_id)

    if res == Status.OK:
        bot.send_message(get_telegram_id(call.message), Message.SUCCESSFUL)
    else:
        bot.send_message(get_telegram_id(call.message), Message.Error.DEFAULT_ERROR)


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.EditUser.SQUAD)
@check_connection_with_server(bot=bot)
def set_squad(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    user = get_user(get_telegram_id(call.message))

    platoon_number = user.platoon
    count_squad = ServerWorker().get_count_platoon_squad(platoon_number)

    events = [Commands.Events.SET_SQUAD_1, Commands.Events.SET_SQUAD_2, Commands.Events.SET_SQUAD_3]

    for squad_num in range(count_squad):
        markup.add(InlineKeyboardButton(squad_num + 1, callback_data=events[squad_num]))

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
@check_connection_with_server(bot=bot)
def handler_callbacks(call: types.CallbackQuery):
    if call.data in edit_users.keys():
        telegram_id = int(call.data)
        listener_edit_user[get_telegram_id(call.message)] = telegram_id
        handler_edit_user(call)


@bot.message_handler(content_types=['document'])
@log
# @check_connection_with_server
@save_user
@security.is_login
@security.is_admin
def handle_excel_platoon(message):
    try:
        user = get_user(get_telegram_id(message))

        if user.state == UploadState.UPLOAD_FILE:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            debug(message.text)
            df = pd.read_excel(downloaded_file)
            df.columns = df.columns.map(lambda x: x.strip())

            users = []

            for offset, (idx, _row) in enumerate(df.iterrows()):
                data_user = {'name': _row[UserAttribute.NAME], 'date_of_birth': _row[UserAttribute.DOB],
                             'phone_number': _row[UserAttribute.PHONE_NUMBER], 'mail': _row[UserAttribute.MAIL],
                             'address': _row[UserAttribute.ADDRESS], 'institute': _row[UserAttribute.INSTITUTE],
                             'direction_of_study': _row[UserAttribute.DOS],
                             'group_study': _row[UserAttribute.GROUP_STUDY]}

                try:
                    data_user['squad'] = int(_row[UserAttribute.SQUAD])
                except ValueError as _:
                    data_user['squad'] = None

                if data_user['squad']:
                    data_user['role'] = Role.COMMANDER_SQUAD if _row[UserAttribute.COMMANDER] == '+' else Role.STUDENT
                elif data_user['squad'] is None and _row[UserAttribute.COMMANDER] == '+':
                    data_user['role'] = Role.COMMANDER_PLATOON
                else:
                    data_user['role'] = Role.STUDENT

                users.append(data_user)

            bot.send_message(get_telegram_id(message), Message.ATTRS_PLATOON)
            bot.register_next_step_handler(message, save_users_from_file, users)
            user.state = None

    except Exception as e:
        bot.reply_to(message, repr(e))


def save_users_from_file(message, users):
    res_msg = ''
    current_user = get_user(get_telegram_id(message))

    try:
        platoon_num, vus, semester = message.text.split(',')
        res = ServerWorker().add_platoon(int(platoon_num), int(vus), int(semester))
    except ValueError as _:
        bot.reply_to(message, Message.Error.DEFAULT_ERROR)
        current_user.state = None

        return

    if res == Status.OK:
        debug(f'{users=}')

        for offset, user in enumerate(users):
            user['platoon_number'] = platoon_num
            res = ServerWorker().save_user(user)

            if res:
                res_msg += f'{offset}) {user['name']} Токен: {res}\n\n'
            else:
                res_msg += f'{offset}) {user['name']} {Message.Error.DEFAULT_ERROR}\n\n'

        bot.reply_to(message, res_msg)
    else:
        bot.reply_to(message, Message.Error.DEFAULT_ERROR)


def handler_edit_user(call):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(Message.EditUser.SQUAD, callback_data=Commands.Events.EditUser.SQUAD))
    markup.add(InlineKeyboardButton(Message.EditUser.ATTEND, callback_data=Commands.Events.EditUser.ATTEND))

    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id, text=Message.EditUser.MAIN, reply_markup=markup)


def handler_registration(user, message):
    res = handler_state(user, message, RegistrationStates, REGISTRATION_VALIDATORS, REGISTRATION_MSG_STATES)

    if res:
        user.writer.next_data(message.text)

        if user.state == RegistrationStates.SQUAD:
            if ServerWorker().get_role(get_telegram_id(message)) == Role.COMMANDER_PLATOON:
                if ServerWorker().get_platoon_commander(int(message.text)):
                    bot.reply_to(message, Message.Error.PLATOON_COMMANDER_ERROR)
                    user.writer.old_data()
                    command_cancel(message)
                    return

        if user.state == RegistrationStates.FINAL:
            res = user.write_data()

            if res:
                bot.send_message(get_telegram_id(message), Message.SUCCESSFUL)
            else:
                bot.send_message(get_telegram_id(message), Message.Error.DEFAULT_ERROR)

            user.state = None


def handler_get_token(user, message):
    res = handler_state(user, message, GetTokenState, GET_TOKEN_VALIDATORS, GET_TOKEN_MSG_STATES)

    if res:
        if user.state == GetTokenState.AMOUNT_TOKEN:
            token_handler.set_role_to_token(message.text)
        elif user.state == GetTokenState.FINAL:
            token_handler.set_amount(int(message.text))

            msg = ''

            for offset, token in enumerate(ServerWorker().get_tokens(*token_handler.get_token_params())):
                msg += f'{offset+1}) {token}\n\n'

            bot.send_message(get_telegram_id(message), msg)

            user.state = None


def handler_edit_squad_user(user, message):
    res = handler_state(user, message, EditSquadUserState, EDIT_SQUAD_USER_VALIDATORS, EDIT_SQUAD_USER_MSG_STATES)

    if res:
        if user.state == EditSquadUserState.FINAL:
            squad_num = int(message.text)

            ServerWorker().set_squad(squad_num, listener_edit_user[get_telegram_id(message)])

            user.state = None

            bot.reply_to(message, Message.SUCCESSFUL)


def handler_upload_platoon(user, message):
    res = handler_state(user, message, UploadState, UPLOAD_VALIDATORS, UPLOAD_PLATOON_MSG_STATES)

    if res:
        if user.state == UploadState.FINAL:
            user.state = None

            bot.reply_to(message, Message.SUCCESSFUL)


def handler_login(user, message):
    res = handler_state(user, message, LoginState, LOGIN_VALIDATORS, LOGIN_MSG_STATES)

    if res:
        if user.state == LoginState.FINAL:
            if ServerWorker().get_role(get_telegram_id(message)) != Status.ERROR:
                bot.reply_to(message, Message.Error.USER_ALREADY_EXISTS)
                user.state = None
                return
            elif ServerWorker().get_role(get_telegram_id(message)) != Status.ERROR:
                bot.reply_to(message, Message.Error.USER_ALREADY_EXISTS)
                user.state = None
                return

            debug('Сохранение юзера.')
            respond = ServerWorker().attach_token_to_user(get_telegram_id(message), message.text)

            if respond == Status.OK:
                bot.reply_to(message, Message.SUCCESSFUL)
                user.state = None
            else:
                bot.reply_to(message, Message.Error.DEFAULT_ERROR)


def handler_state(user, message, state, validators, msg_states) -> bool:
    if user.state == state.FINAL:
        user.state = None

        return False
    else:
        try:
            validators[get_user(get_telegram_id(message)).state](message.text)
        except MainException as e:
            bot.reply_to(message, e)

            return False
        else:
            fsm_worker.get_fsm_obj(get_telegram_id(message)).next_state()
            bot.send_message(get_telegram_id(message), msg_states[get_user(get_telegram_id(message)).state])

            return True


def handler_select_squad(call, target_squad: str):
    markup = InlineKeyboardMarkup()
    platoon_number = get_user(get_telegram_id(call.message)).platoon
    platoon = ServerWorker().get_platoon(platoon_number)

    for user in platoon:
        squad_num = user[-3]
        telegram_id = user[-2]

        if squad_num == target_squad:
            edit_users[telegram_id] = user[0]
            markup.add(InlineKeyboardButton(user[0], callback_data=telegram_id))

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup)


bot.infinity_polling()

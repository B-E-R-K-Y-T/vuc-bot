import datetime

import telebot

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TELEGRAM_BOT_TOKEN, Message, Commands, Role
from utils.fsm.edit_squad_user.edit_squad_user import FiniteStateMachineEditSquadUser
from utils.fsm.edit_squad_user.states import EditSquadUserState, EDIT_SQUAD_USER_MSG_STATES
from utils.fsm.edit_squad_user.validators import EDIT_SQUAD_USER_VALIDATORS
from utils.fsm.fsm_container import FSMContainer
from utils.fsm.login.login_fsm import FiniteStateMachineLogin
from utils.fsm.login.states import LoginState, LOGIN_MSG_STATES
from utils.fsm.registrarion.states import REGISTRATION_MSG_STATES, RegistrationStates
from utils.security.security import Security
from utils.logger import log
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
    bot.send_message(message.chat.id, Message.WELCOME)


@bot.message_handler(commands=[Commands.GET_PLATOON])
@log
@check_connection_with_server(bot=bot)
@save_user
@security.is_login
def command_get_platoon(message: types.Message):
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
@security.is_login
def command_reg(message):
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
    bot.send_message(message.chat.id, Message.GetToken.TYPE_TOKEN)
    state = FiniteStateMachineGetToken(get_user(get_telegram_id(message)))

    fsm_worker.set_fsm_obj(get_telegram_id(message), state)


@bot.message_handler(commands=[Commands.ROLLBACK_PROCESS])
@log
@check_connection_with_server(bot=bot)
@save_user
@security.is_login
def command_stop_process(message):
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
@save_user
def command_login(message):
    bot.send_message(message.chat.id, Message.Login.LOGIN)

    state = FiniteStateMachineLogin(get_user(get_telegram_id(message)))

    fsm_worker.set_fsm_obj(get_telegram_id(message), state)


@bot.message_handler(func=lambda m: True)
@log
@check_connection_with_server(bot=bot)
@save_user
def handler_message_loging_process(message):
    user = get_user(get_telegram_id(message))

    if isinstance(user.state, LoginState):
        handler_login(user, message)
    else:
        security.is_login(handler_message)(message)


@bot.message_handler(func=lambda m: True)
@check_connection_with_server(bot=bot)
@save_user
@security.is_login
def handler_message(message):
    user = get_user(get_telegram_id(message))

    print(f'{user.state=}')

    if isinstance(user.state, RegistrationStates):
        handler_registration(user, message)
    elif isinstance(user.state, GetTokenState):
        handler_get_token(user, message)
    elif isinstance(user.state, EditSquadUserState):
        handler_edit_squad_user(user, message)
    else:
        bot.reply_to(message, Message.DEFAULT)


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.GET_SQUAD_1)
def squad_1(call: types.CallbackQuery):
    handler_select_squad(call, '1')


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.GET_SQUAD_2)
def squad_2(call: types.CallbackQuery):
    handler_select_squad(call, '2')


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.GET_SQUAD_3)
def squad_3(call: types.CallbackQuery):
    handler_select_squad(call, '3')


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.EditUser.ATTEND)
def attend(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(Message.EditUser.ATTEND_NO, callback_data=Commands.Events.EditUser.ATTEND_NO))
    markup.add(InlineKeyboardButton(Message.EditUser.ATTEND_YES, callback_data=Commands.Events.EditUser.ATTEND_YES))

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.EditUser.ATTEND_NO)
def attend_no(call: types.CallbackQuery):
    ServerWorker().add_visit_user(datetime.date.today(), 0, listener_edit_user[get_telegram_id(call.message)])


@bot.callback_query_handler(func=lambda call: call.data == Commands.Events.EditUser.ATTEND_YES)
def attend_no(call: types.CallbackQuery):
    ServerWorker().add_visit_user(datetime.date.today(), 1, listener_edit_user[get_telegram_id(call.message)])


@bot.callback_query_handler(func=lambda call: True)
def handler_callbacks(call: types.CallbackQuery):
    if call.data in edit_users.keys():
        telegram_id = int(call.data)
        listener_edit_user[get_telegram_id(call.message)] = telegram_id
        handler_edit_user(call)
    elif call.data == Commands.Events.EditUser.SQUAD:
        bot.send_message(call.message.chat.id, Message.EditSquadUserState.EDIT)

        state = FiniteStateMachineEditSquadUser(get_user(get_telegram_id(call.message)))

        fsm_worker.set_fsm_obj(get_telegram_id(call.message), state)


def handler_edit_user(call):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(Message.EditUser.SQUAD, callback_data=Commands.Events.EditUser.SQUAD))
    markup.add(InlineKeyboardButton(Message.EditUser.ATTEND, callback_data=Commands.Events.EditUser.ATTEND))

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

            if res == Status.OK:
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


def handler_login(user, message):
    res = handler_state(user, message, LoginState, LOGIN_VALIDATORS, LOGIN_MSG_STATES)

    if res:
        if user.state == LoginState.FINAL:
            if get_telegram_id(message) in ServerWorker().get_login_users():
                bot.reply_to(message, Message.Error.USER_ALREADY_EXISTS)
                user.state = None
                return
            elif get_telegram_id(message) in ServerWorker().get_admin_users():
                bot.reply_to(message, Message.Error.USER_ALREADY_EXISTS)
                user.state = None
                return

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

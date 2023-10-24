import telebot

from config import TELEGRAM_BOT_TOKEN, Message, Commands
from utils.fsm.fsm_container import FSMContainer
from utils.fsm.login.login_fsm import FiniteStateMachineLogin
from utils.fsm.login.states import LoginState, LOGIN_MSG_STATES
from utils.fsm.registrarion.states import REGISTRATION_MSG_STATES, RegistrationStates
from utils.security.security import Security
from utils.logger import log
from utils.server_worker.server_worker import ServerWorker, Status, check_connection_with_server
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


@bot.message_handler(commands=[Commands.START, Commands.HELP])
@log
@save_user
def send_welcome(message):
    bot.send_message(message.chat.id, Message.WELCOME)


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
def handler_message_loging_proces(message):
    user = get_user(get_telegram_id(message))

    if isinstance(user.state, LoginState):
        handler_login(user, message)
    else:
        security.is_login(handler_message)(message)


@bot.message_handler(func=lambda m: True)
@log
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
    else:
        bot.reply_to(message, Message.DEFAULT)


def handler_registration(user, message):
    res = handler_state(user, message, RegistrationStates, REGISTRATION_VALIDATORS, REGISTRATION_MSG_STATES)

    if res:
        user.writer.next_data(message.text)

        if user.state == RegistrationStates.SQUAD:
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


bot.infinity_polling()

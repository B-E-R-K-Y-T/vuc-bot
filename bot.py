import telebot

from config import TELEGRAM_BOT_TOKEN, Message, Commands
from utils.fsm.fsm_worker import FSMWorker
from utils.fsm.registrarion.state import REGISTRATION_MSG_STATES, RegistrationStates
from utils.security.security import Security, get_token
from utils.logger import log
from utils.server_worker.server_worker import ServerWorker
from utils.user_worker.user import save_user, get_telegram_id, get_user
from utils.fsm.registrarion.registration_fsm import FiniteStateMachineRegistration
from utils.fsm.registrarion.validators import REGISTRATION_VALIDATORS
from utils.exceptions import MainException
from utils.fsm.get_token.get_token_fsm import FiniteStateMachineGetToken
from utils.fsm.get_token.state import GET_TOKEN_MSG_STATES, GetTokenState
from utils.fsm.get_token.validators import GET_TOKEN_VALIDATORS

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)
security = Security(bot=bot)
fsm_worker = FSMWorker()
server_worker = ServerWorker()


@bot.message_handler(commands=[Commands.START, Commands.HELP])
@log
@save_user
def send_welcome(message):
    bot.send_message(message.chat.id, Message.WELCOME)


@bot.message_handler(commands=[Commands.REG])
@log
@save_user
def command_reg(message):
    bot.reply_to(message, Message.Registration.WARNING)
    bot.send_message(message.chat.id, Message.Registration.NAME)

    state = FiniteStateMachineRegistration(get_user(get_telegram_id(message)))
    state.next_state()

    get_user(get_telegram_id(message)).writer.data = []

    fsm_worker.set_fsm_obj(get_telegram_id(message), state)


@bot.message_handler(commands=[Commands.GET_TOKEN])
@log
@save_user
@security.is_login
def command_get_token(message):
    if security.is_admin(get_telegram_id(message)):
        bot.send_message(message.chat.id, Message.GetToken.TYPE_TOKEN)
        state = FiniteStateMachineGetToken(get_user(get_telegram_id(message)))
        state.next_state()

        fsm_worker.set_fsm_obj(get_telegram_id(message), state)
    else:
        bot.reply_to(message, Message.ACCESS_DENIED)


@bot.message_handler(commands=[Commands.ROLLBACK_PROCESS])
@log
@save_user
@security.is_login
def command_stop_process(message):
    get_user(get_telegram_id(message)).state = None

    bot.reply_to(message, Message.STOP_PROCESS)


@bot.message_handler(commands=[Commands.SELF])
@log
@save_user
@security.is_login
def command_self(message):
    bot.reply_to(message, get_user(get_telegram_id(message)))


@bot.message_handler(commands=[Commands.LATE])
@log
@save_user
@security.is_login
def command_late(message):
    server_worker.send_request('/test')
    # bot.reply_to(message, get_user(get_telegram_id(message)))


@bot.message_handler(func=lambda m: True)
@log
@save_user
@security.is_login
def handler_message(message):
    user = get_user(get_telegram_id(message))

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

        if user.state == RegistrationStates.FINAL:
            user.write_data()


def handler_get_token(user, message):
    res = handler_state(user, message, GetTokenState, GET_TOKEN_VALIDATORS, GET_TOKEN_MSG_STATES)

    if res:
        if user.state == GetTokenState.FINAL:
            tokens = ''
            amount = int(message.text)

            for number in range(amount):
                tokens += f'{number + 1}) {get_token()}\n\n'

            bot.send_message(get_telegram_id(message), tokens)


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

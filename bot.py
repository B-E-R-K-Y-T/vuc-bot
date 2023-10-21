import telebot

from config import TELEGRAM_BOT_TOKEN, Message, Commands
from utils.fsm.registrarion.state import REGISTRATION_MSG_STATES, RegistrationStates
from utils.security.security import Security, is_admin, get_token
from utils.logger import log
from utils.user_worker.user import save_user, get_telegram_id, get_user
from utils.fsm.registrarion.registration import FiniteStateMachineRegistration
from utils.fsm.registrarion.handlers import REGISTRATION_HANDLERS
from utils.exceptions import MainException
from utils.fsm.get_token.get_token import FiniteStateMachineGetToken
from utils.fsm.get_token.state import GET_TOKEN_MSG_STATES, GetTokenState
from utils.fsm.get_token.handlers import GET_TOKEN_HANDLERS

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)
security = Security(bot=bot, debug=False)
fsm = {}
LOG_MODE = False


@bot.message_handler(commands=[Commands.START, Commands.HELP])
@log(LOG_MODE)
@save_user
def send_welcome(message):
    bot.send_message(message.chat.id, Message.WELCOME)


@bot.message_handler(commands=[Commands.REG])
@log(LOG_MODE)
@save_user
def command_reg(message):
    bot.reply_to(message, Message.Registration.WARNING)
    bot.send_message(message.chat.id, Message.Registration.NAME)
    state = FiniteStateMachineRegistration(get_user(get_telegram_id(message)))
    state.next_state()
    fsm[get_telegram_id(message)] = state


@bot.message_handler(commands=[Commands.GET_TOKEN])
@log(LOG_MODE)
@save_user
@security.is_login
def command_get_token(message):
    if is_admin(get_telegram_id(message)):
        bot.send_message(message.chat.id, Message.GetToken.AMOUNT_TOKEN)
        state = FiniteStateMachineGetToken(get_user(get_telegram_id(message)))
        state.next_state()
        fsm[get_telegram_id(message)] = state


@bot.message_handler(commands=[Commands.STOP_PROCESS])
@log(LOG_MODE)
@save_user
@security.is_login
def command_stop_process(message):
    get_user(get_telegram_id(message)).state = None

    if fsm.get(get_telegram_id(message)) is not None:
        del fsm[get_telegram_id(message)]

    bot.reply_to(message, Message.STOP_PROCESS)


@bot.message_handler(commands=[Commands.SELF])
@log(LOG_MODE)
@save_user
@security.is_login
def command_stop_process(message):
    bot.reply_to(message, get_user(get_telegram_id(message)))


@bot.message_handler(func=lambda m: True)
@log(LOG_MODE)
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
    if handler_state(user, message, RegistrationStates, REGISTRATION_HANDLERS, REGISTRATION_MSG_STATES):
        user.write_data()


def handler_get_token(user, message):
    if handler_state(user, message, GetTokenState, GET_TOKEN_HANDLERS, GET_TOKEN_MSG_STATES):
        tokens = ''
        amount = int(message.text)

        for number in range(amount):
            tokens += f'{number + 1}) {get_token()}\n\n'

        bot.send_message(get_telegram_id(message), tokens)


def handler_state(user, message, state, handlers, msg_states) -> bool:
    if user.state == state.FINAL:
        user.state = None
        del fsm[get_telegram_id(message)]

        return False
    else:
        try:
            handlers[get_user(get_telegram_id(message)).state](message.text)
            fsm[get_telegram_id(message)].next_state()
            bot.send_message(get_telegram_id(message), msg_states[get_user(get_telegram_id(message)).state])
        except MainException as e:
            bot.reply_to(message, e)

            return False

        return True


bot.infinity_polling()

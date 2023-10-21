import telebot

from config import TELEGRAM_BOT_TOKEN, Message, Commands
from utils.fsm.registrarion.state import REGISTRATION_MSG_STATES
from utils.security.security import Security
from utils.logger import log
from utils.user_worker.user import listen_user, USERS
from utils.fsm.registrarion.registration import RegistrationStates, FiniteStateMachineRegistration
from utils.fsm.registrarion.handlers import REGISTRATION_HANDLERS
from utils.exceptions import MainException

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)
security = Security(bot=bot, debug=True)
REG_FSM = {}
LOG_MODE = False


@bot.message_handler(commands=[Commands.START, Commands.HELP])
@log(LOG_MODE)
@listen_user
def send_welcome(message):
    bot.send_message(message.chat.id, Message.WELCOME)


@bot.message_handler(commands=[Commands.REG])
@log(LOG_MODE)
@listen_user
def command_reg(message):
    bot.reply_to(message, Message.Registration.WARNING)
    bot.send_message(message.chat.id, Message.Registration.NAME)
    state = FiniteStateMachineRegistration(USERS[get_id(message)])
    state.next_state()
    REG_FSM[get_id(message)] = state


@bot.message_handler(func=lambda m: True)
@log(LOG_MODE)
@listen_user
@security.is_login
def handler_message(message):
    telegram_id = get_id(message)
    user = USERS[telegram_id]

    if isinstance(user.state, RegistrationStates):
        handler_registration(user, message)
    else:
        bot.reply_to(message, Message.DEFAULT)


def handler_registration(user, message):
    if user.state == RegistrationStates.FINAL:
        user.state = None
        user.write_data()
        del REG_FSM[get_id(message)]
    else:
        try:
            REGISTRATION_HANDLERS[USERS[get_id(message)].state](message.text)
            REG_FSM[get_id(message)].next_state()
            bot.send_message(get_id(message), REGISTRATION_MSG_STATES[USERS[get_id(message)].state])
            user.writer.next_data(message.text)
        except MainException as e:
            bot.reply_to(message, e)


def get_id(message):
    return message.chat.id


bot.infinity_polling()

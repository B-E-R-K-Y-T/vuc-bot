import telebot

from config import TELEGRAM_BOT_TOKEN, Message, Commands
from utils.security.security import Security
from utils.logger import log
from utils.user_worker.user import listen_user, USERS
from utils.fsm.registration import RegistrationStates, MSG_STATES, FiniteStateMachineRegistration

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)
security = Security(bot=bot)
REG_FSM = {}


@bot.message_handler(commands=[Commands.START, Commands.HELP])
@log(False)
@listen_user
def send_welcome(message):
    bot.send_message(message.chat.id, Message.WELCOME)


@bot.message_handler(commands=[Commands.REG])
@log(False)
@listen_user
def handler_reg(message):
    bot.reply_to(message, Message.Registration.WARNING)
    bot.send_message(message.chat.id, Message.Registration.NAME)
    state = FiniteStateMachineRegistration(USERS[get_id(message)])
    state.next_state()
    REG_FSM[get_id(message)] = state


@bot.message_handler(func=lambda m: True)
@log(False)
@listen_user
@security.is_login
def handler_message(message):
    telegram_id = get_id(message)
    user = USERS[telegram_id]

    if isinstance(user.state, RegistrationStates):
        if user.state == RegistrationStates.FINAL:
            user.state = None
            user.write_data()
            del REG_FSM[get_id(message)]
        else:
            REG_FSM[get_id(message)].next_state()
            bot.send_message(get_id(message), MSG_STATES[USERS[get_id(message)].state])
            user.writer.next_data(message.text)
    else:
        bot.reply_to(message, Message.DEFAULT)


def get_id(message):
    return message.chat.id



bot.infinity_polling()

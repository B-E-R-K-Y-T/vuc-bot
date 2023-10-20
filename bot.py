import telebot

from config import TELEGRAM_BOT_TOKEN, Message, Commands
from utils.security import Security

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)
security = Security(bot=bot)


@bot.message_handler(commands=[Commands.START, Commands.HELP])
def send_welcome(message):
	bot.send_message(message.chat.id, Message.WELCOME)


@bot.message_handler(func=lambda m: True)
@security.is_login
def echo_all(message):
	bot.reply_to(message, message.text)


bot.infinity_polling()

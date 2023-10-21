import random
import string

from config import Message, ADMINS_ID, LEN_TOKEN, DEBUG


class Security:
    def __init__(self, bot):
        self.bot = bot

    def is_login(self, func):
        def wrapper(message, *args, **kwargs):
            if DEBUG:
                return func(message, *args, **kwargs)

            # TODO: Сделать проверку, на то, что у пользака есть токен
            if message.chat.id in ADMINS_ID:
                return func(message, *args, **kwargs)
            else:
                self.bot.reply_to(message, Message.ACCESS_DENIED)

        return wrapper


def is_admin(telegram_id):
    if DEBUG:
        return True

    if telegram_id in ADMINS_ID:
        return True
    else:
        return False


def get_token():
    return _generate_token()


def _generate_token():
    length = LEN_TOKEN
    alphabet = string.ascii_letters + string.digits

    list_password = [random.choice(alphabet) for _ in range(length)]
    return ''.join(list_password)


def _save_token_to_db(token, telegram_id):
    ...

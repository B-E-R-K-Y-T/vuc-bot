import random
import string

from config import Message, ADMINS_ID, LEN_TOKEN


class Security:
    def __init__(self, bot, debug):
        self.bot = bot
        self.__debug_mode = debug

    @property
    def debug_mode(self):
        return self.__debug_mode

    @debug_mode.setter
    def debug_mode(self, debug_mode):
        self.__debug_mode = debug_mode

    def is_login(self, func):
        def wrapper(message, *args, **kwargs):
            if self.debug_mode:
                return func(message, *args, **kwargs)

            # TODO: Сделать проверку, на то, что пользак есть в бд
            if message.chat.id in ADMINS_ID:
                return func(message, *args, **kwargs)
            else:
                self.bot.reply_to(message, Message.ACCESS_DENIED)

        return wrapper


def is_admin(telegram_id):
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

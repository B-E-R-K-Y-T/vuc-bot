from config import Message, ADMINS_ID, DEBUG


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

    @staticmethod
    def is_admin(telegram_id):
        if DEBUG:
            return True

        if telegram_id in ADMINS_ID:
            return True
        else:
            return False


def _save_token_to_db(token, telegram_id):
    ...

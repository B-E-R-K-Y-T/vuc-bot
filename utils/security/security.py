from config import Message, DEBUG
from utils.server_worker.server_worker import ServerWorker


class Security:
    def __init__(self, bot):
        self.bot = bot

    def is_login(self, func):
        def wrapper(message, *args, **kwargs):
            if DEBUG:
                return func(message, *args, **kwargs)

            login_users = ServerWorker().get_login_users()
            admin_users = ServerWorker().get_admin_users()

            if (message.chat.id in login_users or
                message.chat.id in admin_users):
                return func(message, *args, **kwargs)
            else:
                self.bot.reply_to(message, Message.ACCESS_DENIED)

        return wrapper

    def is_admin(self, func):
        def wrapper(message, *args, **kwargs):
            if DEBUG:
                return func(message, *args, **kwargs)

            if message.chat.id in ServerWorker().get_admin_users():
                return func(message, *args, **kwargs)
            else:
                self.bot.reply_to(message, Message.ACCESS_DENIED)

        return wrapper

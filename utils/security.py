from config import Message, GOD_ID


class Security:
    def __init__(self, bot):
        self.bot = bot
        self.__debug_mode = False

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

            if message.chat.id == GOD_ID:
                return func(message, *args, **kwargs)
            else:
                self.bot.reply_to(message, Message.ACCESS_DENIED)

        return wrapper

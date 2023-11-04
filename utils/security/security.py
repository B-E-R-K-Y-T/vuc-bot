"""Этот модуль предоставляет класс Security, который содержит декораторы для проверки безопасности доступа к функциям бота.

Классы:

Security: Класс, представляющий механизм безопасности бота. Он содержит два декоратора для проверки доступа к функциям бота. Класс имеет следующие методы:

is_login(func): Декоратор для проверки авторизации пользователя. Если пользователь авторизован (вошел в систему) или является администратором, функция выполняется. В противном случае выводится сообщение об отказе в доступе.

is_admin(func): Декоратор для проверки привилегий администратора. Если пользователь является администратором, функция выполняется. В противном случае выводится сообщение об отказе в доступе.

Модули:

config: Импортирует константы Message и DEBUG, которые используются в декораторах.

utils.server_worker.server_worker: Импортирует класс ServerWorker из модуля server_worker, который используется для проверки доступа к серверным данным."""

from config import Message, DEBUG, ROLES, Role
from utils.logger import debug
from utils.server_worker.server_worker import ServerWorker


class Security:
    def __init__(self, bot):
        self.bot = bot

    def is_login(self, func):
        def wrapper(message, *args, **kwargs):
            if DEBUG:
                return func(message, *args, **kwargs)

            tele_id = message.chat.id
            role = ServerWorker().get_role(tele_id)

            debug(role)

            if role in ROLES or role == Role.ADMIN:
                return func(message, *args, **kwargs)
            else:
                self.bot.reply_to(message, Message.ACCESS_DENIED)

        return wrapper

    def is_admin(self, func):
        def wrapper(message, *args, **kwargs):
            if DEBUG:
                return func(message, *args, **kwargs)

            tele_id = message.chat.id
            role = ServerWorker().get_role(tele_id)

            debug(role)

            if role == Role.ADMIN:
                return func(message, *args, **kwargs)
            else:
                self.bot.reply_to(message, Message.ACCESS_DENIED)

        return wrapper

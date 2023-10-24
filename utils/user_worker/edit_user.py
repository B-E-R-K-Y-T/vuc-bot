"""Этот модуль содержит реализацию класса `ListenerEditUser`, который использует паттерн Singleton для создания единственного экземпляра класса.

Класс:

- `ListenerEditUser`: Класс, представляющий слушателя редактирования пользователя. Этот класс реализует паттерн Singleton, что означает, что он может иметь только один экземпляр во время работы программы. Класс хранит слушателей и связанные с ними идентификаторы пользователей `listener_id` и `listen_telegram_id`. Экземпляр класса можно получить с помощью декоратора `@singleton`.

Методы и свойства класса:

- `__getitem__(self, listener_id: int)`: Метод, позволяющий получить идентификатор пользователя, связанного со слушателем по его `listener_id`.

- `__setitem__(self, listener_id: int, listen_telegram_id: int)`: Метод, позволяющий установить соответствие между `listener_id` слушателя и `listen_telegram_id` идентификатором пользователя.

Используя этот модуль и класс `ListenerEditUser`, вы можете создать слушателя редактирования пользователей, устанавливать и получать связи между слушателями и идентификаторами пользователей. Обратите внимание, что этот модуль гарантирует, что можно будет работать только с одним экземпляром класса `ListenerEditUser` во всей программе, что может быть полезно в некоторых сценариях.
"""

from utils.singleton import singleton


@singleton
class ListenerEditUser:
    def __init__(self):
        self.user = {}

    def __getitem__(self, listener_id: int):
        return self.user[listener_id]

    def __setitem__(self, listener_id: int, listen_telegram_id: int):
        self.user[listener_id] = listen_telegram_id

"""Этот модуль содержит определения классов и функций, связанных с управлением пользователей и их данными.

Классы:

- `User`: Класс, представляющий пользователя. У каждого пользователя есть уникальный идентификатор `telegram_id` и различные атрибуты, такие как имя `name`, дата рождения `date_of_birth`, номер телефона `phone_number`, электронная почта `mail`, адрес `address`, институт `institute` и другие. Класс также имеет методы для записи и получения данных пользователя, а также свойства для доступа к `telegram_id` и состоянию пользователя `state`.

- `WriterData`: Класс, используемый `User` для записи и хранения данных пользователя. Он содержит методы для добавления данных `next_data`, удаления предыдущих данных `old_data` и получения текущих данных `get_data`.

Функции:

- `save_user`: Декоратор функции, который используется для сохранения информации о пользователе. При вызове функции, упакованной в этот декоратор, проверяется наличие пользователя в базе данных `ServerWorker`. Если пользователь уже существует, его данные копируются в экземпляр класса `User`. Если пользователя не существует, создается новый экземпляр `User` для данного `telegram_id`.

- `get_telegram_id`: Функция, которая извлекает `telegram_id` из сообщения.

- `get_user`: Функция, которая возвращает пользователя по его `telegram_id`.

При использовании этого модуля, вы можете создавать, обновлять и получать информацию о пользователях, а также сохранять данные пользователя.
"""

import uuid

from utils.logger import debug
from utils.server_worker.server_worker import ServerWorker, Status

users = {}


class User:
    def __init__(self, telegram_id: int):
        self.writer = WriterData()
        self.__id = uuid.uuid4()
        self.__telegram_id = telegram_id
        self.__state = None
        self.name = None
        self.date_of_brith = None
        self.phone_number = None
        self.mail = None
        self.address = None
        self.institute = None
        self.direction_of_study = None
        self.group_study = None
        self.course_number = None
        self.vus = None
        self.platoon = None
        self.squad = None

        self.__all_data = (self.name, self.date_of_brith, self.phone_number, self.mail, self.address,
                           self.institute, self.direction_of_study, self.group_study, self.course_number,
                           self.vus, self.platoon, self.squad)

    @property
    def telegram_id(self):
        return self.__telegram_id

    @telegram_id.setter
    def telegram_id(self, telegram_id: int):
        self.__telegram_id = telegram_id

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    def get_role(self):
        return ServerWorker().get_role(self.__telegram_id)

    def write_data(self):
        debug(self.writer.get_data())
        (self.name, self.date_of_brith, self.phone_number, self.mail, self.address,
         self.institute, self.direction_of_study, self.group_study, self.course_number,
         self.vus, self.platoon, self.squad) = self.writer.get_data()

        ServerWorker().add_platoon(int(self.platoon), int(self.vus), 1)
        # ServerWorker().attach_user_to_attendance(self.__telegram_id)

        params = {
            'name': self.name,
            'date_of_brith': self.date_of_brith,
            'phone_number': self.phone_number,
            'mail': self.mail,
            'address': self.address,
            'institute': self.institute,
            'direction_of_study': self.direction_of_study,
            'group_study': self.group_study,
            'course_number': self.course_number,
            'vus': self.vus,
            'platoon': self.platoon,
            'squad': self.squad,
            'telegram_id': self.__telegram_id,
            'role': ServerWorker().get_role(telegram_id=self.__telegram_id),
        }

        return ServerWorker().save_user(params)

    def set_data(self):
        (self.name, self.date_of_brith, self.phone_number, self.mail, self.address,
         self.institute, self.direction_of_study, self.group_study, self.course_number,
         self.vus, self.platoon, self.squad) = self.writer.get_data()

    def get_data(self):
        return self.writer.get_data()

    def __str__(self):
        res = ServerWorker().get_user_tg(self.__telegram_id)
        debug(res)
        attrs = res if res else [None for _ in range(100)]

        res = (f'ФИО: {attrs[0]}\n'
               f'Дата рождения: {attrs[1]}\n'
               f'Номер телефона: {attrs[2]}\n'
               f'Почта: {attrs[3]}\n'
               f'Адрес: {attrs[4]}\n'
               f'Институт: {attrs[5]}\n'
               f'Направление: {attrs[6]}\n'
               f'Группа: {attrs[7]}\n'
               f'Номер курса: {attrs[8]}\n'
               f'ВУС: {attrs[9]}\n'
               f'Взвод: {attrs[10]}\n'
               f'Отделение: {attrs[11]}\n'
               f'Должность: {ServerWorker().get_role(self.__telegram_id)}\n'
               f'ID: {self.__telegram_id}\n')

        return res


class WriterData:
    def __init__(self):
        self.__data = []

    def next_data(self, value):
        self.__data.append(value)

    def old_data(self):
        self.__data.pop(-1)

    def get_data(self):
        return self.__data

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, seq: list):
        self.__data = seq


def save_user(func):
    def wrapper(message, *args, **kwargs):
        telegram_id = message.chat.id
        user = ServerWorker().get_user_tg(telegram_id)

        if user != Status.ERROR and not get_user(telegram_id):
            usr = User(telegram_id)

            for attr in user:
                usr.writer.next_data(attr)

            usr.set_data()
            users[telegram_id] = usr
        elif not get_user(telegram_id):
            users[telegram_id] = User(telegram_id)

        return func(message, *args, **kwargs)

    return wrapper


def get_telegram_id(message):
    return message.chat.id


def get_user(telegram_id) -> User:
    return users.get(telegram_id)

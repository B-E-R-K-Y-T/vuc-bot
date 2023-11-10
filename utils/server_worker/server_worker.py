"""Этот модуль предоставляет класс `ServerWorker`, который используется для обращения к удаленному серверу с помощью HTTP-запросов.

Классы:

- `ServerWorker`: Класс, представляющий рабочего сервера. Он содержит методы, которые выполняют различные операции на удаленном сервере, используя HTTP-запросы. Класс имеет следующие методы:

  - `get_tokens(amount: int, role: str)`: Получает указанное количество токенов для указанной роли. Возвращает список полученных токенов.

  - `set_squad(squad_number, telegram_id)`: Устанавливает указанному пользователю указанную команду взвода. Возвращает объект перечисления `Status.OK`, если операция выполнена успешно, и `Status.ERROR` в противном случае.

  - `get_count_platoon_squad(platoon_number: int)`: Получает количество пользователей в указанной команде взвода. Возвращает полученное количество или объект перечисления `Status.ERROR` в случае ошибки.

  - `get_platoon(platoon_number: int)`: Получает всех пользователей из указанной команды взвода. Возвращает список пользователей в формате `[('user1_attr1', 'user1_attr2', ...), ('user2_attr1', 'user2_attr2', ...), ...]` или объект перечисления `Status.ERROR` в случае ошибки.

  - `get_platoon_commander(platoon_number: int)`: Получает идентификатор пользователя, являющегося командиром указанной команды взвода. Возвращает полученный идентификатор или `0` в случае отсутствия командира или объект перечисления `Status.ERROR` в случае ошибки.

  - `get_free_tokens()`: Получает все свободные токены. Возвращает список свободных токенов.

  - `delete_user(telegram_id: int)`: Удаляет указанного пользователя. Возвращает объект перечисления `Status.OK`, если операция выполнена успешно, и `Status.ERROR` в противном случае.

  - `get_user(telegram_id: int)`: Получает информацию о указанном пользователе. Возвращает список информации о пользователе в формате `[attr1, attr2, ...]` или объект перечисления `Status.ERROR` в случае ошибки.

  - `attach_user_to_attendance(telegram_id: int)`: Присоединяет пользователя к присутствию на занятии. Возвращает объект перечисления `Status.OK`, если операция выполнена успешно, и `Status.ERROR` в противном случае.

  - `add_visit_user(date_v, visiting: int, telegram_id: int)`: Добавляет посещение указанному пользователю. Возвращает объект перечисления `Status.OK`, если операция выполнена успешно, и `Status.ERROR` в противном случае.

  - `save_user(data)`: Сохраняет информацию о пользователе с указанными данными. Возвращает объект перечисления `Status.OK`, если операция выполнена успешно, и `Status.ERROR` в противном случае.

  - `get_login_users()`: Получает идентификаторы пользователей, которые вошли в систему. Возвращает список идентификаторов пользователей.

  - `get_len_token()`: Получает количество токенов системы. Возвращает полученное количество.

  - `get_role(telegram_id: int)`: Получает роль указанного пользователя. Возвращает роль пользователя.

  - `get_admin_users()`: Получает идентификаторы администраторов системы. Возвращает список идентификаторов администраторов.

  - `attach_token_to_user(telegram_id: int, token: str)`: Присоединяет токен к указанному пользователю. Возвращает объект перечисления `Status.OK`, если операция выполнена успешно, и `Status.ERROR` в противном случае.

  - `ban_user(telegram_id)`: Блокирует указанного пользователя. Возвращает объект перечисления `Status.OK`, если операция выполнена успешно, и `Status.ERROR` в противном случае.

  - `test_connection()`: Проверяет соединение с удаленным сервером. Возвращает объект перечисления `Status.OK`, если соединение установлено успешно, и `Status.ERROR` в противном случае.

Функции:

- `check_connection_with_server(bot)`: Декоратор, который проверяет соединение с удаленным сервером перед выполнением декорируемой функции. Если соединение установлено успешно, функция выполняется, в противном случае выводится сообщение об ошибке соединения.
"""

import requests

from enum import auto, Enum, unique
from config import CRUD_ADDRESS, EndPoint, Message
from utils.logger import debug


def _check_connection(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            return Status.ERROR
        else:
            return res

    return wrapper


@unique
class Status(Enum):
    OK = auto()
    ERROR = auto()


class ServerWorker:
    def __init__(self):
        self.address = CRUD_ADDRESS

    def get_tokens(self, amount: int, role: str):
        res = requests.get(url=f'{self.address}{EndPoint.GET_TOKEN}',
                           params={'amount': amount, 'role': role})

        if res.status_code == 200:
            return [token for token in res.text.split('&') if token]

    def set_squad(self, squad_number, telegram_id):
        res = requests.get(url=f'{self.address}{EndPoint.SET_PLATOON_SQUAD_OF_USER}',
                           params={'squad_number': squad_number, 'telegram_id': telegram_id})

        if res.status_code == 200:
            return Status.OK
        else:
            return Status.ERROR

    def get_count_platoon_squad(self, platoon_number: int):
        res = requests.get(url=f'{self.address}{EndPoint.GET_COUNT_PLATOON_SQUAD}',
                           params={'platoon_number': platoon_number})

        if res.status_code == 200:
            return int(res.text)
        else:
            return Status.ERROR

    def get_platoon(self, platoon_number: int):
        res = requests.get(url=f'{self.address}{EndPoint.GET_PLATOON}',
                           params={'platoon_number': platoon_number})

        if res.status_code == 200:
            student = res.text.split('%%')
            students = [tuple(a for a in attr.split('&') if a) for attr in student if attr]

            return students

    def get_platoon_commander(self, platoon_number: int):
        res = requests.get(url=f'{self.address}{EndPoint.GET_PLATOON_COMMANDER}',
                           params={'platoon_number': platoon_number})

        if res.status_code == 200:
            return int(res.text) if res.text.isnumeric() else 0
        else:
            return Status.ERROR

    def login(self, token: str):
        res = requests.get(url=f'{self.address}{EndPoint.LOGIN}', params={'token': token})

        if res.status_code == 200:
            return int(res.text)

    def get_free_tokens(self):
        raise Exception('Устарело')

        res = requests.get(url=f'{self.address}{EndPoint.GET_FREE_TOKEN}')

        if res.status_code == 200:
            return [token for token in res.text.split('&') if token]

    def delete_user(self, telegram_id: int):
        res = requests.get(url=f'{self.address}{EndPoint.DELETE_USER}', params={'telegram_id': telegram_id})

        if res.status_code == 200:
            return Status.OK
        else:
            return Status.ERROR

    def get_user(self, telegram_id: int):
        raise Exception('Временно устарело')

        res = requests.get(url=f'{self.address}{EndPoint.GET_USER}', params={'telegram_id': telegram_id})

        if res.status_code == 200:
            return [token for token in res.text.split('&') if token]

    def get_user_tg(self, telegram_id: int):
        res = requests.get(url=f'{self.address}{EndPoint.GET_USER_TG}', params={'telegram_id': telegram_id})

        if res.status_code == 200:
            if res.text == '-1':
                return Status.ERROR

            return [token for token in res.text.split('&') if token]

    def attach_user_to_attendance(self, telegram_id: int):
        res = requests.get(url=f'{self.address}{EndPoint.ATTACH_USER_ATTENDANCE}', params={'telegram_id': telegram_id})

        if res.status_code == 200:
            return Status.OK
        else:
            return Status.ERROR

    def add_visit_user(self, date_v, visiting: int, telegram_id: int):
        res = requests.get(url=f'{self.address}{EndPoint.UPDATE_ATTENDANCE_USER}',
                           params={'date_v': date_v, 'visiting': visiting, 'telegram_id': telegram_id,})

        if res.status_code == 200:
            return Status.OK
        else:
            return Status.ERROR

    def save_user(self, data):
        res = requests.get(url=f'{self.address}{EndPoint.SAVE_USER}', params=data)

        if res.status_code == 200:
            return res.text

    def add_platoon(self, platoon_number: int, vus: int, semester: int):
        res = requests.get(url=f'{self.address}{EndPoint.ADD_PLATOON}', params={'platoon_number': platoon_number,
                                                                                'vus': vus,
                                                                                'semester': semester})

        if res.status_code == 200:
            return Status.OK
        else:
            return Status.ERROR

    def get_login_users(self):
        res = requests.get(url=f'{self.address}{EndPoint.GET_LOGINS}')

        if res.status_code == 200:
            return [int(token) for token in res.text.split('&') if token and token.isnumeric()]

    def get_len_token(self):
        res = requests.get(url=f'{self.address}{EndPoint.GET_LEN_TOKEN}')

        if res.status_code == 200:
            return int(res.text)

    def get_role(self, telegram_id: int):
        res = requests.get(url=f'{self.address}{EndPoint.GET_ROLE}', params={'telegram_id': telegram_id})

        debug(f'{res.text=}')

        if res.status_code == 200:
            if res.text == 'None':
                return Status.ERROR

            return res.text

    def check_admin(self, telegram_id: int):
        res = requests.get(url=f'{self.address}{EndPoint.GET_ADMINS}')

        if res.status_code == 200:
            return [int(token) for token in res.text.split('&') if token and token.isnumeric()]

    def attach_token_to_user(self, telegram_id: int, token: str):
        res = requests.get(url=f'{self.address}{EndPoint.ATTACH_TOKEN}',
                           params={'telegram_id': telegram_id, 'token': token})

        if res.status_code == 200:
            return Status.OK

    def ban_user(self, telegram_id):
        res = requests.get(url=f'{self.address}{EndPoint.BAN_USER}',
                           params={'telegram_id': telegram_id})

        if res.status_code == 200:
            return Status.OK
        else:
            return Status.ERROR

    def test_connection(self):
        try:
            res = requests.get(url=f'{self.address}/')
        except requests.exceptions.ConnectionError as e:
            return Status.ERROR

        if res.status_code == 200:
            return Status.OK
        else:
            return Status.ERROR


def check_connection_with_server(bot):
    def decorator(func):
        def wrapper(message, *args, **kwargs):
            res = ServerWorker().test_connection()

            if res == Status.OK:
                return func(message, *args, **kwargs)
            else:
                bot.reply_to(message, Message.Error.CONNECTION_ERROR)

        return wrapper
    return decorator


if __name__ == '__main__':
    s = ServerWorker()
    print(s.get_tokens(1, 'Студент'))

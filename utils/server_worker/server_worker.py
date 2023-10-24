import requests

from enum import auto, Enum, unique
from config import CRUD_ADDRESS, EndPoint, Message


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

    def get_tokens(self, amount, role):
        res = requests.get(url=f'{self.address}{EndPoint.GET_TOKEN}',
                           params={'amount': amount, 'role': role})

        if res.status_code == 200:
            return [token for token in res.text.split('&') if token]

    def get_free_tokens(self):
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
        res = requests.get(url=f'{self.address}{EndPoint.GET_USER}', params={'telegram_id': telegram_id})

        if res.status_code == 200:
            return [token for token in res.text.split('&') if token]

    def save_user(self, data):
        res = requests.get(url=f'{self.address}{EndPoint.SAVE_USER}', params=data)

        if res.status_code == 200 and res.text == '0':
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

        if res.status_code == 200:
            return res.text

    def get_admin_users(self):
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
        res = requests.get(url=f'{self.address}/')

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

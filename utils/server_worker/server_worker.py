import requests

from enum import auto, Enum, unique
from config import CRUD_ADDRESS, EndPoint


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

    def get_login_users(self):
        res = requests.get(url=f'{self.address}{EndPoint.GET_LOGINS}')

        if res.status_code == 200:
            return [int(token) for token in res.text.split('&') if token and token.isnumeric()]

    def get_len_token(self):
        res = requests.get(url=f'{self.address}{EndPoint.GET_LEN_TOKEN}')

        if res.status_code == 200:
            return int(res.text)

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


if __name__ == '__main__':
    s = ServerWorker()
    print(s.get_tokens(1, 'Студент'))

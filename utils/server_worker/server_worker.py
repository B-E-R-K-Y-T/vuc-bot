import requests

from config import CRUD_ADDRESS, EndPoint


class ServerWorker:
    def __init__(self):
        self.address = CRUD_ADDRESS

    def test(self):
        res = requests.get(url=f'{self.address}/')

        return res

    def get_tokens(self, amount, role):
        res = requests.get(url=f'{self.address}{EndPoint.GET_TOKEN}', params={'amount': amount, 'role': role})

        if res.status_code == 200:
            return [token for token in res.text.split('&') if token]


if __name__ == '__main__':
    s = ServerWorker()
    print(s.get_tokens(1, 'Студент'))

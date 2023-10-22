import requests

from config import CRUD_ADDRESS


class ServerWorker:
    def __init__(self):
        self.address = CRUD_ADDRESS

    def send_request(self, url):
        res = requests.get(url=f'{self.address}{url}')
        print(res, res.text)
        return res

from utils.singleton import singleton


@singleton
class ListenerEditUser:
    def __init__(self):
        self.user = {}

    def __getitem__(self, listener_id: int):
        return self.user[listener_id]

    def __setitem__(self, listener_id: int, listen_telegram_id: int):
        self.user[listener_id] = listen_telegram_id

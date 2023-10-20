USERS = {}


class User:
    def __init__(self, telegram_id: int):
        self.writer = WriterData()
        self.__telegram_id = telegram_id
        self.__state = None
        self.name = UserName()
        self.date_of_brith = None
        self.phone_number = None
        self.mail = None
        self.address = None
        self.institute = None
        self.course_number = None
        self.vus = None

    @property
    def telegram_id(self):
        return self.__telegram_id

    @telegram_id.setter
    def telegram_id(self, telegram_id: int):
        self.telegram_id = telegram_id

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    def write_data(self):
        self.name, self.date_of_brith, self.phone_number, self.mail, self.address, self.institute, self.course_number, self.vus = self.writer.get_data()


class UserName:
    def __init__(self):
        self.__name = None

    def __get__(self):
        return self.__name

    def __set__(self, _, name):
        self.__name = name


class WriterData:
    def __init__(self):
        self.data = []

    def next_data(self, value):
        self.data.append(value)

    def get_data(self):
        return self.data


def listen_user(func):
    def wrapper(message, *args, **kwargs):
        telegram_id = message.chat.id
        if telegram_id not in USERS:
            USERS[telegram_id] = User(telegram_id)

        return func(message, *args, **kwargs)

    return wrapper


if __name__ == '__main__':
    usr = User(123)
    print(usr.name)
    usr.name = '123123'
    print(usr.name)

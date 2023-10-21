users = {}


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
        self.direction_of_study = None
        self.group_study = None
        self.course_number = None
        self.vus = None

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

    def write_data(self):
        (self.name, self.date_of_brith, self.phone_number, self.mail, self.address,
         self.institute, self.direction_of_study, self.group_study, self.course_number, self.vus) = self.writer.get_data()

    def __str__(self):
        res = (f'ФИО: {self.name}'
               f'Дата рождения: {self.date_of_brith}'
               f'Номер телефона: {self.phone_number}'
               f'Почта: {self.mail}'
               f'Адрес: {self.address}'
               f'Институт: {self.institute}'
               f'Направление: {self.direction_of_study}'
               f'Группа: {self.group_study}'
               f'Номер курса: {self.course_number}'
               f'ВУС: {self.course_number}')

        return res


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


def save_user(func):
    def wrapper(message, *args, **kwargs):
        telegram_id = message.chat.id
        if telegram_id not in users:
            users[telegram_id] = User(telegram_id)

        return func(message, *args, **kwargs)

    return wrapper


def get_telegram_id(message):
    return message.chat.id


def get_user(telegram_id):
    return users[telegram_id]


if __name__ == '__main__':
    usr = User(123)
    print(usr.name)
    usr.name = '123123'
    print(usr.name)

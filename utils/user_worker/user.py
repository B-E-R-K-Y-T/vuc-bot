users = {}


class User:
    def __init__(self, telegram_id: int):
        self.writer = WriterData()
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
         self.institute, self.direction_of_study, self.group_study, self.course_number,
         self.vus, self.platoon, self.squad) = self.writer.get_data()

    def __str__(self):
        res = (f'ФИО: {self.name}\n'
               f'Дата рождения: {self.date_of_brith}\n'
               f'Номер телефона: {self.phone_number}\n'
               f'Почта: {self.mail}\n'
               f'Адрес: {self.address}\n'
               f'Институт: {self.institute}\n'
               f'Направление: {self.direction_of_study}\n'
               f'Группа: {self.group_study}\n'
               f'Номер курса: {self.course_number}\n'
               f'ВУС: {self.vus}\n'
               f'Взвод: {self.platoon}\n'
               f'Отделение: {self.squad}\n'
               f'ID: {self.__telegram_id}\n')

        return res


class WriterData:
    def __init__(self):
        self.__data = []

    def next_data(self, value):
        self.__data.append(value)

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
        if telegram_id not in users:
            users[telegram_id] = User(telegram_id)

        return func(message, *args, **kwargs)

    return wrapper


def get_telegram_id(message):
    return message.chat.id


def get_user(telegram_id):
    return users[telegram_id]

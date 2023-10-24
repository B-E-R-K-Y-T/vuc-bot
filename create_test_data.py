import string
import random

from config import Role
from utils.server_worker.server_worker import ServerWorker
from utils.user_worker.user import User


def generate_name():
    name = 'NAME-'

    for _ in range(3):
        for i in range(random.randint(5, 14)):
            name += random.choice(string.ascii_letters)

        name += ' '

    return name


def gen_platoon():
    platoon = []

    for week_num in range(1, 6):
        for num in range(4):
            platoon.append(f'{week_num}{random.randint(1, 5)}{random.randint(1, 5)}0')

    return platoon


def gen_tele_id():
    return random.randint(1_000, 2_000)


def gen_token():
    # tokens = ServerWorker().get_tokens(1, random.choice(config.ENUM_TYPE_TOKEN))
    tokens = ServerWorker().get_tokens(1, Role.STUDENT)

    return tokens[0]


def create_user():
    t_id = gen_tele_id()
    ServerWorker().attach_token_to_user(t_id, gen_token())
    user = User(t_id)
    attrs = [generate_name(), '1.1.1901', '89168118457', 'test@test.ber', 'address', 'name_inst',
             'dir_study', 'BSBO-08-19', 1, 541100, 552, random.randint(1, 3)]

    for attr in attrs:
        user.writer.next_data(attr)

    user.write_data()


def create(amount):
    for _ in range(amount):
        create_user()


if __name__ == '__main__':
    # print(generate_name())
    # print(gen_platoon())
    # print(gen_tele_id())
    # create_user()

    create(30)

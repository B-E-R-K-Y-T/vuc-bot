import re
import string

from enum import Enum, auto, unique
from config import Message, MINIUM_AGE_ENTRANCE
from utils.exceptions import NameException, DateException, PhoneException, MailException, InstituteException, \
    AddressException, CourseNumberException, VusException, DirectionOfStudyException, GroupStudyException
from datetime import datetime


@unique
class RegistrationStates(Enum):
    NAME = auto()
    DATE_OF_BIRTH = auto()
    PHONE_NUMBER = auto()
    MAIL = auto()
    ADDRESS = auto()
    INSTITUTE = auto()
    DIRECTION_OF_STUDY = auto()
    GROUP_STUDY = auto()
    COURSE_NUMBER = auto()
    VUS = auto()
    FINAL = auto()


class FiniteStateMachineRegistration:
    def __init__(self, user):
        self.user = user
        self.states = iter(STATES)

    def next_state(self):
        self.user.state = next(self.states)


def handler_name_state(text: str):
    text = text.split(' ')

    if len(text) != 3:
        raise NameException(Message.Error.NAME)
    else:
        for word in text:
            if word.isdigit():
                raise NameException(Message.Error.NAME_DIGIT)


def handler_date_of_birth(text: str):
    text = [int(i) for i in text.split('.') if i.isnumeric()]

    if len(text) != 3:
        raise DateException(Message.Error.DATE)
    else:
        day, mouth, year = text

        if not 0 <= day <= 31:
            raise DateException(Message.Error.DATE)
        elif not 0 <= mouth <= 12:
            raise DateException(Message.Error.DATE)
        elif not 1901 <= year <= datetime.now().year - MINIUM_AGE_ENTRANCE:
            raise DateException(Message.Error.DATE)


def handler_phone_number(text: str):
    text = text.replace(' ', '')

    if not re.fullmatch(pattern=r'^((\+7|7|8)+([0-9]){10})$', string=text):
        raise PhoneException(Message.Error.PHONE)


def handler_mail(text: str):
    if not re.fullmatch(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', string=text):
        raise MailException(Message.Error.MAIL)


def handler_address(text: str):
    for symbol in text:
        if symbol not in string.punctuation and not symbol.isdigit():
            break
    else:
        raise AddressException(Message.Error.ADDRESS)


def handler_institute(text: str):
    for symbol in text:
        if symbol not in string.punctuation and not symbol.isdigit():
            break
    else:
        raise InstituteException(Message.Error.INSTITUTE)


def handler_direction_of_study(text: str):
    for symbol in text:
        if symbol not in string.punctuation and not symbol.isdigit():
            break
    else:
        raise DirectionOfStudyException(Message.Error.DIRECTION_OF_STUDY)


def handler_group_study(text: str):
    for symbol in text:
        if symbol not in string.punctuation and not symbol.isdigit():
            break
    else:
        raise GroupStudyException(Message.Error.GROUP_STUDY)


def handler_course_number(text: str):
    if not text.isnumeric():
        raise CourseNumberException(Message.Error.COURSE_NUMBER)
    elif not 1 <= int(text) <= 8:
        raise CourseNumberException(Message.Error.COURSE_NUMBER)


def handler_vus(text: str):
    if not text.isdigit():
        raise VusException(Message.Error.VUS)


HANDLERS = {
    RegistrationStates.NAME: handler_name_state,
    RegistrationStates.DATE_OF_BIRTH: handler_date_of_birth,
    RegistrationStates.PHONE_NUMBER: handler_phone_number,
    RegistrationStates.MAIL: handler_mail,
    RegistrationStates.ADDRESS: handler_address,
    RegistrationStates.INSTITUTE: handler_institute,
    RegistrationStates.COURSE_NUMBER: handler_course_number,
    RegistrationStates.VUS: handler_vus,
    RegistrationStates.DIRECTION_OF_STUDY: handler_direction_of_study,
    RegistrationStates.GROUP_STUDY: handler_group_study,
}

MSG_STATES = {
    RegistrationStates.NAME: Message.Registration.NAME,
    RegistrationStates.DATE_OF_BIRTH: Message.Registration.DATE_OF_BIRTH,
    RegistrationStates.PHONE_NUMBER: Message.Registration.PHONE_NUMBER,
    RegistrationStates.MAIL: Message.Registration.MAIL,
    RegistrationStates.ADDRESS: Message.Registration.ADDRESS,
    RegistrationStates.INSTITUTE: Message.Registration.INSTITUTE,
    RegistrationStates.COURSE_NUMBER: Message.Registration.COURSE_NUMBER,
    RegistrationStates.VUS: Message.Registration.VUS,
    RegistrationStates.DIRECTION_OF_STUDY: Message.Registration.DIRECTION_OF_STUDY,
    RegistrationStates.GROUP_STUDY: Message.Registration.GROUP_STUDY,
    RegistrationStates.FINAL: Message.Registration.FINAL,
}

STATES = [
    RegistrationStates.NAME,
    RegistrationStates.DATE_OF_BIRTH,
    RegistrationStates.PHONE_NUMBER,
    RegistrationStates.MAIL,
    RegistrationStates.ADDRESS,
    RegistrationStates.INSTITUTE,
    RegistrationStates.DIRECTION_OF_STUDY,
    RegistrationStates.GROUP_STUDY,
    RegistrationStates.COURSE_NUMBER,
    RegistrationStates.VUS,
    RegistrationStates.FINAL,
]


if __name__ == '__main__':
    s = RegistrationStates(1)


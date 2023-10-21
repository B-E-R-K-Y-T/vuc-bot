import re
import string

from config import Message, MINIUM_AGE_ENTRANCE
from utils.exceptions import NameException, DateException, PhoneException, MailException, InstituteException, \
    AddressException, CourseNumberException, VusException, DirectionOfStudyException, GroupStudyException
from datetime import datetime
from utils.fsm.handlers_worker import HandlerWorker
from utils.fsm.registrarion.state import RegistrationStates

hw = HandlerWorker()


@hw.save_handler(RegistrationStates.NAME)
def handler_name_state(text: str):
    text = text.split(' ')

    if len(text) != 3:
        raise NameException(Message.Error.NAME)
    else:
        for word in text:
            if word.isdigit():
                raise NameException(Message.Error.NAME_DIGIT)


@hw.save_handler(RegistrationStates.DATE_OF_BIRTH)
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


@hw.save_handler(RegistrationStates.PHONE_NUMBER)
def handler_phone_number(text: str):
    text = text.replace(' ', '')

    if not re.fullmatch(pattern=r'^((\+7|7|8)+([0-9]){10})$', string=text):
        raise PhoneException(Message.Error.PHONE)


@hw.save_handler(RegistrationStates.MAIL)
def handler_mail(text: str):
    if not re.fullmatch(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', string=text):
        raise MailException(Message.Error.MAIL)


@hw.save_handler(RegistrationStates.ADDRESS)
def handler_address(text: str):
    for symbol in text:
        if symbol not in string.punctuation and not symbol.isdigit():
            break
    else:
        raise AddressException(Message.Error.ADDRESS)


@hw.save_handler(RegistrationStates.INSTITUTE)
def handler_institute(text: str):
    for symbol in text:
        if symbol not in string.punctuation and not symbol.isdigit():
            break
    else:
        raise InstituteException(Message.Error.INSTITUTE)


@hw.save_handler(RegistrationStates.DIRECTION_OF_STUDY)
def handler_direction_of_study(text: str):
    for symbol in text:
        if symbol not in string.punctuation and not symbol.isdigit():
            break
    else:
        raise DirectionOfStudyException(Message.Error.DIRECTION_OF_STUDY)


@hw.save_handler(RegistrationStates.GROUP_STUDY)
def handler_group_study(text: str):
    for symbol in text:
        if symbol not in string.punctuation and not symbol.isdigit():
            break
    else:
        raise GroupStudyException(Message.Error.GROUP_STUDY)


@hw.save_handler(RegistrationStates.COURSE_NUMBER)
def handler_course_number(text: str):
    if not text.isnumeric():
        raise CourseNumberException(Message.Error.COURSE_NUMBER)
    elif not 1 <= int(text) <= 8:
        raise CourseNumberException(Message.Error.COURSE_NUMBER)


@hw.save_handler(RegistrationStates.VUS)
def handler_vus(text: str):
    if not text.isdigit():
        raise VusException(Message.Error.VUS)


REGISTRATION_HANDLERS = hw.get_handlers()

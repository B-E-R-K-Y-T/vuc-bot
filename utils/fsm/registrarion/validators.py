import re
import string

from config import Message, MINIUM_AGE_ENTRANCE
from utils.exceptions import NameException, DateException, PhoneException, MailException, InstituteException, \
    AddressException, CourseNumberException, VusException, DirectionOfStudyException, GroupStudyException, \
    PlatoonException, SquadException
from datetime import datetime
from utils.fsm.validators_worker import ValidatorWorker
from utils.fsm.registrarion.state import RegistrationStates

vw = ValidatorWorker()


@vw.save_validator(RegistrationStates.NAME)
def validator_name_state(text: str):
    text = text.split(' ')

    if len(text) != 3:
        raise NameException(Message.Error.NAME)
    else:
        for word in text:
            if word.isdigit():
                raise NameException(Message.Error.NAME_DIGIT)


@vw.save_validator(RegistrationStates.DATE_OF_BIRTH)
def validator_date_of_birth(text: str):
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


@vw.save_validator(RegistrationStates.PHONE_NUMBER)
def validator_phone_number(text: str):
    text = text.replace(' ', '')

    if not re.fullmatch(pattern=r'^((\+7|7|8)+([0-9]){10})$', string=text):
        raise PhoneException(Message.Error.PHONE)


@vw.save_validator(RegistrationStates.MAIL)
def validator_mail(text: str):
    if not re.fullmatch(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', string=text):
        raise MailException(Message.Error.MAIL)


@vw.save_validator(RegistrationStates.ADDRESS)
def validator_address(text: str):
    for symbol in text:
        if symbol not in string.punctuation and not symbol.isdigit():
            break
    else:
        raise AddressException(Message.Error.ADDRESS)


@vw.save_validator(RegistrationStates.INSTITUTE)
def validator_institute(text: str):
    for symbol in text:
        if symbol not in string.punctuation and not symbol.isdigit():
            break
    else:
        raise InstituteException(Message.Error.INSTITUTE)


@vw.save_validator(RegistrationStates.DIRECTION_OF_STUDY)
def validator_direction_of_study(text: str):
    for symbol in text:
        if symbol not in string.punctuation and not symbol.isdigit():
            break
    else:
        raise DirectionOfStudyException(Message.Error.DIRECTION_OF_STUDY)


@vw.save_validator(RegistrationStates.GROUP_STUDY)
def validator_group_study(text: str):
    for symbol in text:
        if symbol not in string.punctuation and not symbol.isdigit():
            break
    else:
        raise GroupStudyException(Message.Error.GROUP_STUDY)


@vw.save_validator(RegistrationStates.COURSE_NUMBER)
def validator_course_number(text: str):
    if not text.isnumeric():
        raise CourseNumberException(Message.Error.COURSE_NUMBER)
    elif not 1 <= int(text) <= 8:
        raise CourseNumberException(Message.Error.COURSE_NUMBER)


@vw.save_validator(RegistrationStates.VUS)
def validator_vus(text: str):
    if not text.isdigit():
        raise VusException(Message.Error.VUS)


@vw.save_validator(RegistrationStates.PLATOON)
def validator_platoon(text: str):
    if not text.isdigit():
        raise PlatoonException(Message.Error.PLATOON)


@vw.save_validator(RegistrationStates.SQUAD)
def validator_squad(text: str):
    if not text.isdigit():
        raise SquadException(Message.Error.SQUAD)


REGISTRATION_VALIDATORS = vw.get_validators()

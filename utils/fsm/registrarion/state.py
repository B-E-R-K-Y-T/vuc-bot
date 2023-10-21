from enum import Enum, auto, unique

from config import Message


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


STATE = (
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
)

REGISTRATION_MSG_STATES = {
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

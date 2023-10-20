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
    COURSE_NUMBER = auto()
    VUS = auto()

    FINAL = auto()

    def __contains__(self, item):
        return item in [getattr(self, attr) for attr in dir(self) if attr.isupper()]


class FiniteStateMachineRegistration:
    def __init__(self, user):
        self.user = user
        self.states = iter(STATES)

    def next_state(self):
        self.user.state = next(self.states)


MSG_STATES = {
    RegistrationStates.NAME: Message.Registration.NAME,
    RegistrationStates.DATE_OF_BIRTH: Message.Registration.DATE_OF_BIRTH,
    RegistrationStates.PHONE_NUMBER: Message.Registration.PHONE_NUMBER,
    RegistrationStates.MAIL: Message.Registration.MAIL,
    RegistrationStates.ADDRESS: Message.Registration.ADDRESS,
    RegistrationStates.INSTITUTE: Message.Registration.INSTITUTE,
    RegistrationStates.COURSE_NUMBER: Message.Registration.COURSE_NUMBER,
    RegistrationStates.VUS: Message.Registration.VUS,
    RegistrationStates.FINAL: Message.Registration.FINAL,
}

STATES = [
    RegistrationStates.NAME,
    RegistrationStates.DATE_OF_BIRTH,
    RegistrationStates.PHONE_NUMBER,
    RegistrationStates.MAIL,
    RegistrationStates.ADDRESS,
    RegistrationStates.INSTITUTE,
    RegistrationStates.COURSE_NUMBER,
    RegistrationStates.VUS,
    RegistrationStates.FINAL,
]


if __name__ == '__main__':
    s = RegistrationStates(1)


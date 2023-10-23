from enum import Enum, auto, unique

from config import Message


@unique
class LoginState(Enum):
    LOGIN = auto()
    FINAL = auto()


STATE = (
    LoginState.LOGIN,
    LoginState.FINAL,
)

LOGIN_MSG_STATES = {
    LoginState.LOGIN: Message.Login.LOGIN,
    LoginState.FINAL: Message.Login.FINAL,
}

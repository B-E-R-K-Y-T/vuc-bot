from enum import Enum, auto, unique

from config import Message


@unique
class GetTokenState(Enum):
    TYPE_TOKEN = auto()
    AMOUNT_TOKEN = auto()
    FINAL = auto()


STATE = (
    GetTokenState.TYPE_TOKEN,
    GetTokenState.AMOUNT_TOKEN,
    GetTokenState.FINAL,
)

GET_TOKEN_MSG_STATES = {
    GetTokenState.TYPE_TOKEN: Message.GetToken.TYPE_TOKEN,
    GetTokenState.AMOUNT_TOKEN: Message.GetToken.AMOUNT_TOKEN,
    GetTokenState.FINAL: Message.GetToken.FINAL,
}

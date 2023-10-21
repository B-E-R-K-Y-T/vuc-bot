from enum import Enum, auto, unique

from config import Message


@unique
class GetTokenState(Enum):
    AMOUNT_TOKEN = auto()
    FINAL = auto()


STATE = (
    GetTokenState.AMOUNT_TOKEN,
    GetTokenState.FINAL,
)

GET_TOKEN_MSG_STATES = {
    GetTokenState.AMOUNT_TOKEN: Message.GetToken.AMOUNT_TOKEN,
    GetTokenState.FINAL: Message.GetToken.FINAL,
}

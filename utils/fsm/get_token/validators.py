from config import Message, MAX_AMOUNT_TOKEN, ENUM_TYPE_TOKEN
from utils.fsm.validators_worker import ValidatorWorker
from utils.fsm.get_token.states import GetTokenState
from utils.exceptions import TokenException

vw = ValidatorWorker()


@vw.attach_validator(GetTokenState.AMOUNT_TOKEN)
def validator_amount_token(text: str):
    if not text.isnumeric():
        raise TokenException(Message.Error.AMOUNT_TOKEN)
    elif not 1 <= int(text) <= MAX_AMOUNT_TOKEN:
        raise TokenException(Message.Error.AMOUNT_TOKEN_MAX)


@vw.attach_validator(GetTokenState.TYPE_TOKEN)
def validator_type_token(text: str):
    if text.capitalize() not in ENUM_TYPE_TOKEN:
        raise TokenException(Message.Error.TYPE_TOKEN)


GET_TOKEN_VALIDATORS = vw.get_validators()

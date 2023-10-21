from config import Message, MAX_AMOUNT_TOKEN
from utils.fsm.validators_worker import ValidatorWorker
from utils.fsm.get_token.state import GetTokenState
from utils.exceptions import AmountTokenException

vw = ValidatorWorker()


@vw.save_validator(GetTokenState.AMOUNT_TOKEN)
def validator_amount_token(text: str):
    if not text.isnumeric():
        raise AmountTokenException(Message.Error.AMOUNT_TOKEN)
    elif not 1 <= int(text) <= MAX_AMOUNT_TOKEN:
        raise AmountTokenException(Message.Error.AMOUNT_TOKEN_MAX)


GET_TOKEN_VALIDATORS = vw.get_validators()

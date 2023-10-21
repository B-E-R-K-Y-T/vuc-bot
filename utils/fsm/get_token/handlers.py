from config import Message, MAX_AMOUNT_TOKEN
from utils.fsm.handlers_worker import HandlerWorker
from utils.fsm.get_token.state import GetTokenState
from utils.exceptions import AmountTokenException

hw = HandlerWorker()


@hw.save_handler(GetTokenState.AMOUNT_TOKEN)
def handler_amount_token(text: str):
    if not text.isnumeric():
        raise AmountTokenException(Message.Error.AMOUNT_TOKEN)
    elif not 1 <= int(text) <= MAX_AMOUNT_TOKEN:
        raise AmountTokenException(Message.Error.AMOUNT_TOKEN_MAX)


GET_TOKEN_HANDLERS = hw.get_handlers()

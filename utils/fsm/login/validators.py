from utils.fsm.validators_worker import ValidatorWorker
from utils.fsm.login.states import LoginState
from utils.server_worker.server_worker import ServerWorker
from utils.exceptions import TokenException
from config import Message

vw = ValidatorWorker()


@vw.attach_validator(LoginState.LOGIN)
def validator_login(text: str):
    max_len = ServerWorker().get_len_token()

    if len(text) != max_len:
        raise TokenException(f'{Message.Error.ERROR_LEN_TOKEN}{max_len}')
    elif text not in ServerWorker().get_free_tokens():
        raise TokenException(Message.Error.INVALID_TOKEN)


LOGIN_VALIDATORS = vw.get_validators()

from utils.fsm.validators_worker import ValidatorWorker
from utils.fsm.edit_squad_user.states import EditSquadUserState
from utils.exceptions import SquadException
from config import Message

vw = ValidatorWorker()


@vw.attach_validator(EditSquadUserState.EDIT)
def validator_login(text: str):
    if not text.isnumeric():
        raise SquadException(Message.Error.SQUAD)
    elif not 1 <= int(text) <= 3:
        raise SquadException(Message.Error.SQUAD)


EDIT_SQUAD_USER_VALIDATORS = vw.get_validators()

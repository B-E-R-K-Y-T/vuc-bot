from utils.fsm.validators_worker import ValidatorWorker
from utils.fsm.upload.states import UploadState
from utils.server_worker.server_worker import ServerWorker
from utils.exceptions import TokenException
from config import Message

vw = ValidatorWorker()


@vw.attach_validator(UploadState.UPLOAD_FILE)
def validator_login(text: str):
    return True


UPLOAD_VALIDATORS = vw.get_validators()

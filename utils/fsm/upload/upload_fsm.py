from utils.fsm.upload.states import STATE
from utils.fsm.base_fsm import BaseFiniteStateMachine


class FiniteStateMachineUpload(BaseFiniteStateMachine):
    def __init__(self, user):
        super().__init__(user, STATE)

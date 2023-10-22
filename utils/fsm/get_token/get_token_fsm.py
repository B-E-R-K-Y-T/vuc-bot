from utils.fsm.get_token.states import STATE
from utils.fsm.base_fsm import BaseFiniteStateMachine


class FiniteStateMachineGetToken(BaseFiniteStateMachine):
    def __init__(self, user):
        super().__init__(user, STATE)

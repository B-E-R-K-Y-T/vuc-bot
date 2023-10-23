from utils.fsm.login.states import STATE
from utils.fsm.base_fsm import BaseFiniteStateMachine


class FiniteStateMachineLogin(BaseFiniteStateMachine):
    def __init__(self, user):
        super().__init__(user, STATE)

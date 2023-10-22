from utils.fsm.registrarion.states import STATE
from utils.fsm.base_fsm import BaseFiniteStateMachine


class FiniteStateMachineRegistration(BaseFiniteStateMachine):
    def __init__(self, user):
        super().__init__(user, STATE)

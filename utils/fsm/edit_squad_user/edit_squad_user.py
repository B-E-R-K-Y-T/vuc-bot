from utils.fsm.edit_squad_user.states import STATE
from utils.fsm.base_fsm import BaseFiniteStateMachine


class FiniteStateMachineEditSquadUser(BaseFiniteStateMachine):
    def __init__(self, user):
        super().__init__(user, STATE)

from utils.fsm.get_token.states import STATE


class FiniteStateMachineGetToken:
    def __init__(self, user):
        self.user = user
        self.states = STATE
        self.iter_states = iter(self.states)

    def next_state(self):
        self.user.state = next(self.iter_states)

from utils.fsm.registrarion.state import RegistrationStates, STATE


class FiniteStateMachineRegistration:
    def __init__(self, user):
        self.user = user
        self.states = STATE
        self.iter_states = iter(self.states)

    def next_state(self):
        self.user.state = next(self.iter_states)


if __name__ == '__main__':
    s = RegistrationStates(1)

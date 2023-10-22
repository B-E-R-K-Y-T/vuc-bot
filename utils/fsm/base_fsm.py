class BaseFiniteStateMachine:
    def __init__(self, user, states):
        self.user = user
        self.states = states
        self.iter_states = iter(self.states)

    def next_state(self):
        self.user.state = next(self.iter_states)

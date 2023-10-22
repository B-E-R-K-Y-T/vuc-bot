class BaseFiniteStateMachine:
    def __init__(self, user, states):
        self.user = user
        self.states = states
        self.step = 0
        self.user.state = self.states[0]

    def next_state(self):
        self.step += 1
        self.user.state = self.states[self.step]

    def old_state(self):
        self.step -= 1

        if self.step > 0:
            self.user.state = self.states[self.step]
        else:
            self.user.state = self.states[0]


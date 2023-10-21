class ValidatorWorker:
    def __init__(self):
        self.validators = {}

    def save_validator(self, state):
        def decorator(handler: callable):
            self.validators[state] = handler

        return decorator

    def get_validators(self):
        return self.validators

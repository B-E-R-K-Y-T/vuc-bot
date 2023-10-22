class ValidatorWorker:
    def __init__(self):
        self.validators = {}

    def attach_validator(self, state):
        def decorator(validator: callable):
            self.validators[state] = validator

        return decorator

    def get_validators(self):
        return self.validators

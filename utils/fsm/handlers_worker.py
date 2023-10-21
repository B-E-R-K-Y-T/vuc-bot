class HandlerWorker:
    def __init__(self):
        self.handlers = {}

    def save_handler(self, state):
        def decorator(handler: callable):
            self.handlers[state] = handler

        return decorator

    def get_handlers(self):
        return self.handlers

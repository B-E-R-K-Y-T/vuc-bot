class FSMWorker:
    def __init__(self):
        self.fsm = {}

    def get_fsm_obj(self, telegram_id: int):
        return self.fsm.get(telegram_id)

    def set_fsm_obj(self, telegram_id, state):
        self.fsm[telegram_id] = state

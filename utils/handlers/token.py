class TokenHandler:
    def __init__(self):
        self.token_user: list = [..., ...]

    def set_amount(self, amount: int):
        self.token_user[0] = amount

    def set_role_to_token(self, role: str):
        self.token_user[1] = role

    def get_token_params(self):
        return self.token_user[0], self.token_user[1]

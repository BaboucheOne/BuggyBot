class RegisterStudentRequest:

    def __init__(self, ni: str, discord_id: int):
        self.ni = ni
        self.discord_id = discord_id

    def __repr__(self) -> str:
        return f"RegisterStudentRequest({self.ni}, {self.discord_id})"

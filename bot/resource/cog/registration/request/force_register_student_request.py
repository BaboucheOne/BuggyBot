class ForceRegisterStudentRequest:

    def __init__(self, ni: str, discord_id: int):
        self.ni = ni
        self.discord_id = discord_id

    def __repr__(self) -> str:
        return f"ForceRegisterStudentRequest({self.ni}, {self.discord_id})"

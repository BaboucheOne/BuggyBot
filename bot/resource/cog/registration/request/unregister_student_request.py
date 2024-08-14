class UnregisterStudentRequest:

    def __init__(self, discord_id: int):
        self.discord_id = discord_id

    def __repr__(self) -> str:
        return f"UnregisterStudentRequest({self.discord_id})"

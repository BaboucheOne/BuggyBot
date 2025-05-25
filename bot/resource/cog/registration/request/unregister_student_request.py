from bot.domain.student.attribut.discord_user_id import DiscordUserId


class UnregisterStudentRequest:

    def __init__(self, discord_id: DiscordUserId):
        self.discord_id = discord_id

    def __repr__(self) -> str:
        return f"UnregisterStudentRequest({self.discord_id})"

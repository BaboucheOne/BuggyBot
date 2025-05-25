from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.ni import NI


class ForceRegisterStudentRequest:

    def __init__(self, ni: NI, discord_id: DiscordUserId):
        self.ni = ni
        self.discord_id = discord_id

    def __repr__(self) -> str:
        return f"ForceRegisterStudentRequest({self.ni}, {self.discord_id})"

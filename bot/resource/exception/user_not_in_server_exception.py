from bot.domain.student.attribut.discord_user_id import DiscordUserId


class UserNotInServerException(RuntimeError):

    MESSAGE = "L'utilisateur %s n'est pas présent sur le serveur."

    def __init__(self, discord_id: DiscordUserId):
        super().__init__(self.MESSAGE % discord_id.value)

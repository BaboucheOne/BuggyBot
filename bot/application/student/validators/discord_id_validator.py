class DiscordIdValidator:

    OLD_DISCORD_ID_DIGITS_COUNT = 17
    DISCORD_ID_DIGITS_COUNT = 18

    def __init__(self):
        pass

    def validate(self, discord_id: int) -> bool:
        id_length = len(str(discord_id))
        return (
            id_length == self.OLD_DISCORD_ID_DIGITS_COUNT
            or id_length == self.DISCORD_ID_DIGITS_COUNT
        )

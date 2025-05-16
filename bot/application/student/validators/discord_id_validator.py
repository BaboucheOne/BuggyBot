class DiscordIdValidator:

    DISCORD_ID_DIGITS_COUNT = 18

    def __init__(self):
        pass

    def validate(self, discord_id: int) -> bool:
        return len(str(discord_id)) == self.DISCORD_ID_DIGITS_COUNT

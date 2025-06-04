from bot.application.student.exception.invalid_format_exception import (
    InvalidFormatException,
)


class InvalidDiscordIdFormatException(InvalidFormatException):
    MESSAGE = "%s ne correspond pas au format."

    def __init__(self, discord_id: int):
        super().__init__(self.MESSAGE % repr(discord_id))

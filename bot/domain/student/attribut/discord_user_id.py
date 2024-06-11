from dataclasses import dataclass


@dataclass
class DiscordUserId:

    INVALID_DISCORD_ID = -1

    value: int

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"DiscordUserId({str(self.value)})"

    def is_valid(self) -> bool:
        return self.value != self.INVALID_DISCORD_ID

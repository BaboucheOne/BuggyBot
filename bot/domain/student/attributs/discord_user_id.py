from dataclasses import dataclass


@dataclass
class DiscordUserId:

    INVALID_DISCORD_ID = -1

    value: int

    def is_valid(self) -> bool:
        return self.value != self.INVALID_DISCORD_ID

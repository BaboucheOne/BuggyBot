from dataclasses import dataclass


@dataclass
class DiscordUserId:
    value: int

    def is_valid(self) -> bool:
        return self.value != -1

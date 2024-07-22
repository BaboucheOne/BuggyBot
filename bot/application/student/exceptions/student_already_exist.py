from typing import Union, Optional

from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.ni import NI


class StudentAlreadyExistsException(RuntimeError):
    NI_UNION = Union[NI, int]
    DISCORD_USER_ID_UNION = Union[DiscordUserId, int]

    def __init__(
        self,
        ni: Optional[NI_UNION] = None,
        name: Optional[str] = None,
        discord_id: Optional[DISCORD_USER_ID_UNION] = None,
    ):
        self.ni = ni
        self.name = name
        self.discord_id = discord_id
        super().__init__(self.__generate_message())

    def __generate_message(self) -> str:
        if self.ni is not None:
            return f"L'etudiant {repr(self.ni)} existe deja."
        elif self.discord_id is not None:
            return f"L'etudiant {repr(self.discord_id)} existe deja."
        elif self.name is not None:
            return f"L'etudiant {repr(self.name)} existe deja."
        else:
            return "L'etudiant existe deja."

from typing import Union, Optional

from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.ni import NI


class StudentNotFoundException(RuntimeError):

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
            return f"L'étudiant {repr(self.ni)} n'existe pas."
        if self.discord_id is not None:
            return f"L'étudiant {repr(self.discord_id)} n'existe pas."
        if self.name is not None:
            return f"L'étudiant {repr(self.name)} n'existe pas."
        return "L'étudiant est déjà enregistré."

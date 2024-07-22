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
        for attribute in [self.ni, self.discord_id, self.name]:
            if attribute is not None:
                return f"L'étudiant {repr(attribute)} n'existe pas."
        return "L'étudiant n'existe pas."

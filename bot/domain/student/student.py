from dataclasses import dataclass

from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.firstname import Firstname
from bot.domain.student.attribut.lastname import Lastname
from bot.domain.student.attribut.new_admitted import NewAdmitted
from bot.domain.student.attribut.ni import NI
from bot.domain.student.attribut.program_code import ProgramCode


@dataclass
class Student:
    ni: NI
    firstname: Firstname
    lastname: Lastname
    program_code: ProgramCode
    new_admitted: NewAdmitted
    discord_user_id: DiscordUserId

    def is_registered(self) -> bool:
        return self.discord_user_id.is_valid()

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.ni == other.ni
        return False

    def __hash__(self):
        return hash(self.ni)

from dataclasses import dataclass
from typing import Dict

from bot.domain.student.attributs.discord_user_id import DiscordUserId
from bot.domain.student.attributs.firstname import Firstname
from bot.domain.student.attributs.lastname import Lastname
from bot.domain.student.attributs.new_admitted import NewAdmitted
from bot.domain.student.attributs.ni import NI
from bot.domain.student.attributs.program_code import ProgramCode


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

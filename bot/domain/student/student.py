from dataclasses import dataclass

from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.firstname import Firstname
from bot.domain.student.attribut.lastname import Lastname
from bot.domain.student.attribut.ni import NI
from bot.domain.student.attribut.program_code import ProgramCode


@dataclass
class Student:
    ni: NI
    firstname: Firstname
    lastname: Lastname
    program_code: ProgramCode
    discord_user_id: DiscordUserId

    def is_registered(self) -> bool:
        return self.discord_user_id.is_valid()

    def __str__(self):
        return (
            f"{self.ni}, {self.firstname}, {self.lastname}, {self.program_code}, "
            f"{self.discord_user_id}"
        )

    def __repr__(self):
        return (
            f"Student({self.ni}, {self.firstname}, {self.lastname}, {self.program_code}, "
            f"{self.discord_user_id})"
        )

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self.ni == other.ni

    def __hash__(self):
        return hash(self.ni)

from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.firstname import Firstname
from bot.domain.student.attribut.lastname import Lastname
from bot.domain.student.attribut.ni import NI
from bot.domain.student.attribut.program_code import ProgramCode
from bot.domain.student.student import Student


class StudentFactory:

    INVALID_DISCORD_USER_ID: int = -1

    def __init__(self):
        pass

    def create(
        self,
        ni: NI,
        firstname: Firstname,
        lastname: Lastname,
        program_code: ProgramCode,
    ) -> Student:
        discord_user_id = DiscordUserId(self.INVALID_DISCORD_USER_ID)

        return Student(
            ni=ni,
            firstname=firstname,
            lastname=lastname,
            program_code=program_code,
            discord_user_id=discord_user_id,
        )

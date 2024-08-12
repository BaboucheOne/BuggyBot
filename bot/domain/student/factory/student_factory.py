from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.firstname import Firstname
from bot.domain.student.attribut.lastname import Lastname
from bot.domain.student.attribut.program_code import ProgramCode
from bot.domain.student.factory.ni_factory import NIFactory
from bot.domain.student.student import Student


class StudentFactory:

    INVALID_DISCORD_USER_ID: int = -1

    def __init__(self, ni_factory: NIFactory):
        self.__ni_factory = ni_factory

    def create(
        self,
        ni: str,
        firstname: str,
        lastname: str,
        program_code: str,
    ) -> Student:
        ni = self.__ni_factory.create(ni)
        firstname = Firstname(firstname)
        lastname = Lastname(lastname)
        program_code = ProgramCode(program_code.upper())
        discord_user_id = DiscordUserId(self.INVALID_DISCORD_USER_ID)

        return Student(
            ni=ni,
            firstname=firstname,
            lastname=lastname,
            program_code=program_code,
            discord_user_id=discord_user_id,
        )

from bot.domain.student.attribut.firstname import Firstname
from bot.domain.student.attribut.lastname import Lastname
from bot.domain.student.attribut.ni import NI
from bot.domain.student.attribut.program_code import ProgramCode


class AddStudentRequest:

    def __init__(
        self,
        ni: NI,
        firstname: Firstname,
        lastname: Lastname,
        program_code: ProgramCode,
    ):
        self.ni = ni
        self.firstname = firstname
        self.lastname = lastname
        self.program_code = program_code

    def __repr__(self) -> str:
        return (
            f"AddStudentRequest({self.ni}, {self.firstname}, {self.lastname}, "
            f"{self.program_code})"
        )

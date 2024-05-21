from bot.application.discord.events.student_registered.student_registered_observable import (
    StudentRegisteredObservable,
)
from bot.application.student.exceptions.invalid_ni_format_exception import (
    InvalidNIFormatException,
)
from bot.application.student.exceptions.student_already_registered_exception import (
    StudentAlreadyRegisteredException,
)
from bot.application.student.validators.ni_validator import NIValidator
from bot.domain.constants import UniProgram
from bot.domain.student.attributs.discord_user_id import DiscordUserId
from bot.domain.student.attributs.firstname import Firstname
from bot.domain.student.attributs.lastname import Lastname
from bot.domain.student.attributs.new_admitted import NewAdmitted
from bot.domain.student.attributs.ni import NI
from bot.domain.student.attributs.program_code import ProgramCode
from bot.domain.student.ni_factory import NIFactory
from bot.domain.student.student import Student
from bot.domain.student.student_repository import StudentRepository
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)


class StudentService(StudentRegisteredObservable):

    def __init__(self, student_repository: StudentRepository):
        super().__init__()

        self.__student_repository = student_repository
        self.__ni_validator = NIValidator()
        self.__ni_factory = NIFactory()

    def __does_student_already_registered(self, ni: NI):
        try:
            return self.__student_repository.find_student_by_ni(ni).is_registered()
        except StudentNotFoundException:
            return False

    def str_to_bool(self, s: str):  # TODO : Put this in a utility.
        if s.lower() not in {"true", "1", "yes", "y", "oui", "o"}:
            return False
        return True

    def is_valid_program(self, program: str):  # TODO : Put this somewhere else.
        return program in {
            UniProgram.GLO,
            UniProgram.IFT,
            UniProgram.IIG,
            UniProgram.CERTIFICATE,
        }

    def add_student(
        self,
        request_ni: str,
        request_firstname: str,
        request_lastname: str,
        request_program: str,
        request_new_admitted: str,
    ):
        if not self.is_valid_program(request_program):
            raise Exception()

        ni = self.__ni_factory.create(request_ni)
        firstname = Firstname(request_firstname)
        lastname = Lastname(request_lastname)
        program_code = ProgramCode(request_program)
        new_admitted = NewAdmitted(self.str_to_bool(request_new_admitted))
        discord_user_id = DiscordUserId(-1)

        student = Student(
            ni=ni,
            firstname=firstname,
            lastname=lastname,
            program_code=program_code,
            new_admitted=new_admitted,
            discord_user_id=discord_user_id,
        )

        self.__student_repository.add_student(student)

    def register_student(self, request_ni: str, request_discord_user_id: int):
        if not self.__ni_validator.validate(request_ni):
            raise InvalidNIFormatException()

        student_ni = self.__ni_factory.create(request_ni)
        discord_user_id = DiscordUserId(request_discord_user_id)

        if self.__does_student_already_registered(student_ni):
            raise StudentAlreadyRegisteredException()
        self.__student_repository.register_student(student_ni, discord_user_id)

        self.notify_on_student_registered(student_ni)

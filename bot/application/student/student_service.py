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
from bot.cog.request.add_student_request import AddStudentRequest
from bot.cog.request.register_student_request import RegisterStudentRequest
from bot.domain.constants import UniProgram
from bot.domain.student.attributs.discord_user_id import DiscordUserId
from bot.domain.student.attributs.ni import NI
from bot.domain.student.ni_factory import NIFactory
from bot.domain.student.student_factory import StudentFactory
from bot.domain.student.student_repository import StudentRepository
from bot.domain.utility import Utility
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)


class StudentService(StudentRegisteredObservable):

    def __init__(self, student_repository: StudentRepository):
        super().__init__()

        self.__student_repository = student_repository
        self.__ni_validator = NIValidator()
        self.__ni_factory = NIFactory()
        self.__student_factory = StudentFactory(self.__ni_factory)

    def __does_student_already_registered(self, ni: NI):
        try:
            return self.__student_repository.find_student_by_ni(ni).is_registered()
        except StudentNotFoundException:
            return False

    def is_valid_program(self, program: str):  # TODO : Put this somewhere else.
        return program in {
            UniProgram.GLO,
            UniProgram.IFT,
            UniProgram.IIG,
            UniProgram.CERTIFICATE,
        }

    def add_student(self, add_student_request: AddStudentRequest):
        if not self.__ni_validator.validate(add_student_request.ni):
            raise InvalidNIFormatException()

        if not self.is_valid_program(add_student_request.program_code):
            raise Exception()

        new_admitted = Utility.str_to_bool(add_student_request.new_admitted)
        student = self.__student_factory.create(
            add_student_request.ni,
            add_student_request.firstname,
            add_student_request.lastname,
            add_student_request.program_code,
            new_admitted,
        )

        self.__student_repository.add_student(student)

    def register_student(self, register_student_request: RegisterStudentRequest):
        if not self.__ni_validator.validate(register_student_request.ni):
            raise InvalidNIFormatException()

        student_ni = self.__ni_factory.create(register_student_request.ni)
        discord_user_id = DiscordUserId(register_student_request.discord_id)

        if self.__does_student_already_registered(student_ni):
            raise StudentAlreadyRegisteredException()
        self.__student_repository.register_student(student_ni, discord_user_id)

        self.notify_on_student_registered(student_ni)

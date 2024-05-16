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
from bot.domain.student.attributs.discord_user_id import DiscordUserId
from bot.domain.student.attributs.ni import NI
from bot.domain.student.ni_factory import NIFactory
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

    def register_student(self, request_ni: str, request_discord_user_id: int):
        if not self.__ni_validator.validate(request_ni):
            raise InvalidNIFormatException()

        student_ni = self.__ni_factory.create(request_ni)
        discord_user_id = DiscordUserId(request_discord_user_id)

        if self.__does_student_already_registered(student_ni):
            raise StudentAlreadyRegisteredException()
        self.__student_repository.register_student(student_ni, discord_user_id)

        self.notify_on_student_registered(student_ni)

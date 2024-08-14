from typing import List

from discord import Member

from bot.application.discord.event.member_removed.member_removed_observable import (
    MemberRemovedObservable,
)
from bot.application.discord.event.student_registered.student_registered_observable import (
    StudentRegisteredObservable,
)
from bot.application.student.exceptions.invalid_discord_id_format_exception import (
    InvalidDiscordIdFormatException,
)
from bot.application.student.exceptions.invalid_name_format_exception import (
    InvalidNameFormatException,
)
from bot.application.student.exceptions.invalid_ni_format_exception import (
    InvalidNIFormatException,
)
from bot.application.student.exceptions.missing_program_code_exception import (
    MissingProgramCodeException,
)
from bot.application.student.exceptions.student_already_exist import (
    StudentAlreadyExistsException,
)
from bot.application.student.exceptions.student_already_registered_exception import (
    StudentAlreadyRegisteredException,
)
from bot.application.student.validators.discord_id_validator import DiscordIdValidator
from bot.application.student.validators.name_validator import NameValidator
from bot.application.student.validators.ni_validator import NIValidator
from bot.application.student.validators.program_code_validator import (
    ProgramCodeValidator,
)
from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.utility import Utility
from bot.resource.cog.registration.request.add_student_request import AddStudentRequest
from bot.resource.cog.registration.request.force_register_student_request import (
    ForceRegisterStudentRequest,
)
from bot.resource.cog.registration.request.register_student_request import (
    RegisterStudentRequest,
)
from bot.resource.cog.registration.request.force_unregister_student_request import (
    ForceUnregisterStudentRequest,
)
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.ni import NI
from bot.domain.student.factory.ni_factory import NIFactory
from bot.domain.student.factory.student_factory import StudentFactory
from bot.domain.student.student import Student
from bot.domain.student.student_repository import StudentRepository
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)
from bot.resource.cog.registration.request.unregister_student_request import (
    UnregisterStudentRequest,
)
from bot.resource.exception.user_not_in_server_exception import UserNotInServerException


class StudentService(StudentRegisteredObservable, MemberRemovedObservable):

    def __init__(self, student_repository: StudentRepository):
        super().__init__()

        self.__logger: Logger = ServiceLocator.get_dependency(Logger)
        self.__student_repository = student_repository

        self.__ni_validator = NIValidator()
        self.__name_validator = NameValidator()
        self.__discord_id_validator = DiscordIdValidator()
        self.__program_code_validator = ProgramCodeValidator()

        self.__ni_factory = NIFactory()
        self.__student_factory = StudentFactory(self.__ni_factory)

    def __does_student_registered(self, ni: NI) -> bool:
        try:
            return self.__student_repository.find_student_by_ni(ni).is_registered()
        except StudentNotFoundException:
            return False

    def __does_student_exists(self, ni: NI) -> bool:
        try:
            _ = self.__student_repository.find_student_by_ni(ni)
            return True
        except StudentNotFoundException:
            return False

    def __does_discord_user_id_already_registered_an_account(
        self, discord_user_id: DiscordUserId
    ) -> bool:
        students: List[Student] = (
            self.__student_repository.find_students_by_discord_user_id(discord_user_id)
        )
        return len(students) >= 1

    async def add_student(self, add_student_request: AddStudentRequest):
        self.__logger.info(
            f"Réception de la requête {repr(add_student_request)}", method="add_student"
        )

        if not self.__name_validator.validate(add_student_request.firstname):
            raise InvalidNameFormatException(add_student_request.firstname)

        if not self.__name_validator.validate(add_student_request.lastname):
            raise InvalidNameFormatException(add_student_request.lastname)

        if not self.__ni_validator.validate(add_student_request.ni):
            raise InvalidNIFormatException(add_student_request.ni)

        if not self.__program_code_validator.validate(add_student_request.program_code):
            raise MissingProgramCodeException(add_student_request.program_code)

        student = self.__student_factory.create(
            add_student_request.ni,
            add_student_request.firstname,
            add_student_request.lastname,
            add_student_request.program_code,
        )

        if self.__does_student_exists(student.ni) or self.__does_student_registered(
            student.ni
        ):
            raise StudentAlreadyExistsException(ni=student.ni)

        self.__student_repository.add_student(student)

    async def register_student(self, register_student_request: RegisterStudentRequest):
        self.__logger.info(
            f"Réception de la requête {repr(register_student_request)}",
            method="register_student",
        )

        if not self.__ni_validator.validate(register_student_request.ni):
            raise InvalidNIFormatException(register_student_request.ni)

        student_ni = self.__ni_factory.create(register_student_request.ni)
        discord_user_id = DiscordUserId(register_student_request.discord_id)

        if not self.__does_student_exists(student_ni):
            raise StudentNotFoundException()

        if self.__does_student_registered(
            student_ni
        ) or self.__does_discord_user_id_already_registered_an_account(discord_user_id):
            raise StudentAlreadyRegisteredException(ni=student_ni)

        self.__student_repository.register_student(student_ni, discord_user_id)
        await self.notify_on_student_registered(student_ni)

    async def force_register_student(
        self, force_register_student_request: ForceRegisterStudentRequest
    ):
        self.__logger.info(
            f"Réception de la requête {repr(force_register_student_request)}",
            method="force_register_student",
        )

        if not self.__ni_validator.validate(force_register_student_request.ni):
            raise InvalidNIFormatException(force_register_student_request.ni)

        if not self.__discord_id_validator.validate(
            force_register_student_request.discord_id
        ):
            raise InvalidDiscordIdFormatException(
                force_register_student_request.discord_id
            )

        if not Utility.does_user_exist_on_server(
            force_register_student_request.discord_id
        ):
            raise UserNotInServerException(force_register_student_request.discord_id)

        student_ni = self.__ni_factory.create(force_register_student_request.ni)
        discord_user_id = DiscordUserId(force_register_student_request.discord_id)

        if not self.__does_student_exists(student_ni):
            raise StudentNotFoundException()

        if self.__does_student_registered(
            student_ni
        ) or self.__does_discord_user_id_already_registered_an_account(discord_user_id):
            raise StudentAlreadyRegisteredException(ni=student_ni)

        self.__student_repository.register_student(student_ni, discord_user_id)
        await self.notify_on_student_registered(student_ni)

    async def unregister_student(
        self, unregister_student_request: UnregisterStudentRequest
    ):
        self.__logger.info(
            f"Réception de la requête {repr(unregister_student_request)}",
            method="unregister_student",
        )

        if not Utility.does_user_exist_on_server(unregister_student_request.discord_id):
            raise UserNotInServerException(unregister_student_request.discord_id)

        discord_user_id = DiscordUserId(unregister_student_request.discord_id)

        if not self.__does_discord_user_id_already_registered_an_account(
            discord_user_id
        ):
            raise StudentNotFoundException()

        student = self.__student_repository.find_student_by_discord_user_id(
            discord_user_id
        )

        self.__student_repository.unregister_student(
            student.ni, DiscordUserId(DiscordUserId.INVALID_DISCORD_ID)
        )
        await self.notify_on_student_unregistered(student.discord_user_id)

    async def force_unregister_student(
        self, force_unregister_student_request: ForceUnregisterStudentRequest
    ):
        self.__logger.info(
            f"Réception de la requête {repr(force_unregister_student_request)}",
            method="force_unregister_student",
        )

        if not self.__ni_validator.validate(force_unregister_student_request.ni):
            raise InvalidNIFormatException(force_unregister_student_request.ni)

        student_ni = self.__ni_factory.create(force_unregister_student_request.ni)

        student = self.__student_repository.find_student_by_ni(student_ni)

        self.__student_repository.unregister_student(
            student_ni, DiscordUserId(DiscordUserId.INVALID_DISCORD_ID)
        )
        await self.notify_on_student_unregistered(student.discord_user_id)

    async def remove_member(self, member: Member):
        student: Student = self.__student_repository.find_student_by_discord_user_id(
            DiscordUserId(member.id)
        )

        self.__student_repository.unregister_student(
            student.ni, DiscordUserId(DiscordUserId.INVALID_DISCORD_ID)
        )

        await self.notify_on_member_removed(member)

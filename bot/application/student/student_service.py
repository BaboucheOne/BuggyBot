from typing import List

from discord import Member

from bot.application.discord.event.member_removed.member_removed_observable import (
    MemberRemovedObservable,
)
from bot.application.discord.event.student_registered.student_registered_observable import (
    StudentRegisteredObservable,
)
from bot.application.student.exceptions.student_already_exist import (
    StudentAlreadyExistsException,
)
from bot.application.student.exceptions.student_already_registered_exception import (
    StudentAlreadyRegisteredException,
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

        self.__student_factory = StudentFactory()

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

        student = self.__student_factory.create(
            add_student_request.ni,
            add_student_request.firstname,
            add_student_request.lastname,
            add_student_request.program_code,
        )

        if self.__does_student_registered(student.ni):
            raise StudentAlreadyRegisteredException(ni=student.ni)

        if self.__does_student_exists(student.ni):
            raise StudentAlreadyExistsException(ni=student.ni)

        self.__student_repository.add_student(student)

    async def register_student(self, register_student_request: RegisterStudentRequest):
        self.__logger.info(
            f"Réception de la requête {repr(register_student_request)}",
            method="register_student",
        )

        if not self.__does_student_exists(register_student_request.ni):
            raise StudentNotFoundException()

        if self.__does_student_registered(
            register_student_request.ni
        ) or self.__does_discord_user_id_already_registered_an_account(
            register_student_request.discord_id
        ):
            raise StudentAlreadyRegisteredException(ni=register_student_request.ni)

        self.__student_repository.register_student(
            register_student_request.ni, register_student_request.discord_id
        )
        await self.notify_on_student_registered(register_student_request.ni)

    async def force_register_student(
        self, force_register_student_request: ForceRegisterStudentRequest
    ):
        self.__logger.info(
            f"Réception de la requête {repr(force_register_student_request)}",
            method="force_register_student",
        )

        if not Utility.does_user_exist_on_server(
            force_register_student_request.discord_id.value
        ):
            raise UserNotInServerException(force_register_student_request.discord_id)

        if not self.__does_student_exists(force_register_student_request.ni):
            raise StudentNotFoundException()

        if self.__does_student_registered(
            force_register_student_request.ni
        ) or self.__does_discord_user_id_already_registered_an_account(
            force_register_student_request.discord_id
        ):
            raise StudentAlreadyRegisteredException(
                ni=force_register_student_request.ni
            )

        self.__student_repository.register_student(
            force_register_student_request.ni, force_register_student_request.discord_id
        )
        await self.notify_on_student_registered(force_register_student_request.ni)

    async def unregister_student(
        self, unregister_student_request: UnregisterStudentRequest
    ):
        self.__logger.info(
            f"Réception de la requête {repr(unregister_student_request)}",
            method="unregister_student",
        )

        if not self.__does_discord_user_id_already_registered_an_account(
            unregister_student_request.discord_id
        ):
            raise StudentNotFoundException()

        student = self.__student_repository.find_student_by_discord_user_id(
            unregister_student_request.discord_id
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

        student = self.__student_repository.find_student_by_ni(
            force_unregister_student_request.ni
        )

        self.__student_repository.unregister_student(
            force_unregister_student_request.ni,
            DiscordUserId(DiscordUserId.INVALID_DISCORD_ID),
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

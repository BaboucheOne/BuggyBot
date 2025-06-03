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
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.student.attribut.firstname import Firstname
from bot.domain.student.attribut.lastname import Lastname
from bot.domain.student.attribut.program_code import ProgramCode
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.ni import NI
from bot.domain.student.factory.student_factory import StudentFactory
from bot.domain.student.student import Student
from bot.domain.student.student_repository import StudentRepository
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)
from bot.resource.exception.user_not_in_server_exception import UserNotInServerException


class StudentService(StudentRegisteredObservable, MemberRemovedObservable):

    def __init__(self, student_repository: StudentRepository):
        super().__init__()

        self.__logger: Logger = ServiceLocator.get_dependency(Logger)
        self.__discord_client: DiscordClient = ServiceLocator.get_dependency(
            DiscordClient
        )

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

    async def add_student(
        self,
        ni: NI,
        firstname: Firstname,
        lastname: Lastname,
        program_code: ProgramCode,
    ):
        student = self.__student_factory.create(
            ni,
            firstname,
            lastname,
            program_code,
        )

        if self.__does_student_registered(student.ni):
            raise StudentAlreadyRegisteredException(ni=student.ni)

        if self.__does_student_exists(student.ni):
            raise StudentAlreadyExistsException(ni=student.ni)

        self.__student_repository.add_student(student)

    async def register_student(self, ni: NI, discord_id: DiscordUserId):
        if not self.__does_student_exists(ni):
            raise StudentNotFoundException()

        if self.__does_student_registered(
            ni
        ) or self.__does_discord_user_id_already_registered_an_account(discord_id):
            raise StudentAlreadyRegisteredException(ni=ni)

        self.__student_repository.register_student(ni, discord_id)
        await self.notify_on_student_registered(ni)

    async def force_register_student(self, ni: NI, discord_id: DiscordUserId):
        if not self.__discord_client.does_user_exists(discord_id):
            raise UserNotInServerException(discord_id)

        if not self.__does_student_exists(ni):
            raise StudentNotFoundException()

        if self.__does_student_registered(
            ni
        ) or self.__does_discord_user_id_already_registered_an_account(discord_id):
            raise StudentAlreadyRegisteredException(ni=ni)

        self.__student_repository.register_student(ni, discord_id)
        await self.notify_on_student_registered(ni)

    async def unregister_student(self, discord_id: DiscordUserId):
        if not self.__does_discord_user_id_already_registered_an_account(discord_id):
            raise StudentNotFoundException()

        student = self.__student_repository.find_student_by_discord_user_id(discord_id)

        self.__student_repository.unregister_student(
            student.ni, DiscordUserId(DiscordUserId.INVALID_DISCORD_ID)
        )

        await self.notify_on_student_unregistered(student.discord_user_id)

    async def force_unregister_student(self, ni: NI):

        student = self.__student_repository.find_student_by_ni(ni)

        self.__student_repository.unregister_student(
            ni,
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

import asyncio
from typing import List

import discord
from discord import Role, Member

from bot.application.discord.event.member_removed.member_removed_observer import (
    MemberRemovedObserver,
)
from bot.application.discord.event.student_registered.student_registered_observer import (
    StudentRegisteredObserver,
)
from bot.application.discord.exception.role_not_found_exception import (
    RoleNotFoundException,
)
from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.resource.constants import ReplyMessage
from bot.domain.constants import UniProgram, DiscordRole
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.ni import NI
from bot.domain.student.student_repository import StudentRepository


class DiscordService(StudentRegisteredObserver, MemberRemovedObserver):

    MAX_NICKNAME_LENGTH = 32

    def __init__(
        self, discord_client: DiscordClient, student_repository: StudentRepository
    ):
        self.__discord_client = discord_client
        self.__student_repository = student_repository

        self.__role_mapping = {
            UniProgram.GLO: DiscordRole.GLO,
            UniProgram.IFT: DiscordRole.IFT,
            UniProgram.IIG: DiscordRole.IIG,
            UniProgram.CERTIFICATE: DiscordRole.CERTIFICATE,
            UniProgram.HONORIFIQUE: DiscordRole.HONORIFIQUE,
        }

        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    def __get_role_name(self, program_name: str) -> str:
        if program_name in self.__role_mapping:
            return self.__role_mapping[program_name]

        self.__logger.error(
            f"__get_role_name - Le programme {program_name} n'a pas d'équivalent pour un rôle Discord. "
            f"Il sera donc impossible d'ajouter le rôle à la personne."
        )
        raise RoleNotFoundException(program_name)

    def __get_uni_roles(self, member: Member) -> List[Role]:
        role_names = {
            DiscordRole.IFT,
            DiscordRole.GLO,
            DiscordRole.IIG,
            DiscordRole.CERTIFICATE,
        }
        return list(filter(lambda role: role.name in role_names, member.roles))

    def __get_name(self, student_firstname: str, student_lastname: str) -> str:
        student_name = f"{student_firstname} {student_lastname}"

        if len(student_name) > self.MAX_NICKNAME_LENGTH:
            student_name = f"{student_firstname} {student_lastname[0]}."
            self.__logger.info(
                f"__get_name - L'étudiant {student_firstname} {student_lastname} "
                f"a un nom plus long que {self.MAX_NICKNAME_LENGTH} caractères. "
                f"Il a donc été renommé en {student_name}"
            )

        return student_name

    def on_student_registered(self, ni: NI):
        student = self.__student_repository.find_student_by_ni(ni)
        member = self.__discord_client.server.get_member(student.discord_user_id.value)
        role_name = self.__get_role_name(student.program_code.value)

        role = discord.utils.get(self.__discord_client.server.roles, name=role_name)
        asyncio.ensure_future(member.add_roles(role))

        if member != self.__discord_client.server.owner:
            student_name = self.__get_name(
                student.firstname.value, student.lastname.value
            )
            asyncio.ensure_future(member.edit(nick=student_name))

    def on_student_unregistered(self, discord_user_id: DiscordUserId):
        member = self.__discord_client.server.get_member(discord_user_id.value)

        uni_roles = self.__get_uni_roles(member)
        asyncio.ensure_future(member.remove_roles(*uni_roles))

        asyncio.ensure_future(member.send(ReplyMessage.NOTIFY_UNREGISTER))

    def on_member_removed(self, member: Member):
        uni_roles = self.__get_uni_roles(member)
        asyncio.ensure_future(member.remove_roles(*uni_roles))

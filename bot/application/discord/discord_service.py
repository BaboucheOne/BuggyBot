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
    DEFAULT_NICKNAME = None

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
        raise RoleNotFoundException(program_name)

    def __get_member_uni_roles(self, member: Member) -> List[Role]:
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
                f"L'étudiant {student_firstname} {student_lastname} "
                f"a un nom plus long que {self.MAX_NICKNAME_LENGTH} caractères. "
                f"Il a donc été renommé en {student_name}",
                method="__get_name",
            )

        return student_name

    async def on_student_registered(self, ni: NI):
        student = self.__student_repository.find_student_by_ni(ni)
        member = self.__discord_client.server.get_member(student.discord_user_id.value)
        role_name = self.__get_role_name(student.program_code.value)

        role = discord.utils.get(self.__discord_client.server.roles, name=role_name)
        await self.__add_member_roles(member, role)

        if member != self.__discord_client.server.owner:
            student_name = self.__get_name(
                student.firstname.value, student.lastname.value
            )
            await self.__set_member_nickname(member, student_name)

    async def on_student_unregistered(self, discord_user_id: DiscordUserId):
        member = self.__discord_client.server.get_member(discord_user_id.value)

        if member:
            uni_roles = self.__get_member_uni_roles(member)
            await self.__remove_member_roles(member, uni_roles)
            await self.__set_member_nickname(member, self.DEFAULT_NICKNAME)
        else:
            member = self.__discord_client.get_user(discord_user_id.value)

        await member.send(ReplyMessage.NOTIFY_UNREGISTER)

    async def on_member_removed(self, member: Member):
        uni_roles = self.__get_member_uni_roles(member)
        await self.__remove_member_roles(member, uni_roles)

    async def __set_member_nickname(self, member: Member, nickname: str or None):
        try:
            await member.edit(nick=nickname)
        except (discord.Forbidden, discord.HTTPException) as e:
            self.__logger.error(
                f"Impossible d'ajouter le surnom {nickname} à {member.name}, {member.id} dû à {e}",
                method="__set_member_nick_name",
                exception=e,
            )

    async def __remove_member_roles(self, member: Member, roles: List[Role]):
        try:
            await member.remove_roles(*roles)
        except (discord.Forbidden, discord.HTTPException) as e:
            self.__logger.error(
                f"Impossible d'enlever les roles {roles} à {member.name}, {member.id} dû à {e}",
                method="__remove_member_roles",
                exception=e,
            )

    async def __add_member_roles(self, member: Member, role):
        try:
            await member.add_roles(role)
        except (discord.Forbidden, discord.HTTPException) as e:
            self.__logger.error(
                f"Impossible d'ajouter le role {role} à {member.name}, {member.id} dû à {e}",
                method="__add_member_roles",
                exception=e,
            )

import asyncio

import discord

from bot.application.discord.events.student_registered.student_registered_observer import (
    StudentRegisteredObserver,
)
from bot.application.discord.exception.role_not_found_exception import (
    RoleNotFoundException,
)
from bot.domain.constants import UniProgram, DiscordRole
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.student.attributs.ni import NI
from bot.domain.student.student_repository import StudentRepository


class DiscordService(StudentRegisteredObserver):

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
        }

    def __get_role_name(self, student_role) -> str:
        if student_role in self.__role_mapping:
            return self.__role_mapping[student_role]
        raise RoleNotFoundException(student_role)

    def __get_name(self, student_firstname, student_lastname) -> str:

        student_name = f"{student_firstname} {student_lastname}"

        if len(student_name) > self.MAX_NICKNAME_LENGTH:
            student_name = f"{student_firstname} {student_lastname[0]}."

        return student_name

    def on_student_registered(self, ni: NI):
        student = self.__student_repository.find_student_by_ni(ni)
        member = self.__discord_client.server.get_member(student.discord_user_id.value)
        role_name = self.__get_role_name(student.program_code.value)

        if member != self.__discord_client.server.owner:
            role = discord.utils.get(self.__discord_client.server.roles, name=role_name)
            asyncio.ensure_future(member.add_roles(role))

        student_name = self.__get_name(student.firstname.value, student.lastname.value)
        asyncio.ensure_future(member.edit(nick=student_name))

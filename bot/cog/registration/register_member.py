from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

from bot.application.student.exceptions.student_already_exist import (
    StudentAlreadyExistsException,
)
from bot.application.student.student_service import (
    StudentService,
    StudentAlreadyRegisteredException,
)
from bot.cog.chain_of_responsibility.handlers.keep_digits_handler import (
    KeepDigitsHandler,
)
from bot.cog.chain_of_responsibility.handlers.strip_handler import StripHandler
from bot.cog.chain_of_responsibility.responsibility_builder import ResponsibilityBuilder
from bot.cog.constants import ReplyMessage
from bot.cog.decorators.role_check import role_check
from bot.cog.exceptions.missing_arguments_exception import MissingArgumentsException
from bot.cog.registration.factory.add_student_request_factory import (
    AddStudentRequestFactory,
)
from bot.cog.registration.factory.register_student_request_factory import (
    RegisterStudentRequestFactory,
)
from bot.cog.registration.factory.unregister_student_request_factory import (
    UnregisterStudentRequestFactory,
)
from bot.config.service_locator import ServiceLocator
from bot.domain.constants import DiscordRole
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.utility import Utility


class RegisterMemberCog(commands.Cog):

    def __init__(self):
        self.__bot = ServiceLocator.get_dependency(DiscordClient)
        self.__student_service: StudentService = ServiceLocator.get_dependency(
            StudentService
        )
        self.__ni_sanitizer = (
            ResponsibilityBuilder()
            .with_handler(StripHandler())
            .with_handler(KeepDigitsHandler())
            .build()
        )

        self.__add_student_request_factory = AddStudentRequestFactory(
            self.__ni_sanitizer
        )

        self.__register_student_request_factory = RegisterStudentRequestFactory(
            self.__ni_sanitizer
        )

        self.__unregister_student_request_factory = UnregisterStudentRequestFactory(
            self.__ni_sanitizer
        )

    def __is_self(self, message: Message) -> bool:
        return message.author == self.__bot.user

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(ReplyMessage.WELCOME)

    @commands.command(name="add_student")
    @commands.dm_only()
    @role_check(DiscordRole.ASETIN, DiscordRole.ADMIN)
    async def add_student(self, context: Context):
        message = context.message
        if self.__is_self(message):
            return

        try:
            content = Utility.get_content_without_command(message.content)
            add_student_request = self.__add_student_request_factory.create(content)

            self.__student_service.add_student(add_student_request)

            await message.channel.send(ReplyMessage.SUCCESSFUL_STUDENT_ADDED)
        except StudentAlreadyExistsException:
            await message.channel.send(ReplyMessage.STUDENT_ALREADY_EXISTS)
        except MissingArgumentsException:
            await message.channel.send(ReplyMessage.MISSING_ARGUMENTS_IN_COMMAND)
        except Exception as e:
            print(f"Exception occur {e}")

    @commands.command(name="register")
    @commands.dm_only()
    async def register(self, context: Context):
        message = context.message
        if self.__is_self(message):
            return

        try:
            content = Utility.get_content_without_command(message.content)
            register_student_request = self.__register_student_request_factory.create(
                content, message.author.id
            )

            self.__student_service.register_student(register_student_request)

            await message.channel.send(ReplyMessage.SUCCESSFUL_REGISTRATION)
        except StudentAlreadyRegisteredException:
            await message.channel.send(ReplyMessage.ALREADY_REGISTERED)
        except Exception:
            await message.channel.send(ReplyMessage.UNABLE_TO_REGISTER)

    @commands.command(name="unregister")
    @commands.dm_only()
    @role_check(DiscordRole.ASETIN, DiscordRole.ADMIN)
    async def unregister(self, context: Context):
        message = context.message
        if self.__is_self(message):
            return

        try:
            content = Utility.get_content_without_command(message.content)
            unregister_student_request = (
                self.__unregister_student_request_factory.create(content)
            )
        except Exception as e:
            print(f"Exception occur {e}")

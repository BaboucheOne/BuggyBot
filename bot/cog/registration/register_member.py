import logging

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
from bot.cog.decorator.role_check import role_check
from bot.cog.exception.missing_arguments_exception import MissingArgumentsException
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

logger = logging.getLogger(__name__)


class RegisterMemberCog(commands.Cog, name="Registration"):

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

    @commands.command(
        name="add_student",
        help="Arguments needed in order:\n !add_student ni firstname lastname program_code new_admitted",
        brief="Add a user to the student list. ONLY ADMIN",
    )
    @commands.dm_only()
    @role_check(DiscordRole.ASETIN, DiscordRole.ADMIN)
    async def add_student(self, context: Context):
        logging.info(f"Executing ADD_STUDENT command by {context.message.author}")

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
            logging.error(f"Error while executing ADD_STUDENT command {e}")
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

    @commands.command(
        name="register",
        help="Required your NI. Example !register 123456789",
        brief="Register you to access the discord.",
    )
    @commands.dm_only()
    async def register(self, context: Context):
        logging.info(f"Executing REGISTER command by {context.message.author}")

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
        except Exception as e:
            logging.error(f"Error while executing REGISTER command {e}")
            await message.channel.send(ReplyMessage.UNABLE_TO_REGISTER)

    @commands.command(
        name="unregister",
        help="Arguments needed in order:\n !unregister ni",
        brief="Delete a user from the student list. ONLY ADMIN",
    )
    @commands.dm_only()
    @role_check(DiscordRole.ASETIN, DiscordRole.ADMIN)
    async def unregister(self, context: Context):
        logging.info(f"Executing UNREGISTER command by {context.message.author}")

        message = context.message
        if self.__is_self(message):
            return

        try:
            content = Utility.get_content_without_command(message.content)
            unregister_student_request = (
                self.__unregister_student_request_factory.create(content)
            )

            self.__student_service.unregister_student(unregister_student_request)
            await message.channel.send(ReplyMessage.SUCCESSFUL_UNREGISTER)
        except Exception as e:
            logging.error(f"Error while executing UNREGISTER command {e}")
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

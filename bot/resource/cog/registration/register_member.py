from discord import Message, Member
from discord.ext import commands
from discord.ext.commands import Context

from bot.application.student.exceptions.student_already_exist import (
    StudentAlreadyExistsException,
)
from bot.application.student.student_service import (
    StudentService,
    StudentAlreadyRegisteredException,
)
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)
from bot.resource.chain_of_responsibility.handlers.keep_digits_handler import (
    KeepDigitsHandler,
)
from bot.resource.chain_of_responsibility.handlers.strip_handler import StripHandler
from bot.resource.chain_of_responsibility.responsibility_builder import (
    ResponsibilityBuilder,
)
from bot.resource.constants import ReplyMessage
from bot.resource.decorator.role_check import role_check
from bot.resource.exception.missing_arguments_exception import MissingArgumentsException
from bot.resource.cog.registration.factory.add_student_request_factory import (
    AddStudentRequestFactory,
)
from bot.resource.cog.registration.factory.register_student_request_factory import (
    RegisterStudentRequestFactory,
)
from bot.resource.cog.registration.factory.unregister_student_request_factory import (
    UnregisterStudentRequestFactory,
)
from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.constants import DiscordRole
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.utility import Utility


class RegisterMemberCog(commands.Cog, name="Registration"):

    def __init__(self):
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)
        self.__bot: DiscordClient = ServiceLocator.get_dependency(DiscordClient)
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
    async def on_member_join(self, member: Member):
        await member.create_dm()
        await member.dm_channel.send(ReplyMessage.WELCOME)
        self.__logger.info(
            f"New user named {member.name} with id {member.id} has been messaged."
        )

    @commands.Cog.listener()
    async def on_member_removed(self, member: Member):
        try:
            self.__student_service.remove_member(member)
            self.__logger.info(f"Executing ON_MEMBER_REMOVED command on {member.name}")
        except StudentNotFoundException:
            self.__logger.error(
                f"on_member_removed - {member.name} was not a registered student."
            )
        except Exception as e:
            self.__logger.error(f"Error while executing on_member_removed command {e}")

    @commands.command(
        name="add_student",
        help="Arguments nécessaires dans l'ordre: !add_student ni prénom nom code_programme nouvel_admis",
        brief="Ajouter un utilisateur à la liste des étudiants. Admin SEULEMENT",
    )
    @commands.dm_only()
    @role_check(DiscordRole.ASETIN, DiscordRole.ADMIN)
    async def add_student(self, context: Context):
        self.__logger.info(f"Executing ADD_STUDENT command by {context.message.author}")

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
            self.__logger.error(f"Error while executing ADD_STUDENT command {e}")
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

    @commands.command(
        name="register",
        help="Votre NI est requis. Exemple : !register 123456789",
        brief="Enregistrez-vous pour accéder au Discord.",
    )
    @commands.dm_only()
    async def register(self, context: Context):
        self.__logger.info(f"Executing REGISTER command by {context.message.author}")

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
            self.__logger.error(f"Error while executing REGISTER command {e}")
            await message.channel.send(ReplyMessage.UNABLE_TO_REGISTER)

    @commands.command(
        name="unregister",
        help="Arguments nécessaires dans l'ordre: !unregister ni",
        brief="Supprimer un utilisateur de la liste des étudiants. Admin SEULEMENT",
    )
    @commands.dm_only()
    @role_check(DiscordRole.ASETIN, DiscordRole.ADMIN)
    async def unregister(self, context: Context):
        self.__logger.info(f"Executing UNREGISTER command by {context.message.author}")

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
            self.__logger.error(f"Error while executing UNREGISTER command {e}")
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

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
            f"Un nouveau utilisateur nommé {member.name} avec l'identifiant {member.id} a reçu le message de bienvenue.",
            method="on_member_join",
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        try:
            self.__logger.info(
                f"Exécution de la commande par {member.name}.",
                method="on_member_remove",
            )
            self.__student_service.remove_member(member)
            self.__logger.info(
                "La commande a été exécutée avec succès.", method="on_member_remove"
            )
        except StudentNotFoundException as e:
            self.__logger.error(f"{e}", method="on_member_removed", exception=e)
        except Exception as e:
            self.__logger.error(
                f"Erreur lors de l'exécution de la commande exécutée par {member.name} : {e}",
                method="on_member_remove",
                exception=e,
            )

    @commands.command(
        name="add_student",
        help="Arguments nécessaires dans l'ordre: !add_student ni, prénom, nom, code_programme, nouvel_admis",
        brief="Ajouter un utilisateur à la liste des étudiants. Admin SEULEMENT",
    )
    @commands.dm_only()
    @role_check(DiscordRole.ASETIN, DiscordRole.ADMIN)
    async def add_student(self, context: Context):
        self.__logger.info(
            f"Exécution de la commande par {context.message.author}",
            method="add_student",
        )

        message = context.message
        if self.__is_self(message):
            return

        try:
            content = Utility.get_content_without_command(message.content)
            add_student_request = self.__add_student_request_factory.create(content)

            self.__student_service.add_student(add_student_request)

            await message.channel.send(ReplyMessage.SUCCESSFUL_STUDENT_ADDED)

            self.__logger.info(
                "La commande a été exécutée avec succès.", method="add_student"
            )
        except StudentAlreadyExistsException as e:
            self.__logger.error(f"{e}", method="add_student", exception=e)
            await message.channel.send(ReplyMessage.STUDENT_ALREADY_EXISTS)
        except MissingArgumentsException:
            await message.channel.send(ReplyMessage.MISSING_ARGUMENTS_IN_COMMAND)
        except Exception as e:
            self.__logger.error(
                f"Erreur lors de l'exécution de la commande exécutée par {context.message.author}. {e}",
                method="add_student",
                exception=e,
            )
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

    @commands.command(
        name="register",
        help="Votre NI est requis. Exemple : !register 123456789",
        brief="Enregistrez-vous pour accéder au Discord.",
    )
    @commands.dm_only()
    async def register(self, context: Context):
        self.__logger.info(
            f"Exécution de la commande par {context.message.author}", method="register"
        )

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

            self.__logger.info(
                "La commande a été exécutée avec succès.", method="register"
            )
        except StudentAlreadyRegisteredException as e:
            self.__logger.error(f"{e}", method="register", exception=e)
            await message.channel.send(ReplyMessage.ALREADY_REGISTERED)
        except Exception as e:
            self.__logger.error(
                f"Erreur lors de l'exécution de la commande exécutée par {context.message.author}. {e}",
                method="register",
                exception=e,
            )
            await message.channel.send(ReplyMessage.UNABLE_TO_REGISTER)

    @commands.command(
        name="unregister",
        help="Arguments nécessaires dans l'ordre: !unregister ni",
        brief="Supprimer un utilisateur de la liste des étudiants. Admin SEULEMENT",
    )
    @commands.dm_only()
    @role_check(DiscordRole.ASETIN, DiscordRole.ADMIN)
    async def unregister(self, context: Context):
        self.__logger.info(
            f"Exécution de la commande par {context.message.author}",
            method="unregister",
        )

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

            self.__logger.info(
                "La commande a été exécutée avec succès.", method="unregister"
            )
        except Exception as e:
            self.__logger.error(
                f"Erreur lors de l'exécution de la commande exécutée par {context.message.author}. {e}",
                method="unregister",
                exception=e,
            )
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

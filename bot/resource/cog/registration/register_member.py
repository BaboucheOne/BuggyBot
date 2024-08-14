from discord import Message, Member
from discord.ext import commands
from discord.ext.commands import Context

from bot.application.student.student_service import (
    StudentService,
)
from bot.resource.chain_of_responsibility.handlers.keep_digits_handler import (
    KeepDigitsHandler,
)
from bot.resource.chain_of_responsibility.handlers.strip_handler import StripHandler
from bot.resource.chain_of_responsibility.responsibility_builder import (
    ResponsibilityBuilder,
)
from bot.resource.cog.registration.factory.force_register_student_request_factory import (
    ForceRegisterStudentRequestFactory,
)
from bot.resource.constants import ReplyMessage
from bot.resource.decorator.prohibit_self_message import prohibit_self_message
from bot.resource.decorator.role_check import role_check
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
from bot.resource.decorator.user_in_server import user_in_server


class RegisterMemberCog(commands.Cog, name="Registration"):

    def __init__(self):
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)
        self.__discord_client: DiscordClient = ServiceLocator.get_dependency(
            DiscordClient
        )
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

        self.__force_register_student_request_factory = (
            ForceRegisterStudentRequestFactory(self.__ni_sanitizer)
        )

        self.__unregister_student_request_factory = UnregisterStudentRequestFactory(
            self.__ni_sanitizer
        )

    def __does_user_exist_on_server(self, discord_id: int) -> bool:
        return self.__discord_client.get_user(discord_id) is not None

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
        self.__logger.info(
            f"Exécution de la commande par {member.name}.",
            method="on_member_remove",
        )
        await self.__student_service.remove_member(member)
        self.__logger.info(
            "La commande a été exécutée avec succès.", method="on_member_remove"
        )

    @commands.command(
        name="add_student",
        help="Arguments nécessaires dans l'ordre: !add_student ni, prénom, nom, code_programme.",
        brief="Ajouter un utilisateur à la liste des étudiants. Admin SEULEMENT",
    )
    @commands.dm_only()
    @prohibit_self_message()
    @role_check(DiscordRole.ASETIN, DiscordRole.ADMIN)
    async def add_student(self, context: Context):
        self.__logger.info(
            f"Exécution de la commande par {context.message.author}",
            method="add_student",
        )

        message: Message = context.message

        content = Utility.get_content_without_command(message.content)
        add_student_request = self.__add_student_request_factory.create(content)

        await self.__student_service.add_student(add_student_request)

        await message.channel.send(ReplyMessage.SUCCESSFUL_STUDENT_ADDED)

        self.__logger.info(
            "La commande a été exécutée avec succès.", method="add_student"
        )

    @commands.command(
        name="register",
        help="Votre NI est requis. Exemple : !register 123456789",
        brief="Enregistrez-vous pour accéder au Discord.",
    )
    @commands.dm_only()
    @user_in_server()
    @prohibit_self_message()
    async def register(self, context: Context):
        self.__logger.info(
            f"Exécution de la commande par {context.message.author}", method="register"
        )

        message = context.message

        content = Utility.get_content_without_command(message.content)
        register_student_request = self.__register_student_request_factory.create(
            content, message.author.id
        )

        await self.__student_service.register_student(register_student_request)

        await message.channel.send(ReplyMessage.SUCCESSFUL_REGISTRATION)

        self.__logger.info("La commande a été exécutée avec succès.", method="register")

    @commands.command(
        name="force_register",
        help="Votre NI est requis. Exemple : !force_register 123456789, 3545356457645",
        brief="Forcer l'enregistrez d'un etudiant pour accéder au Discord.",
    )
    @commands.dm_only()
    @role_check(DiscordRole.ASETIN, DiscordRole.ADMIN)
    @prohibit_self_message()
    async def force_register(self, context: Context):
        self.__logger.info(
            f"Exécution de la commande par {context.message.author}",
            method="force_register",
        )

        message = context.message

        content = Utility.get_content_without_command(message.content)
        force_register_student_request = (
            self.__force_register_student_request_factory.create(content)
        )

        await self.__student_service.force_register_student(
            force_register_student_request
        )

        await message.channel.send(ReplyMessage.SUCCESSFUL_FORCE_REGISTRATION)

        member_to_notify = self.__discord_client.get_user(
            force_register_student_request.discord_id
        )
        await member_to_notify.send(ReplyMessage.SUCCESSFUL_REGISTRATION)

        self.__logger.info(
            "La commande a été exécutée avec succès.", method="force_register"
        )

    @commands.command(
        name="unregister",
        help="Arguments nécessaires dans l'ordre: !unregister ni",
        brief="Supprimer un utilisateur de la liste des étudiants. Admin SEULEMENT",
    )
    @commands.dm_only()
    @prohibit_self_message()
    @role_check(DiscordRole.ASETIN, DiscordRole.ADMIN)
    async def unregister(self, context: Context):
        self.__logger.info(
            f"Exécution de la commande par {context.message.author}",
            method="unregister",
        )

        message = context.message

        content = Utility.get_content_without_command(message.content)
        unregister_student_request = self.__unregister_student_request_factory.create(
            content
        )

        await self.__student_service.unregister_student(unregister_student_request)
        await message.channel.send(ReplyMessage.SUCCESSFUL_UNREGISTER)

        self.__logger.info(
            "La commande a été exécutée avec succès.", method="unregister"
        )

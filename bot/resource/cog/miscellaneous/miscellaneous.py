from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

from bot.application.miscellaneous.miscellaneous_service import MiscellaneousService
from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.constants import DiscordRole
from bot.domain.discord_client.discord_client import DiscordClient
from bot.resource.decorator.prohibit_self_message import prohibit_self_message
from bot.resource.decorator.role_check import role_check


class MiscellaneousCog(commands.Cog, name="Miscellaneous"):
    def __init__(self):
        self.__bot = ServiceLocator.get_dependency(DiscordClient)
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)
        self.__miscellaneous_service: MiscellaneousService = (
            ServiceLocator.get_dependency(MiscellaneousService)
        )

    @commands.command(
        name="dashboard",
        help="!dashboard",
        brief="Retourne le lien du dashboard.",
    )
    @commands.dm_only()
    @prohibit_self_message()
    @role_check(DiscordRole.ASETIN, DiscordRole.ADMIN)
    async def get_dashboard_url(self, context: Context):
        self.__logger.info(
            f"Exécution de la commande par {context.message.author}",
            method="get_dashboard_url",
        )

        message: Message = context.message

        dashboard_url: str = self.__miscellaneous_service.retrieve_dashboard_url()
        await message.channel.send(dashboard_url)

        self.__logger.info(
            "La commande a été exécutée avec succès.", method="get_dashboard_url"
        )

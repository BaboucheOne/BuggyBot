from discord.ext import commands
from discord.ext.commands import Context

from bot.resource.cog.association.embed.aeglo_embed import AegloEmbed
from bot.resource.cog.association.embed.asetin_embed import AsetinEmbed
from bot.resource.constants import ReplyMessage
from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient
from bot.resource.decorator.prohibit_self_message import prohibit_self_message


class AssociationCog(commands.Cog, name="Association"):

    def __init__(self):
        self.__bot = ServiceLocator.get_dependency(DiscordClient)
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    @commands.command(
        name="asetin",
        help="Informations sur l'ASETIN.",
        brief="Informations sur l'ASETIN.",
    )
    @commands.dm_only()
    @prohibit_self_message()
    async def asetin(self, context: Context):
        self.__logger.info(
            f"Exécution de la commande par {context.message.author}.",
            method="asetin",
        )

        message = context.message

        try:
            await message.channel.send(embed=AsetinEmbed().embed)
            self.__logger.info(
                "La commande a été exécutée avec succès.", method="asetin"
            )
        except Exception as e:
            self.__logger.error(
                f"Erreur lors de l'exécution de la commande exécutée par {context.message.author}. {e}",
                method="asetin",
                exception=e,
            )
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

    @commands.command(
        name="aeglo",
        help="Informations sur l'AEGLO.",
        brief="Informations sur l'AEGLO.",
    )
    @commands.dm_only()
    @prohibit_self_message()
    async def aeglo(self, context: Context):
        self.__logger.info(
            f"Exécution de la commande exécutée par {context.message.author}",
            method="aeglo",
        )

        message = context.message

        try:
            await message.channel.send(embed=AegloEmbed().embed)
            self.__logger.info(
                "La commande a été exécutée avec succès.", method="aeglo"
            )
        except Exception as e:
            self.__logger.error(
                f"Erreur lors de l'exécution de la commande exécutée par {context.message.author}. {e}",
                method="aeglo",
                exception=e,
            )
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

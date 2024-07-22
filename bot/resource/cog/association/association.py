from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

from bot.resource.cog.association.embed.aeglo_embed import AegloEmbed
from bot.resource.cog.association.embed.asetin_embed import AsetinEmbed
from bot.resource.constants import ReplyMessage
from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient


class AssociationCog(commands.Cog, name="Association"):

    def __init__(self):
        self.__bot = ServiceLocator.get_dependency(DiscordClient)
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    def __is_self(self, message: Message) -> bool:
        return message.author == self.__bot.user

    @commands.command(
        name="asetin",
        help="Informations sur l'ASETIN.",
        brief="Informations sur l'ASETIN.",
    )
    @commands.dm_only()
    async def asetin(self, context: Context):
        self.__logger.info(
            f"Exécution de la commande ASETIN par {context.message.author}."
        )

        message = context.message
        if self.__is_self(message):
            return

        try:
            await message.channel.send(embed=AsetinEmbed().embed)
        except Exception as e:
            self.__logger.error(
                f"{type(e).__name__}, Erreur lors de l'exécution de la commande ASETIN : {e}"
            )
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

    @commands.command(
        name="aeglo",
        help="Informations sur l'AEGLO.",
        brief="Informations sur l'AEGLO.",
    )
    @commands.dm_only()
    async def aeglo(self, context: Context):
        self.__logger.info(
            f"Exécution de la commande ASETIN par {context.message.author}"
        )

        message = context.message
        if self.__is_self(message):
            return

        try:
            await message.channel.send(embed=AegloEmbed().embed)
        except Exception as e:
            self.__logger.error(
                f"{type(e).__name__}, Erreur lors de l'exécution de la commande ASETIN : {e}"
            )
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

import logging

from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

from bot.cog.association.embed.aeglo_embed import AegloEmbed
from bot.cog.association.embed.asetin_embed import AsetinEmbed
from bot.cog.constants import ReplyMessage
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient


logger = logging.getLogger(__name__)


class AssociationCog(commands.Cog, name="Association"):

    def __init__(self):
        self.__bot = ServiceLocator.get_dependency(DiscordClient)

    def __is_self(self, message: Message) -> bool:
        return message.author == self.__bot.user

    @commands.command(
        name="asetin",
        help="Informations sur l'ASETIN.",
        brief="Informations sur l'ASETIN.",
    )
    @commands.dm_only()
    async def asetin(self, context: Context):
        logging.info(f"Executing ASETIN command by {context.message.author}")

        message = context.message
        if self.__is_self(message):
            return

        try:
            await message.channel.send(embed=AsetinEmbed().embed)
        except Exception as e:
            logging.error(f"Error while executing ASETIN command {e}")
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

    @commands.command(
        name="aeglo",
        help="Informations sur l'AEGLO.",
        brief="Informations sur l'AEGLO.",
    )
    @commands.dm_only()
    async def aeglo(self, context: Context):
        logging.info(f"Executing AEGLO command by {context.message.author}")

        message = context.message
        if self.__is_self(message):
            return

        try:
            await message.channel.send(embed=AegloEmbed().embed)
        except Exception as e:
            logging.error(f"Error while executing AEGLO command {e}")
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

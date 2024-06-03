from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

from bot.cog.constants import ReplyMessage
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient


class AssociationCog(commands.Cog, name="Association"):

    def __init__(self):
        self.__bot = ServiceLocator.get_dependency(DiscordClient)

    def __is_self(self, message: Message) -> bool:
        return message.author == self.__bot.user

    @commands.command(
        name="asetin",
        help="Info about ASETIN association.",
        brief="Info about ASETIN association.",
    )
    @commands.dm_only()
    async def asetin(self, context: Context):
        message = context.message
        if self.__is_self(message):
            return

        try:
            await message.channel.send(ReplyMessage.ASETIN_INFO)
        except Exception as e:
            print(f"Exception occur {e}")
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

    @commands.command(
        name="aeglo",
        help="Info about AEGLO association.",
        brief="Info about AEGLO association.",
    )
    @commands.dm_only()
    async def aeglo(self, context: Context):
        message = context.message
        if self.__is_self(message):
            return

        try:
            await message.channel.send(ReplyMessage.AEGLO_INFO)
        except Exception as e:
            print(f"Exception occur {e}")
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

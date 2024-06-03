from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

from bot.cog.constants import ReplyMessage
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient


class RegisterMemberCog(commands.Cog):

    def __init__(self):
        self.__bot = ServiceLocator.get_dependency(DiscordClient)

    def __is_self(self, message: Message) -> bool:
        return message.author == self.__bot.user

    @commands.command(name="help")
    @commands.dm_only()
    async def help(self, context: Context):
        message = context.message
        if self.__is_self(message):
            return

        try:
            await message.channel.send(ReplyMessage.HELP)
        except Exception as e:
            print(f"Exception occur {e}")
            await message.channel.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

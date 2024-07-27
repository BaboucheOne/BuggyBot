from discord.ext import commands
from discord.ext.commands import Context

from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient
from bot.resource.constants import ReplyMessage
from bot.config.exception.exception_handler_locator import (
    ExceptionHandlerLocator,
)


class ErrorHandlerCog(commands.Cog, name="ErrorHandler"):
    def __init__(self):
        self.__bot = ServiceLocator.get_dependency(DiscordClient)
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception):
        try:
            response: str = ExceptionHandlerLocator.get_handler(error)
            await ctx.send(response)
        except Exception:
            await ctx.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

        self.__logger.error(str(error), method="on_command_error")

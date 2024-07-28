from discord.ext import commands
from discord.ext.commands import Context, CommandInvokeError

from bot.config.exception.not_found_exception_handler import (
    NotFoundExceptionHandler,
)
from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient
from bot.config.exception.exception_handler_locator import (
    ExceptionHandlerLocator,
)
from bot.resource.constants import ReplyMessage


class ErrorHandlerCog(commands.Cog, name="ErrorHandler"):
    def __init__(self):
        self.__bot = ServiceLocator.get_dependency(DiscordClient)
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandInvokeError):
        try:
            handler = ExceptionHandlerLocator.get_handler(type(error.original))
            response = handler.response()

            self.__logger.info(
                str(error.original), method="on_command_error", exception=error.original
            )

            await ctx.send(response)
        except NotFoundExceptionHandler as e:
            self.__logger.warning(str(e), method="on_command_error", exception=e)
            await ctx.send(ReplyMessage.UNSUCCESSFUL_GENERIC)
        except Exception as e:
            self.__logger.error(str(e), method="on_command_error", exception=e)
            await ctx.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

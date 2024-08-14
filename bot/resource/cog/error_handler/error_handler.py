from discord.ext import commands
from discord.ext.commands import (
    Context,
    CommandInvokeError,
    CommandNotFound,
    PrivateMessageOnly,
)

from bot.config.exception.mapper_not_found_exception import (
    MapperNotFoundException,
)
from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient
from bot.config.exception.exception_mapper import (
    ExceptionMapper,
)
from bot.resource.constants import ReplyMessage


class ErrorHandlerCog(commands.Cog, name="ErrorHandler"):
    def __init__(self):
        self.__bot = ServiceLocator.get_dependency(DiscordClient)
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    def __is_error_should_be_handled(self, exception: Exception) -> bool:
        return not isinstance(exception, CommandNotFound) or isinstance(
            exception, PrivateMessageOnly
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandInvokeError):

        if not self.__is_error_should_be_handled(error.original):
            return

        try:
            response: str = ExceptionMapper.get_response(type(error.original))

            self.__logger.info(
                str(error.original), method="on_command_error", exception=error.original
            )

            await ctx.send(response)
        except MapperNotFoundException as e:
            self.__logger.warning(str(e), method="on_command_error", exception=e)
            await ctx.send(ReplyMessage.UNSUCCESSFUL_GENERIC)
        except Exception as e:
            self.__logger.error(str(e), method="on_command_error", exception=e)
            await ctx.send(ReplyMessage.UNSUCCESSFUL_GENERIC)

from discord.ext import commands
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient
from bot.resource.exception.user_not_in_server_exception import UserNotInServerException


def user_in_server():
    def predicate(ctx):
        discord_client = ServiceLocator.get_dependency(DiscordClient)
        member = discord_client.server.get_member(ctx.message.author.id)

        if not member:
            raise UserNotInServerException(ctx.message.author.id)

        return True

    return commands.check(predicate)

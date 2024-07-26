from discord.ext import commands
from discord.utils import get

from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient


def role_check(*role_names):
    def predicate(ctx):
        discord_client = ServiceLocator.get_dependency(DiscordClient)
        member = discord_client.server.get_member(ctx.message.author.id)

        if not member:
            return False

        return any(get(member.roles, name=role_name) for role_name in role_names)

    return commands.check(predicate)

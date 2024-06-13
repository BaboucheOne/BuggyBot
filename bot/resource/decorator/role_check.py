import discord
from discord.ext import commands

from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient


def role_check(*role_names):
    def predicate(ctx):
        user = ctx.message.author
        discord_client: DiscordClient = ServiceLocator.get_dependency(DiscordClient)
        member = discord_client.server.get_member(user.id)
        if member is None:
            return False

        for role_name in role_names:
            role = discord.utils.get(member.roles, name=role_name)
            if role is not None:
                return True
        return False

    return commands.check(predicate)

from discord.ext import commands

from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient


def prohibit_self_message():
    def predicate(ctx):
        discord_client: DiscordClient = ServiceLocator.get_dependency(DiscordClient)
        return ctx.message.author.id != discord_client.user.id

    return commands.check(predicate)

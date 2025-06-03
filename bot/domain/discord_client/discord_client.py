from typing import Any

import discord
from discord import Guild
from discord.ext.commands import Bot

from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.student.attribut.discord_user_id import DiscordUserId


class DiscordClient(Bot):
    def __init__(
        self,
        command_prefix,
        *,
        intents: discord.Intents,
        server_id: int,
        **options: Any
    ):
        super().__init__(command_prefix, intents=intents, **options)
        self.__server = None
        self.__server_id = server_id
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    async def on_ready(self):
        self.__server = self.get_guild(self.__server_id)
        self.__logger.info("DiscordClient prêt à fonctionner.", method="on_ready")

    def does_user_exists(self, discord_id: DiscordUserId) -> bool:
        return self.get_user(discord_id.value) is not None

    @property
    def ready(self) -> bool:
        return self.__server is not None

    @property
    def server(self) -> Guild:
        return self.__server

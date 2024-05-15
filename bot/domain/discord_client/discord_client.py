from typing import Any

import discord
from discord import Guild
from discord.ext.commands import Bot


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

    async def on_ready(self):
        self.__server = self.get_guild(self.__server_id)

    @property
    def ready(self) -> bool:
        return self.__server is not None

    @property
    def server(self) -> Guild:
        return self.__server

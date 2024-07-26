import discord
import requests

from typing import Callable

from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.task.task import Task


class SentenceOfTheDayTask(Task):

    MAX_PRESENCE_CHARS: int = 128
    TIMEOUT_IN_SECOND: int = 10
    API_ENDPOINT: str = "https://luha.alwaysdata.net/api/?hour=1"
    RESPONSE_CITATION_KEY: str = "citation"

    def __init__(self, discord_client: DiscordClient, schedule_method: Callable):
        super().__init__(schedule_method)
        self.__discord_client: DiscordClient = discord_client
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    def __get_sentence_of_the_day(self) -> str:
        response = requests.get(self.API_ENDPOINT, timeout=self.TIMEOUT_IN_SECOND)
        response.raise_for_status()
        return response.json()[self.RESPONSE_CITATION_KEY]

    async def do(self):
        self.__logger.info("Début de la tâche.", method="do")

        try:
            citation = self.__get_sentence_of_the_day()
            await self.__discord_client.change_presence(
                activity=discord.Game(name=citation[: self.MAX_PRESENCE_CHARS])
            )

            self.__logger.info("La phrase du jour a été appliquée.", method="do")
        except requests.exceptions.RequestException as e:
            self.__logger.warning(
                f"Impossible de récupérer la phrase du jour en raison de {e}.",
                method="do",
                exception=e,
            )
        except Exception as e:
            self.__logger.warning(
                f"Une erreur s'est produite {e}.", method="do", exception=e
            )

        self.__logger.info("SentenceOfTheDayTask - Fin de la tâche.", method="do")

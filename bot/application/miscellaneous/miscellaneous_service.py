import socket

from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient


class MiscellaneousService:
    def __init__(self):
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)
        self.__discord_client: DiscordClient = ServiceLocator.get_dependency(
            DiscordClient
        )

    def retrieve_dashboard_url(self) -> str:
        try:
            ip_address: str = socket.gethostbyname("host.docker.internal")
            return f"http://{ip_address}:8080"
        except socket.gaierror:
            return "http://127.0.0.1:8080"

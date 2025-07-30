import socket

from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient


class MiscellaneousService:

    DOCKER_HOST: str = "host.docker.internal"

    def __init__(self, dashboard_port: int):
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)
        self.__discord_client: DiscordClient = ServiceLocator.get_dependency(
            DiscordClient
        )

        self.__dashboard_board: int = dashboard_port

    def __get_host_ip_address(self) -> str:
        try:
            ip_address: str = socket.gethostbyname(self.DOCKER_HOST)
            return f"http://{ip_address}"
        except socket.gaierror:
            return f"http://127.0.0.1"

    def retrieve_dashboard_url(self) -> str:
        ip_address: str = self.__get_host_ip_address()
        return f"{ip_address}:{self.__dashboard_board}"

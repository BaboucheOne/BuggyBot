from abc import ABC, abstractmethod
from typing import List, Tuple

from pymongo import MongoClient
from pymongo.collection import Collection

from bot.application.discord.discord_service import DiscordService
from bot.application.student.student_service import StudentService
from bot.cog.registration.register_member import RegisterMemberCog
from bot.config.dotenv_configuration import DotEnvConfiguration
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.student.student_repository import StudentRepository


class ApplicationContext(ABC):
    def __init__(self, configuration_filename: str):
        self._configuration = DotEnvConfiguration(configuration_filename)

    async def start_application(self):
        await ServiceLocator.get_dependency(DiscordClient).start(
            self._configuration.discord_token
        )

    async def build_application(self):
        mongo_client = self._instantiate_mongo_client()
        student_collection = self.__instantiate_student_collection(mongo_client)
        student_repository = self._instantiate_student_repository(student_collection)

        discord_client = self._instantiate_discord_client()

        student_service = self._instantiate_student_service(student_repository)
        discord_service = self._instantiate_discord_service(
            discord_client, student_repository
        )

        student_service.register_to_on_student_registered(discord_service)

        dependencies = [
            (DiscordClient, discord_client),
            (StudentRepository, student_repository),
            (StudentService, student_service),
            (DiscordService, discord_service),
        ]
        self.__assemble_dependencies(dependencies)

        cogs = [self._instantiate_register_member_cog()]
        await self.__register_cogs(discord_client, cogs)

    async def __register_cogs(self, discord_client: DiscordClient, cogs: List):
        for cog in cogs:
            await discord_client.add_cog(cog)

    def __assemble_dependencies(self, dependencies: List[Tuple]):
        ServiceLocator.clear()
        for dependency_type, dependency_instance in dependencies:
            ServiceLocator.register_dependency(dependency_type, dependency_instance)

    def __instantiate_student_collection(self, client: MongoClient) -> Collection:
        database = client[self._configuration.mongodb_database_name]
        return database[self._configuration.student_collection_name]

    @abstractmethod
    def _instantiate_register_member_cog(self) -> RegisterMemberCog:
        pass

    @abstractmethod
    def _instantiate_mongo_client(self) -> MongoClient:
        pass

    @abstractmethod
    def _instantiate_discord_client(self) -> DiscordClient:
        pass

    @abstractmethod
    def _instantiate_student_repository(
        self, student_collection: Collection
    ) -> StudentRepository:
        pass

    @abstractmethod
    def _instantiate_student_service(
        self, student_repository: StudentRepository
    ) -> StudentService:
        pass

    @abstractmethod
    def _instantiate_discord_service(
        self, discord_client: DiscordClient, student_repository: StudentRepository
    ) -> DiscordService:
        pass

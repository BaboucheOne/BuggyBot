from abc import ABC, abstractmethod
from typing import List, Tuple

from discord.ext import commands
from pymongo import MongoClient
from pymongo.collection import Collection

from bot.application.discord.discord_service import DiscordService
from bot.application.student.student_service import StudentService
from bot.domain.task.task import Task
from bot.domain.task.task_scheduler import TaskScheduler
from bot.resource.cog.association.association import AssociationCog
from bot.resource.cog.error_handler.error_handler import ErrorHandlerCog
from bot.resource.cog.registration.register_member import RegisterMemberCog
from bot.config.environment.dotenv_configuration import DotEnvConfiguration
from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.student.student_repository import StudentRepository


class ApplicationContext(ABC):
    def __init__(self):
        self._configuration: DotEnvConfiguration = DotEnvConfiguration()

    def _load_configuration_from_file(self, filename: str):
        self._configuration.from_file(filename)

    async def start_application(self):
        ServiceLocator.get_dependency(TaskScheduler).start()
        await ServiceLocator.get_dependency(DiscordClient).start(
            self._configuration.discord_token
        )

    async def build_application(self):
        ServiceLocator.clear()
        ServiceLocator.register_dependency(Logger, self._instantiate_logger())

        mongo_client = self._instantiate_mongo_client()
        self.__is_database_available(mongo_client)

        student_collection = self.__instantiate_student_collection(mongo_client)
        student_repository = self._instantiate_student_repository(student_collection)

        discord_client = self._instantiate_discord_client()

        task_scheduler = TaskScheduler()

        student_service = self._instantiate_student_service(student_repository)
        discord_service = self._instantiate_discord_service(
            discord_client, student_repository
        )

        student_service.register_to_on_student_registered(discord_service)

        dependencies = [
            (TaskScheduler, task_scheduler),
            (DiscordClient, discord_client),
            (StudentRepository, student_repository),
            (StudentService, student_service),
            (DiscordService, discord_service),
        ]
        self.__assemble_dependencies(dependencies)

        cogs = [
            self._instantiate_register_member_cog(),
            self._instantiate_association_cog(),
            self._instantiate_error_handler_cog(),
        ]
        await self.__register_cogs(discord_client, cogs)

        tasks = self._instantiate_tasks(discord_client)
        task_scheduler.add_tasks(tasks)

    def __is_database_available(self, client: MongoClient):
        client.admin.command("ismaster")

    async def __register_cogs(
        self, discord_client: DiscordClient, cogs: List[commands.Cog]
    ):
        for cog in cogs:
            await discord_client.add_cog(cog)

    def __assemble_dependencies(self, dependencies: List[Tuple]):
        for dependency_type, dependency_instance in dependencies:
            ServiceLocator.register_dependency(dependency_type, dependency_instance)

    def __instantiate_student_collection(self, client: MongoClient) -> Collection:
        database = client[self._configuration.mongodb_database_name]
        return database[self._configuration.student_collection_name]

    @abstractmethod
    def _instantiate_logger(self) -> Logger:
        pass

    @abstractmethod
    def _instantiate_association_cog(self) -> AssociationCog:
        pass

    @abstractmethod
    def _instantiate_register_member_cog(self) -> RegisterMemberCog:
        pass

    @abstractmethod
    def _instantiate_error_handler_cog(self) -> ErrorHandlerCog:
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

    @abstractmethod
    def _instantiate_tasks(self, discord_client: DiscordClient) -> List[Task]:
        pass

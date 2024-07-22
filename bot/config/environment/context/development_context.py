import logging
from typing import List

import discord
import schedule
from pymongo import MongoClient
from pymongo.collection import Collection

from bot.application.discord.discord_service import DiscordService
from bot.application.student.student_service import StudentService
from bot.application.task.kick_unregistered_user_task import KickUnregisteredUserTask
from bot.application.task.sentence_of_the_day_task import SentenceOfTheDayTask
from bot.domain.task.task import Task
from bot.resource.cog.association.association import AssociationCog
from bot.resource.cog.registration.register_member import RegisterMemberCog
from bot.config.environment.context.application_context import ApplicationContext
from bot.config.constants import ConfigurationFilename
from bot.config.logger.logger import Logger
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.student.student_repository import StudentRepository
from bot.infra.student.cached_student_repository import CachedStudentRepository
from bot.infra.student.mongodb_student_repository import MongoDbStudentRepository


class DevelopmentContext(ApplicationContext):

    MIDNIGHT: str = "00:00"

    def __init__(self):
        super().__init__()
        self._load_configuration_from_file(ConfigurationFilename.DEVELOPMENT)

    def _instantiate_mongo_client(self) -> MongoClient:
        return MongoClient(
            self._configuration.mongodb_connection_string,
            connectTimeoutMS=self._configuration.mongodb_connection_timeout_ms,
            timeoutMS=self._configuration.mongodb_connection_timeout_ms,
        )

    def _instantiate_discord_client(self) -> DiscordClient:
        intents = discord.Intents.all()
        return DiscordClient(
            command_prefix="!", intents=intents, server_id=self._configuration.server_id
        )

    def _instantiate_logger(self) -> Logger:
        return Logger(self._configuration.logger_filename, logging.DEBUG)

    def _instantiate_association_cog(self) -> AssociationCog:
        return AssociationCog()

    def _instantiate_register_member_cog(self) -> RegisterMemberCog:
        return RegisterMemberCog()

    def _instantiate_student_repository(
        self, student_collection: Collection
    ) -> StudentRepository:
        student_repository = MongoDbStudentRepository(student_collection)
        return CachedStudentRepository(student_repository)

    def _instantiate_student_service(
        self, student_repository: StudentRepository
    ) -> StudentService:
        return StudentService(student_repository)

    def _instantiate_discord_service(
        self, discord_client: DiscordClient, student_repository: StudentRepository
    ) -> DiscordService:
        return DiscordService(discord_client, student_repository)

    def _instantiate_tasks(self, discord_client: DiscordClient) -> List[Task]:
        return [
            KickUnregisteredUserTask(
                discord_client, schedule.every().day.at(self.MIDNIGHT).do
            ),
            SentenceOfTheDayTask(
                discord_client, schedule.every().day.at(self.MIDNIGHT).do
            ),
        ]

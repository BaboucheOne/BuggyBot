import logging

import discord
from pymongo import MongoClient
from pymongo.collection import Collection

from bot.application.discord.discord_service import DiscordService
from bot.application.student.student_service import StudentService
from bot.cog.association.association import AssociationCog
from bot.cog.registration.register_member import RegisterMemberCog
from bot.config.application_context import ApplicationContext
from bot.config.constants import ConfigurationFilename
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.student.student_repository import StudentRepository
from bot.infra.student.cached_student_repository import CachedStudentRepository
from bot.infra.student.mongodb_student_repository import MongoDbStudentRepository

logger = logging.getLogger(__name__)


class DevelopmentContext(ApplicationContext):

    def __init__(self):
        super().__init__(ConfigurationFilename.DEVELOPMENT)
        logger.info("Using development context")

    def _instantiate_mongo_client(self) -> MongoClient:
        return MongoClient(self._configuration.mongodb_connection_string)

    def _instantiate_discord_client(self) -> DiscordClient:
        intents = discord.Intents.all()
        return DiscordClient(
            command_prefix="!", intents=intents, server_id=self._configuration.server_id
        )

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

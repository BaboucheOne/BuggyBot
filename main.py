import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

from bot.application.discord.discord_service import DiscordService
from bot.application.student.student_service import StudentService
from bot.cog.registration.register_member import RegisterMemberCog
from bot.domain.discord_client.discord_client import DiscordClient
from bot.infra.student.cached_student_repository import CachedStudentRepository
from bot.infra.student.mongodb_student_repository import MongoDbStudentRepository


def create_bot(server_id: int) -> DiscordClient:
    intents = discord.Intents.all()
    return DiscordClient(command_prefix="!", intents=intents, server_id=server_id)


async def register_cogs(bot: commands.Bot, student_service: StudentService):
    await bot.add_cog(RegisterMemberCog(bot, student_service))


def connect_to_mongo_db(connection_url: str) -> MongoClient:
    try:
        return MongoClient(connection_url)
    except ConnectionError as e:
        print(f"Unable to connect to the MongoDB. {e}")
        exit(-1)


async def main():
    load_dotenv()
    discord_token: str = os.getenv("DISCORD_TOKEN")
    server_id: int = int(os.getenv("SERVER_ID"))
    mongodb_localhost_connection_string = os.getenv(
        "MONGODB_LOCALHOST_SERVER_CONNECTION_STRING"
    )

    mongodb_client = connect_to_mongo_db(mongodb_localhost_connection_string)
    database = mongodb_client[os.getenv("MONGODB_DB_NAME")]
    student_collection = database["students"]
    student_repository = MongoDbStudentRepository(student_collection)
    cached_student_repository = CachedStudentRepository(student_repository)

    bot = create_bot(server_id)
    student_service = StudentService(cached_student_repository)
    discord_service = DiscordService(bot, cached_student_repository)

    student_service.register_to_on_student_registered(discord_service)

    await register_cogs(bot, student_service)
    await bot.start(discord_token)

    student_service.unregister_all_from_on_student_registered()


if __name__ == "__main__":
    asyncio.run(main())

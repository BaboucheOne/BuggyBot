import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

from bot.cog.registration.register_member import RegisterMemberCog
from bot.infra.student.mongodb_student_repository import MongoDbStudentRepository


def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    return commands.Bot(command_prefix="!", intents=intents)


async def register_cogs(bot: commands.Bot):
    await bot.add_cog(RegisterMemberCog(bot))


def connect_to_mongo_db(connection_url: str) -> MongoClient:
    try:
        return MongoClient(connection_url)
    except ConnectionError as e:
        print(f"Unable to connect to the MongoDB. {e}")
        exit(-1)


async def main():
    load_dotenv()
    discord_token = os.getenv("DISCORD_TOKEN")
    mongodb_localhost_connection_string = os.getenv(
        "MONGODB_LOCALHOST_SERVER_CONNECTION_STRING"
    )

    mongodb_client = connect_to_mongo_db(mongodb_localhost_connection_string)
    database = mongodb_client[os.getenv("MONGODB_DB_NAME")]
    student_collection = database["students"]
    _ = MongoDbStudentRepository(student_collection)

    bot = create_bot()
    await register_cogs(bot)

    await bot.start(discord_token)


if __name__ == "__main__":
    asyncio.run(main())

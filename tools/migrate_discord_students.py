import asyncio
import concurrent
import copy
import functools
import threading
import time

import discord
from typing import List, Tuple

from discord import Member
from pymongo import MongoClient
from pymongo.collection import Collection

from bot.config.constants import ConfigurationFilename
from bot.config.dotenv_configuration import DotEnvConfiguration
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.student.student import Student
from bot.domain.utility import Utility
from bot.infra.constants import StudentMongoDbKey
from bot.infra.student.assembler.student_assembler import StudentAssembler
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)
from constants import StudentListKey

MISSING_DISCORD_USER_ID = -1
STUDENT_ASSEMBLER: StudentAssembler = StudentAssembler()

MIGRATION_SENDING_REQUEST_SEC = 0.1
MIGRATION_SENDING_MESSAGE_SEC = 0.5
WAIT_FOR_THREAD_INITIALIZATION = 1.0


def read_configurations(filename: str) -> DotEnvConfiguration:
    return DotEnvConfiguration(filename)


def connect_to_mongo_db(connection_url: str) -> MongoClient:
    try:
        return MongoClient(connection_url)
    except ConnectionError as e:
        print(f"Unable to connect to the MongoDB. {e}")
        exit(-1)


def get_unregistered_students(students_collection) -> List[Student]:
    query = {StudentListKey.DISCORD_USER_ID: {"$ne": MISSING_DISCORD_USER_ID}}
    projection = {"_id": 0}
    results = students_collection.find(query, projection)

    return [STUDENT_ASSEMBLER.from_dict(result) for result in results]


def find_with_first_and_lastname(
    students: List[Student], firstname: str, lastname: str
) -> Tuple[int, Student or None]:
    for k, s in enumerate(students):
        if s.firstname.value == firstname and s.lastname.value == lastname:
            return k, s
    raise StudentNotFoundException()


def remove_none_values(list_to_modify: List[Member]):
    for member in list_to_modify:
        if member.bot or member.nick is None:
            list_to_modify.remove(member)


def remove_duplicate_values(
    list_to_modify: List[Member], members_migration_missed: List[Member]
):
    for i, member in enumerate(list_to_modify):
        member_is_removed = False
        for j, other in enumerate(list_to_modify):
            if i == j:
                continue

            if member.nick == other.nick:
                members_migration_missed.append(copy.deepcopy(member))
                members_migration_missed.append(copy.deepcopy(other))

                list_to_modify.remove(member)
                list_to_modify.remove(other)

                member_is_removed = True

                break

        if member_is_removed:
            continue


def migrate_student(collection: Collection, student: Student):
    update_filter = {StudentMongoDbKey.NI: student.ni.value}
    update_operation = {
        "$set": {StudentMongoDbKey.DISCORD_USER_ID: student.discord_user_id.value}
    }
    collection.update_one(update_filter, update_operation)


def check_migration_rules(
    server_members: List[Member],
    students: List[Student],
    members_migration_successful: List[Student],
    members_migration_missed: List[Member],
):
    for member in server_members:
        try:
            split = member.nick.split(" ")
            index, student = find_with_first_and_lastname(students, split[0], split[1])

            if student.discord_user_id.value == -1:
                student.discord_user_id.value = member.id
                members_migration_successful.append(student)
        except StudentNotFoundException or IndexError:
            members_migration_missed.append(member)


async def send_dm_non_migrated_members(members_migration_missed: List[Member]):
    print("Starting contacting people. Can take some times.")
    print(
        f"Time to contact members : {len(members_migration_missed) * MIGRATION_SENDING_MESSAGE_SEC}"
    )
    for member in members_migration_missed:
        await member.send(
            "Hello I'm buggybot from ASETIN's discord!\n"
            "A migration has been done."
            "Unfortunately we were unable to migrate your discord profile to our new database.\n"
            "Use !register [IDUL] to perform this migration.\n"
            "If you need help contact an admin."
        )
        time.sleep(MIGRATION_SENDING_MESSAGE_SEC)
    print("All miss migrated has been contacted.")


def notify_non_migrated_members(
    server_members: List[Member], members_migration_missed: List[Member]
):
    print(
        f"{len(members_migration_missed)} Students has not been migrated due to errors."
    )
    print(
        f"This represent {len(server_members)/len(members_migration_missed) * 100}% of members."
    )
    print("Solution: Contact them and tell them to registered by them self.")
    for member in members_migration_missed:
        print(member.nick)


def perform_migration(
    collection: Collection, members_migration_successful: List[Student]
):
    print("Migration starting...")
    print(
        f"Estimated time to migrate members : {len(members_migration_successful) * MIGRATION_SENDING_REQUEST_SEC}"
    )
    for member in members_migration_successful:
        migrate_student(collection, member)
        time.sleep(MIGRATION_SENDING_REQUEST_SEC)
    print(f"Migration successful for {len(members_migration_successful)} members")


async def migrate(
    collection: Collection, students: List[Student], discord_client: DiscordClient
):
    while not discord_client.ready:
        pass

    members_migration_missed: List[Member] = []
    members_migration_successful: List[Student] = []
    server_members: List[Member] = list(discord_client.server.members)

    remove_none_values(server_members)
    remove_duplicate_values(server_members, members_migration_missed)
    check_migration_rules(
        server_members, students, members_migration_successful, members_migration_missed
    )

    perform_migration(collection, members_migration_successful)
    notify_non_migrated_members(server_members, members_migration_missed)

    response = input("Automatically contact them ?\n Use: true, 1, yes, y, oui or o")
    can_contact = Utility.str_to_bool(response)
    if can_contact:
        await send_dm_non_migrated_members(members_migration_missed)
    else:
        print("You chose to not contact these members")

    await discord_client.close()


def start_bot(discord_client: DiscordClient, configuration: DotEnvConfiguration):
    discord_client.run(configuration.discord_token)


async def main():
    configuration = read_configurations(ConfigurationFilename.PRODUCTION)

    intents = discord.Intents.all()
    discord_client: DiscordClient = DiscordClient(
        command_prefix="!", intents=intents, server_id=configuration.server_id
    )

    client = connect_to_mongo_db(configuration.mongodb_connection_string)
    database = client[configuration.mongodb_database_name]
    students_collection = database[configuration.student_collection_name]

    unregistered_students = get_unregistered_students(students_collection)

    thread = threading.Thread(
        target=start_bot,
        args=(
            discord_client,
            configuration,
        ),
    )
    thread.start()

    time.sleep(WAIT_FOR_THREAD_INITIALIZATION)

    await migrate(students_collection, unregistered_students, discord_client)

    print("Migration done.")

if __name__ == "__main__":
    asyncio.run(main())

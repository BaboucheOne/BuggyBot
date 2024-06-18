import argparse
import asyncio
import threading
import time

import discord
from typing import List

from discord import Member
from pymongo import MongoClient
from pymongo.collection import Collection

from bot.config.context.dotenv_configuration import DotEnvConfiguration
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.student import Student
from bot.domain.utility import Utility
from bot.infra.constants import StudentMongoDbKey
from bot.infra.student.assembler.student_assembler import StudentAssembler
from bot.infra.student.exception.student_not_found_exception import (
    StudentNotFoundException,
)
from constants import StudentCsvKey
from tools.configuration_common import (
    add_configuration_argument,
    get_configuration,
    setup_logger,
)

global logger

STUDENT_ASSEMBLER: StudentAssembler = StudentAssembler()

MIGRATION_SENDING_REQUEST_SEC = 0.1
MIGRATION_SENDING_MESSAGE_SEC = 0.5
WAIT_FOR_THREAD_INITIALIZATION = 1.0


def read_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Migrer les étudiants de Discord vers la base de données."
    )
    add_configuration_argument(parser)

    return parser.parse_args()


def connect_to_mongo_db(connection_url: str) -> MongoClient:
    try:
        return MongoClient(connection_url)
    except ConnectionError as e:
        logger.fatal(f"Unable to connect to the MongoDB. {e}")
        exit(-1)


def get_unregistered_students(students_collection) -> List[Student]:
    query = {StudentCsvKey.DISCORD_USER_ID: {"$ne": DiscordUserId.INVALID_DISCORD_ID}}
    projection = {"_id": 0}
    results = students_collection.find(query, projection)

    return [STUDENT_ASSEMBLER.from_dict(result) for result in results]


def find_with_first_and_lastname(
    students: List[Student], firstname: str, lastname: str
) -> Student:
    for student in students:
        if student.firstname.value == firstname and student.lastname.value == lastname:
            return student
    raise StudentNotFoundException()


def remove_none_values(list_to_modify: List[Member]):
    for member in list_to_modify[:]:
        if member.bot or member.nick is None:
            list_to_modify.remove(member)


def remove_duplicate_values(
    list_to_modify: List[Member], members_migration_missed: List[Member]
):
    for i, member in enumerate(list_to_modify[:]):
        member_is_removed = False
        for j, other in enumerate(list_to_modify[:]):
            if (
                i == j
                or member in members_migration_missed
                or other in members_migration_missed
            ):
                continue

            if member.nick == other.nick:
                members_migration_missed.append(member)
                members_migration_missed.append(other)

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
            student = find_with_first_and_lastname(students, split[0], split[1])
            student.discord_user_id.value = member.id
            members_migration_successful.append(student)
        except StudentNotFoundException or IndexError:
            members_migration_missed.append(member)


async def send_dm_non_migrated_members(members_migration_missed: List[Member]):
    logger.info(
        "Début du contact avec les personnes. Cela peut prendre du temps. "
        f"Temps pour contacter les membres.: {len(members_migration_missed) * MIGRATION_SENDING_MESSAGE_SEC} secs"
    )
    for member in members_migration_missed:
        await member.send(
            "Bonjour, je suis BuggyBot du Discord d'ASETIN !\n"
            "Une migration a été effectuée.\n"
            "Malheureusement, nous n'avons pas pu migrer votre profil Discord vers notre nouvelle base de données.\n"
            "Utilisez !register [NI] pour effectuer cette migration.\n"
            "Si vous avez besoin d'aide, contactez un administrateur."
        )
        time.sleep(MIGRATION_SENDING_MESSAGE_SEC)
    logger.info("Tous les utilisateurs non migrés ont été contactés.")


def notify_non_migrated_members(
    server_members: List[Member], members_migration_missed: List[Member]
):
    members_to_contacts = ", ".join(
        [member.nick for member in members_migration_missed]
    )
    logger.info(
        f"{len(members_migration_missed)} étudiants n'ont pas été migrés en raison d'erreurs. "
        f"Cela représente {len(members_migration_missed)/len(server_members) * 100}% des membres. "
        f"Solution : Les contacter et leur demander de s'inscrire eux-mêmes.\nVoici la liste des personnes à "
        f"contacter: {members_to_contacts}"
    )


def perform_migration(
    collection: Collection, members_migration_successful: List[Student]
):
    logger.info(
        "La migration démarre... "
        f"Temps estimé pour migrer les membres: {len(members_migration_successful) * MIGRATION_SENDING_REQUEST_SEC} secs."
    )
    for member in members_migration_successful:
        migrate_student(collection, member)
        time.sleep(MIGRATION_SENDING_REQUEST_SEC)
    logger.info(f"Migration réussie pour {len(members_migration_successful)} membres.")


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

    if len(members_migration_successful) > 0:
        perform_migration(collection, members_migration_successful)
    else:
        logger.info("Aucun membre à migrer.")

    if len(members_migration_missed) > 0:
        notify_non_migrated_members(server_members, members_migration_missed)
        response = input(
            "Utiliser un message automatisé pour les contacter ? Utilisez: true, 1, yes, y, oui ou o -> "
        )
        can_contact = Utility.str_to_bool(response)
        if can_contact:
            await send_dm_non_migrated_members(members_migration_missed)
        else:
            logger.info("Vous avez choisi de ne pas contacter ces membres.")
    else:
        logger.info("Aucun membre mal migré.")

    logger.info("Migration terminée.")
    exit(0)


def start_bot(discord_client: DiscordClient, configuration: DotEnvConfiguration):
    discord_client.run(configuration.discord_token)


async def main():
    global logger

    arguments = read_arguments()
    configuration: DotEnvConfiguration = get_configuration(arguments)
    logger = setup_logger(configuration.logger_filename)

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


if __name__ == "__main__":
    asyncio.run(main())

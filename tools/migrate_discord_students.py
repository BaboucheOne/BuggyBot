import copy
import threading
import time

import discord
import pandas as pd
from typing import List, Tuple

from discord import Member
from pymongo import MongoClient
from pymongo.collection import Collection

from bot.config.constants import ConfigurationFilename
from bot.config.dotenv_configuration import DotEnvConfiguration
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.student.attributs.firstname import Firstname
from bot.domain.student.attributs.ni import NI
from bot.domain.student.student import Student
from bot.infra.constants import StudentMongoDbKey
from bot.infra.student.assembler.student_assembler import StudentAssembler
from constants import StudentListKey, UniProgram

STUDENTS_LIST_COLUMNS_TO_KEEP: List[str] = [
    StudentListKey.NI,
    StudentListKey.PROGRAM_CODE,
    StudentListKey.LASTNAME,
    StudentListKey.FIRSTNAME,
    StudentListKey.NEW,
]

STUDENT_ALLOWED_PROGRAM = [
    UniProgram.IFT,
    UniProgram.GLO,
    UniProgram.CERTIFICATE,
    UniProgram.IIG,
]

STUDENT_NOUVEAU_COLUMN_MAPPING = {"Oui": True, "Non": False}
STUDENTS_LIST_RENAMING_MAPPING = {
    StudentListKey.NI: StudentMongoDbKey.NI,
    StudentListKey.FIRSTNAME: StudentMongoDbKey.FIRSTNAME,
    StudentListKey.LASTNAME: StudentMongoDbKey.LASTNAME,
    StudentListKey.PROGRAM_CODE: StudentMongoDbKey.PROGRAM_CODE,
    StudentListKey.NEW: StudentMongoDbKey.NEW_ADMITTED,
}

MISSING_DISCORD_USER_ID = -1

STUDENT_ASSEMBLER: StudentAssembler = StudentAssembler()


def read_configurations(filename: str) -> DotEnvConfiguration:
    return DotEnvConfiguration(filename)


def read_students_csv(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path, usecols=STUDENTS_LIST_COLUMNS_TO_KEEP)


def connect_to_mongo_db(connection_url: str) -> MongoClient:
    try:
        return MongoClient(connection_url)
    except ConnectionError as e:
        print(f"Unable to connect to the MongoDB. {e}")
        exit(-1)


def get_unregistered_students(students_collection) -> List[Student]:
    query = {StudentListKey.DISCORD_USER_ID: {"$ne": MISSING_DISCORD_USER_ID}}
    projection = {'_id': 0}
    results = students_collection.find(query, projection)

    students = []
    for r in results:
        students.append(STUDENT_ASSEMBLER.from_dict(r))
    return students


def do(collection: Collection, students: List[Student], discord_client: DiscordClient):
    while not discord_client.ready:
        pass

    miss = []
    migrated = []
    server_members: List[Member] = list(discord_client.server.members)
    # Remove none or bot.
    for member in server_members:
        if member.bot or member.nick is None:
            server_members.remove(member)

    # checks for duplicated and notify them.
    for i, member in enumerate(server_members):
        member_is_removed = False
        for j, other in enumerate(server_members):
            if i == j:
                continue

            if member.nick == other.nick:
                miss.append(copy.deepcopy(member.nick))
                miss.append(copy.deepcopy(other.nick))

                server_members.remove(member)
                server_members.remove(other)

                member_is_removed = True

                break

        if member_is_removed:
            continue

    def find_with_first_and_lastname(firstname: str, lastname: str) -> Tuple[int, Student or None]:
        for k, s in enumerate(students):
            if s.firstname.value == firstname and s.lastname.value == lastname:
                return k, s
        return -1, None

    for member in server_members:
        if member.nick is not None:
            split = member.nick.split(' ')
            if len(split) != 2:
                miss.append(member.nick)
                continue

            index, match = find_with_first_and_lastname(split[0], split[1])
            if index == -1 or match is None:
                miss.append(member.nick)
                continue

            if match.discord_user_id.value == -1:
                match.discord_user_id.value = member.id
                migrated.append(match)
                print(index, member.id, member.nick, member.global_name)

    for m in migrated:
        ffilter = {'ni': m.ni.value}
        operation = {'$set': {'discord_user_id': m.discord_user_id.value}}
        collection.update_one(ffilter, operation)

    print("Student not migrated")
    for m in miss:
        print(m)

    exit(-1)


def main():
    configuration = read_configurations(ConfigurationFilename.PRODUCTION)

    intents = discord.Intents.all()
    discord_client: DiscordClient = DiscordClient(
        command_prefix="!", intents=intents, server_id=configuration.server_id
    )

    client = connect_to_mongo_db(configuration.mongodb_connection_string)
    database = client[configuration.mongodb_database_name]
    students_collection = database[configuration.student_collection_name]

    unregistered_students = get_unregistered_students(students_collection)

    thread = threading.Thread(target=do, args=(students_collection, unregistered_students, discord_client))
    thread.start()

    time.sleep(0.5)

    # for student in unregistered_students:
    #     student["discord_user_id"] = 10
    #     print(student)

    discord_client.run(configuration.discord_token)


if __name__ == "__main__":
    main()

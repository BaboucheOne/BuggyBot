import argparse
import asyncio
import os
import sys
from typing import List

import discord
import pandas as pd
from discord import Member
from pandas import DataFrame
from pymongo import MongoClient
from pymongo.collection import Collection

from bot.config.environment.dotenv_configuration import DotEnvConfiguration
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.student.student import Student
from bot.infra.student.assembler.student_assembler import StudentAssembler
from tools.configuration_common import (
    add_configuration_argument,
    get_configuration,
    setup_logger,
)

global logger

ARGUMENT_FILENAME_KEY = "csv_filename"
INTEGRATION_ROLE_NAME = "Intégrations 2024"

EVELYA_PARTICIPANTS_LIST_COLUMNS_TO_KEEP: List[str] = [
    "Numéro de matricule / NI (9 chiffres, présent entre autre sur votre profil sur le portail et sur votre carte étudiante (virtuelle ou non))"
]

GOOGLE_FORM_LIST_COLUMNS_TO_KEEP: List[str] = [
    "ton NI (check ton profil dans monPortail)"
]

NOTIFY_INTEGRATION_ROLE = (
    "Boo booooo ! :wave:\n\n"
    "Juste un petit message pour te prévenir que tu as maintenant accès au salon de discussion #Integration 2024 ! :speech_left:\n"
    "Ce salon te permettra de recevoir toutes les informations nécessaires durant la semaine d'intégration. Assure-toi de le consulter attentivement ! :bell:\n\n"
    "On se retrouve lors des intégrations ! :rocket:\n\n"
    ":point_right: Si tu as des questions, n'hésite pas à les poser sur les channels Discord."
)


def read_arguments(arguments: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lire le fichier CSV.")
    parser.add_argument(
        ARGUMENT_FILENAME_KEY, type=str, help="Chemin vers le fichier CSV."
    )
    add_configuration_argument(parser)

    return parser.parse_args(arguments)


def connect_to_mongo_db(connection_url: str) -> MongoClient:
    try:
        return MongoClient(connection_url)
    except ConnectionError as e:
        logger.fatal(
            f"Impossible de se connecter à MongoDB. {e}", method="connect_to_mongo_db"
        )
        exit(-1)


async def start_discord_client(discord_client: DiscordClient, token: str):
    await discord_client.start(token)


async def stop_discord_client(discord_client: DiscordClient):
    await discord_client.close()


def select_correct_dataframe(file_path: str) -> DataFrame:
    try:
        return pd.read_excel(
            file_path, usecols=EVELYA_PARTICIPANTS_LIST_COLUMNS_TO_KEEP
        )
    except ValueError as e:
        logger.info(
            f"La colonne {EVELYA_PARTICIPANTS_LIST_COLUMNS_TO_KEEP} n'existe pas. Tentative de lecture du Google Form.",
            method="select_correct_dataframe",
            exception=e,
        )
        try:
            return pd.read_excel(file_path, usecols=GOOGLE_FORM_LIST_COLUMNS_TO_KEEP)
        except ValueError as e:
            logger.fatal(
                f"La colonne {GOOGLE_FORM_LIST_COLUMNS_TO_KEEP} n'existe pas. Impossible de lire le fichier.",
                method="select_correct_dataframe",
                exception=e,
            )
            exit(-1)


def read_participants_csv(file_path: str) -> List[int]:
    df: DataFrame = select_correct_dataframe(file_path)
    df = df.dropna()
    df = df.replace(r"\s+", "", regex=True)
    df = df.astype(int)
    return df.to_numpy().ravel().tolist()


def does_member_have_integration_role(member: Member) -> bool:
    return any(role.name == INTEGRATION_ROLE_NAME for role in member.roles)


async def add_role_to_student(member: Member, student: Student, role):
    try:
        await member.add_roles(role)
        logger.info(
            f"{student.firstname.value} {student.lastname.value} a bien son rôle : {role}.",
            method="add_role_to_student",
        )
    except (discord.Forbidden, discord.HTTPException) as e:
        logger.error(
            f"Impossible d'ajouter le role {role} à {student.firstname.value} {student.lastname.value}, {member.id} dû à {e}",
            method="add_role_to_student",
            exception=e,
        )


async def notify_new_role_to_student(member: Member, student: Student):
    try:
        await member.send(NOTIFY_INTEGRATION_ROLE)

        logger.info(
            f"{student.firstname.value} {student.lastname.value} a été notifié de son nouveau rôle.",
            method="notify_new_role_to_student",
        )
    except (discord.Forbidden, discord.HTTPException) as e:
        logger.error(
            f"Impossible d'envoyer un message à {student.firstname.value} {student.lastname.value} (ID: {member.id}) pour notifier son nouveau rôle en raison de : {e}",
            method="notify_new_role_to_student",
            exception=e,
        )


def find_students_with_nis(
    student_collection: Collection, nis: List[int]
) -> List[Student]:
    student_assembler: StudentAssembler = StudentAssembler()

    query = {"ni": {"$in": nis}}
    students_response = student_collection.find(query)

    students = [
        student_assembler.from_json(student_json) for student_json in students_response
    ]

    return students


async def main(arguments: List[str]):
    global logger

    arguments = read_arguments(arguments)
    configuration: DotEnvConfiguration = get_configuration(arguments)
    logger = setup_logger(configuration.logger_filename)

    if not os.path.exists(arguments.csv_filename):
        logger.fatal(
            f"Le fichier {arguments.csv_filename} n'existe pas. Impossible d'exécuter la commande.",
            method="main",
        )
        exit(-1)

    intents = discord.Intents.all()
    discord_client: DiscordClient = DiscordClient(
        command_prefix="!", intents=intents, server_id=configuration.server_id
    )

    discord_client_task = asyncio.create_task(
        start_discord_client(discord_client, configuration.discord_token)
    )

    while not discord_client.is_ready():
        logger.info("En attente du démarrage du client Discord.", method="main")
        await asyncio.sleep(2)

    client = connect_to_mongo_db(configuration.mongodb_connection_string)
    database = client[configuration.mongodb_database_name]
    student_collection = database[configuration.student_collection_name]

    participants_nis = read_participants_csv(arguments.csv_filename)
    students = find_students_with_nis(student_collection, participants_nis)

    try:
        integration_role = discord.utils.get(
            discord_client.server.roles, name=INTEGRATION_ROLE_NAME
        )

        for student in students:
            if student.discord_user_id.is_valid():
                member = discord_client.server.get_member(student.discord_user_id.value)
                if member and not does_member_have_integration_role(member):
                    await add_role_to_student(member, student, integration_role)
                    await notify_new_role_to_student(member, student)

        discord_client_task.cancel()
    except asyncio.CancelledError:
        client.close()
        await stop_discord_client(discord_client)

    logger.info(
        "La procédure d'ajout du role d'intégration s'est effectuée avec succès.",
        method="main",
    )


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))

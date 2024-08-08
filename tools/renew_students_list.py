import argparse
import asyncio
import sys
from typing import List

import discord
from discord import Member, Role
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import DeleteResult

from bot.config.environment.dotenv_configuration import DotEnvConfiguration
from bot.domain.constants import DiscordRole
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.utility import Utility
from tools.configuration_common import (
    add_configuration_argument,
    get_configuration,
    setup_logger,
)
from tools.update_students_list import update_list

global logger

ARGUMENT_FILENAME_KEY = "csv_filename"


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


def warn_user():
    logger.info(
        "/!\ ATTENTION /!\ Cette commande est IRRÉVERSIBLE et va retirer tous les grades aux étudiants.",
        method="warn_user",
    )
    response = input(
        f"Exécuter cette commande ? Utilisez: {', '.join(Utility.TRUE_BOOL_SET)} -> "
    )
    execute_command = Utility.str_to_bool(response)
    if not execute_command:
        logger.info(
            "L'utilisateur a choisi de ne pas utiliser la commande.",
            method="warn_user",
        )
        exit(0)
    logger.info(
        "L'utilisateur a choisi d'utiliser utiliser la commande.",
        method="warn_user",
    )


def flush_student_collection(student_collection: Collection):
    logger.info(
        "La base de données des étudiants va maintenant être supprimée.",
        method="flush_students_collection",
    )

    result: DeleteResult = student_collection.delete_many({})
    if result.deleted_count > 0:
        logger.info(
            f"Tous les étudiants de la base de données ont été supprimés. {result.deleted_count} supprimés.",
            method="flush_students_collection",
        )
    else:
        logger.info(
            "Aucun étudiant supprimé. La base de données devait être vide.",
            method="flush_students_collection",
        )

    logger.info(
        "La base de données des étudiants a bien été supprimée.",
        method="flush_students_collection",
    )


def populate_student_collection(configuration: DotEnvConfiguration, csv_filename: str):
    logger.info(
        f"Insertion des membres dans la base de données via le fichier {csv_filename}.",
        method="main",
    )
    students_to_inserted = update_list(configuration, csv_filename)
    logger.info(f"{students_to_inserted} nouveaux étudiants insérés.", method="main")
    logger.info("La table des étudiants a été réécrite.", method="main")


def get_member_uni_roles(member: Member) -> List[Role]:
    role_names = {
        DiscordRole.IFT,
        DiscordRole.GLO,
        DiscordRole.IIG,
        DiscordRole.CERTIFICATE,
    }
    return list(filter(lambda role: role.name in role_names, member.roles))


async def remove_roles_from_students(discord_client: DiscordClient):
    logger.info(
        "Les rôles de tous les étudiants vont maintenant être supprimés.",
        method="remove_roles_from_students",
    )

    for member in discord_client.get_all_members():
        try:
            roles = get_member_uni_roles(member)
            await member.remove_roles(*roles)
        except discord.Forbidden as e:
            logger.warning(
                f"Impossible d'enlever les rôles de {member.name}, permission refusée.",
                method="remove_roles_from_students",
                exception=e,
            )

    logger.info(
        "Tous les rôles ont bien été supprimés.", method="remove_roles_from_students"
    )


async def notify_students_to_register(discord_client: DiscordClient):
    logger.info(
        "Les étudiants vont maintenant être informés pour effectuer leurs enregistrements.",
        method="notify_students_to_register",
    )

    for member in discord_client.get_all_members():
        try:
            await member.send(
                "En ce début de nouvelle session, "
                "nous vous demandons de bien vouloir vous enregistrer à nouveau grâce à la commande !register TON_NI. "
                "Exemple : !register 111111111.\n "
                "Noter que si vous avez fait une demande de membre honorifique, "
                "celle-ci sera traitée dans les plus brefs délais et vous serez informé(e) en conséquence.\n"
                "Sur ce, bonne fin d'été à tous, et on se retrouve en septembre ! :tada:"
            )
        except discord.Forbidden as e:
            logger.warning(
                f"Impossible d'envoyer un message à {member.name}, permission refusée.",
                method="notify_students_to_register",
                exception=e,
            )

    logger.info(
        "Tous les étudiants ont été informés.", method="notify_students_to_register"
    )


async def main(arguments: List[str]):
    global logger

    arguments = read_arguments(arguments)
    configuration: DotEnvConfiguration = get_configuration(arguments)
    logger = setup_logger(configuration.logger_filename)

    intents = discord.Intents.all()
    discord_client: DiscordClient = DiscordClient(
        command_prefix="!", intents=intents, server_id=configuration.server_id
    )

    client = connect_to_mongo_db(configuration.mongodb_connection_string)
    database = client[configuration.mongodb_database_name]
    student_collection = database[configuration.student_collection_name]

    warn_user()

    await remove_roles_from_students(discord_client)
    flush_student_collection(student_collection)
    populate_student_collection(configuration, arguments.csv_filename)
    await notify_students_to_register(discord_client)

    logger.info("La procédure s'est effectuée avec succès.", method="main")


if __name__ == "__main__":
    asyncio.run(main(sys.argv))

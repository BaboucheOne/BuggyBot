import sys
import asyncio
import argparse
import os

current_script_path = os.path.dirname(os.path.realpath(__file__))
bot_directory_path = os.path.join(current_script_path, "..")
sys.path.append(bot_directory_path)
import migrate_discord_students  # noqa: E402
import update_students_list  # noqa: E402


TOOL_NAME_MIGRATE_STUDENT: str = "migrate_students"
TOOL_NAME_UPDATE_STUDENTS_LIST: str = "update_students_list"


def read_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lire le fichier CSV.")
    parser.add_argument(
        "migrate_or_update",
        type=str,
        help="Choisissez si vous voulez exécuter la migration des utilisateurs ou la mise à jour de la base de données.",
        choices=[TOOL_NAME_MIGRATE_STUDENT, TOOL_NAME_UPDATE_STUDENTS_LIST],
    )

    return parser.parse_args()


args = read_arguments()
if args.migration_or_update == TOOL_NAME_MIGRATE_STUDENT:
    asyncio.run(migrate_discord_students.main(arguments=sys.argv[2:]))
elif args.migration_or_update == TOOL_NAME_UPDATE_STUDENTS_LIST:
    asyncio.run(update_students_list.main(arguments=sys.argv[2:]))

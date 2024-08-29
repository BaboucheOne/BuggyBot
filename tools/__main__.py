import sys
import asyncio
import argparse
import os

current_script_path = os.path.dirname(os.path.realpath(__file__))
bot_directory_path = os.path.join(current_script_path, "..")
sys.path.append(bot_directory_path)
import migrate_discord_students  # noqa: E402
import update_students_list  # noqa: E402
import renew_students_list  # noqa: E402
import give_integration_role  # noqa: E402


TOOL_NAME_MIGRATE_STUDENT: str = "migrate_students"
TOOL_NAME_UPDATE_STUDENTS_LIST: str = "update_students_list"
TOOL_NAME_RENEW_STUDENTS_LIST: str = "renew_students_list"
TOOL_NAME_GIVE_INTEGRATION_ROLE: str = "give_integration_role"


def read_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute la commande au choix.")
    parser.add_argument(
        "command",
        type=str,
        help="Choisissez si vous voulez exécuter la migration des utilisateurs, la mise à jour de la base de données "
        "ou renouveller le discord.",
        choices=[
            TOOL_NAME_MIGRATE_STUDENT,
            TOOL_NAME_UPDATE_STUDENTS_LIST,
            TOOL_NAME_RENEW_STUDENTS_LIST,
            TOOL_NAME_GIVE_INTEGRATION_ROLE,
        ],
    )

    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments à passer à la commande choisie.",
    )

    return parser.parse_args()


args = read_arguments()
if args.command == TOOL_NAME_MIGRATE_STUDENT:
    asyncio.run(migrate_discord_students.main(arguments=sys.argv[2:]))
elif args.command == TOOL_NAME_UPDATE_STUDENTS_LIST:
    asyncio.run(update_students_list.main(arguments=sys.argv[2:]))
elif args.command == TOOL_NAME_RENEW_STUDENTS_LIST:
    asyncio.run(renew_students_list.main(arguments=sys.argv[2:]))
elif args.command == TOOL_NAME_GIVE_INTEGRATION_ROLE:
    asyncio.run(give_integration_role.main(arguments=sys.argv[2:]))

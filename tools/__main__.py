import sys
import asyncio
import argparse
import os

current_script_path = os.path.dirname(os.path.realpath(__file__))
bot_directory_path = os.path.join(current_script_path, '..')
sys.path.append(bot_directory_path)
import migrate_discord_students
import update_students_list

# write an argument parser with only one argument choosing whether to run the migration or the update
def read_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lire le fichier CSV.")
    parser.add_argument(
        "migration_or_update", type=str, help="Choose whether to run the migration or the update.", choices=["migration", "update"]
    )

    return parser.parse_args()

args = read_arguments()
if args.migration_or_update == "migration":
    asyncio.run(migrate_discord_students.main(arguments=sys.argv[2:]))
else:
    asyncio.run(update_students_list.main(arguments=sys.argv[2:]))
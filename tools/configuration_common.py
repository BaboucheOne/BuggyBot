import argparse
import logging

from bot.config.constants import ConfigurationFilename
from bot.config.dotenv_configuration import DotEnvConfiguration


def get_configuration(args: argparse.Namespace) -> DotEnvConfiguration:
    if args.env == "dev":
        print("La configuration de développement est en cours d'utilisation.")
        return DotEnvConfiguration(ConfigurationFilename.DEVELOPMENT)
    print("La configuration de production est en cours d'utilisation.")
    return DotEnvConfiguration(ConfigurationFilename.PRODUCTION)


def add_configuration_argument(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--env",
        type=str,
        nargs="?",
        dest="env",
        choices=["dev", "prod"],
        default="dev",
        help="Spécifier si le bot doit fonctionner en mode développement (dev) ou production (prod).",
    )


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("../buggy.log"), logging.StreamHandler()],
    )

import argparse
import logging

from bot.config.constants import ConfigurationFilename
from bot.config.environment.dotenv_configuration import DotEnvConfiguration
from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator


def get_configuration(args: argparse.Namespace) -> DotEnvConfiguration:
    if args.env == "dev":
        print("La configuration de développement est en cours d'utilisation.")
        return DotEnvConfiguration().from_file(ConfigurationFilename.DEVELOPMENT)
    print("La configuration de production est en cours d'utilisation.")
    return DotEnvConfiguration().from_file(ConfigurationFilename.PRODUCTION)


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


def setup_logger(filename: str) -> Logger:
    logger = Logger(f"../{filename}", logging.DEBUG)
    ServiceLocator.register_dependency(Logger, logger)
    return logger

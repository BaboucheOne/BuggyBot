import argparse

from bot.config.constants import ConfigurationFilename
from bot.config.dotenv_configuration import DotEnvConfiguration


def get_configuration(args: argparse.Namespace) -> DotEnvConfiguration:
    if args.env == "dev":
        print("Development configuration is being used.")
        return DotEnvConfiguration(ConfigurationFilename.DEVELOPMENT)
    print("Production configuration is being used.")
    return DotEnvConfiguration(ConfigurationFilename.PRODUCTION)


def add_configuration_argument(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--env",
        type=str,
        nargs="?",
        dest="env",
        choices=["dev", "prod"],
        default="dev",
        help="Specify if the bot should run in development (dev) or production (prod) mode",
    )

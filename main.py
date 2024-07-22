import asyncio
import argparse

from pymongo.errors import PyMongoError

from bot.config.environment.context.docker_context import DockerContext
from bot.config.logger.logger import Logger
from bot.config.environment.context.application_context import ApplicationContext
from bot.config.environment.context.development_context import DevelopmentContext
from bot.config.environment.context.production_context import ProductionContext
from bot.config.service_locator import ServiceLocator

LAUNCH_DEVELOPMENT_CONTEXT_NAME = "dev"
LAUNCH_PRODUCTION_CONTEXT_NAME = "prod"
LAUNCH_DOCKER_CONTEXT_NAME = "docker"


def read_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description="Essentiellement un agent des services frontaliers."
    )

    parser.add_argument(
        "--env",
        type=str,
        nargs="?",
        dest="env",
        choices=[
            LAUNCH_DEVELOPMENT_CONTEXT_NAME,
            LAUNCH_PRODUCTION_CONTEXT_NAME,
            LAUNCH_DOCKER_CONTEXT_NAME,
        ],
        default=LAUNCH_DEVELOPMENT_CONTEXT_NAME,
        help=(
            f"Spécifiez si le bot doit fonctionner en mode développement ({LAUNCH_DEVELOPMENT_CONTEXT_NAME}), "
            f"production ({LAUNCH_PRODUCTION_CONTEXT_NAME}) ou docker ({LAUNCH_DOCKER_CONTEXT_NAME}) mode"
        ),
    )

    return parser.parse_args()


def get_application_context(args: argparse.Namespace) -> ApplicationContext:
    if args.env == LAUNCH_DEVELOPMENT_CONTEXT_NAME:
        return DevelopmentContext()
    elif args.env == LAUNCH_PRODUCTION_CONTEXT_NAME:
        return ProductionContext()
    return DockerContext()


async def main():
    args = read_arguments()
    application_context = get_application_context(args)
    try:
        await application_context.build_application()
        ServiceLocator.get_dependency(Logger).info("main - Application construite.")
    except PyMongoError as e:
        ServiceLocator.get_dependency(Logger).fatal(
            f"main - {type(e).__name__}, "
            f"Impossible de se connecter à la base de données Mongo. Fermeture de l'application. {e}"
        )
        exit(-1)
    except Exception as e:
        ServiceLocator.get_dependency(Logger).fatal(
            f"main - {type(e).__name__}, "
            f"Une exception s'est produite lors de la construction de l'application. Fermeture de l'application. {e}"
        )
        exit(-1)

    ServiceLocator.get_dependency(Logger).info("main - Lancement de l'application.")
    await application_context.start_application()


if __name__ == "__main__":
    asyncio.run(main())

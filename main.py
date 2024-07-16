import asyncio
import argparse

from pymongo.errors import PyMongoError

from bot.config.context.docker_context import DockerContext
from bot.config.logger.logger import Logger
from bot.config.context.application_context import ApplicationContext
from bot.config.context.development_context import DevelopmentContext
from bot.config.context.production_context import ProductionContext
from bot.config.service_locator import ServiceLocator

LAUNCH_DEVELOPMENT_CONTEXT_NAME = "dev"
LAUNCH_PRODUCTION_CONTEXT_NAME = "prod"
LAUNCH_DOCKER_CONTEXT_NAME = "docker"


def read_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description="Discord bot which is basically a customs agent for the server"
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
            f"Specify if the bot should run in development ({LAUNCH_DEVELOPMENT_CONTEXT_NAME}), "
            f"production ({LAUNCH_PRODUCTION_CONTEXT_NAME}) or docker ({LAUNCH_DOCKER_CONTEXT_NAME}) mode"
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
        ServiceLocator.get_dependency(Logger).info("main - Application built.")
    except PyMongoError as e:
        ServiceLocator.get_dependency(Logger).fatal(
            f"main - Unable to connect to mongo database. Exiting the app. {e}"
        )
        exit(-1)
    except Exception as e:
        ServiceLocator.get_dependency(Logger).fatal(
            f"main - An exception occured while building the app. Exiting the app. {e}"
        )
        exit(-1)

    ServiceLocator.get_dependency(Logger).info("main - Launching application.")
    await application_context.start_application()


if __name__ == "__main__":
    asyncio.run(main())

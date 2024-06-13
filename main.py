import asyncio
import argparse

from pymongo.errors import PyMongoError

from bot.config.logger.logger import Logger
from bot.config.context.application_context import ApplicationContext
from bot.config.context.development_context import DevelopmentContext
from bot.config.context.production_context import ProductionContext
from bot.config.service_locator import ServiceLocator


def read_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description="Discord bot which is basically a customs agent for the server"
    )

    parser.add_argument(
        "--env",
        type=str,
        nargs="?",
        dest="env",
        choices=["dev", "prod"],
        default="dev",
        help="Specify if the bot should run in development (dev) or production (prod) mode",
    )

    return parser.parse_args()


def get_application_context(args: argparse.Namespace) -> ApplicationContext:
    if args.env == "dev":
        return DevelopmentContext()
    return ProductionContext()


async def main():
    args = read_arguments()
    application_context = get_application_context(args)
    try:
        await application_context.build_application()
        ServiceLocator.get_dependency(Logger).info(f"main - Application build.")
    except PyMongoError as e:
        ServiceLocator.get_dependency(Logger).fatal(
            f"main - Unable to connect to mongo database. Exiting the app. {e}"
        )
        exit(-1)
    except Exception as e:
        ServiceLocator.get_dependency(Logger).fatal(
            f"main - Exception occurs while building the app. Exiting the app. {e}"
        )
        exit(-1)

    ServiceLocator.get_dependency(Logger).info(f"main - Launching application.")
    await application_context.start_application()


if __name__ == "__main__":
    asyncio.run(main())

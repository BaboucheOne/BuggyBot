import asyncio
import argparse
import logging.config

from bot.config.application_context import ApplicationContext
from bot.config.development_context import DevelopmentContext
from bot.config.production_context import ProductionContext

logger = logging.getLogger(__name__)


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


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("buggy.log"), logging.StreamHandler()],
    )


async def main():
    setup_logger()

    args = read_arguments()
    application_context = get_application_context(args)
    try:
        await application_context.build_application()
    except ConnectionError as e:
        logger.fatal(f"Unable to connect to the MongoDB. Exiting the app. {e}")
        exit(-1)

    await application_context.start_application()


if __name__ == "__main__":
    asyncio.run(main())

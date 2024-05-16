import asyncio
import argparse

from bot.config.application_context import ApplicationContext
from bot.config.development_context import DevelopmentContext
from bot.config.production_context import ProductionContext


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
        print("Development context is being used.")
        return DevelopmentContext()
    print("Production context is being used.")
    return ProductionContext()


async def main():
    args = read_arguments()

    application_context = get_application_context(args)
    await application_context.build_application()
    await application_context.start_application()


if __name__ == "__main__":
    asyncio.run(main())

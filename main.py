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
        description="Bot Discord qui est essentiellement un agent des douanes pour le serveur."
    )

    parser.add_argument(
        "--env",
        type=str,
        nargs="?",
        dest="env",
        choices=["dev", "prod"],
        default="dev",
        help="Spécifiez si le bot doit fonctionner en mode développement (dev) ou production (prod)",
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
        ServiceLocator.get_dependency(Logger).info("main - Application construite.")
    except PyMongoError as e:
        ServiceLocator.get_dependency(Logger).fatal(
            f"main - Impossible de se connecter à la base de données Mongo. Fermeture de l'application. {e}"
        )
        exit(-1)
    except Exception as e:
        ServiceLocator.get_dependency(Logger).fatal(
            f"main - Une exception s'est produite lors de la construction de l'application. Fermeture de l'application. {e}"
        )
        exit(-1)

    ServiceLocator.get_dependency(Logger).info("main - Lancement de l'application.")
    await application_context.start_application()


if __name__ == "__main__":
    asyncio.run(main())

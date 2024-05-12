import os
import asyncio
import discord
import argparse
from discord.ext import commands
from dotenv import load_dotenv


from bot.cog.registration.register_member import RegisterMemberCog
from bot.config.context import ServiceLocator


def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    return commands.Bot(command_prefix="!", intents=intents)


async def register_cogs(bot: commands.Bot):
    await bot.add_cog(RegisterMemberCog(bot))


def read_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Discord bot which is basically a customs agent for the server")

    parser.add_argument("--env",
                        type=str,
                        nargs="?",
                        choices=["dev", "prod"],
                        default="prod",
                        help="Specify if the bot should run in development (dev) or production (prod) mode")

    return parser.parse_args()


async def main():
    args = read_arguments()
    service_locator = ServiceLocator(args.env)
    mode_service = service_locator.get_database_service()



    bot = create_bot()
    await register_cogs(bot)

    # bot.run(discord_token)


if __name__ == "__main__":
    asyncio.run(main())

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot.cog.registration.register_member import RegisterMemberCog


def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    return commands.Bot(command_prefix="!", intents=intents)


async def register_cogs(bot: commands.Bot):
    await bot.add_cog(RegisterMemberCog(bot))


async def main():
    load_dotenv()
    _ = os.getenv("DISCORD_TOKEN")

    bot = create_bot()
    await register_cogs(bot)

    # bot.run(discord_token)


if __name__ == "__main__":
    asyncio.run(main())

import discord
from discord import Message
from discord.ext import commands

from bot.cog.chain_of_responsibility.handlers.keep_digits_handler import KeepDigitsHandler
from bot.cog.chain_of_responsibility.handlers.strip_handler import StripHandler
from bot.cog.chain_of_responsibility.responsibility_builder import ResponsibilityBuilder
from bot.domain.student.attributs.ni import NI


class RegisterMemberCog(commands.Cog):

    NI_DIGITS_COUNT = 9

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ni_sanitizer = ResponsibilityBuilder()\
            .with_handler(StripHandler())\
            .with_handler(KeepDigitsHandler()).build()

    def __is_self(self, message: Message) -> bool:
        return message.author == self.bot.user

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(f"Hi {member.name}, welcome to my Discord server!")

    @commands.Cog.listener("on_message")
    async def retrieve_ni(self, message: Message):
        if self.__is_self(message):
            return

        if isinstance(message.channel, discord.channel.DMChannel):
            sanitized_ni = self.ni_sanitizer.handle(message.content)
            if len(sanitized_ni) is not self.NI_DIGITS_COUNT:
                await message.channel.send("Bad NI")
                await self.bot.process_commands(message)
                return

            _ = NI(int(sanitized_ni))
            await message.channel.send("Good NI")
            await self.bot.process_commands(message)

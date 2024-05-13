import discord
from discord import Message
from discord.ext import commands

from bot.application.student.student_service import (
    StudentService,
    StudentAlreadyRegisteredException,
)
from bot.cog.chain_of_responsibility.handlers.keep_digits_handler import (
    KeepDigitsHandler,
)
from bot.cog.chain_of_responsibility.handlers.strip_handler import StripHandler
from bot.cog.chain_of_responsibility.responsibility_builder import ResponsibilityBuilder


class RegisterMemberCog(commands.Cog):

    def __init__(self, bot: commands.Bot, student_service: StudentService):
        self.__bot = bot
        self.__student_service = student_service
        self.__ni_sanitizer = (
            ResponsibilityBuilder()
            .with_handler(StripHandler())
            .with_handler(KeepDigitsHandler())
            .build()
        )

    def __is_self(self, message: Message) -> bool:
        return message.author == self.__bot.user

    def __is_dm_message(self, message: Message) -> bool:
        return isinstance(message.channel, discord.channel.DMChannel)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(f"Hi {member.name}, welcome to my Discord server!")

    @commands.Cog.listener("on_message")
    async def retrieve_ni(self, message: Message):
        if self.__is_self(message) or not self.__is_dm_message(message):
            return

        try:
            ni = self.__ni_sanitizer.handle(message.content)
            self.__student_service.register_student(ni, message.author.id)
            await message.channel.send("Good NI")
        except StudentAlreadyRegisteredException:
            await message.channel.send(
                "Your are already registered.\nIf you haven't registered yet, please contact an admin."
            )
        except Exception as e:
            await message.channel.send(
                "Unable to registered you.\nCheck your NI. If your NI is the good one, please contact an admin."
            )
            print(e)
            await self.__bot.process_commands(message)

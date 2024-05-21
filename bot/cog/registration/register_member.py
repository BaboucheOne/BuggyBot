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
from bot.cog.constants import ReplyMessage
from bot.config.service_locator import ServiceLocator


class RegisterMemberCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__student_service: StudentService = ServiceLocator.get_dependency(
            StudentService
        )
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
        await member.dm_channel.send(ReplyMessage.WELCOME)

    @commands.command(name="add_student")
    async def add_student(self, message: Message):
        if self.__is_self(message) or not self.__is_dm_message(message):
            return

        try:
            # TODO : Create a request class.
            # TODO : Add a not empty string handler.
            arguments = message.content.split(" ")
            ni = arguments[0].strip()
            firstname = arguments[1].strip()
            lastname = arguments[2].strip()
            program = arguments[3].strip()
            new_admitted = arguments[4].strip()

            self.__student_service.add_student(
                ni, firstname, lastname, program, new_admitted
            )

        except Exception:
            pass

    @commands.Cog.listener("on_message")
    async def retrieve_ni(self, message: Message):
        if self.__is_self(message) or not self.__is_dm_message(message):
            return

        try:
            ni = self.__ni_sanitizer.handle(message.content)
            # TODO : Create a request class.
            self.__student_service.register_student(ni, message.author.id)
            await message.channel.send(ReplyMessage.SUCCESSFUL_REGISTRATION)
        except StudentAlreadyRegisteredException:
            await message.channel.send(ReplyMessage.ALREADY_REGISTERED)
        except Exception:
            await message.channel.send(ReplyMessage.UNABLE_TO_REGISTER)
        finally:
            await self.__bot.process_commands(message)

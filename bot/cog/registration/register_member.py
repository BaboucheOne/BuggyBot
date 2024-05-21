import discord
from discord import Message
from discord.ext import commands

from bot.application.student.exceptions.student_already_exist import (
    StudentAlreadyExistsException,
)
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
from bot.cog.registration.add_student_request_factory import AddStudentRequestFactory
from bot.cog.request.register_student_request import RegisterStudentRequest
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

        self.__add_student_request_factory = AddStudentRequestFactory(
            self.__ni_sanitizer
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
            add_student_request = self.__add_student_request_factory.create(
                message.content
            )

            self.__student_service.add_student(add_student_request)

            await message.channel.send(ReplyMessage.SUCCESSFUL_STUDENT_ADDED)
        except StudentAlreadyExistsException:
            await message.channel.send(ReplyMessage.STUDENT_ALREADY_EXISTS)
        except Exception as e:
            print(f"Exception occurs {e}")
        finally:
            await self.__bot.process_commands(message)

    @commands.Cog.listener("on_message")
    async def retrieve_ni(self, message: Message):
        if self.__is_self(message) or not self.__is_dm_message(message):
            return

        try:
            ni = self.__ni_sanitizer.handle(message.content)
            register_student_request = RegisterStudentRequest(ni, message.author.id)

            self.__student_service.register_student(register_student_request)

            await message.channel.send(ReplyMessage.SUCCESSFUL_REGISTRATION)
        except StudentAlreadyRegisteredException:
            await message.channel.send(ReplyMessage.ALREADY_REGISTERED)
        except Exception:
            await message.channel.send(ReplyMessage.UNABLE_TO_REGISTER)
        finally:
            await self.__bot.process_commands(message)

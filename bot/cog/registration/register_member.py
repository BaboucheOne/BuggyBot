from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

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
from bot.cog.exceptions.missing_arguments_exception import MissingArgumentsException
from bot.cog.registration.add_student_request_factory import AddStudentRequestFactory
from bot.cog.request.register_student_request import RegisterStudentRequest
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient


class RegisterMemberCog(commands.Cog):

    def __init__(self):
        self.__bot = ServiceLocator.get_dependency(DiscordClient)
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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(ReplyMessage.WELCOME)

    @commands.command(name="add_student")
    @commands.dm_only()
    async def add_student(self, context: Context):
        message = context.message
        if self.__is_self(message):
            return

        try:
            add_student_request = self.__add_student_request_factory.create(
                message.content
            )

            self.__student_service.add_student(add_student_request)

            await message.channel.send(ReplyMessage.SUCCESSFUL_STUDENT_ADDED)
        except StudentAlreadyExistsException:
            await message.channel.send(ReplyMessage.STUDENT_ALREADY_EXISTS)
        except MissingArgumentsException:
            await message.channel.send(ReplyMessage.MISSING_ARGUMENTS_IN_COMMAND)
        except Exception as e:
            print(f"Exception occurs {e}")
        finally:
            await self.__bot.process_commands(message)

    @commands.Cog.listener("on_message")
    @commands.dm_only()
    async def retrieve_ni(self, message: Message):
        if self.__is_self(message):
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

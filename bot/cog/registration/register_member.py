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

        await member.dm_channel.send(f"Bienvenue {member.name} dans le serveur Discord de l'ASETIN (Association des étudiantes et étudiants en informatique)! \n"
                                     f"L'ASETIN représente les intérêts des étudiantes et étudiants de premier cycle en informatique auprès des différentes instances officielles de l’Université Laval,"
                                     f" sur les différents comités et devant les autres associations étudiantes."
                                     f"Afin de confirmer que tu es bel et bien un(e) étudiant(e) inscrit(e) à l'association, entre ton numéro d'identification personnel (NI).\n"
                                     f"Au plaisir de te rencontrer!\n"
                                     f"ps: Si tu ne sais pas où trouver ton NI, tu peux le consulter sur MonPortail ou encore sur ta carte étudiante.")

        await member.dm_channel.send(ReplyMessage.WELCOME)

    @commands.Cog.listener("on_message")
    async def retrieve_ni(self, message: Message):
        if self.__is_self(message) or not self.__is_dm_message(message):
            return

        try:
            ni = self.__ni_sanitizer.handle(message.content)
            self.__student_service.register_student(ni, message.author.id)
            await message.channel.send(ReplyMessage.SUCCESSFUL_REGISTRATION)
        except StudentAlreadyRegisteredException:
            await message.channel.send(ReplyMessage.ALREADY_REGISTERED)
        except Exception:
            await message.channel.send(ReplyMessage.UNABLE_TO_REGISTER)
            await self.__bot.process_commands(message)
            

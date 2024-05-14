from discord.ext import commands

from bot.application.discord.events.student_registered.student_registered_observer import (
    StudentRegisteredObserver,
)
from bot.domain.student.attributs.ni import NI
from bot.domain.student.student_repository import StudentRepository


class DiscordService(StudentRegisteredObserver):

    def __init__(self, bot: commands.Bot, student_repository: StudentRepository):
        self.__bot = bot
        self.__student_repository = student_repository

    def on_student_registered(self, ni: NI):
        student = self.__student_repository.find_student_by_ni(ni)
        print(
            f"new student registered with ni {student.ni.value} and discord id {student.discord_user_id.value}. {student.firstname.value} {student.lastname.value}"
        )

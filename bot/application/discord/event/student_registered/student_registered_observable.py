from typing import List

from discord import Member

from bot.application.discord.event.student_registered.student_registered_observer import (
    StudentRegisteredObserver,
)
from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.ni import NI


class StudentRegisteredObservable:
    def __init__(self):
        self.__observers: List[StudentRegisteredObserver] = []

    def register_to_on_student_registered(self, observer: StudentRegisteredObserver):
        self.__observers.append(observer)

    def unregister_all_from_on_student_registered(self):
        self.__observers.clear()

    def notify_on_student_registered(self, ni: NI):
        for observer in self.__observers:
            observer.on_student_registered(ni)

    def notify_on_student_unregistered(self, discord_user_id: DiscordUserId):
        for observer in self.__observers:
            observer.on_student_unregistered(discord_user_id)

    def notify_on_member_removed(self, member: Member):
        for observer in self.__observers:
            observer.on_member_removed(member)

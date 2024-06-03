from typing import List

from bot.application.discord.events.student_registered.student_registered_observer import (
    StudentRegisteredObserver,
)
from bot.domain.student.attributs.discord_user_id import DiscordUserId
from bot.domain.student.attributs.ni import NI


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

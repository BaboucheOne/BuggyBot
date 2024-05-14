from abc import ABC, abstractmethod

from bot.domain.student.attributs.discord_user_id import DiscordUserId
from bot.domain.student.attributs.ni import NI
from bot.domain.student.student import Student


class StudentRepository(ABC):
    @abstractmethod
    def find_student_by_ni(self, ni: NI) -> Student:
        pass

    @abstractmethod
    def update_student(self, student: Student):
        pass

    @abstractmethod
    def register_student(self, ni: NI, discord_user_id: DiscordUserId):
        pass

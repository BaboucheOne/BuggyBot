from abc import ABC, abstractmethod
from typing import List

from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.ni import NI
from bot.domain.student.student import Student


class StudentRepository(ABC):
    @abstractmethod
    def find_students_by_discord_user_id(
        self, discord_user_id: DiscordUserId
    ) -> List[Student]:
        pass

    @abstractmethod
    def find_student_by_ni(self, ni: NI) -> Student:
        pass

    @abstractmethod
    def add_student(self, student: Student):
        pass

    @abstractmethod
    def update_student(self, student: Student):
        pass

    @abstractmethod
    def register_student(self, ni: NI, discord_user_id: DiscordUserId):
        pass

    @abstractmethod
    def unregister_student(self, ni: NI, discord_user_id: DiscordUserId):
        pass

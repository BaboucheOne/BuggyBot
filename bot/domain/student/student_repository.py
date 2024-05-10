from abc import ABC, abstractmethod

from bot.domain.student.student import Student


class StudentRepository(ABC):
    @abstractmethod
    def get_student_by_ni(self, ni: str) -> Student:
        pass

    @abstractmethod
    def update_student(self, student: Student):
        pass

from abc import ABC, abstractmethod

from bot.domain.student.attributs.ni import NI


class StudentRegisteredObserver(ABC):
    @abstractmethod
    def on_student_registered(self, ni: NI):
        pass

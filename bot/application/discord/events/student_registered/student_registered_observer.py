from abc import ABC, abstractmethod

from bot.domain.student.attributs.discord_user_id import DiscordUserId
from bot.domain.student.attributs.ni import NI


class StudentRegisteredObserver(ABC):
    @abstractmethod
    def on_student_registered(self, ni: NI):
        pass

    @abstractmethod
    def on_student_unregistered(self, discord_user_id: DiscordUserId):
        pass

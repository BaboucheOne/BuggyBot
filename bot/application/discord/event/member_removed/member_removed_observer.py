from abc import ABC, abstractmethod

from discord import Member

from bot.domain.student.attribut.discord_user_id import DiscordUserId
from bot.domain.student.attribut.ni import NI


class MemberRemovedObserver(ABC):
    @abstractmethod
    def on_member_removed(self, member: Member):
        pass

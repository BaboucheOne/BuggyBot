from abc import ABC, abstractmethod

from discord import Member


class MemberRemovedObserver(ABC):
    @abstractmethod
    async def on_member_removed(self, member: Member):
        pass

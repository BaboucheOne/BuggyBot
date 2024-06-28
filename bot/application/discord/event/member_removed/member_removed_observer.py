from abc import ABC, abstractmethod

from discord import Member



class MemberRemovedObserver(ABC):
    @abstractmethod
    def on_member_removed(self, member: Member):
        pass

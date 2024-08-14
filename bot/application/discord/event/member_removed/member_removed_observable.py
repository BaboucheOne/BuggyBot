from typing import List

from discord import Member

from bot.application.discord.event.member_removed.member_removed_observer import (
    MemberRemovedObserver,
)


class MemberRemovedObservable:
    def __init__(self):
        self.__observers: List[MemberRemovedObserver] = []

    def register_to_on_member_registered(self, observer: MemberRemovedObserver):
        self.__observers.append(observer)

    def unregister_all_from_on_member_registered(self):
        self.__observers.clear()

    async def notify_on_member_removed(self, member: Member):
        for observer in self.__observers:
            await observer.on_member_removed(member)

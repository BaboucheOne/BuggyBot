import discord

from datetime import datetime, timezone, timedelta
from typing import List, Callable

from discord import Member

from bot.config.logger.logger import Logger
from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient
from bot.domain.task.task import Task


class KickUnregisteredUserTask(Task):

    KICK_REASON: str = (
        "Vous avez rejoint le serveur il y a plus d'une semaine et vous ne vous êtes pas enregistré. "
        "Par conséquent, vous avez été ejecté du serveur. Il est possible de rejoindre le serveur à "
        "nouveau et de vous identifier."
    )

    FIRST_OF_AUGUST = (8, 1)
    FIFTEENTH_OF_SEPTEMBER = (9, 15)

    def __init__(self, discord_client: DiscordClient, schedule_method: Callable):
        super().__init__(schedule_method)
        self.__discord_client: DiscordClient = discord_client
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    def __is_in_school_start_period(self) -> bool:
        today_date = datetime.now()
        today_month_day = today_date.month, today_date.day
        return self.FIRST_OF_AUGUST <= today_month_day <= self.FIFTEENTH_OF_SEPTEMBER

    def __has_no_role(self, member: Member) -> bool:
        return len(member.roles) == 1

    def __has_joined_one_week_ago(self, member: Member):
        one_week_ago = datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(
            weeks=1
        )
        return member.joined_at <= one_week_ago

    async def do(self):
        self.__logger.info("Début de la tâche.", method="do")

        if self.__is_in_begging_of_school():
            self.__logger.info(
                "La tâche d'expulsion ne s'exécutera pas car nous sommes dans la période de la rentrée scolaire.",
                method="do",
            )
            self.__logger.info("Fin de la tâche.", method="do")
            return

        no_role_members: List[Member] = list(
            filter(self.__has_no_role, self.__discord_client.server.members)
        )
        verification_expired_members: List[Member] = list(
            filter(self.__has_joined_one_week_ago, no_role_members)
        )

        self.__logger.info(
            f"{len(verification_expired_members)} utilisateur(s) vont être expulsé(s).",
            method="do",
        )

        for member in verification_expired_members:
            try:
                await member.kick(reason=self.KICK_REASON)
                self.__logger.info(f"{member.name} a été expulsé.", method="do")
            except discord.Forbidden as e:
                self.__logger.warning(
                    f"Impossible d'expulser {member.nick}, permission refusée.",
                    method="do",
                    exception=e,
                )
            except discord.NotFound as e:
                self.__logger.info(
                    f"Impossible d'expulser {member.nick}, non trouvé.",
                    method="do",
                    exception=e,
                )
            except discord.HTTPException as e:
                self.__logger.error(
                    f"Impossible d'expulser {member.nick}, erreur http {e}.",
                    method="do",
                    exception=e,
                )

        self.__logger.info("Fin de la tâche.", method="do")

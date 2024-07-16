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

    def __init__(self, discord_client: DiscordClient, schedule_method: Callable):
        super().__init__(schedule_method)
        self.__discord_client: DiscordClient = discord_client
        self.__logger: Logger = ServiceLocator.get_dependency(Logger)

    def __has_no_role(self, member: Member) -> bool:
        return len(member.roles) == 1

    def __has_joined_one_week_ago(self, member: Member):
        one_week_ago = datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(
            weeks=1
        )
        return member.joined_at <= one_week_ago

    async def do(self):
        self.__logger.info("KickUnregisteredUserTask - Début de la tâche.")

        no_role_members: List[Member] = list(
            filter(self.__has_no_role, self.__discord_client.server.members)
        )
        verification_expired_members: List[Member] = list(
            filter(self.__has_joined_one_week_ago, no_role_members)
        )

        self.__logger.info(
            f"KickUnregisteredUserTask - {len(verification_expired_members)} utilisateur(s) vont être expulsé(s)."
        )

        for member in verification_expired_members:
            try:
                await member.kick(reason=self.KICK_REASON)
                self.__logger.info(
                    f"KickUnregisteredUserTask - {member.name} a été expulsé."
                )
            except discord.Forbidden:
                self.__logger.info(
                    f"KickUnregisteredUserTask - mpossible d'expulser {member.nick}, permission refusée."
                )
            except discord.NotFound:
                self.__logger.info(
                    f"KickUnregisteredUserTask - mpossible d'expulser {member.nick}, non trouvé."
                )
            except discord.HTTPException as e:
                self.__logger.info(
                    f"KickUnregisteredUserTask - mpossible d'expulser {member.nick}, erreur http {e}."
                )

        self.__logger.info("KickUnregisteredUserTask - Fin de la tâche.")

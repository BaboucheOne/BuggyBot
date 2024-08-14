from bot.config.service_locator import ServiceLocator
from bot.domain.discord_client.discord_client import DiscordClient
from bot.resource.exception.missing_arguments_exception import MissingArgumentsException


class Utility:

    TRUE_BOOL_SET = {"true", "1", "yes", "y", "oui", "o"}

    @staticmethod
    def str_to_bool(s: str):
        return s.lower() in Utility.TRUE_BOOL_SET

    @staticmethod
    def get_content_without_command(content: str):
        args = content.split()
        if len(args) < 2:
            raise MissingArgumentsException(0)
        return " ".join(args[1:])

    @staticmethod
    def does_user_exist_on_server(discord_id: int) -> bool:
        discord_client: DiscordClient = ServiceLocator.get_dependency(DiscordClient)

        return discord_client.get_user(discord_id) is not None

import os

from dotenv import load_dotenv, find_dotenv

from bot.config.constants import DotenvConfigurationKey


class DotEnvConfiguration:
    def __init__(self):
        pass

    def from_file(self, filename: str):
        dotenv_path = find_dotenv(filename=filename)
        load_dotenv(dotenv_path=dotenv_path)

    @property
    def mongodb_connection_string(self) -> str:
        return os.getenv(DotenvConfigurationKey.MONGODB_CONNECTION_STRING)

    @property
    def mongodb_connection_timeout_ms(self) -> int:
        return int(os.getenv(DotenvConfigurationKey.MONGODB_CONNECTION_TIMEOUT_MS))

    @property
    def mongodb_database_name(self) -> str:
        return os.getenv(DotenvConfigurationKey.MONGODB_DATABASE_NAME)

    @property
    def student_collection_name(self) -> str:
        return os.getenv(DotenvConfigurationKey.STUDENT_COLLECTION_NAME)

    @property
    def discord_token(self) -> str:
        return os.getenv(DotenvConfigurationKey.DISCORD_TOKEN)

    @property
    def server_id(self) -> int:
        return int(os.getenv(DotenvConfigurationKey.SERVER_ID))

    @property
    def logger_filename(self) -> str:
        return os.getenv(DotenvConfigurationKey.LOGGER_FILENAME)

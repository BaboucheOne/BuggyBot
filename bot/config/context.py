from dotenv import load_dotenv
import os


class ModeService:
    def __init__(self):
        self.CONNECTION_STRING = None
        self.DB_NAME = None
        self.TOKEN = None
        self.GUILD_ID = None


class ProductionModeService(ModeService):

    def __init__(self):
        super().__init__()
        load_dotenv(".env.prod")
        self.CONNECTION_STRING = os.getenv("MONGODB_SERVER_CONNECTION_STRING")
        self.DB_NAME = os.getenv("MONGODB_DB_NAME")
        self.TOKEN = os.getenv("DISCORD_TOKEN")
        self.GUILD_ID = os.getenv("DISCORD_GUILD_ID")


class DevelopmentModeService(ModeService):

    def __init__(self):
        super().__init__()
        load_dotenv(".env.dev")
        self.CONNECTION_STRING = os.getenv("MONGODB_LOCALHOST_SERVER_CONNECTION_STRING")
        self.DB_NAME = os.getenv("MONGODB_DB_NAME")
        self.TOKEN = os.getenv("DISCORD_TOKEN")
        self.GUILD_ID = os.getenv("DISCORD_GUILD_ID")


class Cache:
    def __init__(self):
        self.services = []

    def add_service(self, service: ModeService):

        for s in self.services:
            if s.__class__.__name__ == service.__class__.__name__:
                return

        self.services.append(service)

    def get_service(self, service_name: str) -> ModeService:
        for service in self.services:
            if service.__class__.__name__ == service_name:
                return service
        return None


class ServiceLocator:
    cache = Cache()

    def get_service(self, service_name: str == "prod") -> ModeService:
        service = self.cache.get_service(service_name)
        if service is None:
            context_service = InitialContext(str)
            service = context_service.get_database_service()
            self.cache.add_service(service)

        return service


class InitialContext:
    def __init__(self, mode: str):
        self.mode = mode

    def set_mode(self, mode: str):
        self.mode = mode

    def get_database_service(self) -> ModeService:
        if self.mode == "prod":
            return ProductionModeService()
        else:
            return DevelopmentModeService()

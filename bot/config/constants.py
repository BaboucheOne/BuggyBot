class ConfigurationFilename:
    PRODUCTION: str = ".env.prod"
    DEVELOPMENT: str = ".env.dev"


class DotenvConfigurationKey:
    MONGODB_CONNECTION_STRING: str = "MONGODB_CONNECTION_STRING"
    MONGODB_DATABASE_NAME: str = "MONGODB_DATABASE_NAME"
    STUDENT_COLLECTION_NAME: str = "STUDENT_COLLECTION_NAME"
    DISCORD_TOKEN: str = "DISCORD_TOKEN"
    SERVER_ID: str = "SERVER_ID"

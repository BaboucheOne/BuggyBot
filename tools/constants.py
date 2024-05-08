class Filename:
    ENV = ".env"


class StudentListKey:
    NI: str = "NI"
    PROGRAM_CODE: str = "CODE_PROGRAMME"
    LASTNAME: str = "Nom"
    FIRSTNAME: str = "Prenom"
    NEW: str = "NOUVEAUX"
    DISCORD_USER_ID: str = "DiscordUserId"


class StudentMongoDbKey:
    NI: str = "ni"
    FIRSTNAME: str = "firstname"
    LASTNAME: str = "lastname"
    PROGRAM_CODE: str = "program_code"
    NEW: str = "new"
    DISCORD_USER_ID: str = "discord_user_id"


class UniProgram:
    IFT: str = "B-IFT"
    GLO: str = "B-GLO"
    IIG: str = "B-IIG"
    CERTIFICATE: str = "C-IFT"

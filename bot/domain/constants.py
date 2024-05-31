from typing import List


class UniProgram:
    IFT: str = "B-IFT"
    GLO: str = "B-GLO"
    IIG: str = "B-IIG"
    CERTIFICATE: str = "C-IFT"


class DiscordRole:
    IFT: str = "IFT"
    GLO: str = "GLO"
    IIG: str = "IIG"
    CERTIFICATE: str = "CERTIFICAT"

    ASETIN: str = "ASETIN"
    AEGLO: str = "AEGLO"
    ADMIN: str = "ADMIN"

    ADMINS: List[str] = [ASETIN, AEGLO, ADMIN]

from typing import List


class UniProgram:
    IFT: str = "B-IFT"
    GLO: str = "B-GLO"
    IIG: str = "B-IIG"
    CERTIFICATE: str = "C-IFT"
    HONORIFIQUE: str = "HONORIFIQUE"


class DiscordRole:
    IFT: str = "IFT"
    GLO: str = "GLO"
    IIG: str = "IIG"
    CERTIFICATE: str = "CERTIFICAT"

    HONORIFIQUE: str = "Membre Honorifique"

    ASETIN: str = "ASETIN"
    AEGLO: str = "AEGLO"
    ADMIN: str = "Admin"

    ADMINS: List[str] = [ASETIN, ADMIN]

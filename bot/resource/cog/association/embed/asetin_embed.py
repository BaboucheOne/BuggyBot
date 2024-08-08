from discord import Embed


class AsetinEmbed:
    TITLE: str = "ASETIN"
    TITLE_URL: str = "https://www.facebook.com/groups/180156004739308"
    DESCRIPTION: str = (
        "Association des étudiants et étudiantes en informatique de l'Université Laval"
    )
    COLOR: int = 0xFC03C6

    THUMBNAIL_URL: str = "https://asetin.ift.ulaval.ca/res/img/logo_540.png"

    WHO_WE_ARE_FIELD_NAME: str = "Qui sommes-nous?"
    WHO_WE_ARE_FIELD_DESCRIPTION: str = (
        "Nous sommes votre association étudiante, dédiée à offrir une variété de services aux étudiants. Nos activités incluent : \n- L'assistance aux étudiants.\n- L'organisation de concours.\n- La planification d'événements.\n- Un lieu de rencontre convivial.\nL'ASETIN représente les intérêts des étudiants et étudiantes de premier cycle en informatique auprès des différentes instances officielles de l’Université Laval, sur les différents comités et devant les autres associations étudiantes."
    )

    PART_OF_FIELD_NAME: str = "Qui en fait partie?"
    PART_OF_FIELD_VALUE: str = (
        "- Informatique\n- Génie logiciel\n- Informatique et gestion\n- Certificats en informatique"
    )

    LOCAL_FIELD_NAME: str = "Local"
    LOCAL_FIELD_VALUE: str = "PLT-3902"

    LINK_FIELD_NAME: str = "Réseaux"
    LINK_FIELD_VALUE: str = (
        "[Facebook](https://www.facebook.com/groups/180156004739308)\n[Instagram](https://www.instagram.com/asetin_ulaval/)\n[Site web](https://asetin.ift.ulaval.ca/)"
    )

    FOOTER_TEXT: str = (
        "Pro tip: Restez informé via le Discord, le groupe Facebook ou la page Instagram!"
    )

    def __init__(self):
        self.embed = Embed(
            title=self.TITLE,
            url=self.TITLE_URL,
            description=self.DESCRIPTION,
            color=self.COLOR,
        )
        self.embed.set_thumbnail(url=self.THUMBNAIL_URL)

        self.embed.add_field(
            name=self.WHO_WE_ARE_FIELD_NAME,
            value=self.WHO_WE_ARE_FIELD_DESCRIPTION,
            inline=False,
        )
        self.embed.add_field(
            name=self.PART_OF_FIELD_NAME, value=self.PART_OF_FIELD_VALUE, inline=True
        )
        self.embed.add_field(
            name=self.LOCAL_FIELD_NAME, value=self.LOCAL_FIELD_VALUE, inline=True
        )
        self.embed.add_field(
            name=self.LINK_FIELD_NAME, value=self.LINK_FIELD_VALUE, inline=False
        )

        self.embed.set_footer(text=self.FOOTER_TEXT)

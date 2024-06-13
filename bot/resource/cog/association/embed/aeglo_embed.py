from discord import Embed


class AegloEmbed:
    TITLE: str = "AEGLO"
    TITLE_URL: str = "https://www.facebook.com/groups/aeglo"
    DESCRIPTION: str = (
        "Association des étudiants et étudiantes en génie logiciel de l'Université Laval"
    )
    COLOR: int = 0x000000

    THUMBNAIL_URL: str = "https://aeglo.ift.ulaval.ca/aeglo_logo.png"

    WHO_WE_ARE_FIELD_NAME: str = "Qui sommes-nous?"
    WHO_WE_ARE_FIELD_DESCRIPTION: str = (
        "Nous sommes votre association étudiante, dédiée à offrir une variété de services aux étudiants. Nos activités incluent : \n- L'assistance aux étudiants.\n- La planification d'événements.\n- Un lieu de rencontre convivial."
    )

    PART_OF_FIELD_NAME: str = "Qui en fait partie?"
    PART_OF_FIELD_VALUE: str = "Étudiant en génie logiciel"

    LOCAL_FIELD_NAME: str = "Local"
    LOCAL_FIELD_VALUE: str = "VCH-00113"

    LINK_FIELD_NAME: str = "Réseaux"
    LINK_FIELD_VALUE: str = (
        "[Facebook](https://www.facebook.com/groups/aeglo)\n[Site web](https://aeglo.ift.ulaval.ca/)"
    )

    FOOTER_TEXT: str = "Pro tip: Restez informé via le Discord ou le groupe Facebook!"

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

from discord.ext import commands


class RegisterMemberCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(f"Bienvenue {member.name} dans le serveur Discord de l'ASETIN (Association des étudiantes et étudiants en informatique)! \n"
                                     "Afin de confirmer que tu es bel et bien un(e) étudiant(e) inscrit(e) à l'association, entre ton numéro d'identification personnel (NI).\n"
                                     "Au plaisir de te rencontrer!\n"
                                     "ps: Si tu ne sais pas où trouver ton NI, tu peux le consulter sur MonPortail ou encore sur ta carte étudiante.")

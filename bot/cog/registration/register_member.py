from discord.ext import commands
from tools.constants import Messages


class RegisterMemberCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(Messages.WELCOME)

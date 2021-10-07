from discord.ext import commands
from discord.utils import get

class Reactions(commands.Cog):
    """ Work with Reactions """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(reaction.emoji)
        if reaction.emoji == "👍":
            role = user.guild.ger_role(893584463592849418)
            await user.add_roles(role)


def setup(bot):
    bot.add_cog(Reactions(bot))

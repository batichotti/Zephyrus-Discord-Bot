from discord.ext import commands


class Images(commands.Cog):
    """ Works with Images """
    def __init__(self, bot):
        self.bot = bot
    

def setup(bot):
    bot.add_cog(Images(bot))

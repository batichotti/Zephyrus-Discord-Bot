from discord.ext import commands


class Cleaner(commands.Cog):
    """ Clean Messages """
    def __init__(self, bot):
        self.bot = bot
    

def setup(bot):
    bot.add_cog(Cleaner(bot))

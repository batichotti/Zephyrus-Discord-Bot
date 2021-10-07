from discord.ext import commands, tasks
import datetime

class Dates(commands.Cog):
    """ Work with dates """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.current_time.start()

    @tasks.Cog.loop(hours=0.5)
    async def current_time(self):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y às %H:%M:%S")
        channels = [891426585419325470]
        for channel in channels:
            channel = self.bot.get_channel(channel)
            await channel.send(f"Data atual: {now}")

def setup(bot):
    bot.add_cog(Dates(bot))

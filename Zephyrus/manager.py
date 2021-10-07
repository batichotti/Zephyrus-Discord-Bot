from discord.ext import commands
import datetime
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound

class Manager(commands.Cog):
    """ Manage the bot """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Estamos conectados como {self.bot.user}')
        now = datetime.datetime.now()
        print(f'Conexão iniciada: {now.strftime("%d/%m/%Y às %H:%M:%S")}')
        print('>' + '-'*34 + '<')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Favor enviar todos os Argumentos. Digite \\help para ver os parâmetros de cada comando")
        elif isinstance(error, CommandNotFound):
            await ctx.send("O comando não existe.  Digite \\help para ver todos os comandos")
        else:
            raise error


def setup(bot):
    bot.add_cog(Manager(bot))

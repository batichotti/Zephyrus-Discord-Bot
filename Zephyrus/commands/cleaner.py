from discord.ext import commands
from time import sleep

class Cleaner(commands.Cog):
    """ Clean Messages """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="limpar", help="Limpa mensagens enviadas no chat. Argumentos: Quantia de mensagens a serem deletadas (limite = 300)")
    async def clean(self, ctx, lim):
        try:
            lim = int(lim) + 1
            if lim > 301:
                lim = 301
            elif lim == 0:
                await self.bot.send(f"Impossível apagar uma quantia nula de mensagens, {ctx.author.mention}")
                return
            elif lim < 0:
                await self.bot.send(f"Impossível apagar uma quantia negativa de mensagens, {ctx.author.mention}"),
                return
            await ctx.channel.purge(limit=lim)
            await ctx.send(f"Foram apagadas {lim-1} mensagens!")
            sleep(1.5)
            await ctx.channel.purge(limit=1)
        except Exception as e:
            await ctx.send("Ops... Erro")
            print(e)
    

def setup(bot):
    bot.add_cog(Cleaner(bot))

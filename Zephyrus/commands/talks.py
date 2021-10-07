from discord.ext import commands


class Talks(commands.Cog):
    """ Talks with user """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="oi", help="Envia uma saudação (Não requer argumentos)")
    async def send_hello(ctx):
        name = ctx.author.mention
        response = f"Olá, {name}!"
        await ctx.send(response)

def setup(bot):
    bot.add_cog(Talks(bot))

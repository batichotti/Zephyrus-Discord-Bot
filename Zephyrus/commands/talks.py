from discord.ext import commands
import discord
class Talks(commands.Cog):
    """ Talks with user """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="oi", help="Envia uma saudação (Não requer argumentos)")
    async def send_hello(self, ctx):
        name = ctx.author.mention
        response = f"Olá, {name}!"
        await ctx.send(response)

    @commands.command(name="conversa", help="Manda uma mensagem no privado de quem utilizou o comando. (Não requer argumentos)")
    async def talk(self, ctx):
        try:
            await ctx.author.send("Olá! Se inscreva no canal do meu dev: https://www.youtube.com/channel/UChMVeWXTvteLDSMjxlPGmCA")
        except discord.errors.Forbidden:
            await ctx.send(f"@{ctx.author.mention} não podemos conversar ;-; Habilite receber mensagens de qualquer um do servidor (Opções > Privacidade)")

def setup(bot):
    bot.add_cog(Talks(bot))

from discord.ext import commands


class Smarts(commands.Cog):
    """ A lot of Smarts Commands """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="calcular", help="Calcula uma expressão. Argumentos: Expressão")
    async def calculate_expression(self, ctx, *expression):
        try:
            expression = ''.join(expression)
            response = eval(expression)
            await ctx.send(f"A resposta é {response}")
        except Exception as e:
            await self.bot.send("Ops... Erro detectado!")
            print(e)

def setup(bot):
    bot.add_cog(Smarts(bot))

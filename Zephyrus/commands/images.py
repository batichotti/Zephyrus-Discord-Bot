from discord.ext import commands
import discord

class Images(commands.Cog):
    """ Works with Images """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="foto", help="Mostra uma imagem aleatória. (Não requer argumentos)")
    async def get_random_image(self, ctx):
        url_image = "https://picsum.photos/1920/1080"
        embed = discord.Embed(
            title = "Resultado da busca de imagem",
            description = "PS: A busca é totalmente aleatória",
            color = 0x0000FF
        )

        embed.set_author(name=self.bot.user.name, icon_url = self.bot.user.avatar_url)
        embed.set_footer(text = f"By: {self.bot.user.name}", icon_url = self.bot.user.avatar_url)

        embed.add_field(name="API", value="foi utilizada a API do https://picsum.photos/")
        embed.add_field(name="Parâmetros", value="{largura}/{altura}")

        embed.add_field(name="Exemplo:", value=url_image, inline=False)

        embed.set_image(url=url_image)

        await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(Images(bot))

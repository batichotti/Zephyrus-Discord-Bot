from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bs

class Coins(commands.Cog):
    """ Works with Coins and Cryptocurrency Values """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="crypto", help="Verifica o preço de um par envolvendo uma cryptomoeda na binance. Argumentos: moeda, base")
    async def binance(self, ctx, coin, base):
        try:
            response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}{base.upper()}")
            data = response.json()
            price = data.get("price")
            if price:
                await ctx.send(f"O valor do par {coin}/{base} é {round(price, 2)}")
            else:
                await ctx.send(f"O par {coin}/{base} é invalido")
        except Exception as e:
            await ctx.send("Ops... Erro detectado!")
            print(e)

    @commands.command(name="dólar", help="Verifica a cotação atual do Dólar em reais. (Não requer argumentos)")
    async def dollar(self, ctx):
        try:
            url = requests.get('https://www.remessaonline.com.br/cotacao/cotacao-dolar')
            soup = bs(url.text, 'html.parser')
            dolar = soup.find('div', {'class': 'style__Text-sc-15flwue-2 cSuXFv'}).text[0:4]
            await ctx.send(f"Um dólar custa R${dolar} ")
        except Exception as e:
            await ctx.send("Ops... Erro detectado!")
            print(e)

    @commands.command(help="Verifica a cotação atual do Euro em reais. (Não requer argumentos)")
    async def euro(self, ctx):
        try:
            url = requests.get('https://www.remessaonline.com.br/cotacao/cotacao-euro')
            soup = bs(url.text, 'html.parser')
            euro = soup.find('div', {'class': 'style__Text-sc-15flwue-2 cSuXFv'}).text[0:4]
            await ctx.send(f"Um euro custa R${euro} ")
        except Exception as e:
            await ctx.send("Ops... Erro detectado!")
            print(e)

def setup(bot):
    bot.add_cog(Coins(bot))

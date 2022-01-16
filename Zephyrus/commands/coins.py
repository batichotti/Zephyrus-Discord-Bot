from discord.ext import commands
import requests

class Coins(commands.Cog):
    """ Works with Coins and Cryptocurrency Values """
    def __init__(self, bot):
        self.bot = bot

    def get_price(self, coin_code):
        link = f"https://economia.awesomeapi.com.br/last/{coin_code}-BRL"
        request = requests.get(link)
        dic_request = request.json()
        coin_price = dic_request[f"{coin_code}BRL"]["bid"]
        coin_price_float = float(coin_price)
        coin_price = str(round(coin_price_float, 2)).replace('.', ',')
        return coin_price
    
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

    @commands.command(name="dólar", help="Verifica a cotação atual do Dólar em reais. (Não requer argumentos)", aliases = ['Dólar', 'Dolar', 'Dollar', 'dolar', 'dollar'])
    async def dollar(self, ctx):
        try:
            dolar = self.get_price('USD')
            await ctx.send(f"DÓLAR -> R${dolar}")
        except Exception as e:
            await ctx.send("Ops... Erro detectado!")
            print(e)

    @commands.command(name="euro", help="Verifica a cotação atual do Euro em reais. (Não requer argumentos)", aliases = ['Euro'])
    async def euro(self, ctx):
        try:
            euro = self.get_price('EUR')
            await ctx.send(f"EURO -> R${euro}")
        except Exception as e:
            await ctx.send("Ops... Erro detectado!")
            print(e)

def setup(bot):
    bot.add_cog(Coins(bot))

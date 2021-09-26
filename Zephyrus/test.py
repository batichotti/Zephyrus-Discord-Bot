import discord
from discord.ext import commands, tasks
import datetime
import requests
from bs4 import BeautifulSoup as bs
from requests.models import Response

bot = commands.Bot("\\")

@bot.event
async def on_ready():
    print(f'Estamos conectados como {bot.user}')
    print('>' + '-'*34 + '<')
    current_time.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "Gojo" in message.content:
        await message.channel.send(f"Por favor, @{message.author.name}, não diga o nome de deus em vão!")
    if "Maki" in message.content:
        await message.channel.send(f"Falou o nome da Mak*? Eu tenho que apagar isso!")
        await message.delete()

    await bot.process_commands(message)

@bot.command(name="oi")
async def send_hello(ctx):
    name = ctx.author.name
    response = f"Olá, {name}!"
    await ctx.send(response)

@bot.command(name="calcular")
async def calculate_expression(ctx, *expression):
    expression = ''.join(expression)
    response = eval(expression)
    await ctx.send(f"A resposta é {response}")

@bot.command(name="crypto")
async def binance(ctx, coin, base):
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

@bot.command(name="dólar")
async def dollar(ctx):
    try:
        url = requests.get('https://www.remessaonline.com.br/cotacao/cotacao-dolar')
        soup = bs(url.text, 'html.parser')
        dolar = soup.find('div', {'class': 'style__Text-sc-15flwue-2 cSuXFv'}).text[0:4]
        await ctx.send(f"Um dólar custa R${dolar} ")
    except Exception as e:
        await ctx.send("Ops... Erro detectado!")
        print(e)

@bot.command()
async def euro(ctx):
    try:
        url = requests.get('https://www.remessaonline.com.br/cotacao/cotacao-euro')
        soup = bs(url.text, 'html.parser')
        euro = soup.find('div', {'class': 'style__Text-sc-15flwue-2 cSuXFv'}).text[0:4]
        await ctx.send(f"Um euro custa R${euro} ")
    except Exception as e:
        await ctx.send("Ops... Erro detectado!")
        print(e)

@tasks.loop(hours=1)
async def current_time():
    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y às %H:%M:%S")
    channel = bot.get_channel(891426585419325470)
    await channel.send(f"Data atual: {now}")

bot.run('ODkxMzUxMTQxNjk3MzUxNzQw.YU9FcA.fSckrOmA0fl2-6aZwjz5h2W8DvE')

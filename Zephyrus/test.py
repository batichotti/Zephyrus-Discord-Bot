import discord
from discord.ext import commands, tasks
import datetime

bot = commands.Bot("$")

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

@bot.command()
async def binance(ctx, coin, base):
    pass

@tasks.loop(minutes=60)
async def current_time():
    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y às %H:%M:%S")
    channel = bot.get_channel(891426585419325470)
    await channel.send(f"Data atual: {now}")

bot.run('ODkxMzUxMTQxNjk3MzUxNzQw.YU9FcA.fSckrOmA0fl2-6aZwjz5h2W8DvE')

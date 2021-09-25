import discord
from discord.ext import commands

bot = commands.Bot("$")

@bot.event
async def on_ready():
    print(f'Estamos conectados como {bot.user}')
    print('>' + '-'*34 + '<')

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

bot.run('ODkxMzUxMTQxNjk3MzUxNzQw.YU9FcA.fSckrOmA0fl2-6aZwjz5h2W8DvE')

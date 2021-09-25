import discord
from discord.ext import commands

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('-'*40)

@client.event
async def on_message(message):
    print('Message from {0.author} in {0.channel} channel: {0.content}'.format(message))
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$gordo'):
        await message.channel.send(f'O {message.author} é muito gordo, parece até o Lucas')

client.run('ODkxMzUxMTQxNjk3MzUxNzQw.YU9FcA.fSckrOmA0fl2-6aZwjz5h2W8DvE')

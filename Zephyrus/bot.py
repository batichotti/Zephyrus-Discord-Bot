from discord.ext import commands
from decouple import config

bot = commands.Bot("\\")


TOKEN = config("TOKEN")
bot.run(TOKEN)

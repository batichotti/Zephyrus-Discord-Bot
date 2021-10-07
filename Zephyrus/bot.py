from discord.ext import commands
from decouple import config
import os

bot = commands.Bot("\\") #Uses the \

def load_cogs(bot):
    bot.load_extension("manager")

    for file in os.listdir("commands"):
        cog = file[:-3]
        bot.load_extension(f"commands.{cog}")

load_cogs(bot)

TOKEN = config("TOKEN")
bot.run(TOKEN)

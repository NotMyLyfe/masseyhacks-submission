import discord
from discord.ext import commands
import logging # remove logging in release

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='c!', description="A bot with COVID-19 Statistics")


file = 'token.txt'
with open(file, 'r') as token:
    token = token.read()


@bot.event
async def on_ready():
    print('The bot has logged in under the account ' + bot.user.name + "#" + bot.user.discriminator)


while True:
    bot.run(token)

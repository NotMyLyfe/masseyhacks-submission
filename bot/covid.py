import discord
from discord.ext import commands
import requests
import logging  # remove logging in release

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='c!', description="A bot with COVID-19 Statistics")
bot.remove_command('help')

file = 'token.txt'
with open(file, 'r') as token:
    token = token.read()


@bot.event
async def on_ready():
    print('The bot has logged in under the account ' + bot.user.name + "#" + bot.user.discriminator)


@bot.command()
async def help(ctx):
    emb = discord.Embed(title="COVID Data Commands", description="The commands in this bot", color=0xff0000)
    emb.add_field(name="c!help", value="Displays this help embed.", inline=False)
    emb.add_field(name="c!data [country code]", value="Displays the statistic for the specified country.", inline=False)
    await ctx.send(embed=emb)


@bot.command()
async def data(ctx, arg1):
    country = arg1.lower
    try:
        url = 'https://api.thevirustracker.com/free-api?countryTotal=' + country
        infos = requests.request(url=url)
        print(infos)
    except IndexError:
        await ctx.send("ERROR: You did not provide a valid country code.")
    await ctx.send(embed=emb)


while True:
    bot.run(token)

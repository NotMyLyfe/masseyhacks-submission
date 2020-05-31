import discord
from discord.ext import commands
import requests
import json
import os
import logging  # remove logging in release

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='c!', description="A bot with COVID-19 Statistics")
bot.remove_command('help')

token = os.getenv('COVID-Token')
with open("the_Countries.json", "r") as read_file:
    countries = json.load(read_file)


@bot.event
async def on_ready():
    print('The bot has logged in under the account ' + bot.user.name + "#" + bot.user.discriminator)


@bot.command()
async def help(ctx):
    emb = discord.Embed(title="COVID Data Commands", description="The commands in this bot", color=0xff0000)
    emb.add_field(name="c!help", value="Displays this help embed.", inline=False)
    emb.add_field(name="c!data [country name or 2 letter code]", value="Displays the statistics for the specified "
                                                                       "country.", inline=False)
    await ctx.send(embed=emb)


@bot.command()
async def data(ctx, *args):
    if len(args[0].lower()) == 2:
        country = args[0].lower()
    else:
        arghs = list(args)
        echo = ""
        while arghs:
            echo = echo + " " + arghs[0]
            del arghs[0]
        country = countries[echo.strip()]
    url = 'https://api.thevirustracker.com/free-api?countryTotal=' + country
    infos = requests.get(url)
    infos = json.loads(infos.text)
    try:
        infos = infos['countrydata'][0]
    except KeyError:
        await ctx.send("Incorrect input. The correct syntax is c!data [2 letter country code]")
        return
    finally:
        emb = discord.Embed(title="Coronavirus Stats for the Country of {}".format(infos['info']['title']),
                            description="Total Cases: {}".format(str(infos['total_cases'])), color=0xff0000)
        emb.add_field(name="Total Recovered", value=str(infos['total_recovered']), inline=True)
        emb.add_field(name="Total Unresolved", value=str(infos['total_unresolved']), inline=True)
        emb.add_field(name="Total Deaths", value=str(infos['total_deaths']), inline=True)
        emb.add_field(name="Total New Cases Today", value=str(infos['total_new_cases_today']), inline=True)
        emb.add_field(name="Total New Deaths Today", value=str(infos['total_new_deaths_today']), inline=True)
        emb.add_field(name="Total Active Cases", value=str(infos['total_active_cases']), inline=True)
        emb.add_field(name="Total Serious Cases", value=str(infos['total_serious_cases']), inline=True)
        await ctx.send(embed=emb)


@data.error
async def data_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Incorrect syntax. The correct syntax is c!data [country name or 2 letter code]")
    else:
        raise error


while True:
    bot.run(token)

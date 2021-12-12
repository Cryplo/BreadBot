# NOTES: ADD A SPACE INFRONT OF EACH COMMAND
#pip install -U git+https://github.com/Pycord-Development/pycord
import discord
import discord.utils
from discord.ext import commands

import config
# from commands import update_log
from functions import *
from keep_alive import keep_alive


prefix = '.bread'
madlibs = {}
collectors = []
pantry_limit = config.pantry_limit
common_bread = config.common_bread
rare_bread = config.rare_bread
mythical_bread = config.mythical_bread
legendary_bread = config.legendary_bread
updateLog = config.updateLog
helpContent = config.helpContent
faqContent = config.faqContent

# database stuff
cluster = pymongo.MongoClient(os.getenv('CONNECTION_URL'))
database = cluster["UserData"]
collection = database["UserData"]

client = commands.Bot(command_prefix='.b ')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('.b help'))


@client.event
async def on_guild_join(guild):
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Game('.b help; In ' + str(len(client.guilds)) + ' servers'))



client.load_extension("cogs.misc")
client.load_extension("cogs.game")
client.load_extension("cogs.battle")

keep_alive()

client.run(os.getenv('TOKEN'))

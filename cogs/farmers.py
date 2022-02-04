import random
import time
from collections import Counter
import math
import discord
from discord.ext import commands
from collections import OrderedDict
from operator import getitem
import config
from functions import *
import sys
from discord.ui import Button, View
import asyncio




pantry_limit = config.pantry_limit
common_bread = config.common_bread
rare_bread = config.rare_bread
mythical_bread = config.mythical_bread
legendary_bread = config.legendary_bread
updateLog = config.updateLog
helpContent = config.helpContent
faqContent = config.faqContent
bakePercents = config.bake_percents


async def db_push(id, key, value):
    collection.update_one({"_id": id}, {"$push": {key: value}})


async def db_set(id, key, value):
    collection.update_one({"_id": id}, {"$set": {key: value}})

async def initCommand(ctx):
    global users
    global myquery
    global user
    global collection
    global database
    global cluster
    await asyncio.sleep(0.1)
    cluster = pymongo.MongoClient(os.getenv('CONNECTION_URL'))
    database = cluster["UserData"]
    collection = database["UserData"]
    myquery = {"_id": ctx.author.id}
    user = collection.find(myquery)
    if (collection.count_documents(myquery) == 0):
        post = {"_id": ctx.author.id, "pantry": [], "card_cooldown": 0, "grain": int(0), "farm_cooldown": 0,
                "name": ctx.author.name, "quest": [], "quest_cooldown": 0}
        collection.insert_one(post)
    global common_pantry
    global rare_pantry
    global mythical_pantry
    global legendary_pantry
    global pantry
    global card_cooldown
    global farm_cooldown
    global grain
    global quest
    global counted_pantry
    global simplified_common_pantry
    global simplified_rare_pantry
    global simplified_mythical_pantry
    global simplified_legendary_pantry
    global quest_cooldown
    global chests
    global hourly_cooldown
    global daily_cooldown
    global forage_cooldown
    collection.update_one({"_id": ctx.author.id}, {"$set": {"name": ctx.author.name}})
    document = collection.find_one(myquery)
    for result in user:
      pantry = result["pantry"]
      card_cooldown = result["card_cooldown"]
      farm_cooldown = result["farm_cooldown"]
      grain = int(result["grain"])
      
      if "quest" in document.keys():
          # for result in user:
          quest = result["quest"]
          quest_cooldown = result["quest_cooldown"]
      if "quest" not in document.keys():
          collection.update_one({"_id": ctx.author.id}, {"$set": {"quest": []}})
          collection.update_one({"_id": ctx.author.id}, {"$set": {"quest_cooldown": 0}})
          quest = []
          quest_cooldown = 0
      if "chests" in document.keys():
          chests = result["chests"]
      if "chests" not in document.keys():
          await db_set(ctx.author.id,"chests",{"1st":0,"2nd":0,"3rd":0,"4th":0,"5th":0})
          chests = result["chests"]
      if "hourly_cooldown" in document.keys():
          hourly_cooldown = result["hourly_cooldown"]
      if "hourly_cooldown" not in document.keys():
          collection.update_one({"_id": ctx.author.id}, {"$set": {"hourly_cooldown": 0}})
          hourly_cooldown = 0
      if "daily_cooldown" in document.keys():
          daily_cooldown = result["daily_cooldown"]
      if "daily_cooldown" not in document.keys():
          collection.update_one({"_id": ctx.author.id}, {"$set": {"daily_cooldown": 0}})
          daily_cooldown = 0
      if "forage_cooldown" in document.keys():
          forage_cooldown = result["forage_cooldown"]
      if "forage_cooldown" not in document.keys():
          collection.update_one({"_id": ctx.author.id}, {"$set": {"forage_cooldown": 0}})
          forage_cooldown = 0
    common_pantry = []
    rare_pantry = []
    mythical_pantry = []
    legendary_pantry = []
    for x in pantry:
        if x in common_bread:
            common_pantry.append(x)
        elif x in rare_bread:
            rare_pantry.append(x)
        elif x in mythical_bread:
            mythical_pantry.append(x)
        elif x in legendary_bread:
            legendary_pantry.append(x)
    counted_pantry = Counter(pantry)
    simplified_common_pantry = set(common_pantry)
    simplified_rare_pantry = set(rare_pantry)
    simplified_mythical_pantry = set(mythical_pantry)
    simplified_legendary_pantry = set(legendary_pantry)



class Farmers(commands.Cog):

  def __init__(self, client):
        self.client = client

  @commands.command(name="hire")
  async def hire(self,ctx,amount):
    await initCommand()

def setup(client):
    client.add_cog(Farmers(client))
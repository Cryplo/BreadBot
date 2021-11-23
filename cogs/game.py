from functions import *
import discord
from discord.ext import commands
import config
import random
import time
import datetime
pantry_limit = config.pantry_limit
common_bread = config.common_bread
rare_bread = config.rare_bread
mythical_bread = config.mythical_bread
legendary_bread = config.legendary_bread
updateLog = config.updateLog
helpContent = config.helpContent
faqContent = config.faqContent

async def initCommand(ctx):
  global myquery
  global user
  global collection
  global database
  global cluster
  cluster = pymongo.MongoClient(os.getenv('CONNECTION_URL'))
  database = cluster["UserData"]
  collection = database["UserData"]
  myquery = { "_id": ctx.author.id }
  user = collection.find(myquery)
  if (collection.count_documents(myquery) == 0):
          post = {"_id": ctx.author.id, "pantry": [], "common_pantry": [], "rare_pantry":[],"mythical_pantry":[],"legendary_pantry":[],"card_cooldown":0,"grain":int(0), "farm_cooldown":0, "name":ctx.author.name, "quest": [], "quest_cooldown":0} 
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
  collection.update_one({"_id":ctx.author.id}, {"$set":{"name":ctx.author.name}})
  for result in user:
    pantry = result["pantry"]
    card_cooldown = result["card_cooldown"]
    farm_cooldown = result["farm_cooldown"]
    grain = int(result["grain"])
  
    document = collection.find_one(myquery)

    if "quest" in document.keys():
    #for result in user:
      quest = result["quest"]
      quest_cooldown = result["quest_cooldown"]
  
    if "quest" not in document.keys():
      collection.update_one({"_id":ctx.author.id},{"$set":{"quest":[]}})
      collection.update_one({"_id":ctx.author.id},{"$set":{"quest_cooldown":0}})
      quest = []
      quest_cooldown = 0
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

  
class Game(commands.Cog):
  """Core Game"""
  def __init__(self,client):
    self.client = client
  @commands.command(name="bake")
  async def bake(self,ctx):
        await initCommand(ctx)
        #Checks to make sure baking meets requirements
        if time.time() - card_cooldown >= config.bake_cooldown and len(pantry)<pantry_limit:
          ran_card_category = random.randint(1,1000)
          #Common Card Baked
          if ran_card_category > 0 and ran_card_category <= 700:
              card_category="common"
              card = common_bread[random.randint(0,len(common_bread)-1)]
              embed = discord.Embed(description = "Congratulations, you baked a "+card+". This card is a common", colour = 0x808080)
              await ctx.send(embed = embed)
            #Rare Card Baked
          if ran_card_category > 700 and ran_card_category <= 975:
              card = rare_bread[random.randint(0,len(rare_bread)-1)]
              card_category="rare"

              embed = discord.Embed(description = "Congratulations, you baked a "+card+". This card is a rare", colour = 0x0073ff)
              await ctx.send(embed = embed)

          #Mythical Card Baked
          if ran_card_category > 975 and ran_card_category <= 997:
              card = mythical_bread[random.randint(0,len(mythical_bread)-1)]
              card_category="mythical"

              embed = discord.Embed(description = "Congratulations, you baked a "+card+". This card is a mythical", colour = 0xb700ff)
              await ctx.send(embed = embed)
          #Legendary Card Baked
          if ran_card_category > 997 and ran_card_category <= 1000:
              card = legendary_bread[random.randint(0,len(legendary_bread)-1)]
              card_category="legendary"
              embed = discord.Embed(description = "Congratulations, you baked a "+card+". This card is a LEGENDARY!", colour = 0xfbff00)
              await ctx.send(embed = embed)
          db_push(ctx.author.id,card_category+"_pantry",card)
          db_push(ctx.author.id,"pantry",card)
          db_set(ctx.author.id,"card_cooldown",time.time())
          return
          #Cooldown Time
        if time.time() - card_cooldown < config.bake_cooldown:
          delay_left = config.bake_cooldown- (time.time() - card_cooldown)
          embed = discord.Embed(description = 'You have ' +convert(delay_left)+' left until you can use this command again', colour = 0xff1100)
          await ctx.send(embed = embed)
        else:
          embed = discord.Embed(description = "You have don't have any more room left in your pantry", colour = 0xff1100)
          await ctx.send(embed = embed)
  @commands.command(name="pantry")
  async def show_pantry(self,ctx):
    await initCommand(ctx)
    common_shown = [count_duplicates(x, counted_pantry) for x in simplified_common_pantry]
    rare_shown = [count_duplicates(x, counted_pantry) for x in simplified_rare_pantry]
    mythical_shown = [count_duplicates(x, counted_pantry) for x in simplified_mythical_pantry]
    legendary_shown = [count_duplicates(x, counted_pantry) for x in simplified_legendary_pantry]

    seperator = ", "
      
    pantry_shown = '**Commons**: '+seperator.join(sorted(common_shown))+'\n\n**Rares**: '+seperator.join(sorted(rare_shown))+'\n\n**Mythicals**: '+seperator.join(sorted(mythical_shown))+'\n\n**Legendaries** '+seperator.join(sorted(legendary_shown))
      
    embed = discord.Embed(title = ctx.author.name+"'s pantry:", description = pantry_shown, colour = 0x000000)
    embed.set_footer(text = 'Cards sell value: '+str(len(common_pantry)*500+len(rare_pantry)*2500+len(mythical_pantry)*6000+len(legendary_pantry)*20000)+' grain'+" | Size: "+str(len(pantry))+"/"+str(pantry_limit))
    await ctx.send(embed = embed)
  @commands.command(name="grain")
  async def show_grain(self,ctx,member: discord.Member=None):
    await initCommand(ctx)
    if member!=None:
      viewing_id = member.id
    else:
      viewing_id = ctx.author.id
    viewing = collection.find({ "_id": viewing_id })
    if collection.count_documents({ "_id": viewing_id }) == 1:
      for result in viewing:
          grain = result["grain"]
    viewing_user = await self.client.fetch_user(viewing_id)
    embed = discord.Embed(title = str(viewing_user.name)+"'s grain:", description = grain, colour = 0x000000)
    await ctx.send(embed = embed)
def setup(client):
  client.add_cog(Game(client))
#NOTES: ADD A SPACE INFRONT OF EACH COMMAND
import discord
import os
import random
from discord.ext import commands
import time
import datetime
from datetime import datetime
from replit import db
from keep_alive import keep_alive
import pymongo
import dns
import discord.utils
from discord.utils import get
from pymongo import MongoClient
import math
import collections
from collections import Counter
#from commands import update_log
from functions import *
import config


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



      









#database stuff
cluster = pymongo.MongoClient(os.getenv('CONNECTION_URL'))
database = cluster["UserData"]
collection = database["UserData"]














client = commands.Bot(command_prefix='.bread ')




  






@client.event
async def on_ready():
    
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('bot is being rewritten'))
    prefix = '.bread'

@client.event
async def on_guild_join(guild):
    
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('.bread help; In '+str(len(client.guilds))+' servers'))
    prefix = '.bread'


#initTest(client)
@client.command(name="test")
async def test(ctx,arg):
  await ctx.send(ctx.author.id)



@client.listen("on_message")
async def something(message):
    
    global prefix
    global after_keyowrd
    global player
    global madlibs
    global collectors
    global card_cooldown
    global common_pantry
    global rare_pantry
    global mythical_pantry
    global legendary_pantry
    global pantry
    global grain
    global quest
    global quest_cooldown
    global counted_pantry
    global user
    global collection
    #If message of author is client, then ignore
    if message.author == client.user:
        return
    if message.content.startswith(prefix):
      null, null,command = message.content.partition(prefix)
      command = command.strip()
    else:
      return

    #Searching for user data
    myquery = { "_id": message.author.id }
    user = collection.find(myquery)




    #if message.content.startswith(prefix+' request'):
      #null,null,request = message.content.partition('request')
      #if request != None:
        #request_file = open('requests.txt', 'a')
        #request_file.write(str(message.author.id)+": "+request+"\n")



    ################
    #   
    #
    ##########
    #
    #
    #bread_card_game    

    #Starts user account
    #Idk why theres two different blocks of code for starting a user account

      

####

        #collection.update_one({"_id":message.author.id}, {"$set":{"score":score}})
        
####      
    #Baking
    #if command == 'bake':
      #await bake()
    
    

    
      


      
      



      
    

      


      
      

      




    
    if message.content.startswith(prefix+' trade'):

      if 'for' in message.content and ',' in message.content:
        offer = message.content
        offer = offer.replace(prefix+' trade','') 
        before, null, after = offer.partition(' for ')

        offering_cards = before.split(',')
        offering_cards = [x.strip() for x in offering_cards]
        wanting_cards = after.split(',')
        wanting_cards = [x.strip() for x in wanting_cards]
        all_bread = common_bread[:]+rare_bread[:]+mythical_bread[:]+legendary_bread[:]

        raw_offer_count = len(offering_cards)
        raw_want_count = len(wanting_cards)
        offering_cards = [x for x in offering_cards if x in pantry]
        wanting_cards = [x for x in wanting_cards if x in all_bread]

        if len(offering_cards) == raw_offer_count:
          if len(wanting_cards) == raw_want_count:
            if len(wanting_cards) == len(set(wanting_cards)) and len(offering_cards) == len(set(offering_cards)):
              separator = ", "
              embed = discord.Embed(title = "Trade Offer!", description = message.author.mention+' is trading\n'+separator.join(offering_cards)+" \nfor\n"+separator.join(wanting_cards), colour = 0x0dff00)
              embed.set_footer(text = "React to this message to accept the offer")
              await message.channel.send(embed = embed)
            else:
              embed = discord.Embed(description ="Error: You can't trade two of the same card", colour = 0xff1100)
              await message.channel.send(embed=embed)

          elif str(wanting_cards) not in all_bread:
            embed = discord.Embed(description ="Error: The card(s) you're requesting doesn't exist", colour = 0xff1100)
            await message.channel.send(embed=embed)

        else:
          embed = discord.Embed(description ="Error: You don't have these card(s)!", colour = 0xff1100)
          await message.channel.send(embed=embed)
      #single trade
      if 'for' in message.content and ',' not in message.content:
        offer = message.content
        offer = offer.replace(prefix+' trade','') 
        before, null, after = offer.partition(' for ')

        offering_cards = before
        wanting_cards = after


        embed = discord.Embed(title = "Trade Offer!", description = message.author.mention+' is trading\n'+offering_cards+" \nfor\n"+wanting_cards, colour = 0x0dff00)
        embed.set_footer(text = "React to this message to accept the offer")
        await message.channel.send(embed = embed)


      elif str(wanting_cards) not in all_bread:
        embed = discord.Embed(description ="Error: The card(s) you're requesting doesn't exist", colour = 0xff1100)
        await message.channel.send(embed=embed)

      else:
          embed = discord.Embed(description ="Error: You don't have these card(s)!", colour = 0xff1100)
          await message.channel.send(embed=embed)

    
    if message.content == prefix+' start quest':
      if time.time()-quest_cooldown > 86400 and len(quest) != 3:
        collection.update_one({"_id":message.author.id}, {"$set":{"quest_cooldown":time.time()}})
      
        available_bread = common_bread[:]

        card_1 = available_bread[random.randint(0, len(available_bread)-1)]
        
        available_bread.remove(card_1)
        
        card_2 = available_bread[random.randint(0, len(available_bread)-1)]
        
        available_bread.remove(card_2)
        
        card_3 = available_bread[random.randint(0, len(available_bread)-1)]

        available_bread.remove(card_3)
      
        collection.update_one({"_id":message.author.id}, {"$push":{"quest":card_1}})
        collection.update_one({"_id":message.author.id}, {"$push":{"quest":card_2}})
        collection.update_one({"_id":message.author.id}, {"$push":{"quest":card_3}})
        embed = discord.Embed(title = 'Quest Started!', description = message.author.mention+' must get '+card_1+', '+card_2+', '+card_3+' in 24 hours in order to receive an award of 2500 grain', colour = 0x0dff00)
        await message.channel.send(embed = embed)
        return
      if time.time()-quest_cooldown > 86400 and len(quest) == 3:
        collection.update_one({"_id":message.author.id}, {"$set":{"quest":[]}})
        collection.update_one({"_id":message.author.id}, {"$set":{"quest_cooldown":time.time()}})
      
        available_bread = common_bread[:]

        card_1 = available_bread[random.randint(0, len(available_bread)-1)]
        available_bread.remove(card_1)
        card_2 = available_bread[random.randint(0, len(available_bread)-1)]
        available_bread.remove(card_2)
        card_3 = available_bread[random.randint(0, len(available_bread)-1)]
        available_bread.remove(card_3)
      
        collection.update_one({"_id":message.author.id}, {"$push":{"quest":card_1}})
        collection.update_one({"_id":message.author.id}, {"$push":{"quest":card_2}})
        collection.update_one({"_id":message.author.id}, {"$push":{"quest":card_3}})
        embed = discord.Embed(title = 'Quest Started!', description = message.author.mention+' must get '+card_1+', '+card_2+', '+card_3+' in 24 hours in order to receive an award of 2500 grain', colour = 0x0dff00)
        await message.channel.send(embed = embed)
        return   
      
      else:
        time_left = convert((quest_cooldown+86400)-time.time())
        embed = discord.Embed(description = message.author.mention+"You can't start a new quest at the moment. The cooldown ends in "+str(time_left), colour = 0xff1100)
        embed.set_footer(text = "Type .bread view quest to see your ongoing quest")
        await message.channel.send(embed = embed)
    
    if message.content == prefix+ ' view quest':

      if len(quest) == 3 and time.time()-quest_cooldown<86400:
        time_left = convert((quest_cooldown+86400)-time.time())
        embed = discord.Embed(title = message.author.name+"'s on going quest:", description = message.author.mention+" needs to get "+quest[0]+", "+quest[1]+", "+quest[2]+" in "+time_left+" in order to claim an award of 2500 grain", colour = 0x0dff00)
        await message.channel.send(embed = embed)
      elif quest_cooldown == 0:
        embed = discord.Embed(description = "It seems like you haven't started a quest yet. Type .bread start quest to start a quest", colour = 0xff1100)
        await message.channel.send(embed = embed)
      elif quest_cooldown+86400<time.time():
        embed = discord.Embed(description = "Looks like it's been more than 24 hours since you started your quest, so the quest is inactive",colour = 0xff1100)
        embed.set_footer(text = "Type .bread start quest to start a new quest")
        await message.channel.send(embed = embed)
      else:
        time_left = convert((quest_cooldown+86400)-time.time())
        embed = discord.Embed(description = "It seems like you've already completed your quest. The cooldown ends in "+str(time_left), colour = 0xff1100)
        await message.channel.send(embed = embed)
    
    if message.content == prefix+' claim quest':
      if len(quest)==3 and time.time()<quest_cooldown+86400:
        card_1 = quest[0]
        card_2 = quest[1]
        card_3 = quest[2]
        if card_1 in common_pantry and card_2 in common_pantry and card_3 in common_pantry:

          common_pantry.remove(card_1)
          pantry.remove(card_1)
          collection.update_one({"_id":message.author.id}, {"$set":{"common_pantry":common_pantry}})
          collection.update_one({"_id":message.author.id}, {"$set":{"pantry":pantry}})

          common_pantry.remove(card_2)
          pantry.remove(card_2)
          collection.update_one({"_id":message.author.id}, {"$set":{"common_pantry":common_pantry}})
          collection.update_one({"_id":message.author.id}, {"$set":{"pantry":pantry}})

          common_pantry.remove(card_3)
          pantry.remove(card_3)
          collection.update_one({"_id":message.author.id}, {"$set":{"common_pantry":common_pantry}})
          collection.update_one({"_id":message.author.id}, {"$set":{"pantry":pantry}})
        
          collection.update_one({"_id":message.author.id}, {"$set":{"quest":[]}})
        
          collection.update_one({"_id":message.author.id}, {"$set":{"grain":grain+3000}})
          embed = discord.Embed(title = "Quest Complete!", description = message.author.name+" completed their quest",colour = 0x0dff00)

          await message.channel.send(embed = embed)
        else:
          embed = discord.Embed(description = "Looks like you don't have the needed cards yet",colour = 0xff1100)
          embed.set_footer(text = "Type .bread view quest to show your ongoing quest")
          await message.channel.send(embed = embed)

      elif quest_cooldown == 0:
        embed = discord.Embed(description = "Looks like you haven't started a quest yet",colour = 0xff1100)
        embed.set_footer(text = "Type .bread start quest to start a quest")
        await message.channel.send(embed = embed)
      
      elif quest_cooldown + 86400 < time.time():
        embed = discord.Embed(description = "Looks like it's been more than 24 hours since you started your quest, so the quest is in active",colour = 0xff1100)
        embed.set_footer(text = "Type .bread start quest to start a new quest")
        await message.channel.send(embed = embed)


      else:
        embed = discord.Embed(description = "Looks like you don't have the needed cards yet",colour = 0xff1100)
        embed.set_footer(text = "Type .bread view quest to show your ongoing quest")
        await message.channel.send(embed = embed)











  





@client.event
async def on_raw_reaction_add (payload):
  
  
  message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
  author = message.author
  reaction = get(message.reactions)
  
  
  if author == client.user and message.embeds[0].title == 'Trade Offer!' and reaction.count == 1:
      global trader_common_pantry
      global trader_rare_pantry
      global trader_mythical_pantry
      global trader_legendary_pantry
      global trader_pantry
      global trader

      global accepter_common_pantry
      global accepter_rare_pantry
      global accepter_mythical_pantry
      global accepter_legendary_pantry
      global accepter_pantry
      global offering
      global wanting
      global accepter
      msg_description=message.embeds[0].description
      accepter = payload.user_id
      front, null, null = msg_description.partition('>')
      null, null, trader = front.partition('@')

      #print(reaction.message.mentions)



      null, null, end = msg_description.partition('trading')

      offering, null, wanting = end.partition('for')

      offering = offering.strip()
      wanting = wanting.strip()
      trader = str(trader).replace("!","")
      accepter = str(accepter).replace("!","")
      trader = str(trader).strip()
      accepter = str(accepter).strip()
      trader = int(trader)
      accepter = int(accepter)


      offering_cards = offering.split(',')
      offering_cards = [x.strip() for x in offering_cards]
      wanting_cards = wanting.split(',')
      wanting_cards = [x.strip() for x in wanting_cards]






      
      trader_query = { "_id": trader }
      accepter_query = { "_id": accepter }
      trader_find = collection.find(trader_query)
      accepter_find = collection.find(accepter_query)




      for result in trader_find:
        trader_common_pantry = result["common_pantry"]
        trader_rare_pantry = result["rare_pantry"]
        trader_mythical_pantry = result["mythical_pantry"]
        trader_legendary_pantry = result["legendary_pantry"]
        trader_pantry = result["pantry"]
        trader_card_cooldown = result["card_cooldown"]
        trader_farm_cooldown = result["farm_cooldown"]
        trader_grain = int(result["grain"])
      
      for result in accepter_find:
        accepter_common_pantry = result["common_pantry"]
        accepter_rare_pantry = result["rare_pantry"]
        accepter_mythical_pantry = result["mythical_pantry"]
        accepter_legendary_pantry = result["legendary_pantry"]
        accepter_pantry = result["pantry"]
        accepter_card_cooldown = result["card_cooldown"]
        accepter_farm_cooldown = result["farm_cooldown"]
        accepter_grain = int(result["grain"])


      raw_offer_count = len(offering_cards)
      raw_want_count = len(wanting_cards)
      
      offering_cards = [x for x in offering_cards if x in trader_pantry]
      wanting_cards = [x for x in wanting_cards if x in accepter_pantry]



      if len(offering_cards) == raw_offer_count and len(wanting_cards) == raw_want_count and len(offering_cards) == len(set(offering_cards)) and len(wanting_cards) == len(set(wanting_cards)):
        #trader_pantry = [x for x in trader_pantry if x in offering_cards]
        #print(trader_pantry)
        #print(accepter_pantry)
        for x in offering_cards:
          trader_pantry.remove(x)
          if x in common_bread:
            trader_common_pantry.remove(x)

          if x in rare_bread:
            trader_rare_pantry.remove(x)

          if x in mythical_bread:
            trader_mythical_pantry.remove(x)

          if x in legendary_bread:
            trader_legendary_pantry.remove(x)

        for y in wanting_cards:
          
          accepter_pantry.remove(y)
          
          if y in common_bread:
            accepter_common_pantry.remove(y)

          if y in rare_bread:
            accepter_rare_pantry.remove(y)

          if y in mythical_bread:
            accepter_mythical_pantry.remove(y)

          if y in legendary_bread:
            accepter_legendary_pantry.remove(y)
        

        

        
        
        for x in wanting_cards:
          trader_pantry.append(x)
          if x in common_bread:
            trader_common_pantry.append(x)

          if x in rare_bread:
            trader_rare_pantry.append(x)

          if x in mythical_bread:
            trader_mythical_pantry.append(x)

          if x in legendary_bread:
            trader_legendary_pantry.append(x)
        
        for x in offering_cards:
          accepter_pantry.append(x)
          if x in common_bread:
            accepter_common_pantry.append(x)

          if x in rare_bread:
            accepter_rare_pantry.append(x)

          if x in mythical_bread:
            accepter_mythical_pantry.append(x)

          if x in legendary_bread:
            accepter_legendary_pantry.append(x)
        
        collection.update_one({"_id":trader}, {"$set":{"pantry":trader_pantry}})
        collection.update_one({"_id":trader}, {"$set":{"common_pantry":trader_common_pantry}})
        collection.update_one({"_id":trader}, {"$set":{"rare_pantry":trader_rare_pantry}})
        collection.update_one({"_id":trader}, {"$set":{"mythical_pantry":trader_mythical_pantry}})
        collection.update_one({"_id":trader}, {"$set":{"legendary_pantry":trader_legendary_pantry}})

        collection.update_one({"_id":accepter}, {"$set":{"pantry":accepter_pantry}})
        collection.update_one({"_id":accepter}, {"$set":{"common_pantry":accepter_common_pantry}})
        collection.update_one({"_id":accepter}, {"$set":{"rare_pantry":accepter_rare_pantry}})
        collection.update_one({"_id":accepter}, {"$set":{"mythical_pantry":accepter_mythical_pantry}})
        collection.update_one({"_id":accepter}, {"$set":{"legendary_pantry":accepter_legendary_pantry}})
        
        embed = discord.Embed(description = "Trade Complete!", colour =0x0dff00)
        await message.edit(embed = embed)

          

      elif trader == accepter:
        embed = discord.Embed(description = "Trade cancelled", colour = 0xff1100)
        await message.edit(embed = embed)
      else:
        embed = discord.Embed(description = "Error: Cards aren't available", colour = 0xff1100)
        embed.set_footer(text = "You also can't trade two of the same card")
        await message.edit(embed = embed)



client.load_extension("cogs.misc")
client.load_extension("cogs.game") 



 
keep_alive()

client.run(os.getenv('TOKEN'))

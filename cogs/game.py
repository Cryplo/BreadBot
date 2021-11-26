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


pantry_limit = config.pantry_limit
common_bread = config.common_bread
rare_bread = config.rare_bread
mythical_bread = config.mythical_bread
legendary_bread = config.legendary_bread
updateLog = config.updateLog
helpContent = config.helpContent
faqContent = config.faqContent
bakePercents = config.bake_percents

async def initCommand(ctx):
    global myquery
    global user
    global collection
    global database
    global cluster
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
    collection.update_one({"_id": ctx.author.id}, {"$set": {"name": ctx.author.name}})
    for result in user:
        pantry = result["pantry"]
        card_cooldown = result["card_cooldown"]
        farm_cooldown = result["farm_cooldown"]
        grain = int(result["grain"])
        document = collection.find_one(myquery)
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
            db_set(ctx.author.id,"chests",{"1st":0,"2nd":0,"3rd":0,"4th":0,"5th":0})
            chests = result["chests"]
        if "hourly_cooldown" in document.keys():
            hourly_cooldown = result["hourly_cooldown"]
        if "chests" not in document.keys():
            db_set(ctx.author.id,"hourly_cooldown",0)
            hourly_cooldown = result["hourly_cooldown"]
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

    def __init__(self, client):
        self.client = client

    @commands.command(name="bake")
    async def bake(self, ctx):
        await initCommand(ctx)
        # Checks to make sure baking meets requirements
        if time.time() - card_cooldown >= config.bake_cooldown and len(pantry) < pantry_limit:
            ran_card_category = random.randint(1, 1000)
            # Common Card Baked
            if ran_card_category <= bakePercents[0]:
                card_category = "common"
                card = common_bread[random.randint(0, len(common_bread) - 1)]
                embed = discord.Embed(description="Congratulations, you baked a " + card + ". This card is a common",
                                      colour=0x808080)
                await ctx.send(embed=embed)
            # Rare Card Baked
            elif ran_card_category <= bakePercents[0]+bakePercents[1]:
                card = rare_bread[random.randint(0, len(rare_bread) - 1)]
                card_category = "rare"
                embed = discord.Embed(description="Congratulations, you baked a " + card + ". This card is a rare",
                                      colour=0x0073ff)
                await ctx.send(embed=embed)
            # Mythical Card Baked
            elif ran_card_category <= bakePercents[0]+bakePercents[1]+bakePercents[2]:
                card = mythical_bread[random.randint(0, len(mythical_bread) - 1)]
                card_category = "mythical"
                embed = discord.Embed(description="Congratulations, you baked a " + card + ". This card is a mythical",
                                      colour=0xb700ff)
                await ctx.send(embed=embed)
            # Legendary Card Baked
            elif ran_card_category:
                card = legendary_bread[random.randint(0, len(legendary_bread) - 1)]
                card_category = "legendary"
                embed = discord.Embed(
                    description="Congratulations, you baked a " + card + ". This card is a LEGENDARY!", colour=0xfbff00)
                await ctx.send(embed=embed)
            db_push(ctx.author.id, "pantry", card)
            db_set(ctx.author.id, "card_cooldown", time.time())
            return
            # Cooldown Time
        if time.time() - card_cooldown < config.bake_cooldown:
            delay_left = config.bake_cooldown - (time.time() - card_cooldown)
            embed = discord.Embed(
                description='You have ' + convert(delay_left) + ' left until you can use this command again',
                colour=0xff1100)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="You have don't have any more room left in your pantry", colour=0xff1100)
            await ctx.send(embed=embed)

    @commands.command(name="pantry")
    async def show_pantry(self, ctx, member: discord.Member = None):
        await initCommand(ctx)
        global pantry
        global common_pantry
        global rare_pantry
        global mythical_pantry
        global legendary_pantry
        global simplified_common_pantry
        global simplified_rare_pantry
        global simplified_mythical_pantry
        global simplified_legendary_pantry
        await initCommand(ctx)
        global user
        if member != None:
            myquery = {"_id": member.id}
            if (collection.count_documents(myquery) == 0):
                return
            user = collection.find(myquery)
            viewing_user = await self.client.fetch_user(member.id)
        else:
            viewing_user = ctx.author
        for result in user:
            pantry = result["pantry"]
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

        common_shown = [count_duplicates(x, counted_pantry) for x in simplified_common_pantry]
        rare_shown = [count_duplicates(x, counted_pantry) for x in simplified_rare_pantry]
        mythical_shown = [count_duplicates(x, counted_pantry) for x in simplified_mythical_pantry]
        legendary_shown = [count_duplicates(x, counted_pantry) for x in simplified_legendary_pantry]
        seperator = ", "
        pantry_shown = '**Commons**: ' + seperator.join(sorted(common_shown)) + '\n\n**Rares**: ' + seperator.join(
            sorted(rare_shown)) + '\n\n**Mythicals**: ' + seperator.join(
            sorted(mythical_shown)) + '\n\n**Legendaries** ' + seperator.join(sorted(legendary_shown))

        embed = discord.Embed(title=viewing_user.name + "'s pantry:", description=pantry_shown, colour=0x000000)
        embed.set_footer(text='Cards sell value: ' + str(
            len(common_pantry) * 500 + len(rare_pantry) * 2500 + len(mythical_pantry) * 6000 + len(
                legendary_pantry) * 20000) + ' grain' + " | Size: " + str(len(pantry)) + "/" + str(pantry_limit))
        await ctx.send(embed=embed)

    @commands.command(name="grain")
    async def show_grain(self, ctx, member: discord.Member = None):
        await initCommand(ctx)
        if member != None:
            viewing_id = member.id
        else:
            viewing_id = ctx.author.id
        viewing = collection.find({"_id": viewing_id})
        if collection.count_documents({"_id": viewing_id}) == 1:
            for result in viewing:
                grain = result["grain"]
        viewing_user = await self.client.fetch_user(viewing_id)
        embed = discord.Embed(title=str(viewing_user.name) + "'s grain:", description=grain, colour=0x000000)
        await ctx.send(embed=embed)

    @commands.command(name="farm")
    async def farm(self, ctx):
        await initCommand(ctx)
        global grain
        global farm_cooldown
        jackpot = random.randint(1, 100)
        if time.time() - farm_cooldown > 10 and jackpot < 90:
            grain_gained = random.randint(10, 25)
            farm_cooldown = time.time()
            grain = grain + grain_gained
            embed = discord.Embed(description='You gained ' + str(grain_gained) + ' pieces of grain', colour=0x0dff00)
            await ctx.send(embed=embed)
            db_set(ctx.author.id, "grain", grain)
            db_set(ctx.author.id, "farm_cooldown", farm_cooldown)
            return
        if time.time() - farm_cooldown > 10 and jackpot >= 90 and jackpot < 99:
            grain_gained = random.randint(35, 65)
            farm_cooldown = time.time()
            grain = grain + grain_gained
            embed = discord.Embed(description='Mini Jackpot! You gained ' + str(grain_gained) + ' pieces of grain',
                                  colour=0x0dff00)
            await ctx.send(embed=embed)
            db_set(ctx.author.id, "grain", grain)
            db_set(ctx.author.id, "farm_cooldown", farm_cooldown)
            return
        if time.time() - farm_cooldown > 10 and jackpot >= 99:
            grain_gained = random.randint(110, 140)
            farm_cooldown = time.time()
            grain = grain + grain_gained
            embed = discord.Embed(description='HUGE JACKPOT!!! You gained ' + str(grain_gained) + ' pieces of grain',
                                  colour=0x0dff00)
            await ctx.send(embed=embed)
            db_set(ctx.author.id, "grain", grain)
            db_set(ctx.author.id, "farm_cooldown", farm_cooldown)
            return
        else:
            farm_delay_left = 10 - (int(time.time()) - int(farm_cooldown))
            embed = discord.Embed(
                description='You have ' + str(farm_delay_left) + ' seconds left until you can use this command again',
                colour=0xff1100)
            await ctx.send(embed=embed)

    @commands.command(name="sell")
    async def sell(self, ctx, *, sell_input):
        global grain
        await initCommand(ctx)
        selling_cards = []
        if sell_input in pantry:
            if sell_input in common_pantry:
                pantry.remove(sell_input)
                grain = grain + 500
                embed = discord.Embed(title=sell_input + " has been sold!",
                                      description=sell_input + " has been sold for 500 grain", colour=0x0dff00)
                await ctx.send(embed=embed)
            if sell_input in rare_pantry:
                pantry.remove(sell_input)
                grain = grain + 2500
                embed = discord.Embed(title=sell_input + " has been sold!",
                                      description=sell_input + " has been sold for 2500 grain", colour=0x0dff00)
                await ctx.send(embed=embed)
            if sell_input in mythical_pantry:
                pantry.remove(sell_input)
                grain = grain + 6000
                embed = discord.Embed(title=sell_input + " has been sold!",
                                      description=sell_input + " has been sold for 6000 grain", colour=0x0dff00)
                await ctx.send(embed=embed)
            if sell_input in legendary_pantry:
                pantry.remove(sell_input)
                grain = grain + 20000
                embed = discord.Embed(title=sell_input + " has been sold!",
                                      description=sell_input + " has been sold for 20000 grain", colour=0x0dff00)
                await ctx.send(embed=embed)
            db_set(ctx.author.id, "pantry", pantry)
            db_set(ctx.author.id, "grain", grain)
            return
        if sell_input == 'all':
            collection.update_one({"_id": ctx.author.id}, {"$set": {"pantry": []}})
            grain_gained = len(common_pantry) * 500 + len(rare_pantry) * 2500 + len(mythical_pantry) * 6000 + len(
                legendary_pantry) * 20000
            collection.update_one({"_id": ctx.author.id}, {"$set": {"grain": grain + grain_gained}})

            embed = discord.Embed(title="You have sold your entire pantry",
                                  description="You have sold your entire pantry and gained " + str(
                                      grain_gained) + " grain", colour=0x0dff00)
            await ctx.send(embed=embed)
            return
        if sell_input == "commons":
            collection.update_one({"_id": ctx.author.id},
                                  {"$set": {"pantry": [x for x in pantry if x not in common_pantry]}})

            grain_gained = len(common_pantry) * 500

            collection.update_one({"_id": ctx.author.id}, {"$set": {"grain": grain + grain_gained}})

            embed = discord.Embed(title="You have sold all your common cards",
                                  description="You have sold all your common cards and gained " + str(
                                      grain_gained) + " grain", colour=0x0dff00)
            await ctx.send(embed=embed)
            return

        if sell_input == "rares":
            collection.update_one({"_id": ctx.author.id},
                                  {"$set": {"pantry": [x for x in pantry if x not in rare_pantry]}})

            grain_gained = len(rare_pantry) * 2500

            collection.update_one({"_id": ctx.author.id}, {"$set": {"grain": grain + grain_gained}})

            embed = discord.Embed(title="You have sold all your rare cards",
                                  description="You have sold all your rare cards and gained " + str(
                                      grain_gained) + " grain", colour=0x0dff00)
            await ctx.send(embed=embed)
            return

        if sell_input == "mythicals":
            collection.update_one({"_id": ctx.author.id},
                                  {"$set": {"pantry": [x for x in pantry if x not in mythical_pantry]}})

            grain_gained = len(mythical_pantry) * 12000

            collection.update_one({"_id": ctx.author.id}, {"$set": {"grain": grain + grain_gained}})

            embed = discord.Embed(title="You have sold all your mythical cards",
                                  description="You have sold all your mythical cards and gained " + str(
                                      grain_gained) + " grain", colour=0x0dff00)
            await ctx.send(embed=embed)
            return

        if sell_input == "legendaries":
            collection.update_one({"_id": ctx.author.id},
                                  {"$set": {"pantry": [x for x in pantry if x not in legendary_pantry]}})

            grain_gained = len(legendary_pantry) * 40000

            collection.update_one({"_id": ctx.author.id}, {"$set": {"grain": grain + grain_gained}})

            embed = discord.Embed(title="You have sold all your legendary cards",
                                  description="You have sold all your legendary cards and gained " + str(
                                      grain_gained) + " grain", colour=0x0dff00)
            await ctx.send(embed=embed)
            return
        else:
            await ctx.send("You either don't have this item or it doesn't exist")

    @commands.command(name="cards")
    async def cards(self, ctx):
        seperator = ', '
        cards_shown = '**Commons**: ' + seperator.join(sorted(common_bread)) + '\n\n**Rares**: ' + seperator.join(
            sorted(rare_bread)) + '\n\n**Mythicals**: ' + seperator.join(
            sorted(mythical_bread)) + '\n\n**Legendaries**: ' + seperator.join(sorted(legendary_bread))

        embed = discord.Embed(title="All cards:", description=cards_shown, colour=0x000000)
        await ctx.send(embed=embed)

    @commands.command(name="prices")
    async def prices(self, ctx):
        embed = discord.Embed(title="Prices:",
                              description="**Buying**\n`Common cards`: 1000 grain\n`Rare cards`: 5000 grain\n `Mythical cards`: 12000 grain\n `Legendary cards`: 40000 grain\n\n**Selling**\n`Common cards`: 500 grain\n`Rare cards`: 2500 grain\n `Mythical cards`: 6000 grain\n`Legendary cards`: 20000 grain",
                              colour=0x000000)
        await ctx.send(embed=embed)

    @commands.command(name="buy")
    async def buy(self, ctx, *, buying_card):
        await initCommand(ctx)
        global grain
        for result in user:
            grain = int(result["grain"])
        if buying_card in common_bread and grain >= 1000 and len(pantry) < pantry_limit:
            grain = grain - 1000
            card = buying_card
            embed = discord.Embed(
                description="Congratulations, you bought a " + card + " for 1000 grain. This card is a common",
                colour=0x808080)
            await ctx.send(embed=embed)
            collection.update_one({"_id": ctx.author.id}, {"$push": {"pantry": card}})
            collection.update_one({"_id": ctx.author.id}, {"$set": {"grain": grain}})
            return
        if buying_card in rare_bread and grain >= 5000 and len(pantry) < pantry_limit:
            card = buying_card
            grain = grain - 5000
            embed = discord.Embed(
                description="Congratulations, you bought a " + card + " for 5000 grain. This card is a rare",
                colour=0x0073ff)
            await ctx.send(embed=embed)
            collection.update_one({"_id": ctx.author.id}, {"$push": {"pantry": card}})
            collection.update_one({"_id": ctx.author.id}, {"$set": {"grain": grain}})
            return

        if buying_card in mythical_bread and grain >= 12000 and len(pantry) < pantry_limit:
            card = buying_card
            grain = grain - 12000

            embed = discord.Embed(
                description="Congratulations, you bought a " + card + " for 12000 grain. This card is a mythical",
                colour=0xb700ff)
            await ctx.send(embed=embed)
            collection.update_one({"_id": ctx.author.id}, {"$push": {"pantry": card}})
            collection.update_one({"_id": ctx.author.id}, {"$set": {"grain": grain}})

            return

        if buying_card in legendary_bread and grain >= 40000 and len(pantry) < pantry_limit:
            card = buying_card
            grain = grain - 40000

            embed = discord.Embed(
                description="Congratulations, you bought a " + card + " for 40000 grain. This card is a LEGENDARY!",
                colour=0xfbff00)
            await ctx.send(embed=embed)
            collection.update_one({"_id": ctx.author.id}, {"$push": {"pantry": card}})

            collection.update_one({"_id": ctx.author.id}, {"$set": {"grain": grain}})
            return

        if buying_card not in legendary_bread and buying_card not in mythical_bread and buying_card not in rare_bread and buying_card not in common_bread:
            embed = discord.Embed(description="This card doesn't exist", colour=0xff1100)
            embed.set_footer(text="To check all cards, type .bread cards")
            await ctx.send(embed=embed)

        elif len(pantry) >= pantry_limit:
            embed = discord.Embed(description="You have don't have any more room left in your pantry", colour=0xff1100)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description="You don't have enough grain", colour=0xff1100)
            embed.set_footer(text="To check the prices of bread, type .bread prices")
            await ctx.send(embed=embed)

    @commands.command(name="bet")
    async def bet(self, ctx, gambling: str):
        await initCommand(ctx)
        if str(gambling).isdigit() == True and int(gambling) <= grain:
            coin = random.randint(1, 100)
            if coin <= 60:
                gambling = int(gambling)
                gambling = gambling * (random.randint(20, 100) / 100)
                gambling = math.floor(gambling)

                collection.update_one({"_id": ctx.author.id}, {"$set": {"grain": grain + gambling}})
                embed = discord.Embed(title="You won the bet!",
                                      description="You won the bet and gained " + str(gambling) + " pieces of grain",
                                      colour=0x0dff00)

                await ctx.send(embed=embed)

            if coin > 60:
                gambling = int(gambling)
                collection.update_one({"_id": ctx.author.id}, {"$set": {"grain": grain - gambling}})

                embed = discord.Embed(title="You lost the bet.",
                                      description="You lost the bet and lost " + str(gambling) + " pieces of grain",
                                      colour=0xff1100)

                await ctx.send(embed=embed)

        if str(gambling).isdigit() == True and int(gambling) > grain:
            embed = discord.Embed(description="You don't have this much grain", colour=0xff1100)

            await ctx.send(embed=embed)

        if str(gambling).isdigit() == False:
            embed = discord.Embed(description="Please enter a non-negative integer to bet", colour=0xff1100)

            await ctx.send(embed=embed)
    @commands.command(name="leaderboard")
    async def leaderboard(self,ctx):
      global common_pantry
      global rare_pantry
      global mythical_pantry
      global legendary_pantry
      global pantry
      leaderboard = []
      for doc in collection.find():
        pantry = doc["pantry"]
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
        networth = len(common_pantry) * 1000 + len(rare_pantry) * 5000 + len(mythical_pantry) * 12000 + len(legendary_pantry) * 40000
        doc.update({"networth":networth+doc["grain"]})
        leaderboard.append(doc)
      leaderboard.sort(key=lambda e: e['networth'], reverse = True)
      sending_string = ""
      for n in range(0,10):
        user = await self.client.fetch_user(leaderboard[n]["_id"])
        sending_string += user.name+": "+str(f"{leaderboard[n]['networth']:,}")+"\n"
      embed = discord.Embed(title="Global Leaderboard By Networth",
          description=sending_string,
          colour=0x0dff00)
      await ctx.send(embed=embed)
    @commands.command(name="open")
    async def open_chest(self,ctx,tier:int):
      await initCommand(ctx)
      chest_cards = {}
      if tier == 5:
        if chests["5th"]>0:
          chest_cards.update({rare_bread[random.randint(0, len(rare_bread) - 1)]:"rare"})
          chest_cards.update({common_bread[random.randint(0, len(common_bread) - 1)]:"common"})
          chest_cards.update({common_bread[random.randint(0, len(common_bread) - 1)]:"common"})
          for n in chest_cards:
            db_push(ctx.author.id,"pantry",n)
          embed = discord.Embed(title=ctx.author.name+"'s fifth tier chest has been opened!",description="It contains:\n**"+list(chest_cards.keys())[0]+"**: "+list(chest_cards.values())[0]+"\n**"+list(chest_cards.keys())[1]+"**: "+list(chest_cards.values())[1]+"\n**"+list(chest_cards.keys())[2]+"**: "+list(chest_cards.values())[2])
          db_set(ctx.author.id,"chests.5th",chests["5th"]-1)
          await ctx.send(embed=embed)
    @commands.command(name="chests")
    async def show_chests(self,ctx):
      await initCommand(ctx)
      embed= discord.Embed(title=ctx.author.name+"'s' chests", description = "1st Tier Chests: "+str(chests["1st"])+"\n2nd Tier Chests: "+str(chests["2nd"])+"\n3rd Tier Chests: "+str(chests["3rd"])+"\n4th Tier Chests: "+str(chests["4th"])+"\n5th Tier Chests: "+str(chests["5th"]))
      await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Game(client))

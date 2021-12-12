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

class BreadCard:
  def __init__(self,name,atk,hp):
    self.name = name
    self.attack = atk
    self.health = hp
class Boss:
  def __init__(self,name,atk,hp):
    self.name = name
    self.attack = atk
    self.health = hp
class Battle(commands.Cog):
  def __init__(self, client):
    self.client = client
  @commands.command(name="battle")
  async def battle(self,ctx):
    await ctx.send("Battle Started!")
    playerBread = []
    for i in range(0,8):
      playerBread.append(BreadCard("Test Bread",10,10))
    msg = ctx.author.name+"'s deck:\n"
    for i in range(0,len(playerBread)-1):
      bread = playerBread[i]
      msg += bread.name+": "+str(bread.attack)+"atk "+str(bread.health)+"hp\n"
    await ctx.send(msg)
      
  


def setup(client):
  client.add_cog(Battle(client))
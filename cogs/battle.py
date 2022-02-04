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
from discord.ui import Button, View, Select
import asyncio

class BreadCard:
  def __init__(self,name,atk,hp,shield,crit,heal):
    self.name = name
    self.attack = atk
    self.health = hp
    self.shield = shield
    self.crit = crit
    self.heal = heal
class Boss:
  def __init__(self,name,atk,hp,shield,crit):
    self.name = name
    self.attack = atk
    self.health = hp
    self.shield = shield
    self.crit = crit
class Battle(commands.Cog):
  def __init__(self, client):
    self.client = client
  @commands.command(name="battle")
  async def battle(self,ctx):
    global breadDisplayIndex
    await ctx.send("Battle Started!")
    playerBread = []
    for i in range(0,8):
      playerBread.append(BreadCard("Test Bread "+str(i+1),10,10,5,0.05,5))
    
    boss = Boss("Joe",20,400,30,0.05)
    shownBread = 0
    breadDisplayIndex = 0
    async def getBreadInfo(i):
      bread = playerBread[i]
      msg = f"""**{bread.name}**
      ⚔️ {bread.attack}
      💥 {str(bread.crit*100)+"%"}
      ❤️ {bread.health}
      💖 {bread.heal}
      🛡️ {bread.shield}\n"""
      
      return msg
    
    view = View()
    button1 = Button(
      label = "<<<",
      style= discord.ButtonStyle.green,
      )
    button2 = Button(
      label = "<",
      style= discord.ButtonStyle.green,
      )
    button3 = Button(
      label = ">",
      style= discord.ButtonStyle.green,
      )
    button4 = Button(
      label = ">>>",
      style= discord.ButtonStyle.green,
      )
    
    
    async def button1_callback(interaction):
      global breadDisplayIndex
      if interaction.user.id != ctx.author.id:
        return
      breadDisplayIndex = 0
      await editDisplayMessage(interaction)
    async def button2_callback(interaction):
      global breadDisplayIndex
      if interaction.user.id != ctx.author.id:
        return
      breadDisplayIndex -= 1
      await editDisplayMessage(interaction)
    async def button3_callback(interaction):
      global breadDisplayIndex
      if interaction.user.id != ctx.author.id:
        return
      breadDisplayIndex += 1
      await editDisplayMessage(interaction)
    async def button4_callback(interaction):
      global breadDisplayIndex
      if interaction.user.id != ctx.author.id:
        return
      breadDisplayIndex = 7
      await editDisplayMessage(interaction)
    async def editDisplayMessage(interaction):
      global breadDisplayIndex
      if breadDisplayIndex > 7:
        breadDisplayIndex = 0
      if breadDisplayIndex < 0:
        breadDisplayIndex = 7
      msg = await getBreadInfo(breadDisplayIndex)
      await interaction.response.edit_message(content=msg)
    
    button1.callback = button1_callback
    button2.callback = button2_callback
    button3.callback = button3_callback
    button4.callback = button4_callback
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)


    msg = await getBreadInfo(breadDisplayIndex)
    await ctx.send(msg, view = view)

    msg = f"""**Boss: {boss.name}**
      ⚔️ {boss.attack}  💥 {str(boss.crit*100)+"%"}  ❤️ {boss.health}  🛡️ {boss.shield}
      """
    await ctx.send(msg)
    await ctx.send("Are you sure you want to battle? (y/n)")
    text = await self.client.wait_for("message", check = lambda message: message.content.lower()=="y" or message.content.lower()=="n")
    if text.content.lower() != "y":
      await ctx.send("Exited battle")
      return
    startingCards = []
    backupCards = playerBread.copy()
    for i in range(0,4):
      randomCard = backupCards[random.randint(0,len(backupCards)-1)]
      startingCards.append(randomCard)
      backupCards.remove(randomCard)
    
    

    
    
    battle = True
    runOnce = 0
    global turn
    turn = 0

    async def getBattleMsg(turn):
      msg = "Battle!\n"
      msg += f"""{boss.name}
      ❤️ {boss.health}     🛡️ {boss.shield}\n"""
      for i in range(0,4):
        if i == turn:
          bread = startingCards[i]
          msg+=f"""**Turn: {bread.name}**
          ⚔️ {bread.attack}  💥 {str(bread.crit*100)+"%"}  ❤️ {bread.health}  💖 {bread.heal}  🛡️ {bread.shield}\n"""
        else:
          bread = startingCards[i]
          msg+=f"""{bread.name}
          ⚔️ {bread.attack}  💥 {str(bread.crit*100)+"%"}  ❤️ {bread.health}  💖 {bread.heal}  🛡️ {bread.shield}\n"""
      return msg



    async def callbackAttack(interaction):
      global turn
      boss.health -= startingCards[turn].attack
      turn += 1
      msg = await getBattleMsg(turn)
      await interaction.response.edit_message(content = msg,view=view)
      

      
    buttonAttack = Button(
      label = "Attack",
      style = discord.ButtonStyle.primary
    )
    buttonHeal = Button(
      label = "Heal",
      style = discord.ButtonStyle.primary
    )
    view = View()
    buttonAttack.callback = callbackAttack
    view.add_item(buttonAttack)
    view.add_item(buttonHeal)
    
      
    
    
    if runOnce == 0:
      msg = await getBattleMsg(turn)
      await ctx.send(msg,view=view)
      runOnce = 1
      
      
      

    
      
  


def setup(client):
  client.add_cog(Battle(client))
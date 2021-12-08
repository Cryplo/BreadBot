import discord
from discord.ext import commands
import random
import config


class Misc(commands.Cog):
    """Miscellaneous Commands"""

    def __init__(self, client):
        self.client = client

    @commands.command(name="github")
    async def github(self, ctx):
        await ctx.send("Contribute to the Bot! https://github.com/Cryplo/BreadBot")

    @commands.command(name="servers")
    async def servers(self, ctx):
        await ctx.send("I'm in " + str(len(self.client.guilds)) + " servers.")

    @commands.command(name="invitelink")
    async def invitelink(self, ctx):
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=819653343839911956&permissions=8&scope=bot')

    @commands.command(name="updatelog")
    async def showUpdateLog(self, ctx):
        embed = discord.Embed(description=config.updateLog, colour=0x000000)
        await ctx.send(embed=embed)

    @commands.command(name="faq")
    async def faq(self, ctx):
        embed = discord.Embed(description=config.faqContent, colour=0x000000)
        await ctx.send(embed=embed)
    @commands.command(name="guess")
    async def guess(self,ctx):
      await ctx.send('Guess a number between 1 and 10.')

      def is_correct(m):
          return m.author == ctx.author and m.content.isdigit()

      answer = random.randint(1, 10)
      correct = False
      while correct == False:
        guess = await self.client.wait_for('message', check=is_correct)


        if int(guess.content) == answer:
          await ctx.send('You are right!')
          correct = True
        else:
          await ctx.send('Oops. Guess Again.')

    @commands.command(name="thumb")
    async def thumb(self,ctx):
      await ctx.send('Send me that 👍 reaction, mate')

      def check(reaction, user):
          return user == ctx.author

      reaction, user = await self.client.wait_for('reaction_add', check=check)
      if (reaction.emoji) == '👍':
        await ctx.send('👍')
      else:
        await ctx.send('👍 emoji not '+reaction.emoji)


def setup(client):
    client.add_cog(Misc(client))

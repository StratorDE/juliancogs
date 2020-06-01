from redbot.core import commands
import praw
import discord
import random

class Frage(commands.Cog):


    @commands.command()
    async def frage(self,ctx, frage):
            lines = ['Ja!', 'Nein!', 'Vielleicht.']
            nachricht = random.choice(lines)
            await ctx.send(nachricht)

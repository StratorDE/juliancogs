from redbot.core import commands
import discord

class Sponge(commands.Cog):


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        msg = message.content


    @commands.command()
    async def sponge(self, ctx):
        msg = "".join(c.lower() if i % 2 == 1 else c for i, c in enumerate(msg.upper()))
        await ctx.send(msg)
        

        

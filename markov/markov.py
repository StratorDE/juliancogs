from redbot.core import commands
from chattymarkov import ChattyMarkov
import discord
class Markov(commands.Cog):
    
    markov = ChattyMarkov('redis:///home/strator/.redis/sock;db=0')
    #markov = ChattyMarkov('redis://localhost:6379;db=0')


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content.startswith('?'):
            return
        leser = ChattyMarkov('redis:///home/strator/.redis/sock;db=0')
        leser.learn(message.content)


    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def schlaganfall(self,ctx):
        await ctx.message.delete()
        nachricht = self.markov.generate()
        nachricht = nachricht.replace('"','')
        await ctx.send(nachricht)

    @schlaganfall.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()

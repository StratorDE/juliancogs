from redbot.core import commands
from chattymarkov import ChattyMarkov
import discord
class Markov(commands.Cog):
    
    markov = ChattyMarkov('redis:///home/strator/.redis/sock;db=0')
    isActive = True



    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content.startswith('?'):
            return
        if not self.isActive:
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
    
    @commands.command()
    async def markovstatus(self, ctx):
        if self.isActive:
            nachricht = 'Markov ist aktiv.'
        else:
            nachricht = 'Markov ist inaktiv.'
        await ctx.send(nachricht)
    
    @commands.command()
    async def markovaus(self, ctx):
        self.isActive = False
    
    @commands.command()
    async def markovan(self, ctx):
        self.isActive = True

    @schlaganfall.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()

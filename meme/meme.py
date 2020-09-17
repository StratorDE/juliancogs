from redbot.core import commands
import praw
import discord
import random

class Meme(commands.Cog):
	reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,user_agent=USER_AGENT, username=USERNAME, password=PASSWORD)


    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def meme(self,ctx):
            lines = ['me_irl', 'dankmemes']
            sub = random.choice(lines)
            randomsub = self.reddit.subreddit(sub).random()
            await ctx.send(randomsub.title)
            await ctx.send(randomsub.url)
    @meme.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def maimai(self,ctx):
            lines = ['ich_iel', 'okbrudimongo']
            sub = random.choice(lines)
            randomsub = self.reddit.subreddit(sub).random()
            await ctx.send(randomsub.title)
            await ctx.send(randomsub.url)
    @maimai.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()
    
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def nerd(self,ctx):
            lines = ['programmerhumor', 'chemistrymemes', 'biologymemes', 'networkingmemes']
            sub = random.choice(lines)
            randomsub = self.reddit.subreddit(sub).random()
            await ctx.send(randomsub.title)
            await ctx.send(randomsub.url)
    @nerd.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def ente(self,ctx):
            lines = ['ltb_iel']
            sub = random.choice(lines)
            randomsub = self.reddit.subreddit(sub).random()
            await ctx.send(randomsub.title)
            await ctx.send(randomsub.url)
    @ente.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def mbmeme(self,ctx):
            lines = ['mbdiscordperlen','mbundestagmemes']
            sub = random.choice(lines)
            randomsub = self.reddit.subreddit(sub).random()
            await ctx.send(randomsub.title)
            await ctx.send(randomsub.url)
    @mbmeme.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()

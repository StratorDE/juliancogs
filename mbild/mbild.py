from redbot.core import commands
import praw
import discord

class mbild(commands.Cog):

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None:
            return
        

        if message.content.startswith("+++") and message.content.endswith("+++") and len(message.content) >= 8:
            reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,user_agent=USER_AGENT, username=USERNAME, password=PASSWORD)
            subreddit = 'mbild'
            titel = message.content
            reddit.subreddit('mbild').submit(titel, selftext="Siehe Titel.")
            emoji = '📰'
            await message.add_reaction(emoji)

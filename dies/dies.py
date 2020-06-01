from redbot.core import commands
import discord
from random import randint

class Dies(commands.Cog):

    counter = 0
    pruefung = randint(25, 150)
    


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        if message.author.id == 569097256217870336:
            return

        if self.pruefung == self.counter:
            self.counter = 0
            emoji = '<:diesuezs:617269686341599243>'
            await message.add_reaction(emoji)
            self.pruefung = randint(25,150)

        self.counter = self.counter + 1

        

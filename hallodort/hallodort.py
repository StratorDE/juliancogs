from redbot.core import commands
import discord


#Dieses Modul stammt nicht von mir, sonder von tim. Vielen Dank tim!

class HalloDort(commands.Cog):

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
    
        if any(x in message.content.lower() for x in {"hallo dort", "hello there"}):
            await message.channel.send("General Kenobi!")

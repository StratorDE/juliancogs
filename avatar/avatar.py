from redbot.core import commands
import discord

class Avatar(commands.Cog):



    @commands.command()
    async def avatar(self,ctx,user: discord.User = None):
        if user is None:
            user = ctx.author

        avatar_url = user.avatar_url_as(static_format='png')

        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.title = f"Profilbild von {user.display_name}"
        embed.description = f"[LINK]({avatar_url})"
        embed.set_image(url=str(avatar_url))
        await ctx.send(embed=embed)

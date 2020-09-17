from .teststore import Teststore

def setup(bot):
    bot.add_cog(Teststore(bot))

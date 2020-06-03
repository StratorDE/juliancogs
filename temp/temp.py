from redbot.core import commands
import Adafruit_DHT

class Temp(commands.Cog):




    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def stratortemp(self,ctx):
        pin = 2
        sensor = Adafruit_DHT.DHT22
        humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)
        humidity = str(round(humidity, 2))
        temperature = str(round(temperature, 2))

        await ctx.send(f"Die Temperatur in Strators Zimmer beträgt {temperature} Grad Celsius, bei einer Luftfeuchtigkeit von {humidity}%!")

    @stratortemp.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()

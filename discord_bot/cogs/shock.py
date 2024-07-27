import nextcord
from nextcord.ext import commands
from helpers import jsonHelper, embedHelper, arduinoHelper
import asyncio

config = jsonHelper.loadConfig()

modes = {
    "shock" : 83,
    "vibrate" : 86,
    'beep' : 66,
    'pair' : 80,
    'stop' : 69
}

# actually the other button sends duration 300?
async def shock(intensity, dur, mode):
    dur = int(dur / 30 * 25.6)
    if(dur < 1):
        dur = 1
    if(dur >= 256):
        dur = 255
    print(dur)
    arduinoHelper.arduino.write(bytearray([modes[mode], 1, intensity, dur]))
    await asyncio.sleep(0.05)
    data = arduinoHelper.arduino.readline()
    int_val = int.from_bytes(data, "big")
    return int_val


class Shock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    async def shock(self, ctx,
            power: int = nextcord.SlashOption(description="Shock strength (between 1-99)"),
            duration: int = nextcord.SlashOption(description="Shock duration, in tenths of a second (between 1-300)")
        ):
        """
        Send a shock!
        """
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(ctx.user.id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "You are not whitelisted!"
            ))
            return
        if(not (0 <= power <= 99)):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "Please input a value between 1 and 99 for shock strength."
            ))
            return
        val = await shock(power, duration, 'shock')
        if(val == 0):
            await ctx.send(embed = embedHelper.sucEmbed(
            "Shock Successful!",
            "Please await your cries."
        ))
            print(f"Shocked at power: {power} for duration: {duration}")
        else:
            await ctx.send(embed = embedHelper.errEmbed(
            "Shock Unsuccessful!",
            "Operation already in progress."
        ))
            
    @nextcord.slash_command()
    async def vibe(self, ctx,
            power: int = nextcord.SlashOption(description="Vibration strength (between 1-99)"),
            duration: int = nextcord.SlashOption(description="Vibration duration, in tenths of a second (between 1-300)")
        ):
        """
        Send a vibration!
        """
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(ctx.user.id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Vibration Unsuccessful!",
                "You are not whitelisted!"
            ))
            return
        if(not (0 <= power <= 99)):
            await ctx.send(embed = embedHelper.errEmbed(
                "Vibration Unsuccessful!",
                "Please input a value between 1 and 99 for shock strength."
            ))
            return
        val = await shock(power, duration, 'vibrate')
        if(val == 0):
            await ctx.send(embed = embedHelper.sucEmbed(
            "Vibration Successful!",
            "Please await your cries."
        ))
            print(f"Vibrated at power: {power} for duration: {duration}")
        else:
            await ctx.send(embed = embedHelper.errEmbed(
            "Vibration Unsuccessful!",
            "Operation already in progress."
        ))
            
    @nextcord.slash_command()
    async def beep(self, ctx,
            duration: int = nextcord.SlashOption(description="Beeping duration, in tenths of a second (between 1-300)")
        ):
        """
        Send a beep!
        """
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(ctx.user.id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Beep Unsuccessful!",
                "You are not whitelisted!"
            ))
            return
        val = await shock(1, duration, 'beep')
        if(val == 0):
            await ctx.send(embed = embedHelper.sucEmbed(
            "Beep Successful!",
            "Please await your cries."
        ))
            print(f"Beeped for duration: {duration}")
        else:
            await ctx.send(embed = embedHelper.errEmbed(
            "Beep Unsuccessful!",
            "Operation already in progress."
        ))
            
    @nextcord.slash_command()
    async def stop(self, ctx,):
        """
        Stop your shocker!
        """
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(ctx.user.id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Stop Unsuccessful!",
                "You are not whitelisted!"
            ))
            return
        val = await shock(1, 1, 'stop')
        if(val == 0):
            await ctx.send(embed = embedHelper.sucEmbed(
            "Stop Successful!",
            "Please await your cries."
        ))
            print(f"Stopped!")
        else:
            await ctx.send(embed = embedHelper.errEmbed(
            "Stop Unsuccessful!",
            "Operation already in progress."
        ))
            
    @nextcord.slash_command()
    async def pair(self, ctx,):
        """
        Pair your shocker!
        """
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(ctx.user.id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Pair Unsuccessful!",
                "You are not whitelisted!"
            ))
            return
        val = await shock(0, 0, 'pair')
        if(val == 0):
            await ctx.send(embed = embedHelper.sucEmbed(
            "Pair Successful!",
            "Please await your cries."
        ))
            print(f"Pairing!")
        else:
            await ctx.send(embed = embedHelper.errEmbed(
            "Pair Unsuccessful!",
            "Operation already in progress."
        ))
        
        
    @nextcord.slash_command()
    async def whitelist(self, ctx,
            user: nextcord.Member = nextcord.SlashOption(description="User to whitelist")
        ):
        """
        Whitelist a user!
        """
        if(ctx.user.id != config["user"]):
            await ctx.send(embed = embedHelper.errEmbed(
                "Whitelist Failed!",
                f"You aren't authorized."
            ))
            return
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(user.id in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Whitelist Failed!",
                f"User already whitelisted."
            ))
            return
        whitelist.append(user.id)
        jsonHelper.setJson("data/whitelist.json", whitelist)
        
        await ctx.send(embed = embedHelper.sucEmbed(
            "Whitelist Successful!",
            f"Whitelisted <@{user.id}>"
        ))

    @nextcord.slash_command()
    async def unwhitelist(self, ctx,
            user: nextcord.Member = nextcord.SlashOption(description="User to unwhitelist")
        ):
        """
        Unwhitelist a user!
        """
        if(ctx.user.id != config["user"]):
            await ctx.send(embed = embedHelper.errEmbed(
                "Whitelist Failed!",
                f"You aren't authorized."
            ))
            return
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(user.id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Whitelist Failed!",
                f"User not whitelisted."
            ))
            return
        whitelist.remove(user.id)
    
        jsonHelper.setJson("data/whitelist.json", whitelist)
        
        await ctx.send(embed = embedHelper.sucEmbed(
            "Unwhitelist Successful!",
            f"Unwhitelisted <@{user.id}>"
        ))

def setup(bot):
  bot.add_cog(Shock(bot))
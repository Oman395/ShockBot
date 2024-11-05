import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands
load_dotenv()
from helpers import jsonHelper, embedHelper
config = jsonHelper.loadConfig()

import pathlib
path = pathlib.Path(__file__).parent.resolve()

activity = nextcord.Activity(
    name="a bunch of freaks!!!",
    type = nextcord.ActivityType.watching, 
)

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents = intents)

@bot.event
async def on_ready():
    #print(f"[bot] present as {bot.user}")
    await bot.change_presence(status=nextcord.Status.online, activity=activity)

async def on_message(message):
    if message.author == bot.user:
        return

@bot.slash_command(description="Reload's the bots modules.")
async def reload(ctx):
    config = jsonHelper.loadConfig()
    for filename in os.listdir(path / "cogs"):
        if filename.endswith(".py"):
            if filename[:-3] not in config["disabledCogs"]:
                try:
                    bot.unload_extension(f"cogs.{filename[:-3]}")
                    bot.load_extension(f"cogs.{filename[:-3]}")
                    await ctx.send(embed = embedHelper.sucEmbed(
                        "Reload Successful!",
                        f"`{filename[:-3]}` has been reloaded."
                    ))
                except commands.ExtensionNotLoaded:
                    bot.load_extension(f"cogs.{filename[:-3]}")
                    await ctx.send(embed = embedHelper.sucEmbed(
                        "Load Successful!",
                        f"`{filename[:-3]}` has been loaded."
                    ))
            else:
                try:
                    bot.unload_extension(f"cogs.{filename[:-3]}")
                    await ctx.send(embed = embedHelper.errEmbed(
                        "Unload Successful!",
                        f"`{filename[:-3]}` has been unloaded."
                    ))
                except:
                    continue
    await ctx.send(embed = embedHelper.sucEmbed(
        "Reload Successful!",
        "All cogs have been reloaded."
    ))

for filename in os.listdir(path / "cogs"):
    if filename.endswith(".py") and filename[:-3] not in config["disabledCogs"]:
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv('bot_token'))

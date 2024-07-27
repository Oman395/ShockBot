from datetime import datetime
import nextcord

def defaultEmbed(title, description):
  defaultColor = nextcord.Colour.from_rgb(131,0,255)
  embed = nextcord.Embed(
    title = title,
    description = description,
    color = defaultColor,
  )
  return embed

def listEmbed(title, description, items):
  embed = defaultEmbed(title, description)
  for item in items:
    embed.add_field(name = item[0], value = item[1], inline=False)
  return embed

def logEmbed(title, description):
  embed = nextcord.Embed(
    title = title,
    description = description,
    color = nextcord.Colour.light_gray(),
    timestamp=datetime.now()
  )
  return embed

def errEmbed(title, description):
  embed = nextcord.Embed(
    title = title,
    description = description,
    color = nextcord.Colour.red(),
    timestamp=datetime.now()
  )
  return embed

def sucEmbed(title, description):
  embed = nextcord.Embed(
    title = title,
    description = description,
    color = nextcord.Colour.green(),
    timestamp=datetime.now()
  )
  return embed
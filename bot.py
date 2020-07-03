import discord
from discord.ext import commands
import config

client = commands.Bot(command_prefix='.')
@client.event
async def on_ready():
    print('Hello, world.')

client.run(config.token)
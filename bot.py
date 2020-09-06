"""
file: bot.py
author: Misty Zheng
description: bot to keep track of members' reputation in a Discord Server
"""

from discord.ext import commands
import os
import config as c


@commands.command()
async def load(ctx, extension):
    c.client.load_extension(f'cogs.{extension}')

@commands.command()
async def unload(ctx, extension):
    c.client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        c.client.load_extension(f'cogs.{filename[:-3]}')

c.client.run(c.token)
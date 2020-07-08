"""
file: bot.py
author: Misty Zheng
description: bot to keep track of members' reputation in a Discord Server
"""

import discord
#import random
from discord.ext import commands
import config

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('Hello, world.')

@client.event
async def on_member_join(member):
    print(f'Welcome {member}, the Potato Lord does not hate you.')
    #await client.send(f'Welcome {member}, the Potato Lord does not hate you.')
    channel = client.get_channel(id=701270246496927797)
    await channel.send(f'Welcome {member}, the Potato Lord does not hate you.')

@client.event
async def on_member_remove(member):
    print(f'{member}, begone thot.')
    #await client.send_message(f'{member}, begone thot.')
    channel = client.get_channel(id=701270246496927797)
    await channel.send(f'{member}, begone thot.')

"""
@client.command(aliases=['read'])
async def readme(ctx):
    responses = ['This bot was created to help run the dictatorship',
                 'Hail the Potato Lord',
                 'idk what you expected as a response']
    await ctx.send(f'{random.choice(responses)}')
"""

@client.command()
@commands.has_role('server god')
async def rep(ctx, member : discord.Member, number=0, *, reason='i feel like it'):
    channel = client.get_channel(id=729546471757840454)
    if (number >= 0):
        await channel.send(f'{member} gains {number} rep because {reason}.')
    else:
        await channel.send(f'{member} loses {number} rep because {reason}.')
@rep.error
async def rep_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Lmao, only the dictator can use this command, scrub.')

client.run(config.token)
"""
file: bot.py
author: Misty Zheng
description: bot to keep track of members' reputation in a Discord Server
"""

import discord
#import random
import person
from discord.ext import commands
import config

client = commands.Bot(command_prefix='.')

""" 
Sends a message to the terminal and creates a list 
of members with the default value of reputation when the bot is online
"""
@client.event
async def on_ready():
    global people
    people = []
    print('Hello, world.')
    x = client.get_all_members()
    for members in x:
        #print(members)
        people.append(members)

"""
Sends a welcome message to the server when a member joins and 
adds them to the list of members 
:param member: the name of the member
"""
@client.event
async def on_member_join(member):
    print(f'Welcome {member}, the Potato Lord does not hate you.')
    #await client.send(f'Welcome {member}, the Potato Lord does not hate you.')
    channel = client.get_channel(id=701270246496927797)
    await channel.send(f'Welcome {member}, the Potato Lord does not hate you.')
    people.append(member)

"""
Sends a goodbye message to the server when a member leaves and 
removes them from the list of members 
:param member: the name of the member
"""
@client.event
async def on_member_remove(member):
    print(f'{member}, begone thot.')
    #await client.send_message(f'{member}, begone thot.')
    channel = client.get_channel(id=701270246496927797)
    await channel.send(f'{member}, begone thot.')
    people.pop(member)

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
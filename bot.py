"""
file: bot.py
author: Misty Zheng
description: bot to keep track of members' reputation in a Discord Server
"""

import discord
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
        people.append(person.Person(members.name, members.id, 0))

"""
Sends a welcome message to the server when a member joins and 
adds them to the list of members 
:param member: the name of the member
"""
@client.event
async def on_member_join(member):
    print(f'Welcome {member}, the Potato Lord does not hate you.')
    channel = client.get_channel(id=701270246496927797)
    await channel.send(f'Welcome {member.display_name}, the Potato Lord does not hate you.')
    people.append(person.Person(member.name, member.id, 0))
    print(member.display_name, " has been added")

"""
Sends a goodbye message to the server when a member leaves and 
removes them from the list of members 
:param member: the name of the member
"""
@client.event
async def on_member_remove(member):
    print(f'{member}, begone thot.')
    channel = client.get_channel(id=701270246496927797)
    await channel.send(f'{member.display_name}, begone thot.')
    #people.remove(member) TODO probably need to change this

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
        for person in people:
            if person.id == member.id:
                person.change_rep(number)
                await channel.send(f'{member.display_name} gains {number} rep because {reason}.')
                await channel.send(f'{member.display_name} new rep is {person.rep}')
                break
    else:
        for person in people:
            if person.id == member.id:
                person.change_rep(number)
                await channel.send(f'{member} loses {number} rep because {reason}.')
                await channel.send(f'{member.display_name} new rep is {person.rep}')
                break
@rep.error
async def rep_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Lmao, only the dictator can use this command, scrub.')

client.run(config.token)
"""
file: bot.py
author: Misty Zheng
description: bot to keep track of members' reputation in a Discord Server
"""

import discord
import person
import botdata
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
    botdata.load_data(people)
    activity = discord.Game(name='.info | potatobot')
    await client.change_presence(activity=activity)

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
    # people.remove(member)
    # TODO need to finish this

"""
Sends an info message of the server, introducing the bot
and listing its commands
"""
@client.command()
async def info(ctx):
    await ctx.send(f'Hello, I am Potato Bot and my job is to help run the dictatorship of this server\n\n'
                   'COMMANDS \n .rep [@member] [value] [reason] : changes the rep of a member\n'
                   '.leaderboard : displays the top 5 members with the most rep \n'
                   '.shameboard : displays the top 5 members with the least amount of rep \n'
                   '.checkRep : displays the reputation of a single member \n')

"""
Adds/removes reputation to a discord member
:param member: the discord member
:param number: the amount of reputation added/removed
:param reason: the reason why the reputation changed 
"""
@client.command()
@commands.has_role('bot powers')
async def rep(ctx, member: discord.Member, number=0, *, reason='i feel like it'):
    if (number >= 0):   #adds reputation
        for person in people:
            if person.id == member.id:
                person.change_rep(number)
                await ctx.send(f'{member.display_name} gains {number} rep because {reason}.')
                await ctx.send(f'{member.display_name} new rep is {person.rep}')
                botdata.save_data(people)
                break
    else:              #removes reputation
        for person in people:
            if person.id == member.id:
                person.change_rep(number)
                await ctx.send(f'{member} loses {number} rep because {reason}.')
                await ctx.send(f'{member.display_name} new rep is {person.rep}')
                botdata.save_data(people)
                break

"""
Sends an error message if a member who does not have the correct
role tries to use the .rep command
"""
@rep.error
async def rep_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Lmao, only people with bot powers can use this command, scrub.')

"""
Returns the reputation of a given Discord member
:param person: the discord member
:return: the reputation value
"""
def by_rep(person):
    return person.rep

"""
Displays the top 5 people in the server with the most reputation
"""
@client.command()
async def leaderboard(ctx):
    people.sort(reverse=True, key=by_rep)
    counter = 1
    await ctx.send(f'Good job')
    msg = ''
    for person in people:
        msg += f'{counter} {person.name} has {person.rep} rep \n'
        counter += 1
        if counter == 6:
            break
    await ctx.send(msg)

"""
Displays the top 5 people in the server with the least amount of reputation
"""
@client.command()
async def shameboard(ctx):
    people.sort(reverse=False, key=by_rep)
    counter = 1
    await ctx.send(f'Leaderboard of shame')
    msg = ''
    for person in people:
        msg += f'{counter} {person.name} has {person.rep} rep \n'
        counter += 1
        if counter == 6:
            break
    await ctx.send(msg)


"""
Displays the reputation of a single member
:param member: the discord member
"""
@client.command()
async def checkRep(ctx, member: discord.Member = None):
    rep = 0
    if (member == None):
        member = ctx.author
    for person in people:
        if person.id == member.id:
            rep = person.rep
            break

    embed = discord.Embed(title=member.display_name + "'s Reputation",
            description=member.display_name + " has " + str(rep) + " reputation")
    embed.set_thumbnail(url=f"{member.avatar_url}")
    await ctx.send(embed=embed)

client.run(config.token)
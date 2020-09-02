import discord
import botdata
from discord.ext import commands
import bot.people as people

client = commands.Bot(command_prefix='.')

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

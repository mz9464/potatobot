import discord
import botdata
from discord.ext import commands
import config as c
from discord.utils import get
import asyncio

class Rep(commands.Cog):
    def __init__(self, client):
        self.client = client

    """
    Adds/removes reputation to a discord member
    :param member: the discord member
    :param number: the amount of reputation added/removed
    :param reason: the reason why the reputation changed 
    """

    @commands.command()
    @commands.has_role('bot powers')
    async def rep(self, ctx, member: discord.Member, number=0, *, reason='i feel like it'):
        if (number >= 0):  # adds reputation
            for person in c.people:
                if person.id == member.id:
                    person.change_rep(number)
                    embed = discord.Embed(title=member.display_name + "'s Reputation",
                                          description= f'**{member.display_name} gains {number} rep.** \n'
                                                       f'Reason: {reason}. \n'
                                                       f'{member.display_name} new rep is {person.rep}')
                    embed.set_thumbnail(url=f"{member.avatar_url}")
                    await ctx.send(embed=embed)
                    botdata.save_data(c.people)
                    break
        else:  # removes reputation
            for person in c.people:
                if person.id == member.id:
                    person.change_rep(number)
                    embed = discord.Embed(title=member.display_name + "'s Reputation",
                                          description= f'**{member.display_name} loses {number} rep.** \n'
                                                       f'Reason: {reason}. \n'
                                                       f'{member.display_name} new rep is {person.rep}')
                    embed.set_thumbnail(url=f"{member.avatar_url}")
                    await ctx.send(embed=embed)
                    botdata.save_data(c.people)
                    break

    """
    Sends an error message if a member who does not have the correct
    role tries to use the .rep command
    """

    @rep.error
    async def rep_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send('Lmao, only people with bot powers can use this command, scrub.')

    """
    Returns the reputation of a given Discord member
    :param person: the discord member
    :return: the reputation value
    """

    def by_rep(self, person):
        return person.rep

    """
    Displays the top 5 people in the server with the most reputation
    """

    @commands.command()
    async def leaderboard(self, ctx):
        c.people.sort(reverse=True, key=self.by_rep)
        counter = 1
        msg = ''
        for person in c.people:
            if (person.get_rep() < 0 or counter == 6):
                break
            msg += f'{counter} {person.name} with {person.rep} rep \n'
            counter += 1

        embed = discord.Embed(title="LEADERBOARD",
                              description=(
                                  f'**GOOD JOB TO**\n {msg}'),
                              color=ctx.author.color)
        for member in self.client.get_all_members():
            if str(member.id) == str(c.people[0].get_id()):
                embed.set_thumbnail(url=f"{member.avatar_url}")
                break
        await ctx.send(embed=embed)

    """
    Displays the top 5 people in the server with the least amount of reputation
    """

    @commands.command()
    async def shameboard(self, ctx):
        c.people.sort(reverse=False, key=self.by_rep)
        counter = 1
        msg = ''
        for person in c.people:
            if (person.get_rep() > 0 or counter == 6):
                break
            msg += f'{counter} {person.name} with {person.rep} rep \n'
            counter += 1

        embed = discord.Embed(title="LEADERBOARD OF SHAME",
                              description=(
                                  f'**GIT GUD**\n {msg}'),
                              color=ctx.author.color)
        for member in self.client.get_all_members():
            if str(member.id) == str(c.people[0].get_id()):
                embed.set_thumbnail(url=f"{member.avatar_url}")
                break
        await ctx.send(embed=embed)

    """
    Displays the reputation of a single member
    :param member: the discord member
    """

    @commands.command()
    async def checkRep(self, ctx, member: discord.Member = None):
        rep = 0
        if (member == None):
            member = ctx.author
        for person in c.people:
            if person.id == member.id:
                rep = person.rep
                break

        embed = discord.Embed(title=member.display_name + "'s Reputation",
                              description=member.display_name + " has " + str(rep) + " reputation")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        await ctx.send(embed=embed)

    """
    Adds the 'censored' role to a member
    :param member: the discord member
    :param time: amount of time the player has the role
    """
    @commands.command(pass_context = True , aliases=['hornyjail', 'censor', 'bad'])
    @commands.has_role('bot powers')
    async def jail(self, ctx, member: discord.Member, time=60):
        role = get(member.guild.roles, name = "censored")
        await member.add_roles(role)
        embed = discord.Embed(title="All hail the Potato Lord",
                              description=f"{member.display_name} has been put in jail for {time} seconds.",
                              color=ctx.author.color)
        embed.set_thumbnail(url=f"{member.avatar_url}")
        await ctx.send(embed=embed)
        await asyncio.sleep(time)
        await member.remove_roles(role)
        await ctx.send(f"{member.display_name} has been released from jail.")

def setup(client):
    client.add_cog(Rep(client))
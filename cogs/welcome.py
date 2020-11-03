"""
file: welcome.py
author: Misty Zheng
description: bot setup, keeps track of members and contains a custom help command
"""
import discord
import person
import botdata
from discord.ext import commands
import config as c

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    """ 
    Sends a message to the terminal and creates a list 
    of members with the default value of reputation when the bot is online
    """
    @commands.Cog.listener()
    async def on_ready(self):
        print('Hello, world.')
        await self.client.wait_until_ready()
        async for guild in self.client.fetch_guilds(limit=150):
            people = []
            async for member in guild.fetch_members(limit=150):
                people.append(person.Person(member.name, member.id, 0))
            c.Dict[guild.id] = botdata.load_data(guild.id, people)
        activity = discord.Game(name='.help | potatobot')
        await self.client.change_presence(activity=activity)

    """
    Sends a welcome message to the server when a member joins and 
    adds them to the list of members 
    :param member: the name of the member
    """
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title=f'Welcome {member.display_name}',
                              description='The Potato Lord does not hate you')
        embed.set_thumbnail(url=f'{member.avatar_url}')
        for channel in member.guild.channels:
            if str(channel) == "general":
                await channel.send(embed=embed)
        guild = member.guild
        c.Dict[guild.id].append(person.Person(member.name, member.id, 0))
        print(member.display_name, " has been added")
        botdata.save_data(c.Dict[guild.id])

    """
    Sends a goodbye message to the server when a member leaves and 
    removes them from the list of members 
    :param member: the name of the member
    """
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        i=0
        for p in c.Dict[guild.id]:
            if (str(p.id) == str(member.id)):
                print('found')
                break
            else:
                i += 1
        for channel in member.guild.channels:
            if str(channel) == "general":
                await channel.send(f'{member.display_name}, begone thot.')
        botdata.delete_member(guild.id, member, c.Dict[guild.id])
        if i <= len(c.Dict[guild.id]):
            c.Dict[guild.id].pop(i)
        print(f'{member} has been removed.')

    """
    Sends an info message of the server, introducing the bot
    and listing its commands
    """
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Potato Bot",
                              description=(
                                  f'Hello! I am Potato Bot and my job is to help run the dictatorship of this server\n\n'
                                  '**RESERVED COMMANDS** \n `.rep [@member] [value] [reason]` : changes the rep of a member\n'
                                  '`.jail [@member] [duration]` : puts server member in jail \n\n'
                                  '**REGULAR COMMANDS** \n `.leaderboard` : displays the top 5 members with the most rep \n'
                                  '`.shameboard` : displays the top 5 members with the least rep \n'
                                  '`.checkRep` : displays the reputation of a single member \n'),
                              color=ctx.author.color)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Welcome(client))

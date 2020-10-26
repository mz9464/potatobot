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
            server = self.client.get_guild(guild.id)
            for members in server.members:
                people.append(person.Person(members.name, members.id, 0))
                #print(members)
            c.Dict[guild.id] = people
            #print(c.Dict[guild.id])
            c.Dict[guild.id] = botdata.load_data(botdata.load_data(guild.id, people)) # need to fix this line
        #TODO need to work for all guilds
        """"
        guild = self.client.get_guild(751995614916509698)
        botdata.select_file(751995614916509698)
        for members in guild.members:
            c.people.append(person.Person(members.name, members.id, 0))
        botdata.load_data(c.people)
        """
        activity = discord.Game(name='.help | potatobot')
        await self.client.change_presence(activity=activity)

    """
    Sends a welcome message to the server when a member joins and 
    adds them to the list of members 
    :param member: the name of the member
    """

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(id=751995615382208534)
        embed = discord.Embed(title=f'Welcome {member.display_name}',
                              description='The Potato Lord does not hate you')
        embed.set_thumbnail(url=f'{member.avatar_url}')
        await channel.send(embed=embed)
        c.people.append(person.Person(member.name, member.id, 0))
        print(member.display_name, " has been added")
        botdata.save_data(c.people)

    """
    Sends a goodbye message to the server when a member leaves and 
    removes them from the list of members 
    :param member: the name of the member
    """

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(id=751995615382208534)
        i=0
        for p in c.people:
            if (str(p.id) == str(member.id)):
                print('found')
                break
            else:
                i += 1
        await channel.send(f'{member.display_name}, begone thot.')
        botdata.delete_member(member, c.people)
        if i <= len(c.people):
            c.people.pop(i)
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
                                  '**RESERVED COMMANDS** \n .rep [@member] [value] [reason] : changes the rep of a member\n'
                                  '.jail [@member] [duration] : puts server member in jail \n\n'
                                  '**REGULAR COMMANDS** \n .leaderboard : displays the top 5 members with the most rep \n'
                                  '.shameboard : displays the top 5 members with the least rep \n'
                                  '.checkRep : displays the reputation of a single member \n'),
                              color=ctx.author.color)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Welcome(client))

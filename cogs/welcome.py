import discord
import person
import botdata
from discord.ext import commands
import config as c

client = commands.Bot(command_prefix='.')

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    """ 
    Sends a message to the terminal and creates a list 
    of members with the default value of reputation when the bot is online
    """

    @commands.Cog.listener()
    async def on_ready(self):
        people = []
        # client.remove_command("help")
        print('Hello, world.')
        x = client.get_all_members()
        for members in x:
            people.append(person.Person(members.name, members.id, 0))
        botdata.load_data(people)
        activity = discord.Game(name='.info | potatobot')
        await self.client.change_presence(activity=activity)

    """
    Sends a welcome message to the server when a member joins and 
    adds them to the list of members 
    :param member: the name of the member
    """

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'Welcome {member}, the Potato Lord does not hate you.')
        channel = client.get_channel(id=701270246496927797)
        await channel.send(f'Welcome {member.display_name}, the Potato Lord does not hate you.')
        c.people.append(person.Person(member.name, member.id, 0))
        print(member.display_name, " has been added")

    """
    Sends a goodbye message to the server when a member leaves and 
    removes them from the list of members 
    :param member: the name of the member
    """

    @commands.Cog.listener()
    async def on_member_remove(self, member):
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
    async def info(self, ctx):
        embed = discord.Embed(title="Potato Bot",
                              description=(
                                  f'Hello! I am Potato Bot and my job is to help run the dictatorship of this server\n\n'
                                  '**COMMANDS** \n `.rep` [@member] [value] [reason] : changes the rep of a member\n'
                                  '.leaderboard : displays the top 5 members with the most rep \n'
                                  '.shameboard : displays the top 5 members with the least amount of rep \n'
                                  '.checkRep : displays the reputation of a single member \n'),
                              color=ctx.author.color)
        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Welcome(client))

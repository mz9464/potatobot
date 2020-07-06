import discord
from discord.ext import commands
import config

client = commands.Bot(command_prefix='.')
@client.event
async def on_ready():
    print('Hello, world.')


@client.event
async def on_member_join(member):
    print(f'Welcome {member}, the Potato Lord does not hate you.')

@client.event
async def on_member_remove(member):
    print(f'{member}, begone thot.')

client.run(config.token)
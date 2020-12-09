import discord
from discord.ext import commands
import asyncio
import random
from collections import Counter
import os

from dotenv import load_dotenv

load_dotenv(verbose=True)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
client = discord.Client(intents = intents)
client = commands.Bot(command_prefix = '.')

class Cog : 
    def __init__(self, N_securise, N_desamorce, N_bombe, N_picked, peoples_cards) : 
        self.mutants = N_mutant
        self.sain = N_sain



@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    print(f'{member} has join the server')
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, merci d'avoir rejoint mon serveur de test, n'oublie pas de désactiver les notifs!"
    )
    

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')


in_progress = False

@client.command(name='clear')
async def clear(ctx):
    
    
    await ctx.channel.purge(limit = 100)


@client.command(name='sporz')
async def sporz(ctx, *args):


    N_players = len(args)
    
    def from_membername_get_member(member_name : str):
        for guild in client.guilds:
            for member in guild.members:
                if str(member).split('#')[0]==member_name:
                    return member
                
                
    await ctx.send(f'{N_players} players')
    await ctx.send('Lets play!')


    playing_members = []
    async for member in ctx.guild.fetch_members(limit=None):
        print(member)
        if str(member).split('#')[0] in args:
            playing_members.append(member)


    list_roles = ['Mutant_zéro', 'médecin', 'médecin', 'informaticien', 'psy', 'espion', 'astronaute', 'astronaute']
    peoples_role={role : [] for role in list_roles}
    random.shuffle(list_roles)
    print(peoples_role)
    print(playing_members)
    for i,member in enumerate(playing_members):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, tu es un {list_roles[i]}!'
        )
        print(f'Hi {member.name}, tu es un {list_roles[i]}!')
        peoples_role[list_roles[i]].append(member)

    


################################ESSAIS##################################


client.run(TOKEN)

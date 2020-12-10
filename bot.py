import discord
import os
import random
import time
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Global variables
GAME_OPENED = False
GAME_RUNNING = False
USERS = {}
ROLES = ['Mutant_zéro', 'Médecin', 'Médecin', 'Informaticien', 'Psy', 'Espion', 'Astronaute']

intents = discord.Intents.all()
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    print(f'{member} has join the server')
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, bienvenue sur le serveur Sporz des MP2"
    )
 
@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server')


@bot.command(name='clear', help='Clear the current channel')
@commands.has_role('Admin')
async def clear(ctx):
    await ctx.channel.purge(limit = 1000)

@bot.command(name='launch-game', help='Initialize and prepare a game (admin only)')
@commands.has_role('Admin')
async def launch_game(ctx, duration='24'):
    global GAME_OPENED
    global GAME_RUNNING
    global USERS

    if not GAME_OPENED and not GAME_RUNNING:
        GAME_OPENED = True
        USERS = {}
        await ctx.send(f"{ctx.message.guild.default_role}\n{ctx.message.author.mention} created a new game !")
    else:
        await ctx.send("A game is already running")

@bot.command(name='join-game', help='Join the game created by the administrator')
async def join_game(ctx):
    global GAME_OPENED
    global GAME_RUNNING
    global USERS

    if GAME_OPENED and not GAME_RUNNING:
        if ctx.author.id not in USERS:
            add_user(ctx.author.id,ctx.author.name)
            await ctx.send(f"Welcome on the ship {ctx.message.author.name}!")
        else:
            await ctx.send(f"{ctx.message.author.name}, you're already on the ship")
    else:
        await ctx.send("There are no game currently running")

@bot.command(name='leave-game', help='Leave the game created by the administrator')
async def leave_game(ctx):
    global GAME_OPENED
    global GAME_RUNNING
    global USERS

    if GAME_OPENED and not GAME_RUNNING:
        remove_user(ctx.author.id)
        await ctx.send(f"{ctx.message.author.name} has left the game")
    else:
        await ctx.send("There are no game currently running")

@bot.command(name='players', help='Show a list of the players actually in game')
async def players_in_game(ctx):
    global GAME_OPENED
    global USERS

    if GAME_OPENED:
        nb_users = len(USERS)
        if nb_users:
            if nb_users == 1:
                await ctx.send("There is one player on the ship :")
            else:
                await ctx.send(f"There are {nb_users} players on the ship :")
            for user in USERS:
                await ctx.send(f" - {USERS[user]['name']}")
        else:
            await ctx.send("There is no one in the ship right now")
    else:
        await ctx.send("There are no game currently running")

@bot.command(name='sporz-play', help='Start the Sporz game')
async def start_game(ctx):
    global GAME_OPENED
    global USERS
    global GAME_RUNNING

    if GAME_OPENED and not GAME_RUNNING:
        if len(USERS) >=7 :  
            await ctx.send(f"Are you sure you want to launch the game ?\n y or n")

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and \
                msg.content.lower() in ["yes", "no"]

            msg = await bot.wait_for("message", check=check)
            
            if msg.content.lower() == "yes":
                await ctx.send("Ok let's start then !")
                await ctx.send("Let's shuffle the roles !")
                define_roles()
                for member in USERS:
                    member_obj = ctx.guild.get_member(member)
                    await member_obj.create_dm()
                    await member_obj.dm_channel.send(
                        f"Hi {member_obj.name}, tu es un {USERS[member]['role']} !"
                    )
                GAME_RUNNING = True
                await ctx.send("The roles have been attributed, let's play !")
            else:
                await ctx.send("You said no!")
        else:
            await ctx.send("You need to be at least 7 players to play")
    else:
        await ctx.send("There are no game currently running")

# Different functions that has to be called by the bot to manage variables and players.
def add_user(user_id,user_name):
    global USERS

    user_dict = {
        'name' : user_name,
        'role' : "",
        'mutant' : False,
        'paralysed' : False,
        'alive' : True,
        'chief' : False,
        'genome' : "",
    }
    USERS[user_id] = user_dict

def remove_user(user_id):
    global USERS

    del USERS[user_id]

def define_roles():
    global USERS
    global ROLES

    nb_players = len(USERS)
    if nb_players == 7:
        list_roles = ROLES
    else:
        list_roles = ROLES + ['Fanatique'] + (nb_players - 8)*['Astronaute']
    
    random.shuffle(list_roles)
    for i, member in enumerate(USERS):
        USERS[member]['role'] = list_roles[i]
        if list_roles[i] == 'Mutant_zéro':
             USERS[member]['mutant'] = True

bot.run(TOKEN)


import os
import random
import time
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

GAME_RUNNING = False
USERS = {}

bot = commands.Bot(command_prefix='!')

@bot.command(name='clear', help='Clear the current channel')
async def clear(ctx):
    await ctx.channel.purge(limit = 1000)

@bot.command(name='launch-game', help='Initialize and prepare a game (admin only)')
@commands.has_role('Admin')
async def launch_game(ctx, duration='24'):
    global GAME_RUNNING
    global USERS

    if not GAME_RUNNING:
        GAME_RUNNING = True
        USERS = {}
        await ctx.send(f"{ctx.message.guild.default_role}\n{ctx.message.author.mention} created a new game !")
    else:
        await ctx.send("A game is already running")

@bot.command(name='join-game', help='Join the game created by the administrator')
async def join_game(ctx):
    global GAME_RUNNING
    global USERS

    if GAME_RUNNING:
        if ctx.author.id not in USERS:
            add_user(ctx.author.id,ctx.author.name)
            await ctx.send(f"Welcome on the ship {ctx.message.author.name}!")
        else:
            await ctx.send(f"{ctx.message.author.name}, you're already on the ship")
    else:
        await ctx.send("There are no game currently running")

@bot.command(name='leave-game', help='Leave the game created by the administrator')
async def leave_game(ctx):
    global GAME_RUNNING
    global USERS

    if GAME_RUNNING:
        remove_user(ctx.author.id)
        await ctx.send(f"{ctx.message.author.name} has left the game")
    else:
        await ctx.send("There are no game currently running")

@bot.command(name='players', help='Show a list of the players actually in game')
async def players_in_game(ctx):
    global GAME_RUNNING
    global USERS

    if GAME_RUNNING:
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


# Different functions that has to be called by the bot to manage variables and players.
def add_user(user_id,user_name):
    global USERS

    user_dict = {
        'name' : user_name,
        'role' : "",
        'mutant' : False,
        'infected' : False,
        'paralysed' : False,
        'alive' : True,
        'chief' : False,
        'genome' : "",
    }
    USERS[user_id] = user_dict

def remove_user(user_id):
    global USERS

    del USERS[user_id]



bot.run(TOKEN)


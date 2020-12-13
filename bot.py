import discord
import os
import random
import time
import asyncio

from datetime import datetime
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Global variables
LOG_FILE = ''
GAME_OPENED = False
GAME_RUNNING = False
USERS = {}
# ROLES = ['Initial_mutant', 'Doctor', 'Doctor', 'Computer Scientist', 'Psychologist', 'Spy', 'Astronaut']
ROLES = ['Initial_mutant']
NIGHT = False

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server')
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, welcome on this sporz server"
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
        set_logfile()
        await ctx.send(f"{ctx.message.guild.default_role}\n{ctx.message.author.mention} created a new game !")
        write_logfile(f"{ctx.message.author.name} created a new game !\n=====\n")
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
@commands.has_role('Admin')
async def start_game(ctx):
    global GAME_OPENED
    global USERS
    global GAME_RUNNING

    if GAME_OPENED and not GAME_RUNNING:
        if len(USERS) >= 0:  
            await ctx.send(f"Are you sure you want to launch the game ?\n yes or no")

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and \
                msg.content.lower() in ["yes", "no"]

            msg = await bot.wait_for("message", check=check)
            
            if msg.content.lower() == "yes":
                msg_log = "Players : Roles\n"
                await ctx.send("Ok let's start then !")
                await ctx.send("Let's shuffle the roles !")
                define_roles()
                for member in USERS:
                    member_obj = ctx.guild.get_member(member)
                    await member_obj.create_dm()
                    await member_obj.dm_channel.send(
                        f"Hi {member_obj.name}, you're {USERS[member]['role']} !"
                    )
                    msg_log += f"{member_obj.name} : {USERS[member]['role']}\n"
                GAME_RUNNING = True
                await ctx.send("The roles have been attributed, let's play !")
                write_logfile(msg_log)
                
                doctors = get_player(ctx,USERS,'Doctor')
                guild = ctx.guild
                admin_role = get(guild.roles, name="Admin")
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False,read_messages=False,send_messages=False),
                    admin_role: discord.PermissionOverwrite(view_channel=False,read_messages=False,send_messages=False)
                }
                msg_doctor = ''
                for doctor in doctors:
                    overwrites[doctor] = discord.PermissionOverwrite(view_channel=True,read_messages=True,send_messages=True)
                    msg_doctor += f"{doctor.mention} "
                doctors_channel = await guild.create_text_channel('doctors',overwrites=overwrites)
                await doctors_channel.send("Welcome on this private channel for doctors only")
                for doctor in doctors:
                    await doctors_channel.send(f"{msg_doctor} you are the two doctors of this ship" )
            else:
                await ctx.send("You said no !")
        else:
            await ctx.send("You need to be at least 7 players to play")
    else:
        await ctx.send("There are no game currently running")

@bot.command(name='night', help='Launch a night')
@commands.has_role('Admin')
async def night(ctx):
    global USERS
    global GAME_RUNNING

    await ctx.send("The night begins, the whole ship falls asleep")
    mutants = get_mutants(ctx,USERS)
    guild = ctx.guild
    admin_role = get(guild.roles, name="Admin")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False,read_messages=False,send_messages=False),
        admin_role: discord.PermissionOverwrite(view_channel=False,read_messages=False,send_messages=False)
    }
    for mutant in mutants:
        overwrites[mutant] = discord.PermissionOverwrite(view_channel=True,read_messages=True,send_messages=True)
    mutants_channel = await guild.create_text_channel('mutants',overwrites=overwrites)
    await mutants_channel.send("The mutants awake\n You have to chose one people to infect and one people to paralyse this night !")
    await mutants_channel.send("The mutants awake")





    # mutants_channel.delete()



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
    if nb_players >= 0 :
        list_roles = ROLES
    else:
        list_roles = ROLES + ['Fanatic'] + (nb_players - 8)*['Astronaut']
    
    random.shuffle(list_roles)
    for i, member in enumerate(USERS):
        USERS[member]['role'] = list_roles[i]
        if list_roles[i] == 'Initial_mutant':
             USERS[member]['mutant'] = True

def set_logfile():
    global LOG_FILE

    i = 0
    while os.path.exists("logfiles/sample_%s.txt" % i):
        i += 1
    LOG_FILE = f'logfiles/sample_{i}.txt'

def write_logfile(msg):
    global LOG_FILE

    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %Hh%M")
    f = open(LOG_FILE, "a+")
    # f.write(f"{dt_string} : {msg}")
    f.write(msg)

def get_player(ctx,users,role):
    players = []
    for member in users:
        if users[member]['role'] == role:
            member_obj = ctx.guild.get_member(member)
            players.append(member_obj)
    return players

def get_mutants(ctx,users):
    players = []
    for member in users:
        if users[member]['mutant']:
            member_obj = ctx.guild.get_member(member)
            players.append(member_obj)
    return players

bot.run(TOKEN)


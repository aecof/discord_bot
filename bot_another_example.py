# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:09:14 2020

@author: arthu
"""
import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
    
@client.event

async def on_message(message):
    if message.author == client.user : 
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    
    
    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
    
        await message.channel.send(response)
    
    
@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
client.run('NzEyNjQ1NzgwODk2MjE5MTU2.XsUlJA.tUhEN7vn5hdvVEb_qO6BHSY_4KU')
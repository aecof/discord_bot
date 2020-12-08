# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:28:42 2020

@author: arthu
"""


import discord
from discord.ext import commands
import random
from collections import Counter

client = commands.Bot(command_prefix = '.')

class Cog : 
    def __init__(self, N_securise, N_desamorce, N_bombe, N_picked, peoples_cards) : 
        self.securise = N_securise
        self.desamorce = N_desamorce
        self.bombe = N_bombe
        self.picked = N_picked
        self.peoples_cards = peoples_cards
        self.peoples_roles = {} 
        self.end_of_round = False
        self.picking_before = None 
        self.picking = None
        
@client.event
async def on_ready():
    print('Bot is ready')
    
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
    
    
@client.command(name='99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)
    
@client.command(name='stop')
async def stop_game(ctx):
    await ctx.send('stopping game')    
    
@client.command(name='members')
async def member_list(ctx):
    response = ''
    for guild in  client.guilds:
        for member in guild.members:
            response += str(member)
    await ctx.send(response)

in_progress = False
@client.command(name='timebomb')
async def time_bomb(ctx, *args):


    N_players = len(args)
    
    def from_membername_get_member(member_name : str):
        for guild in client.guilds:
            for member in guild.members:
                if str(member).split('#')[0]==member_name:
                    return member
                
                
    await ctx.send(f'{N_players} players')
    await ctx.send('Lets play!')
    
    N_gentils = 0
    N_mechants = 0 
    N_securise = 0 
    N_desamorce = 0
    N_bombe = 0 
    N_picked = 0 
    peoples_cards = {}
    
    if N_players == 2 : #Test 
        N_gentils = 3
        N_mechants = 2 
        list_roles = ['gentil','gentil','gentil','méchant','méchant']
        N_securise = 15
        N_desamorce = 4
        N_bombe = 1
        
        
        
    elif N_players == 4 : 
        N_gentils = 3
        N_mechants = 2 
        list_roles = ['gentil','gentil','gentil','méchant','méchant']
        N_securise = 15
        N_desamorce = 4
        N_bombe = 1
        
    elif N_players == 5:
        N_gentils = 3
        N_mechants = 2 
        list_roles = ['gentil','gentil','gentil','méchant','méchant']
        N_securise = 19
        N_desamorce = 5
        N_bombe = 1
    
    elif N_players == 6:
        N_gentils = 4
        N_mechants = 2 
        list_roles = ['gentil','gentil','gentil','gentil','méchant','méchant']
        N_securise = 23
        N_desamorce = 6
        N_bombe = 1
        
    elif N_players == 7:
        N_gentils = 5
        N_mechants = 3
        list_roles = ['gentil','gentil','gentil','gentil','gentil','méchant','méchant','méchant']
        N_securise = 27
        N_desamorce = 7
        N_bombe = 1
    
    elif N_players == 8:
        N_gentils = 5
        N_mechants = 3
        list_roles = ['gentil','gentil','gentil','gentil','gentil','méchant','méchant','méchant']
        N_securise = 31
        N_desamorce = 8
        N_bombe = 1
        
    else : 
        await ctx.send('Trop de joueurs, maximum : 8')
        return
        
    
    infos = Cog(N_securise, N_desamorce, N_bombe, N_picked, peoples_cards)
    
    
    random.shuffle(list_roles)
    playing_members = []
    for guild in client.guilds:
        for member in guild.members:
            if str(member).split('#')[0] in args:
                playing_members.append(member)
                
    
    for i,member in enumerate(playing_members):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, tu es un {list_roles[i]}!'
        )
        
    
    await ctx.send('Someone send .next_round to begin game')
    
    
    
    
    
    @client.command(name = 'pick_card')
    async def pick_card(ctx, member_name, infos= infos): 
        #if (ctx.message.author != infos.picking) or (ctx.message.author.id == 365868464805511168) :
        #    await ctx.send(f'Non, {infos.picking.name} doit jouer, pas toi')
        #    return
        global N_picked
        
        
        
        member_of_interest = from_membername_get_member(member_name)
        if infos.end_of_round == True : 
            await ctx.send("Round is finished, please start a new round with .next_round")
            return
        
        if member_of_interest == infos.picking_before :
            await ctx.send(f'Tu ne peux pas piocher chez la personne qui a pioché chez toi')
            return
        
        if member_of_interest == ctx.message.author : 
            await ctx.send(f'Tu peux pas piocher chez toi')
            return 
        infos.picking_before = infos.picking 
        infos.picking = member_of_interest
        
        
        his_cards = infos.peoples_cards[member_of_interest]
        if his_cards ==[] :
            await ctx.send("Ce joueur n'a plus de cartes, choisis en un autre")
        choice = random.choice(his_cards)
        his_cards.remove(choice)
        tmp = his_cards
        str_to_send= str(Counter(tmp)).split("Counter")[1][1:-1]
        infos.peoples_cards[member_of_interest] = tmp 
        await member_of_interest.dm_channel.send(f'Remaining cards : {tmp}, en resume {str_to_send}')
        await ctx.send(f'{choice} card was picked ! ')
        
        if choice == 'desamorce':
            await ctx.send(f'Well done ! Ca avance')
            infos.desamorce -=1 
            if infos.desamorce == 0:
                await ctx.send(f' Les gentils ont gagnés !! ')
            
        elif choice == 'securise':
            await ctx.send(f'On avance pas..')
            infos.securise -=1 
        
        elif choice == 'bombe':
            await ctx.send("C'est finiii les méchants ont gagnés")
            infos.bombe -=1 
            
        infos.picked+=1
        
        if infos.picked == N_players : 
            infos.end_of_round = True
            await ctx.send('End of rounds, please send .next_round')
            N_picked =0 
        
        
    @client.command(name = 'next_round')
    async def round_of_play(ctx, infos = infos):
        infos.end_of_round = False
        await ctx.send(f'Il reste {infos.desamorce} carte désamorçage à trouver')
        N_picked = 0 
        if infos.picking == None : 
            if infos.picking_before != None : 
                infos.picking = infos.picking_before
            else :
                infos.picking = random.choice(playing_members)
        
        cards = ['securise' for i in range(infos.securise)] + ['desamorce' for i in range(infos.desamorce)] + ['bombe' for i in range(infos.bombe)]
        random.shuffle(cards)
        step = len(cards)//N_players
        
        
        
        for i,member in enumerate(playing_members):
            to_send = cards[i*step:(i+1)*step]
            infos.peoples_cards[member] = to_send
            str_to_send= str(Counter(to_send)).split("Counter")[1][1:-1]
            await member.create_dm()
            await member.dm_channel.send( f'{to_send}, en resume {str_to_send}' )
        
        await ctx.send(f'{infos.picking.name} commence à jouer')
    
        

client.run('NzEyNjQ1NzgwODk2MjE5MTU2.XsUlJA.tUhEN7vn5hdvVEb_qO6BHSY_4KU')


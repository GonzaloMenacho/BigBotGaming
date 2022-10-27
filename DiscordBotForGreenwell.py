#python -m pip install discord.py
#
import discord
from discord.ext import commands

import json
import os
import random
import sys

import scripts
#import scripts.genericdiscordfunction

from dotenv import load_dotenv

from scripts.minigames.NumberGuess import playNumberGuesser

load_dotenv()

"""
if os.path.exists(os.getcwd() + "/config.json"):
    pass
else:
    configTemplate = {"Token": "",
                      "Prefix": "g!"}

    with open(os.getcwd() + "/config.json", "w+") as fs:
        json.dump(configTemplate, fs)
"""

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)


#------------Events--------------#
@client.event
async def on_ready():
    print(f'Logged in as a bot {client.user}')
    print(client.user.name)
    print(client.user.id)
    print('------')

    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )

# member joining and leaving the server
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')

#------------Commands--------------#

# display ping
@client.command()
async def ping(ctx):
    await ctx.send(f"Ping: {round(client.latency * 1000)}ms")

# kick
@client.command()
async def kick(ctx, member : discord.Member, *, reason =None): 
    await member.kick(reason=reason)

# ban
@client.command()
async def ban(ctx, member : discord.Member, *, reason =None): 
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

# number guesser minigame test function
@client.command()
async def numberguess(ctx, member : discord.Member):
    await playNumberGuesser(ctx, member)



client.run(TOKEN)

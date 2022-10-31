#python -m pip install discord.py
#
from xml.dom import pulldom

from mysql.connector.pooling import connect
import discord
from discord.ext import commands

import giphy_client
from giphy_client.rest import ApiException

import json
import os
import random
import sys

import scripts
#import scripts.genericdiscordfunction

from dotenv import load_dotenv

from scripts.Gif import playGif
from scripts.minigames.NumberGuess import playNumberGuesser
from scripts.minigames.RedditPull import pullRedditPost
from scripts.dbmanagement.SQLServerConnect import connect_to_DB

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
DBPASSWORD = os.getenv('DBPASSWORD')
GIPHY_API = os.getenv('GIPHY_API')

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

# member joining the server, bot sends welcome title, description, and random welcome gif
@client.event
async def on_member_join(member: discord.Member=None):
    api_key = GIPHY_API
    api_instance = giphy_client.DefaultApi()
    # arguments for gifs_search_get
    q = 'welcome' 
    rating = 'g' # filters based on rating (g, pg, pg-13, r)
    limit = 10
    name = member.display_name
    channel = client.get_channel(1035188653951041627)
    try:
        # searches all Giphy Gifs based on arguments above
        api_response = api_instance.gifs_search_get(api_key, q, limit=limit, rating=rating)
        # embeded bot response
        embed = discord.Embed(title=(f'Hi {name}! Welcome to the server.'),description="You are one of us now  \U0001f600.")
        # select random gif from list[Gif] and set as embeded image as the orignal image url from the Gif Object
        gifs = list(api_response.data)
        gif = random.choice(gifs)
        embed.set_image(url=gif.images.original.url)
        await channel.send(embed=embed)
    except ApiException as e:
        print("Exception when calling DefaultApi-'>gifs_search_get': %s\n" % e)

# member leaving servers
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

# number guesser minigame
@client.command()
async def numberguess(ctx):
    await playNumberGuesser(ctx, client)

# reddit posting function
@client.command()
async def redditpost(ctx):
    await pullRedditPost(ctx)

# connect to the localhost database
@client.command()
async def dbconnect(ctx):
    await connect_to_DB(ctx, DBPASSWORD)

# pass a topic and bot sends a randomized gif 
@client.command()
async def gif(ctx,*,topic):
    await playGif(ctx,topic)

client.run(TOKEN)

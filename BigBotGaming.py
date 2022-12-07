#python -m pip install discord.py
#
from xml.dom import pulldom

#from mysql.connector.pooling import connect
import discord
from discord.ext import commands
from discord import app_commands

import giphy_client
from giphy_client.rest import ApiException

import json
import os
import random
import sys

from dotenv import load_dotenv

from scripts.Gif import playGif
from scripts.minigames.RockPaperScissors import play_rock_paper_scissors
from scripts.minigames.Battle import play_battle
from scripts.minigames.NumberGuess import playNumberGuesser
from scripts.minigames.RedditPull import pullRedditPost
from scripts.minigames.ConnectFour import playConnectFour
from scripts.dbmanagement.SQLiteDBHandler import view_top5, test_points, test_gold, get_stats
from scripts.bibleversememe.versescript import sendverse
from scripts.tweet import grab_latest_tweet
from scripts.RPGGame.RPGGame import playRPG

load_dotenv()

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
GIPHY_API = os.getenv('GIPHY_API')

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)


#------------Singleton Checks-----------#
# to ensure that each user is only running 1 game at a time
client.current_users = set()

def add_user_to_playing_list(ctx):
    client.current_users.add(ctx.author)

def remove_user_from_playing_list(ctx):
    client.current_users.remove(ctx.author)

"""
@client.check
async def is_user_playing(ctx):
    if not ctx.author in client.current_users:
        client.current_users.add(ctx.author)
        return True
    return False
"""

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
    channel = discord.utils.get(member.guild.text_channels, name="welcome")

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

# rock, paper, scissors
@client.command(name="rockpaperscissors", aliases=["rps", "jankenpon","jkp"])
async def rock_paper_scissors(ctx):
    await play_rock_paper_scissors(ctx, client)

# battle
@client.command(name="battle")
async def battle(ctx):
    await play_battle(ctx, client)

# display ping
@client.command(name="ping")
async def on_ping(ctx):
    await ctx.send(f"Ping: {round(client.latency * 1000)}ms")

# kick
@client.command(name="kick")
async def on_kick(ctx, member : discord.Member, *, reason =None): 
    await member.kick(reason=reason)

# ban
@client.command(name="ban")
async def on_ban(ctx, member : discord.Member, *, reason =None): 
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

# number guesser minigame
@client.command(name="numberguess")
async def on_number_guesser(ctx):
    await playNumberGuesser(ctx, client)

# connect four minigame
@client.command(name="connect4", help="!connect4 @<User>")
async def on_connect_four(ctx, opponent: discord.Member):
    await playConnectFour(ctx, ctx.author, opponent)

# reddit posting function
@client.command(name="reddit",help="!reddit <subreddit>")
async def on_reddit_post(ctx, subredditname: str="okaybuddyretard"):
    await pullRedditPost(ctx, subredditname)

# displays the stats of all users on the server
@client.command(name="serverstats")
async def on_serverstats(ctx):
    await view_top5(ctx)

# displays a specific user's stats
@client.command(name="stats", help="!stats @<User>")
async def on_stats(ctx, userChecked: discord.Member):
    await get_stats(ctx, userChecked)

# displays the user's stats (overloaded command)
@on_stats.error
async def my_stats(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await get_stats(ctx, ctx.author)

# gives points to the user
@client.command(name="gibpoints")
async def on_gibpoints(ctx):
    await test_points(ctx)

# gives gold to the user
@client.command(name="gibgold")
async def on_gibgold(ctx):
    await test_gold(ctx)

# pass a topic and bot sends a randomized gif 
@client.command(name="gif", help="!gif <search term>")
async def on_gif(ctx,*,topic):
    await playGif(ctx,topic)

# send random bible verse that is deemed "funny" or "unordinary"
@client.command(name="bible")
async def on_bible(ctx):
    await sendverse(ctx)

# sends specific users latest tweet DO NOT USE MORE THAN 900 TIMES IN 15 MINUTES
@client.command(name="DeepLeffen")
async def on_DeepLeffen(ctx):
    await grab_latest_tweet(ctx)


@client.command(name="rpg")
async def on_RPG(ctx):
    if ctx.author not in client.current_users:
        add_user_to_playing_list(ctx)
        print(client.current_users)
        await playRPG(ctx)
        remove_user_from_playing_list(ctx)
        print(client.current_users)
    else:
        await ctx.send("You are in a game already!")

client.run(TOKEN)

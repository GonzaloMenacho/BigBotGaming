#python -m pip install discord.py
#
from pickle import TRUE
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
client.remove_command("help")


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
    channel = member.guild.system_channel

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

# on reaction emoji moderation
@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel

    # prompt users to vote
    if reaction.emoji == "🤓": 
        await channel.send(f"{user.name} has voted for a message to be deleted. React with an {reaction.emoji} if you agree.")

    # delete message
    if reaction.count >= 3 and reaction.emoji == "🤓": 
        await reaction.message.delete()
        await channel.send("Message has been deleted.")     

#------------Commands--------------#

# rock, paper, scissors
@client.command(name="rps", aliases=["rockpaperscissors", "jankenpon","jkp"], help="!rps or !rockpaperscissors or !jankenpon or !jkp")
async def rps(ctx):
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
"""
@client.command(name="connect4", help="!connect4 @<User>")
async def on_connect_four(ctx, opponent: discord.Member):
    await playConnectFour(ctx, ctx.author, opponent)
"""

# reddit posting function
@client.command(name="reddit",help="!reddit <subreddit>")
async def on_reddit_post(ctx, subredditname: str="197"):
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
async def on_gif(ctx,*,topic="among us"):
    await playGif(ctx,topic)

# send random bible verse that is deemed "funny" or "unordinary"
@client.command(name="quote")
async def on_quote(ctx):
    await sendverse(ctx)

# sends specific users latest tweet DO NOT USE MORE THAN 900 TIMES IN 15 MINUTES
@client.command(name="tweet")
async def on_Tweet(ctx, handle="dril"):
    await grab_latest_tweet(ctx, handle)


@client.command(name="rpg")
async def on_RPG(ctx):
    if ctx.author not in client.current_users:
        add_user_to_playing_list(ctx)
        print(client.current_users)
        try:
            await playRPG(ctx)
        except:
            await ctx.send("The thread was deleted while playing RPG!")
        remove_user_from_playing_list(ctx)
        print(client.current_users)
    else:
        await ctx.send("You are in a game already!")

@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title= "Help", description = "Use !help <command> for extended info on a command.", color = discord.Color.green())
    
    em.add_field(name = "Moderation", value = "kick :clap: | ban :hammer: | gibpoints | gibgold", inline=False)
    em.add_field(name = "MiniGames", value = "rps :right_fist: | battle :speak_no_evil: | numberguess :1234: | rpg :crossed_swords:", inline=False)
    em.add_field(name= "Social Media", value="tweet :bird: | reddit :nerd: | gif :eyes:", inline=False)
    em.add_field(name="Stats", value="serverstats :trophy: | stats :coffee:", inline=False)
    em.add_field(name= "Misc.", value="ping :timer: | quote :speaking_head:", inline=False)

    await ctx.send(embed = em)

@help.command()
async def kick(ctx):
    em = discord.Embed(title="kick",description="Will kick a user from the server.", color = discord.Color.green())
    em.add_field(name="Syntax", value="!kick <user> [reason]")
    await ctx.send(embed = em)

@help.command()
async def ban(ctx):
    em = discord.Embed(title="ban",description="Will ban a user from the server.", color = discord.Color.green())
    em.add_field(name="Syntax", value="!ban <user> [reason]")
    await ctx.send(embed = em)

@help.command()
async def rps(ctx):
    em = discord.Embed(title="rps",description="Starts a game of rock, paper, scissors", color = discord.Color.green())
    em.add_field(name="Syntax", value="!rps")
    await ctx.send(embed = em)

@help.command()
async def battle(ctx):
    em = discord.Embed(title="battle",description="Starts a battle", color = discord.Color.green())
    em.add_field(name="Syntax", value="!battle")
    await ctx.send(embed = em)

@help.command()
async def numberguess(ctx):
    em = discord.Embed(title="numberguess",description="Guess the number right and you might get a prize!", color = discord.Color.green())
    em.add_field(name="Syntax", value="!numberguess")
    await ctx.send(embed = em)

@help.command()
async def rpg(ctx):
    em = discord.Embed(title="rpg",description="Small rpg minigame!", color = discord.Color.green())
    em.add_field(name="Syntax", value="!rpg")
    await ctx.send(embed = em)

@help.command()
async def tweet(ctx):
    em = discord.Embed(title="tweet",description="Sends latest tweet of specified user!", color = discord.Color.green())
    em.add_field(name="Syntax", value="!tweet [user]")
    await ctx.send(embed = em)

@help.command()
async def reddit(ctx):
    em = discord.Embed(title="reddit",description="Sends a random post from the subreddit chosen.", color = discord.Color.green())
    em.add_field(name="Syntax", value="!reddit <subreddit>")
    await ctx.send(embed = em)

@help.command()
async def gif(ctx):
    em = discord.Embed(title="gif",description="Sends a gif of the chosen topic.", color = discord.Color.green())
    em.add_field(name="Syntax", value="!gif <topic>")
    await ctx.send(embed = em)

@help.command()
async def serverstats(ctx):
    em = discord.Embed(title="serverstats",description="Displays stats of all users.", color = discord.Color.green())
    em.add_field(name="Syntax", value="!serverstats")
    await ctx.send(embed = em)

@help.command()
async def stats(ctx):
    em = discord.Embed(title="stats",description="Displays stats of a specified user.", color = discord.Color.green())
    em.add_field(name="Syntax", value="!stats @<user>")
    await ctx.send(embed = em)

@help.command()
async def gibpoints(ctx):
    em = discord.Embed(title="gibpoints",description="Give points to a user.", color = discord.Color.green())
    em.add_field(name="Syntax", value="!gibpoints")
    await ctx.send(embed = em)

@help.command()
async def gibgold(ctx):
    em = discord.Embed(title="gibgold",description="Give gold to a user.", color = discord.Color.green())
    em.add_field(name="Syntax", value="!gibgold")
    await ctx.send(embed = em)

@help.command()
async def quote(ctx):
    em = discord.Embed(title="quote",description="Sends a funny quote from film.", color = discord.Color.green())
    em.add_field(name="Syntax", value="!quote")
    await ctx.send(embed = em)

@help.command()
async def ping(ctx):
    em = discord.Embed(title="ping",description="Sends your ping to Discord server.", color = discord.Color.green())
    em.add_field(name="Syntax", value="!ping")
    await ctx.send(embed = em)



client.run(TOKEN)

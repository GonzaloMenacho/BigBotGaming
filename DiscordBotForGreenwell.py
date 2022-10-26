#python -m pip install discord.py
#
import discord
from discord.ext import commands

import json
import os
import random
from dotenv import load_dotenv


load_dotenv()

if os.path.exists(os.getcwd() + "/config.json"):
    pass
else:
    configTemplate = {"Token": "",
                      "Prefix": "g!"}

    with open(os.getcwd() + "/config.json", "w+") as fs:
        json.dump(configTemplate, fs)

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

"""
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
"""

@client.event
async def on_ready():
    print(f'Logged in as a bot {client.user}')
    print(client.user.name)
    print(client.user.id)
    print('------')

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )


client.run(TOKEN)

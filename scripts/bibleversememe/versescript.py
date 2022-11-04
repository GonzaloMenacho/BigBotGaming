import discord
import random

async def sendverse(ctx):
    line = random.randint(0,13)
    file = open("scripts/bibleversememe/verse.txt")
    content = file.readlines()
    #print(content[line])
    await ctx.send(content[line])


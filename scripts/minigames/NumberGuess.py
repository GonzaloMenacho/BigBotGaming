import random
import discord


async def playNumberGuesser(ctx):
    rand = random.randrange(1,10)
    #ctx.send(f"{member.mention}, you are a {rand}!")
    await ctx.send(f"You are a {rand}!")
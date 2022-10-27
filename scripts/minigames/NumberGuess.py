import random
import discord


async def playNumberGuesser(ctx, member : discord.member):
    rand = random.randrange(1,11)
    #ctx.send(f"{member.mention}, you are a {rand}!")
    await ctx.send(f"{member.mention}, you are a {rand}!")
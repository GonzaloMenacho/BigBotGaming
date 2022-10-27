import random
import discord


def playNumberGuesser(ctx, member: discord.Member, ):
    rand = random.randrange(1,10)
    ctx.send(f"{member}, you are a {rand}!")
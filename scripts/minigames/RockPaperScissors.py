import random
import discord
import asyncio
import time
from scripts.dbmanagement.SQLiteDBHandler import update_points


choices = ["rock", "paper", "scissors"]

async def play_rock_paper_scissors(ctx, client):
    member = ctx.message.author
    # prompt user for choice
    await ctx.send(f"{member.mention}, choose your weapon! Enter rock, paper, or scissors!")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content
    
    # bot picks 1 of the 3 random weapons
    rand = random.randint(0,2)
    bot_weapon = choices[rand]

    try:   
        # get user input
        msg = await client.wait_for("message", check=check)
        weapon = str(msg.content).lower()

        await ctx.send(f"I attack you with a {bot_weapon}")
        
        # results
        if weapon == "rock" and bot_weapon == "scissors":
            await win(ctx)
        elif weapon == "paper" and bot_weapon == "rock":
            await win(ctx)
        elif weapon == "scissors" and bot_weapon == "paper":
            await win(ctx)
        elif weapon == bot_weapon:
            await ctx.send(f"A tie! Wp.")
            # Award 1 point
            userID = ctx.message.author.id
            update_points(userID, int(1))
        else:
            await ctx.send(f"You lost!")

    except asyncio.TimeoutError:
        await ctx.send("This is not that hard, try faster next time!")

async def win(ctx):
    await ctx.send(f"You won!")
    # Award 5 points
    userID = ctx.message.author.id
    update_points(userID, int(5))
import random
import discord
import asyncio
import time

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
            await ctx.send(f"You won!")
        elif weapon == "paper" and bot_weapon == "rock":
            await ctx.send(f"You won!")
        elif weapon == "scissors" and bot_weapon == "paper":
            await ctx.send(f"You won!")
        elif weapon == bot_weapon:
            await ctx.send(f"A tie! Wp.")
        else:
            await ctx.send(f"You lost!")

    except asyncio.TimeoutError:
        await ctx.send("This is not that hard, try faster next time!")
    
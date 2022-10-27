import praw
import random
import discord

reddit = praw.Reddit(
    client_id="my client id",
    client_secret="my client secret",
    user_agent="my user agent",
)

async def pullRedditPost(ctx):
    await ctx.send(f"Reddit is installed and read only? {reddit.read_only}")
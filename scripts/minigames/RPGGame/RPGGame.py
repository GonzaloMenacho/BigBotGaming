
import random
import json
import os
import time
import discord.ext.commands.context as ctxt
import discord
import re
import asyncio

current_users = set()

async def playRPG(ctx : ctxt):
    thread = await set_up_game_channel(ctx)
    await wait_for_message_in_channel(ctx, thread)


async def set_up_game_channel(ctx: ctxt):
    discorduser = ctx.message.author
    channelname = get_thread_name(ctx)
    discordthread = await create_discord_thread(ctx, channelname)
    message = f"Hello {discorduser.name}"
    await send_message_in_thread(discordthread, message)
    return discordthread


def get_thread_name(ctx: ctxt) -> str:
    channelname = f"{ctx.message.author}"
    channelname = re.sub(r"[^a-zA-Z0-9]", "", channelname).lower()
    channelname = f"{channelname}-rpg"
    return channelname


async def check_if_channel_exists(ctx : ctxt, name):
    req_channel = None
    for channel in ctx.guild.channels:
        if channel.name == name:
            req_channel = channel
            #print(channel.name)

    for thread in ctx.guild.threads:
        if thread.name == name:
            req_channel = thread
            #print(thread.name)

    #print(req_channel)
    #print(req_channel.id)
    return req_channel


async def create_discord_thread(ctx, channelname) -> discord.TextChannel:
    channel = await check_if_channel_exists(ctx, channelname)

    if (channel is None):
        discordthread = await ctx.message.create_thread(name=channelname)
        return discordthread

    elif isinstance(channel, discord.Thread):
        pass
        #await ctx.message.send(f"I'm here! {ctx.message.author.mention}'")

    return channel


async def wait_for_message_in_channel(ctx, thread : discord.TextChannel):
    def check(m):
        return m.content and m.channel == thread and m.author == ctx.message.author

    try:
        await thread.send('foo')
        message = await ctx.bot.wait_for("message", timeout = 15.0, check=check)
        await thread.send(message.content)
    except asyncio.TimeoutError:
        await thread.send("Your time is up")


async def send_message_in_thread(channel : discord.TextChannel, message):
    await channel.send(message)


def add_user_to_playing_list(ctx):
    pass


async def initialize_character():
    pass
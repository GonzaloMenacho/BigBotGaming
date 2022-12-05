
import random
import json
import os
import time
import discord.ext.commands.context as ctxt
import discord
import re

async def playRPG(ctx : ctxt):
    await set_up_game_channel(ctx)


async def set_up_game_channel(ctx: ctxt):
    discorduser = ctx.message.author
    channelname = get_thread_name(ctx)
    discordthread = await create_discord_thread(ctx, channelname)
    message = f"Hello {discorduser.name}"
    await send_message_in_thread(discordthread, message)


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

    print(req_channel)
    print(req_channel.id)
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


async def send_message_in_channel_with_id(ctx, id):
    pass


async def send_message_in_thread(channel : discord.TextChannel, message):
    await channel.send(message)


async def initialize_character():
    pass
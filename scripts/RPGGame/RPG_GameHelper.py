import discord.ext.commands.context as ctxt
import discord
import re
import asyncio

#because python imports suck
from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from dbmanagement import SQLiteDBHandler as db


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


async def wait_for_message_in_channel(ctx, 
                                      thread : discord.TextChannel, 
                                      message = "Enter a value: "):
    def check(m):
        return m.content and m.channel == thread and m.author == ctx.message.author

    try:
        await thread.send(message)
        message = await ctx.bot.wait_for("message", timeout = 30.0, check=check)
        return message.content
    except asyncio.TimeoutError:
        await thread.send("Your time is up.")
        return -1


async def send_message_in_thread(channel : discord.TextChannel, message):
    await channel.send(message)

def create_player_stats():
    """
Creates starting dictionary values for gamestate file.
    :return: player stats dictionary
    """
    player_dict = {
        "level": 1,
        "exp": 0,
        "gold": 300
    }

    return player_dict


async def get_all_chars_from_db(ctx : ctxt, thread : discord.Thread):
    characterlist = db.get_character_from_db(ctx.message.author.id)
    print(characterlist)
    message = ""
    chardicts = []
    for x in range(len(characterlist)):
        char_dict = convert_char_tuple_to_dict(characterlist[x])
        chardicts.append(char_dict)
        message = "".join([message, f"{x+1}: {char_dict['name']}\n"])
    await send_message_in_thread(thread, message)
    return chardicts


def convert_char_tuple_to_dict(chartuple : tuple) -> dict:
    dictkeys = ("id",
                "discordid",
                 "name",
                 "level",
                 "exp",
                 "hp",
                 "mp",
                 "strength",
                 "dexterity",
                 "vitality",
                 "magic",
                 "spirit",
                 "luck",
                 "weapon",
                 "skill_type",
                 "skill_1",
                 "skill_2",
                 "skill_3",
                 "skill_4",
                 "skill_5",
                )
    tempchardict = {}
    for x in range(20):
        tempchardict[dictkeys[x]] = chartuple[x]

    skills = [
        tempchardict['skill_1'],
        tempchardict['skill_2'],
        tempchardict['skill_3'],
        tempchardict['skill_4'],
        tempchardict['skill_5'],
        ]

    chardict = {
            "name": tempchardict['name'],
            "level": tempchardict['level'],
            "exp": tempchardict['exp'],
            "hp": tempchardict['hp'],
            "mp": tempchardict['mp'],
            "strength": tempchardict['strength'],
            "dexterity": tempchardict['dexterity'],
            "vitality": tempchardict['vitality'],
            "magic": tempchardict['magic'],
            "spirit": tempchardict['spirit'],
            "luck": tempchardict['luck'],
            "weapon": tempchardict['weapon'],
            "skill_type": tempchardict['skill_type'],
            "skills": skills,
        }
    return chardict

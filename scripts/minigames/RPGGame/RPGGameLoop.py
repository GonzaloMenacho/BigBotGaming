import discord
import discord.ext.commands.context as ctxt
import sys
import asyncio

async def play_RPG_game_loop(ctx : ctxt, thread : discord.Thread):
    await print_main_menu(ctx, thread)


async def print_main_menu(ctx: ctxt, thread : discord.Thread):
    main_menu = '''
Main Menu:
[1] Send Adventuring Party
[2] Hire Adventurer
[3] View Adventurer Stats
[4] Guild Promotion
[5] View Guild Hall Status
[k] Kill
[r] Initialize
[0] Close Program
    '''
    #await send_message_in_thread(thread, main_menu)
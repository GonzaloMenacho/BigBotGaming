import discord
import discord.ext.commands.context as ctxt
import sys
import asyncio
from . import RPG_GameHelper as rpg

async def playRPG(ctx : ctxt):
    thread = await rpg.set_up_game_channel(ctx)
    gameloop = True
    await play_RPG_game_loop(ctx, thread)
    await rpg.send_message_in_thread(thread, "Thanks for playing!")
    #await rpg.wait_for_message_in_channel(ctx, thread)


async def play_RPG_game_loop(ctx : ctxt, thread : discord.Thread):
    gameloop = True
    while(gameloop):
        gameloop = await play_main_menu(ctx, thread)


async def play_main_menu(ctx: ctxt, thread : discord.Thread):
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

Enter your option:
    '''
    message = await rpg.wait_for_message_in_channel(ctx, thread, main_menu)

    # i wish i had match-case in 3.9
    if message == "1":
        await rpg.send_message_in_thread(thread, "Send Adventuring Party")
    elif message == "2":
        await rpg.send_message_in_thread(thread, "Hire Adventurer")
    elif message == "3":
        await rpg.send_message_in_thread(thread, "View Adventurer Stats")
    elif message == "4":
        await rpg.send_message_in_thread(thread, "Guild Promotion")
    elif message == "5":
        await rpg.send_message_in_thread(thread, "View Guild Hall Status")
    elif message == "k":
        await rpg.send_message_in_thread(thread, "Kill")
    elif message == "r":
        await rpg.send_message_in_thread(thread, "Initialize")
    elif message == "0":
        await rpg.send_message_in_thread(thread, "Close Program")
        return False
    else:
        await rpg.send_message_in_thread(thread, "Unknown Input!")

    return True
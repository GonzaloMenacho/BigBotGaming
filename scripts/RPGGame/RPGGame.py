import discord
import discord.ext.commands.context as ctxt
import sys
import asyncio
from . import RPG_GameHelper as rpg
from . import RPG_Character as rpgc

async def playRPG(ctx : ctxt):
    thread = await rpg.set_up_game_channel(ctx)
    gameloop = True
    await play_RPG_game_loop(ctx, thread)
    await rpg.send_message_in_thread(thread, "Thanks for playing!")
    #await rpg.wait_for_message_in_channel(ctx, thread)


async def play_RPG_game_loop(ctx : ctxt, thread : discord.Thread):
    #rpgc.get_character(ctx.message.author.id, "China")
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
        #await rpg.send_message_in_thread(thread, "Hire Adventurer")
        await create_char(ctx, thread)
    elif message == "3":
        #await rpg.send_message_in_thread(thread, "View Adventurer Stats")
        await print_chars_in_db(ctx, thread)
    elif message == "4":
        await rpg.send_message_in_thread(thread, "Guild Promotion")
    elif message == "5":
        await rpg.send_message_in_thread(thread, "View Guild Hall Status")
    elif message == "k":
        await rpg.send_message_in_thread(thread, "Kill")
    elif message == "r":
        await rpg.send_message_in_thread(thread, "Initialize")
    elif message == "0" or message == -1:
        await rpg.send_message_in_thread(thread, "Close Program")
        return False
    else:
        await rpg.send_message_in_thread(thread, "Unknown Input!")

    return True


async def create_char(ctx: ctxt, thread : discord.Thread):
    message = await rpgc.initialize_char(ctx, thread)
    await rpg.send_message_in_thread(thread, message)


async def print_chars_in_db(ctx: ctxt, thread : discord.Thread):
    characterlist = await rpg.get_all_chars_from_db(ctx, thread)

    print(characterlist[0])
    charselect = await rpg.wait_for_message_in_channel(ctx, thread)
    try:
        select = int(charselect)-1
        if select == -1:
            message = 'Returning to Main Menu'
        if select < len(characterlist) and select > 0:
            print(characterlist[select])
            message = rpgc.print_char_stats(characterlist[select])
        else:
            message = 'Not a valid character. Return to Main Menu.'
        await rpg.send_message_in_thread(thread, message)
    except:
        message = 'Unknown Input. Returning to Main Menu.'
        await rpg.send_message_in_thread(thread, message)
import discord
import discord.ext.commands.context as ctxt
import sys
import asyncio
from . import RPG_GameHelper as rpg
from . import RPG_Character as rpgc

#because python imports suck
from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from dbmanagement import SQLiteDBHandler as db

async def playRPG(ctx : ctxt):
    db.user_exists(ctx.message.author.id)
    thread = await rpg.set_up_game_channel(ctx)
    gameloop = True
    #print(rpgc.get_character_stats(ctx.message.author.id, "China"))
    #print(await rpg.get_player_stats(ctx))
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
[5] Level Up
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
        # await rpg.send_message_in_thread(thread, "Level Up")
        await rpgc.level_up_from_menu(ctx, thread)
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
    if len(characterlist) == 0:
        return
    charselect = await rpg.wait_for_message_in_channel(ctx, thread)
    select = await rpg.get_character_choice_from_index(characterlist, charselect)
    if select == -1:
        message = 'Returning to Main Menu.'
    elif select is None:
        message = 'Not a valid character.  Returning to Main Menu.'
    else:
        message = rpgc.print_char_stats(characterlist[select])
    await rpg.send_message_in_thread(thread, message)
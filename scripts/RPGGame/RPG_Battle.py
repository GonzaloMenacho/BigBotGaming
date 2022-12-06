from . import RPG_GameHelper as rpg
from . import RPG_Character as rpgc
import random
import asyncio
import discord
import discord.ext.commands.context as ctxt


async def initialize_battle(ctx, thread):
    """
A script where you can send your party into battle.
    :return: False if something goes wrong or declined by user
    """
    party_chars = initialize_char_select()  # grabs a list of 3 chars
    if not party_chars:
        print("Returning to Main Menu... ")
    else:
        char1, char2, char3 = party_chars  # unpacks list into variables
        print(char1['name'], ", ", char2['name'], ", and ", char3['name'],
              " will be partying up together.", sep='')
        location_list = await generate_location_list()
        message = "Where will the party be adventuring? :"
        try:
            location = select_file(location_list, message)  # select level
            if not location:
                print("Returning to Main Menu...")
                return False
            else:
                pass
            print(char1['name'], ", ", char2['name'] + ", and ", char3['name'],
                  " will be heading to ", location, ".", sep='')
            agreement = input("Are you sure you want to send this party out? "
                              "(y/n) :")
            if agreement == "y":
                start_battle(char1, char2, char3, location)
            else:
                print("Returning to Main Menu...")
                return False
        except TypeError:
            print("Returning to Main Menu...")


async def initialize_char_select(ctx, thread):
    """
Asks for 3 characters to be used in the battle script.
    :return: party_stats, which is a list of character dictionaries from files.
    """
    party_stats = []
    char_list = await rpg.get_all_chars_from_db(ctx, thread)

    if len(char_list) == 0:
        message = "You don't have any adventurers to form a party!\nCome back with at least three adventurers."
        await rpg.send_message_in_thread(thread, message)
        return False
    elif len(char_list) < 3:
        message = "You don't have enough adventurers to form a party!\nCome back with at least three adventurers."
        await rpg.send_message_in_thread(thread, message)
        return False

    message = "Which adventurers will party together?\n Enter '0' to quit."
    char_select = None

    while len(party_stats) < 3 and char_select != -1:
        try:
            char_index = await rpg.wait_for_message_in_channel(ctx, thread, message)
            char_select = await rpg.get_character_choice_from_index(char_list, char_index)
            
            if char_select == -1:
                return False
            else:
                message = f"{char_list[char_select]['name']} has been added to the party."
                party_stats.append(char_list[char_select])
                char_list.remove(char_list[char_select])

                await rpg.send_message_in_thread(thread, message)

                if len(party_stats) >= 3:
                    continue

                message = "Who else will party up?\n"
                for x in range(len(char_list)):
                    message = "".join([message, f"{x+1}: {char_list[x]['name']}\n"])

        except TypeError:  # type the number, not the name, plz
            message = "That was not a valid adventurer!\n(enter '0' to go back.)"
    return party_stats


async def generate_location_list(ctx):
    """
Generates list of locations depending on player level.
    :return:  location_list, selectable locations
    """
    player_dict = await rpg.get_player_stats(ctx)
    total_locations = ["Flowering Plains", "Misty Rainforest", "Graven Marsh",
                       "Bellowing Mountains", "Cryptic Caverns",
                       "Ancient Spire", "Cloudy Peaks", "Canada",
                       "Volcanic Isles", "Desolate Wasteland"]
    location_list = []

    if player_dict["level"] > 10:
        for location in range(10):
            location_list.append(total_locations[location])
    else:
        for location in range(player_dict["level"]):
            location_list.append(total_locations[location])

    return location_list


def level_up_guild(player_dict, message):
    """
Levels up dictionary level using check function
    :param player_dict: any dictionary
    :param message: given level up message
    """
    lvl_change = check_level_up(player_dict)
    if lvl_change:
        level = player_dict["level"] + 1
        print(message)
        return level
    else:
        return player_dict["level"]


def check_level_up(player_dict):
    """
Checks player exp vs their level to see if guild level increases
    :param player_dict: any dictionary
    :return:
    """
    if player_dict["exp"] > (5 << player_dict["level"]):
        return True
    else:
        return False

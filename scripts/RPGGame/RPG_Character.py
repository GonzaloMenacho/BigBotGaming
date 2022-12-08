from . import RPG_GameHelper as rpg
import random
import asyncio
import discord
import discord.ext.commands.context as ctxt
from scripts.dbmanagement.SQLiteDBHandler import update_points

#because python imports suck
from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from dbmanagement import SQLiteDBHandler as db


async def initialize_char(ctx: ctxt, thread : discord.Thread):
    """
Creates character file, using name user inputs.
Rolls a bunch of stats using roll_stats() and roll_skills()
and saves values to a dictionary, and character file.
    """
    name = await rpg.wait_for_message_in_channel(ctx, thread, "What's the name of the scouted adventurer? :")
    #print(name)
    if name == -1:
        return -1

    if not check_name_characters(name):
        return "This name is invalid!"
    #print(name)

    dbcheck = db.get_character_from_db(ctx.message.author.id, name)
    #print(dbcheck)
    if len(dbcheck) != 0:
        return "This person is already a registered adventurer!"
    else:
        skills = [None] * 5
        lv = 0
        exp = 0
        (lv, hp, mp, strength, dexterity, vitality, magic, spirit,
            luck) = roll_stats(lv)
        weapon_choice, skill_type = roll_weapon()
        skills = roll_skills(lv, skill_type, skills)

        stat_dict = {
            "name": name,
            "level": lv,
            "exp": exp,
            "hp": hp,
            "mp": mp,
            "strength": strength,
            "dexterity": dexterity,
            "vitality": vitality,
            "magic": magic,
            "spirit": spirit,
            "luck": luck,
            "weapon": weapon_choice,
            "skill_type": skill_type,
            "skills": skills,
        }
        message = save_char_data(ctx, stat_dict)
        #print(message)
        return message


def check_name_characters(name):
    """
    Checks if filename is valid.
    :param name: name
    :return: better name
    """
    name = name.replace(" ", "A")  # allows spaces...
    if name == "" or name.lower() == "null":
        return False
    elif name.isalnum():  # ...but no other special chars
        return True
    else:
        return False


async def level_up_from_menu(ctx, thread):
    """
Takes character file, rolls stats, changes file dictionary, and saves file.
    """
    player_dict = await rpg.get_player_stats(ctx)

    if player_dict["gold"] < 100:  # checks player file's gold value
        message = "It takes 100 gold to level up a character! \nCome back when you're a bit... mmmh... richer!"
        await rpg.send_message_in_thread(thread, message)
        return False

    char_list = await rpg.get_all_chars_from_db(ctx, thread)
    if len(char_list) == 0:
        message = "You don't have any adventurers to promote!"
        await rpg.send_message_in_thread(thread, message)
        return message
    await asyncio.sleep(1)
    message = f"""
    It costs 100 gold to level up a character.
    You have {player_dict['gold']} gold.
    Who would you like to level up?\n
    """
    charselect = await rpg.wait_for_message_in_channel(ctx, thread, message)
    charindex = await rpg.get_character_choice_from_index(char_list, charselect)
    #print(charindex, charselect)
    if charindex == -1:
        message = "Returning to Main Menu."
    elif charindex is None:
        message = "Returning to Main Menu."
    else:
        character = char_list[charindex]
        player_dict["gold"] -= 100
        save_player_data(player_dict)
        message = level_up_stats(ctx, character)
    await rpg.send_message_in_thread(thread, message)


def level_up_stats(ctx : ctxt, char_dict : dict):
    """
Rolls stats and adds them to chosen filename's dictionary
    :param file_select: name of file dictionary
    """
    stat_list = roll_stats(char_dict["level"])
    skill_list = roll_skills(char_dict['level'], char_dict['skill_type'],
                char_dict['skills'])

    char_dict_updated = {
        'level': char_dict["level"] + 1,
        'exp': 0,
        'hp': char_dict['hp'] + stat_list[0],
        'mp': char_dict['mp'] + stat_list[1],
        'strength': char_dict['strength'] + stat_list[2],
        'dexterity': char_dict['dexterity'] + stat_list[3],
        'vitality': char_dict['vitality'] + stat_list[4],
        'magic': char_dict['magic'] + stat_list[5],
        'spirit': char_dict['spirit'] + stat_list[6],
        'skills' : skill_list
    }
    char_dict.update(char_dict_updated)
    save_char_data(ctx, char_dict)
    message = f"{char_dict['name']} has been successfully promoted to level {char_dict['level']}! :bulb:"

    # Award 5 points
    userID = ctx.message.author.id
    update_points(userID, int(5))
    message = "\n".join([message, "You gained 5 points!"])
    return message


def roll_stats(lv):
    """
Rolls a new character or rolls stat additions to existing character.
    :param lv: integer of character level, taken from file.
    :return: stat_list, to be used as list, or as additions to stats
    """
    stat_list = []
    if lv == 0:  # roll new lvl 1 char
        stat_list.append(lv + 1)
        stat_list.append(random.randrange(20, 34))  # hp
        stat_list.append(random.randrange(10, 23))  # mp
        for x in range(5):
            stat_list.append(random.randrange(6, 16))  # str,dex,vit,mag,spi
        stat_list.append(random.randrange(1, 6))  # luck
        return stat_list

    else:  # roll stat additions
        lv += 1
        stat_list.append(random.randrange(3 * lv + 5, 4 * lv + 5) + lv + 1)  # hp
        stat_list.append(random.randrange(lv, 2 * lv) + (lv // 2) + 1)  # mp
        for x in range(5):
            stat_list.append(random.randrange(1, 5))  # str,dex,vit,mag,spi
        return stat_list


def roll_weapon():
    """
Rolls and outputs weapon and weapon type
    :return: weapon, skill_type
    """
    skill_type_list = ["melee", "ranged", "magic"]
    skill_type = random.choice(skill_type_list)
    if skill_type == "melee":
        weapon_list = ['Greatsword', 'Longsword', 'Axe', 'Lance', 'Dagger',
                       'Hammer', 'Falchion', 'Polearm', 'Spear', 'Shortsword',
                       'Fists', 'Gauntlets']
    elif skill_type == "ranged":
        weapon_list = ['Longbow', 'Crossbow', 'Shortbow', 'Javelin',
                       'Throwing-Knife', 'Sling', 'Dagger', 'Gun']
    elif skill_type == "magic":
        weapon_list = ['Staff', 'Tome', 'Wand', 'Magecraft', 'Orb-of-Casting',
                       'BDE', 'Rod', 'Scepter']
    else:
        skill_type = "normal"
        weapon_list = ['Fists', 'Pitchfork', 'Shotgun', 'Words']
    weapon = random.choice(weapon_list)
    return weapon, skill_type


def roll_skills(lv, skill_type, skills) -> list:
    """
Checks level to see if character is new, or is a lv where lv % 8 = 0.
For new char, rolls 2 stats and saves as list.
For existing char, rolls a stat, and appends to existing skill list.
    :param lv: level of char grabbed from file
    :param skill_type: skill_type of char's weapon
    :param skills: chars already learned skills
    :return: skills as list
    """
    skill_list = determine_skill_list(skill_type)
    if lv == 1:
        for x in range(2):
            skills[x] = random.choice(skill_list)
            skill_list.remove(skills[x])
    elif lv % 5 == 0 and lv <= 16:
        for x in range(len(skills)):
            if skills[x] == None:
                skills[x] = random.choice(skill_list)
                break
    else:
        pass
    return skills


def determine_skill_list(skill_type):
    """
Prints skills available, determined by skill_type.
    :param skill_type: type of skill, from roll.
    :return: skill_list as list
    """
    if skill_type == "melee":
        skill_list = ['Rising-Force', 'Overhead-Swing', 'Vital-Piercer',
                      'Judo-Grapple', 'Thunder-Cross-Split-Attack', 
                      'Dual-Palm-Strike', 'Demon-Flip', 'Feint', 
                      'Hilt-Thrust', 'Wide-Slash', 'Air-Slash',
                      'Kingly-Slash', 'French-Beheading']
    elif skill_type == "ranged":
        skill_list = ['Triple-Shot', 'Exploding-Shot', 'Armor-Piercer',
                      'Poison-Tip', 'Oil-Tipped-Flint', 'Curved-Shot',
                      "Bulls-Eye", 'Snake-Shot', 'Asphyxiating-Arrow',
                      'Wyvern-Shot', 'Thieves-Aim', "Rangers-Guile"]
    elif skill_type == "magic":
        skill_list = ['Fireball', 'Stun-Edge', 'Nosferatu', 'Fortify-Arms',
                      'Summon-Ghosts', 'Ancient-Power', 'Dragons-Breath',
                      'Confusion-Ray', 'UnHealing', 'UnRestore', 'UnCure',
                      'Mad-Taunt', 'Poison-Spit', 'Flood']
    else:
        skill_list = ['Hide', 'Run', 'Yell', 'Dance', 'Cry']
    return skill_list


def save_player_data(player_dict : dict):
    db.update_user_info(player_dict)


def save_char_data(ctx: ctxt, stat_dict : dict):
    """
Takes given char dictionary and file name and saves to char's file name
    :return: "Adventurer stats successfully recorded!"
    """
    message = "failed save_character_into_db()"
    try:
        message = db.save_character_into_db(ctx.message.author.id, stat_dict)
    except:
        print(message)
        message = "Saving your adventurer stats has failed!"
    return message


def get_character_stats(discordid : int, charname : str) -> dict:
    character =  db.get_character_from_db(discordid, charname)
    if character is None:
        return
    for value in character:
        char = rpg.convert_char_tuple_to_dict(value)
        return char


def print_char_stats(chardict : dict):
    message = ""
    for i in chardict:  # prints the dict in the file
        message = "".join([message, f"{i}: {chardict[i]}\n"])
    return message


def kill_char(ctx, char_dict : dict):
    name = char_dict['name']
    db.delete_char_from_table(ctx, name)
    return name

from . import RPG_GameHelper as rpg
import random
import asyncio
import discord
import discord.ext.commands.context as ctxt

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
    print(name)
    if name == -1:
        return -1

    if not check_name_characters(name):
        return "This name is invalid!"
    print(name)

    dbcheck = db.get_character_from_db(ctx.message.author.id, name)
    print(dbcheck)
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

        print(stat_dict)
        print(stat_dict['name'])
        message = save_char_data(ctx, stat_dict)
        print(message)
        return message


def check_name_characters(name):
    """
    Checks if filename is valid.
    :param name: name
    :return: better name
    """
    """

    ACCESS DATABASE
    GET ALL CHARACTERS WITH THE DISCORD'S ID
    SEE IF ANY OF THOSE ROWS HAVE THE SAME NAME


    """
    name = name.replace(" ", "A")  # allows spaces...
    if name == "" or name.lower() == "null":
        return False
    elif name.isalnum():  # ...but no other special chars
        return True
    else:
        return False


def level_up_from_menu():
    """
Takes character file, rolls stats, changes file dictionary, and saves file.
    """
    try:
        player_dict = get_stats("gamestate")
        if player_dict["gold"] < 100:  # checks player file's gold value
            print("It takes 100 gold to level up a character! \nCome back "
                  "when you're a bit... mmmh... richer!")
            return False
        else:
            pass
        prompt = "It costs 100 gold to level up a character. \nYou have " + \
                 str(player_dict["gold"]) + " gold. \nWho would you like to " \
                                            "level up? :"
        char_list = get_char_list()
        file_select = select_file(char_list, prompt)
        if not char_list:
            print(
                "You don't have any adventurers to promote! \nReturning to "
                "Main Menu... ")
        elif not file_select:
            print("Returning to Main Menu... ")
        else:
            player_dict["gold"] -= 100
            save_char_data(player_dict, "gamestate")
            level_up_stats(file_select)
    except FileNotFoundError:
        print('\nThe \\characterFiles folder was not found! \nPlease '
              'initialize the game by pressing "r" on the Main Menu!\n')


def level_up_stats(file_select):
    """
Rolls stats and adds them to chosen filename's dictionary
    :param file_select: name of file dictionary
    """
    char_dict = get_stats(file_select)
    stat_list = roll_stats(char_dict["level"])
    roll_skills(char_dict['level'], char_dict['skill_type'],
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
    }

    char_dict.update(char_dict_updated)
    save_char_data(char_dict, char_dict['name'])
    print(char_dict['name'], " has been successfully promoted to level ",
          char_dict['level'], "!", sep='')


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
        for x in range(skills):
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


def get_stats(char_select):
    """
Outputs chosen character file as dictionary
    :param char_select: name grabbed from other functions.
    :return: character dictionary if true, False if file doesn't exist.
    """
    try:
        path = get_file_directory()
        with open(os.path.join(path, char_select), 'r') as openfile:
            char_dict = json.load(openfile)
        return char_dict

    except TypeError:
        return False


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


def get_character(discordid : int, charname : str):
    character =  db.get_character_from_db(discordid, charname)
    print(character)
    if character is None:
        return "None"
    for value in character:
        print(value)


def print_char_stats(chardict : dict):
    message = ""
    for i in chardict:  # prints the dict in the file
        message = "".join([message, f"{i}: {chardict[i]}\n"])
    return message





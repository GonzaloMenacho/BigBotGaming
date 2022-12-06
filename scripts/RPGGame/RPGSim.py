"""
RPG Battle Sim for Integration Project
This is a script that plays like an autoclicker with RPG elements. It uses
python's tools to manage files, perform calculations, and present information
that show off what I learned about the language.
Sources:
https://gamefaqs.gamespot.com/ps/197341-final-fantasy-vii/faqs/22395
https://www.w3schools.com/
https://www.tutorialspoint.com/python/index.htm
https://realpython.com/
"""
__author__ = "Michael D'Agostino"


"""
For Elijah:
Table: Characters
Columns: DiscordID | charName | level | exp | hp | mp | strength | dexterity | vitality | magic | spirit | luck | weapon | skill_type | skill_1 | skill_2 | skill_3 | skill_4 | skill_5
DiscordID = i think it's an int? whatever the big string of numbers fits into. | (Primary Key) (Foreign Key)
charName = string | # what the discord user names their character(s), discord user can have multiple chars | (Primary Key)
level = int | char's level
exp
hp = int | char's max hp
mp = int | char's max mp
strength = int
dexterity = int
vitality = int
magic = int
spirit = int
luck = int
weapon = string
skill_type = string
skill_1 = string, default null
skill_2 = string, default null
skill_3 = string, default null
skill_4 = string, default null
skill_5 = string, default null


Table: Discord Users
Columns: DiscordID | points | gold | level | exp
gold = int
level = int
exp = int

"""


import random
import json
import os
import time


def main():
    """
Displays main menu, where user selects what function the program should run.
    """
    print("Welcome to my Integration Project! \nIt's a small game about "
          "managing a fantasy guild that serves to demonstrate my "
          "knowledge of Python programming!"
          '\nIf this is your first time playing, start by selecting '
          '"Initialize" from the menu by pressing "r".')
    display_main_menu()
    menu_loop = True
    while menu_loop:  # simple main menu loop
        menu_selection = input("What would you like to do? :")
        if menu_selection == "1":
            print("Sending Adventuring Party...")
            initialize_battle()
            display_main_menu()
        elif menu_selection == "2":
            print("Scouting a new adventurer...")
            initialize_char()
            display_main_menu()
        elif menu_selection == "3":
            print("Viewing Adventurer Stats...")
            display_char_stats()
            display_main_menu()
        elif menu_selection == "4":
            print("Commencing Guild Promotion...")
            level_up_from_menu()
            display_main_menu()
        elif menu_selection == "5":
            print("Viewing Guild Hall Status...")
            display_player_stats()
            display_main_menu()
        elif menu_selection == "k":
            print("Bringing out the shovel...")
            kill_char_from_menu()
            display_main_menu()
        elif menu_selection == "r":
            restart_game = input(
                "Are you sure you want to initialize the game? (y/n) :")
            if restart_game == "y":
                initialize_game()
                display_main_menu()
            else:
                print("Returning to Main Menu... ")
                display_main_menu()
        elif menu_selection == "0":
            close_game = input("Are you sure you want to quit? (y/n) :")
            if close_game == "y":
                menu_loop = False
                print("Thanks for playing!")
            else:
                print("Returning to Main Menu... ")
                display_main_menu()
        else:
            print("Unknown command input. Try again!")


def display_main_menu():
    """
Prints the main menu.
    """
    print('''
Main Menu:
[1] Send Adventuring Party
[2] Hire Adventurer
[3] View Adventurer Stats
[4] Guild Promotion
[5] View Guild Hall Status
[k] Kill
[r] Initialize
[0] Close Program
    ''')


def initialize_game():
    """
Creates gamestate.txt if it doesn't exist, which is used to store player data.
    """
    path = get_file_directory()

    try:
        os.makedirs(path)
        player_dict = create_player_stats()
        name = "gamestate"
        save_char_data(player_dict, name)
        print("Game Successfully Initialized! \nNow that you're all set up,"
              "try hiring some adventurers to party up!")

    except FileExistsError:
        print("You have a working \\characterFiles folder at", path, ".")
        print(
            "If you wish to restart the game, please delete the contents of "
            "\\characterFiles and the file itself.")
        print("Returning to Main Menu... ")


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


def initialize_char():
    """
Creates character file, using name user inputs.
Rolls a bunch of stats using roll_stats() and roll_skills()
and saves values to a dictionary, and character file.
    """
    name = str(input("What's the name of the scouted adventurer? :"))
    name_check = check_name_characters(name)  # check if name is valid
    path = get_file_directory()

    try:
        if not name_check:
            print("This name is invalid!")
        elif name in os.listdir(path):
            print("This person is already a registered adventurer!")
        else:
            skills = []
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

            save_char_data(stat_dict, name)
            print("Adventurer Successfully Registered!")

    except FileNotFoundError:
        print('\nThe \\characterFiles folder was not found! \nPlease '
              'initialize the game by pressing "r" on the Main Menu!\n')


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
        stat_list.append(random.randrange(20, 30))  # hp
        stat_list.append(random.randrange(10, 20))  # mp
        for x in range(5):
            stat_list.append(random.randrange(6, 15))  # str,dex,vit,mag,spi
        stat_list.append(random.randrange(1, 5))  # luck
        return stat_list

    else:  # roll stat additions
        lv += 1
        stat_list.append(random.randrange(3 * lv + 5, 4 * lv + 5) + lv)  # hp
        stat_list.append(random.randrange(lv, 2 * lv) + (lv // 2))  # mp
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
                       'Hammer']
    elif skill_type == "ranged":
        weapon_list = ['Longbow', 'Crossbow', 'Shortbow', 'Javelin',
                       'Throwing Knife', 'Sling']
    elif skill_type == "magic":
        weapon_list = ['Staff', 'Tome', 'Wand', 'Magecraft', 'Orb of Casting',
                       'BDE']
    else:
        skill_type = "normal"
        weapon_list = ['Fists', 'Pitchfork', 'Shotgun', 'Words']
    weapon = random.choice(weapon_list)
    return weapon, skill_type


def roll_skills(lv, skill_type, skills):
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
        skills = []
        for skill in range(2):
            skills.append(random.choice(skill_list))
            skill_list.remove(skills[skill])
    elif lv % 5 == 0 and lv <= 16:
        skill_list_set = set(skill_list)
        skills_set = set(skills)
        skill_list = list(skill_list_set - skills_set)
        skills.append(random.choice(skill_list))
    else:
        skills = skills
    return skills


def determine_skill_list(skill_type):
    """
Prints skills available, determined by skill_type.
    :param skill_type: type of skill, from roll.
    :return: skill_list as list
    """
    if skill_type == "melee":
        skill_list = ['Rising Force', 'Overhead Swing', 'Vital Piercer',
                      'Judo Grapple', 'Mother Rosario', 'Dual Wield',
                      'Demon Mode', 'Feint Strike', 'Hilt Thrust',
                      'The move that Levy from Attack on Titan uses',
                      'Kingly Slash', 'French Beheading']
    elif skill_type == "ranged":
        skill_list = ['Rapid Fire', 'Exploding Shot', 'Armor Piercer',
                      'Poison Tip', 'Oil-Tipped Flint', 'Curved Shot',
                      "Bull's Eye", 'Steady Aim', 'Asphyxiating Arrow',
                      'Wyvern Shot', 'Thieves Aim', "Rangers' Guile"]
    elif skill_type == "magic":
        skill_list = ['Fireball', 'Thunderstruck', 'Nosferatu', 'Fortify Arms',
                      'Summon Ghosts', 'Ancient Power', 'Draconian Breath',
                      'Confusing Ray', 'UnHealing', 'UnRestore', 'UnCure',
                      'Fortnite Dance', 'Slurred Cantrips', 'Mundane Thesis']
    else:
        skill_list = ['Hide', 'Run', 'Yell', 'Fortnite Dance']
    return skill_list


def initialize_battle():
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
        location_list = generate_location_list()
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


def generate_location_list():
    """
Generates list of locations depending on player level.
    :return:  location_list, selectable locations
    """
    player_dict = get_stats("gamestate")
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


def start_battle(char1, char2, char3, location):
    """
Starts a battle using selected player characters, and an enemy created from
selected location.
    :param char1: character 1
    :param char2: character 2
    :param char3: character 3
    :param location: chosen location from location list
    """
    enemy = generate_enemy(location)
    print("\nThe party encountered a ", enemy["name"], "!", sep='')
    time.sleep(3)
    party_list = [char1, char2, char3]
    battle_list = [char1, char2, char3, enemy]
    battle_list.sort(reverse=True, key=grab_char_dex_stat)

    x = 0
    while enemy["hp"] > 0 and char1["hp"] > 0 and char2["hp"] > 0 and \
            char3["hp"] > 0:
        action = select_char_action(battle_list[x]["mp"])
        if 'money' in battle_list[x]:
            attacker = battle_list[x]
            defender = random.choice(party_list)
        else:
            attacker = battle_list[x]
            defender = enemy
        if action == "Attack":
            print(attacker['name'], " performs an attack on ",
                  defender['name'], "!", sep='')
        elif action == "Skill":
            print(battle_list[x]['name'], " uses ",
                  random.choice(attacker["skills"]), " on ",
                  defender['name'], "!", sep='')
            battle_list[x]['mp'] -= random.randrange(
                6 * battle_list[x]['level'] / 2,
                10 * battle_list[x]['level'] / 2)
        time.sleep(2)
        attack_damage = calculate_action_damage(attacker, defender, action)
        defender["hp"] -= attack_damage
        print(defender["name"], " is at ", defender["hp"], " HP!", sep='')
        print()
        time.sleep(3)
        # checks if dead guy is ally or enemy, then cues respective scene
        if defender["hp"] <= 0:
            defender_team = check_defender_team(defender, party_list)
            if defender_team:
                cue_party_member_death(defender)
            else:
                cue_enemy_death(defender, char1, char2, char3)
        else:
            x += 1
            if x == 4:
                x = 0
            else:
                pass
    print("Returning to Main Menu...")


def initialize_char_select():
    """
Asks for 3 characters to be used in the battle script.
    :return: party_stats, which is a list of character dictionaries from files.
    """
    party_stats = []
    char_select = None
    char_list = get_char_list()

    if not char_list:  # this if/else branch checks number of chars
        print(
            "You don't have any adventurers to form a party! "
            "\nCome back with at least three adventurers.")
        return False
    elif len(char_list) < 3:
        print(
            "You don't have enough adventurers to form a party! "
            "\nCome back with at least three adventurers.")
        return False
    else:
        message = "Which adventurers will party together? :"

        while len(party_stats) < 3 and char_select != "0":
            try:
                character = select_file(char_list, message)

                if character is False:  # this one if 0 was entered
                    return False
                else:
                    party_stats.append(get_stats(character))
                    char_list.remove(character)
                    print(character, "has been added to the party.")
                    message = "Who else will party up? :"

            except TypeError:  # type the number, not the name, plz
                print(
                    "Please enter the ID number of the adventurer you will "
                    "use, \nor enter 0 to go back.")

        return party_stats


def generate_enemy(location):
    """
Generates enemy used for battle.
    :param location: Selected location
    :return: enemy name, enemy_stats as dict
    """
    enemy_list = []
    if location == "Flowering Plains":
        enemies = ["Slime", "Cursed Cornstalk", "Buzzy Bee", "Feral Mutt"]
        lv = 1
    elif location == "Misty Rainforest":
        enemies = ["Slime", "Cain Toad", "Vociferous Viper", "Crocodire"]
        lv = 2
    elif location == "Graven Marsh":
        enemies = ["Slime", "Wild Roots", "Pecking Vulture", "Breaking Bat"]
        lv = 3
    elif location == "Bellowing Mountains":
        enemies = ["Slime", "Billy Goat", "Mountain Ape", "Laughing Lion"]
        lv = 4
    elif location == "Cryptic Caverns":
        enemies = ["Cryptic Slime", "Walking Dead", "Ghast", "Spider Monkey",
                   "????"]
        lv = 5
    elif location == "Ancient Spire":
        enemies = ["Slime Knight", "Haunted Armor", "Kobold Squadron",
                   "Rock Solid"]
        lv = 6
    elif location == "Cloudy Peaks":
        enemies = ["Liquid Slime", "Gilded Goose", "Dragon Hatchling",
                   "Mountain Giant"]
        lv = 7
    elif location == "Canada":
        enemies = ["Canadian Slime", "Dire Wolf", "Friendless Citizen", "Pal"]
        lv = 8
    elif location == "Volcanic Isles":
        enemies = ["Flaming Slime", "Lava Golem", "Dancing Devil"]
        lv = 9
    elif location == "Desolate Wasteland":
        enemies = ["Metal Slime", "Fallout Zombie Hoard", "Dragon Remains",
                   "Roaming Gargantuan"]
        lv = 10
    else:
        print("Something went wrong, and the location name wasn't found!")
        return False

    enemy_list.extend(enemies)  # puts enemy list into empty list
    enemy = random.choice(enemy_list)  # selects random choice from list
    enemy_stats = roll_enemy_stats(lv, enemy)  # rolls stats for enemy
    return enemy_stats


def roll_enemy_stats(lv, enemy):
    """
Generates enemy stats based on location level, and assigns it to enemy
dictionary.
    :param lv: Level of chosen location
    :param enemy: name of enemy
    :return: enemy stats as dictionary
    """
    exp = random.randrange((1 << lv) + (lv * 5), ((1 << lv) * 2) + (lv * 5))
    hp = random.randrange((2 ** lv) + (lv * 15),
                          ((2 ** lv) * 2) + (lv * 15)) + (20 * lv)
    mp = random.randrange((2 ** lv) + (lv * 10), ((2 ** lv) * 2) + (lv * 10))
    strength = random.randrange(3 * lv, 4 * lv) + 8 + lv
    dexterity = random.randrange(3 * lv, 4 * lv) + 8 + lv
    vitality = random.randrange(3 * lv, 4 * lv) + 8 + lv
    magic = random.randrange(3 * lv, 4 * lv) + 8 + lv
    spirit = random.randrange(3 * lv, 4 * lv) + 8 + lv
    luck = random.randrange(1, 4)
    skill_type = random.choice(["melee", "ranged", "magic"])
    money = random.randrange((2 ** lv) + (lv * 5), ((2 ** lv) * 2) + (lv * 5))
    # money used to distinguish enemy from party, given to player after battle

    enemy_dict = {
        "name": enemy,
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
        "skill_type": skill_type,
        "skills": ["Sweeping Attack", "Heavy Blow", "Enraged Charge",
                   "Leaping Crush", "Wild Swing"],
        "money": money
    }

    return enemy_dict


def select_char_action(character_mp):
    """
Selects random action dependant on mp
    :param character_mp: mp taken from loaded char dictionary
    :return: action_choice
    """
    if character_mp > 0:
        action_list = ["Attack", "Skill"]
        action_choice = random.choices(action_list, weights=[8, 2])
        choice = action_choice[0]
    else:
        choice = "Attack"
    return choice


def calculate_hit_probability(attacker, defender):
    """
Calculates probability of hitting based on dexterity values
    :param attacker: attaacker dexterity
    :param defender: defender dexterity
    :return: probability of hitting defender
    """
    hit_probability = round((((10 - (defender / attacker)) ** 3) / 10), 2)
    # a triple roll probability, then given in percent form

    return hit_probability


def calculate_hit_roll(probability):
    """
Calculates if attack hits using calculated probability
    :param probability: hit probability
    :return: true or false, did attack hit or not
    """
    hit_roll = ((random.randrange(0, 100) + (random.randrange(0, 100))) / 2)
    if hit_roll <= probability:
        return True
    else:
        return False


def grab_char_dex_stat(char_dict):
    """
Grabs stat from dictionary and returns it
    :return: the stat found in the dictionary
    """
    return char_dict["dexterity"]


def calculate_action_damage(attacker, defender, action):
    """
Determine what effect happens when action takes place.
    :param attacker: attacker dictionary
    :param defender: defender dictionary
    :param action:
    """
    hit_probability = calculate_hit_probability(attacker["dexterity"],
                                                defender["dexterity"])
    hit_roll = calculate_hit_roll(hit_probability)
    if action == "Attack" and hit_roll is not False:
        damage = calculate_attack_damage(attacker["level"],
                                         attacker["skill_type"],
                                         attacker["strength"],
                                         attacker["magic"],
                                         attacker["luck"],
                                         defender["vitality"],
                                         defender["spirit"],
                                         defender["luck"])
        print("The ", action, " does ", damage, " damage!", sep='')
    elif action == "Skill" and hit_roll is not False:
        base_damage = calculate_attack_damage(attacker["level"],
                                              attacker["skill_type"],
                                              attacker["strength"],
                                              attacker["magic"],
                                              attacker["luck"],
                                              defender["vitality"],
                                              defender["spirit"],
                                              defender["luck"])
        damage_mod = random.randrange(2, 5) / 2  # multiplies damage by mod
        damage = round(base_damage * damage_mod)
        print("The ", action, " does ", damage, " damage!", sep='')
    else:
        print("The ", action, " missed!", sep='')
        damage = 0
    time.sleep(2)
    return damage


def calculate_attack_damage(atlvl, attype, atstr, atmag, atlu, dfvit, dfspi,
                            dflu):
    """
Calculates attack damage from given attacker and defender parameters.
    :param atlvl: attacker level
    :param attype: attacker skill type
    :param atstr: attacker strength
    :param atmag: attacker magic
    :param atlu: attacker luck
    :param dfvit: defender vitality
    :param dfspi: defender spirit
    :param dflu: defender luck
    :return: damage
    """
    if attype == "melee":  # inspired by ffvii damage calcs (sources)
        base_damage = atstr + ((atstr + atlvl) / 32) * ((atstr * atlvl) / 32)
        damage = round(base_damage + atlvl - ((base_damage + atstr) / dfvit))
    elif attype == "ranged":
        base_damage = atstr + ((atstr + atlvl) / 32) * ((atstr * atlvl) / 32)
        damage = round(base_damage + atlvl - ((base_damage + atstr) / dfvit))
    elif attype == "magic":
        base_damage = atmag + ((atmag + atlvl) / 32) * ((atmag * atlvl) / 32)
        damage = round(base_damage + atmag + atlvl - ((base_damage + atmag)
                                                      / dfspi) - (dfspi // 2))
    else:
        damage = 1

    critical_hit = ((atlu + atlvl - dflu) / 4) + 1
    random_critical = random.randrange(1, 16)

    if random_critical <= critical_hit:
        damage *= 3
        print("Critical Hit!!" * 2)
        time.sleep(2)
    else:
        pass

    if damage < 0:
        damage = 1
    else:
        pass

    return damage


def check_defender_team(defender, party_list):
    """
Checks if killed object was a player object or enemy object
    :param defender:
    :param party_list:
    :return:
    """
    if defender in party_list:
        print(defender["name"], "has perished!")
        return True
    else:
        print("The enemy ", defender["name"], " has perished!", sep='')
        return False


def cue_enemy_death(defender, char1, char2, char3):
    """
Runs script when enemy is killed in battle.
    :param defender: enemy dictionary
    :param char1: char 1 dict
    :param char2: char 2 dict
    :param char3:  char 3 dict
    """
    print("\nThe victorious adventurers return to the guild with their heads\n"
          "held high. The trip proved successful thanks to your great \n"
          "thinking. The odds of battle proved to be no better than your \n"
          "party's teamwork and your planning. Well done, guild master.\n")
    time.sleep(4)
    player_dict = get_stats("gamestate")
    player_dict["gold"] += defender["money"]
    player_dict["exp"] += defender["exp"]

    # Does the Guild level up?
    message = "Your Guild Hall has leveled up!"
    player_dict["level"] = level_up_guild(player_dict, message)
    time.sleep(2)
    save_char_data(player_dict, "gamestate")

    # Update char exp, and check for level up
    file1 = get_stats(char1["name"])
    file2 = get_stats(char2["name"])
    file3 = get_stats(char3["name"])
    file1["exp"] += defender["exp"] * 2
    file2["exp"] += defender["exp"] * 2
    file3["exp"] += defender["exp"] * 2
    lvl_check = check_level_up(file1)
    if lvl_check:
        level_up_stats(file1["name"])
        time.sleep(2)
    else:
        pass
    lvl_check = check_level_up(file2)
    if lvl_check:
        level_up_stats(file2["name"])
        time.sleep(2)
    else:
        pass
    lvl_check = check_level_up(file3)
    if lvl_check:
        level_up_stats(file3["name"])
        time.sleep(2)
    else:
        pass


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


def cue_party_member_death(defender):
    """
May the dead rest in peace.
    :param defender: you let this happen
    """
    print("\nThe adventurers return to the guild, defeated, and with one "
          "less \nmember in tow. Their inadequacy and your lack of judgement "
          "has \nled to one of your guild members perishing. The dead won't "
          "be \nreturning anytime soon, so don't expect to come across",
          defender["name"], "\nagain. Reflect, and don't make the same "
                            "mistake next time.")
    time.sleep(8)
    kill_char(defender)


def display_char_stats():
    """
Asks for which character to be shown, and displays stats from file.
    :return:
    """
    prompt = "Whose stats would you like to see? :"
    char_list = get_char_list()

    if not char_list:
        print(
            "You don't have any adventurers! \nTry hiring some from the "
            "Main Menu!")
    else:
        file_select = select_file(char_list, prompt)

        if file_select in char_list:
            stat_line = ["name", "level", "exp", "hp", "mp", "strength",
                         "dexterity", "vitality",
                         "magic", "spirit", "weapon", "skills"]
            stats = get_stats(file_select)

            for index in range(12):
                print(stat_line[index], ":", stats.get(stat_line[index]))

        else:
            print("Returning to Main Menu... ")


def kill_char_from_menu():
    """
Removes character from file directory, essentially killing character
    :return:
    """
    try:
        prompt = "Who would you like to kill? :"
        char_list = get_char_list()

        if not char_list:
            print(
                "There are no lucky adventurers for you to kill! "
                "Try hiring some!")
        char_select = select_file(char_list, prompt)
        char_file = get_stats(char_select)
        kill_choice = input("Are you sure you want to kill " + char_file[
            'name'] + " ? (y/n) :")

        if kill_choice == "y":
            print(char_file['name'],
                  "has been put down. \nReturning to Main Menu.")  # F
            kill_char(char_file)
        else:
            print("Returning to Main Menu... ")

    except TypeError:
        print("Returning to Main Menu... ")


def kill_char(char_file):
    """
Modular remove file from characterFiles directory
    :param char_file: name of file
    """
    path = get_file_directory()
    os.remove(path + '\\' + char_file['name'])


def select_file(char_list, message):
    """
Displays char list in numbered format, asks for selection as number, returns
given file name.
    :param char_list: list of characters grabbed from function
    :param message: message taken from other function, allows modularity
    :return: the specific file name to be read as file, or False to return to
    Main Menu.
    """
    if not char_list:
        return False

    print("\nEnter an ID number, or enter 0 to go back.")
    for value, char in enumerate(char_list, start=1):  # woah, enumerate
        print("[", value, "] ", char, sep="")

    while True:

        try:
            file_select = int(input("\n" + message)) - 1  # fixing for index
            if 0 <= file_select <= (len(char_list) - 1):  # choice is number
                return char_list[file_select]
            elif file_select == (-1):  # if input is 0, return to main menu
                return False
            else:
                print(
                    "This is not a valid selection! "
                    "\nTry another ID, or enter 0 to go back.")

        except ValueError:  # If value not a number, repeat loop
            print(
                "This is not a valid selection! "
                "\nTry another ID, or enter 0 to go back.")


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


def display_player_stats():
    """
Prints stats found in gamestate file.
    """
    try:
        char_select = "gamestate"
        player_dict = get_stats(char_select)
        for key, value in player_dict.items():  # prints the dict in the file
            print(value, ":", key)
    except FileNotFoundError:
        print('\nThe \\characterFiles folder was not found! \nPlease '
              'initialize the game by pressing "r" on the Main Menu!',
              end='\n\n')


def save_char_data(stat_dict, name):
    """
Takes given char dictionary and file name and saves to char's file name
    :return: "Adventurer stats successfully recorded!"
    """
    char_json = json.dumps(stat_dict, indent=4)  # turns the dict into json
    path = get_file_directory()

    with open(os.path.join(path, name), 'w') as writer:
        writer.write(char_json)  # saves json to file

    message = "Adventurer stats successfully recorded!"
    return message


def get_char_list():
    """
View files in the game file directory,
check if none exist, and output as list
    :return: char_list as list
    """
    try:
        path = get_file_directory()
        files = os.listdir(path)
        char_list = []

        for file in files:  # prints all files found in \\characterFiles
            char_list.append(file)  # reads stores all files from dir into list

        char_list.remove("gamestate")  # removes the gamestate file
        if not char_list:  # checks if list is empty
            return False
        else:
            return char_list

    except FileNotFoundError:
        print('\nThe \\characterFiles folder was not found! \nPlease '
              'initialize the game by pressing "r" on the Main Menu!\n')


def check_name_characters(name):
    """
Checks if filename is valid.
https://www.mtu.edu/umc/services/websites/writing/characters-avoid/
    :param name: name
    :return: better name
    """
    name = name.replace(" ", "A")  # allows spaces...
    if name == "" or name == "0" or name == "gamestate":
        return False
    elif name.isalnum():  # ...but no other special chars
        return True
    else:
        return False


def get_file_directory():
    """
Get the directory where the game files are stored, = cwd\\characterFiles
    :return: path for files
    """
    path = os.getcwd() + "\\characterFiles"
    return path

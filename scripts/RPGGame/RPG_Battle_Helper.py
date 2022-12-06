from . import RPG_GameHelper as rpg
from . import RPG_Character as rpgc
from . import RPG_Battle as rpgb
import time
import random
import asyncio
import discord
import discord.ext.commands.context as ctxt


async def start_battle(ctx, thread, char1 : dict, char2 : dict, char3 : dict, location : str):
    """
Starts a battle using selected player characters, and an enemy created from
selected location.
    :param char1: character 1
    :param char2: character 2
    :param char3: character 3
    :param location: chosen location from location list
    """
    enemy = generate_enemy(location)
    message = f"The party encountered a {enemy['name']}!\n The {enemy['name']} has {enemy['hp']} HP."
    await rpg.send_message_in_thread(thread, message)
    #print("\nThe party encountered a ", enemy["name"], "!", sep='')
    time.sleep(3)
    party_list = [char1, char2, char3]
    battle_list = [char1, char2, char3, enemy]
    battle_list.sort(reverse=True, key=grab_char_dex_stat)

    x = 0
    while enemy["hp"] > 0 and char1["hp"] > 0 and char2["hp"] > 0 and char3["hp"] > 0:
        message = ""
        action = select_char_action(battle_list[x]["mp"])

        if 'money' in battle_list[x]:
            attacker = battle_list[x]
            defender = random.choice(party_list)
        else:
            attacker = battle_list[x]
            defender = enemy

        if action == "Attack":
            if 'weapon' in battle_list[x]:
                message = "".join([message, 
                               f"{attacker['name']} uses their {attacker['weapon']} to perform an attack on {defender['name']}!\n"])
            else:
                message = "".join([message, 
                                    f"{attacker['name']} performs an attack on {defender['name']}!\n"])
            #print(attacker['name'], " performs an attack on ",
                  #defender['name'], "!", sep='')
        elif action == "Skill":
            message = "".join([message, 
                               f"{battle_list[x]['name']} uses {random.choice(attacker['skills'])} on {defender['name']}!\n"])
            #print(battle_list[x]['name'], " uses ",
                 # random.choice(attacker["skills"]), " on ",
                  #defender['name'], "!", sep='')
            battle_list[x]['mp'] -= random.randrange(
                6 * battle_list[x]['level'] / 2,
                10 * battle_list[x]['level'] / 2)

        attack_damage, actionmessage = calculate_action_damage(attacker, defender, action)
        message = "".join([message, actionmessage])
        defender["hp"] -= attack_damage
        message = "".join([message, 
                           f"{defender['name']} is at {defender['hp']} HP!"])
        #print(defender["name"], " is at ", defender["hp"], " HP!", sep='')
        #print()

        # checks if dead guy is ally or enemy, then cues respective scene
        await rpg.send_message_in_thread(thread, message)
        time.sleep(4)

        if defender["hp"] <= 0:
            defender_team = await check_defender_team(thread, defender, party_list)
            if defender_team:
                await cue_party_member_death(ctx, thread, defender)
            else:
                await cue_enemy_death(ctx, thread, defender, char1, char2, char3)
        else:
            x += 1
            if x == 4:
                x = 0
            else:
                pass
    print("Returning to Main Menu...")


def generate_enemy(location : str):
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


def grab_char_dex_stat(char_dict):
    """
Grabs stat from dictionary and returns it
    :return: the stat found in the dictionary
    """
    return char_dict["dexterity"]


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

    message = ""
    attackmessage = ""
    if action == "Attack" and hit_roll is not False:
        damage, attackmessage = calculate_attack_damage(attacker["level"],
                                         attacker["skill_type"],
                                         attacker["strength"],
                                         attacker["magic"],
                                         attacker["luck"],
                                         defender["vitality"],
                                         defender["spirit"],
                                         defender["luck"])
        print("The ", action, " does ", damage, " damage!", sep='')
    elif action == "Skill" and hit_roll is not False:
        base_damage, attackmessage = calculate_attack_damage(attacker["level"],
                                              attacker["skill_type"],
                                              attacker["strength"],
                                              attacker["magic"],
                                              attacker["luck"],
                                              defender["vitality"],
                                              defender["spirit"],
                                              defender["luck"])
        damage_mod = random.randrange(2, 5) / 2  # multiplies damage by mod
        damage = round(base_damage * damage_mod)
        message = f"The {action} does {damage} damage!\n"
        #print("The ", action, " does ", damage, " damage!", sep='')
    else:
        message = f"The {action} missed!\n"
        attackmessage = ""
        #print("The ", action, " missed!", sep='')
        damage = 0
    if attackmessage != "":
        message = "".join([message, attackmessage])
    return damage, message


def calculate_hit_probability(attacker, defender):
    """
Calculates probability of hitting based on dexterity values
a triple roll probability, then given in percent form
    :param attacker: attaacker dexterity
    :param defender: defender dexterity
    :return: probability of hitting defender
    """
    hit_probability = round((((10 - (defender / attacker)) ** 3) / 10), 2)
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
        message = ("Critical Hit!! Critical Hit!!\n")
        #print("Critical Hit!!" * 2)
        #time.sleep(2)
    else:
        message = ""

    if damage < 0:
        damage = 1
    else:
        pass

    return damage, message


async def check_defender_team(thread, defender, party_list):
    """
Checks if killed object was a player object or enemy object
    :param defender:
    :param party_list:
    :return:
    """
    if defender in party_list:
        await rpg.send_message_in_thread(thread, f"{defender['name']} has perished!")
        #print(defender["name"], "has perished!")
        return True
    else:
        await rpg.send_message_in_thread(thread, f"The enemy {defender['name']} has perished!")
        #print("The enemy ", defender["name"], " has perished!", sep='')
        return False


async def cue_enemy_death(ctx, thread, defender, char1, char2, char3):
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
    player_dict = await rpg.get_player_stats(ctx)
    player_dict["gold"] += defender["money"]
    player_dict["exp"] += defender["exp"]

    # Does the Guild level up?
    level = rpgb.level_up_guild(player_dict)
    if level > player_dict['level']:
        await rpg.send_message_in_thread(thread, "Your Guild Hall has leveled up!")
    player_dict["level"] = level
    #time.sleep(2)
    rpgc.save_player_data(player_dict)

    # Update char exp, and check for level up
    #file1 = get_stats(char1["name"])
    #file2 = get_stats(char2["name"])
    #file3 = get_stats(char3["name"])
    char1["exp"] += defender["exp"] * 2
    char2["exp"] += defender["exp"] * 2
    char3["exp"] += defender["exp"] * 2
    lvl_check = rpgb.check_level_up(char1)
    if lvl_check:
        await rpg.send_message_in_thread(thread, rpgc.level_up_stats(ctx, char1))
        time.sleep(2)

    lvl_check = rpgb.check_level_up(char2)
    if lvl_check:
        await rpg.send_message_in_thread(thread, rpgc.level_up_stats(ctx, char2))
        time.sleep(2)

    lvl_check = rpgb.check_level_up(char3)
    if lvl_check:
        await rpg.send_message_in_thread(thread, rpgc.level_up_stats(ctx, char3))
        time.sleep(2)
    
    return


async def cue_party_member_death(ctx, thread, defender):
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
    message = f"""
    The adventurers return to the guild, defeated, and with one less member in tow.
    """
    await rpg.send_message_in_thread(thread, message)
    time.sleep(3)

    message = f"""
    Your lack of judgement has led to one of your guild members perishing.
    """
    await rpg.send_message_in_thread(thread, message)
    time.sleep(2)

    message = f"""
    The dead don't rise where you're from, so don't expect to see {defender['name']} again.
    """
    await rpg.send_message_in_thread(thread, message)
    time.sleep(3)
    rpgc.kill_char(ctx, defender)
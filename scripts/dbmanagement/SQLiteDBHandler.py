# Run the following commands to install the packages before importing:
# pip install pandas
# praw, discord, dotenv, sqlite3

import discord
import dotenv
import os
import pandas as pd
import sqlite3
from itertools import chain

DBPASSWORD = os.getenv('DBPASSWORD')

def connectDB():
    # connect to database
    connection = sqlite3.connect(r"scripts\dbmanagement\UserInfo.db")
    print("Database opened successfully")
    # create db cursor
    cur = connection.cursor()
    print("Connection made")
    return connection, cur

# for creating tables and inserting data
def execute_query(query):
    connection, cur = connectDB()
    try:
        cur.execute(query)
        connection.commit()
        print("Query successful")
        connection.close()          # saves the commit
    except Exception as err:
        print(f"Error: '{err}'")

# for viewing tables and data
def read_query(query):
    connection, cur = connectDB()
    result = None
    try:
        cur.execute(query)
        result = cur.fetchall()
        return result
    except Exception as err:
        print(f"Error: '{err}'")

def user_exists(userID):
    """Checks if the user exists in the DB. If they don't, it puts them in """
    findUsers = """
    SELECT ID FROM UserStats;
    """
    knownUsers = read_query(findUsers)      # returns as nested list
    knownUsers = chain.from_iterable(knownUsers)
    if userID in knownUsers:
        return True
    else:
        updateQuery = f"""
        INSERT INTO UserStats VALUES
        ({userID}, 0, 0);
        """
        execute_query(updateQuery)
        return False

def update_points(userID, points_to_add):
    """Updates the user's points in the DB. To get userID, try using ctx.message.author.id"""
    points_to_add = int(points_to_add)
    if user_exists(userID):
        findPoints = f"""
        SELECT Points FROM UserStats
        WHERE ID = {userID}
        """
        currentPoints = read_query(findPoints)
        # grab value from nested list
        currentPoints = currentPoints[0][0]

        newPoints = currentPoints + points_to_add
        updateQuery = f"""
        UPDATE UserStats
        SET Points = {newPoints}
        WHERE ID = {userID};
        """
    else:
        updateQuery = f"""
        INSERT INTO UserStats VALUES
        ({userID}, {points_to_add}, 0);
        """
    execute_query(updateQuery)

def update_gold(userID, gold_to_add):
    """Updates the user's gold in the DB. To get userID, try using ctx.message.author.id"""
    gold_to_add = int(gold_to_add)
    if user_exists(userID):
        findGold = f"""
        SELECT Gold FROM UserStats
        WHERE ID = {userID};
        """
        currentGold = read_query(findGold)
        # grab value from nested list
        currentGold = currentGold[0][0]

        newGold = currentGold + gold_to_add
        updateQuery = f"""
        UPDATE UserStats
        SET Gold = {newGold}
        WHERE ID = {userID};
        """
    else:
        updateQuery = f"""
        INSERT INTO UserStats VALUES
        ({userID}, 0, {gold_to_add});
        """
    execute_query(updateQuery)

async def print_full_tuples(ctx, results: str):
    for result in results:
        ID, points, gold = result
        member = await ctx.bot.fetch_user(ID)
        await ctx.send(f"{member.name}\nPoints: {points}\nGold: {gold}")

async def view_stats(ctx):
    select_query = """
    SELECT * FROM UserStats;
    """
    
    results = read_query(select_query)
    await print_full_tuples(ctx, results)

async def get_stats(ctx, user: discord.Member):
    userID = user.id
    user_exists(userID)

    select_query = f"""
    SELECT * FROM UserStats
    WHERE ID = {userID};
    """
    result = read_query(select_query)
    await print_full_tuples(ctx, result)


def get_character_from_db(discordid : int, charname = None) -> list:
    if (discordid is None):
        print("bad discordID")
        return
    findChar = f"""
    SELECT * FROM Characters
    WHERE discordID = {discordid};
    """
    if charname is not None:
        findChar = f"""
        SELECT * FROM Characters
        WHERE discordID = {discordid}
        AND name = '{charname}';
        """
    result = read_query(findChar)
    return result


def save_character_into_db(discordid : int, stat_dict : dict) -> list:
    if (discordid is None or stat_dict is None):
        return
    query = f"""
    SELECT * FROM Characters
    WHERE ID = {discordid}
    AND name = {stat_dict['name']};
    """
    if read_query(query) is not None:
        query = f"""
        UPDATE Characters
        SET level = {stat_dict['level']},
            exp = {stat_dict['exp']},
            hp = {stat_dict['hp']},
            mp = {stat_dict['mp']},
            strength = {stat_dict['strength']},
            dexterity = {stat_dict['dexterity']},
            vitality = {stat_dict['vitality']},
            magic = {stat_dict['magic']},
            spirit = {stat_dict['spirit']},
        WHERE discordID = {discordid}
        AND name = {stat_dict['name']};
        """
        message = "Character Saved!"
    else:
        print("Character doesn't exist, moving to create.")
        skill_1 = f"'{stat_dict['skills'][0]}'" if stat_dict['skills'][0] is not None else 'NULL'
        skill_2 = f"'{stat_dict['skills'][1]}'" if stat_dict['skills'][1] is not None else 'NULL'
        skill_3 = f"'{stat_dict['skills'][2]}'" if stat_dict['skills'][2] is not None else 'NULL'
        skill_4 = f"'{stat_dict['skills'][3]}'" if stat_dict['skills'][3] is not None else 'NULL'
        skill_5 = f"'{stat_dict['skills'][4]}'" if stat_dict['skills'][4] is not None else 'NULL'
        print(skill_1, skill_2, skill_3, skill_4, skill_5)
        query = f"""
        INSERT INTO Characters (
            ID,
            discordID,
            name,
            level,
            exp,
            hp,
            mp,
            strength,
            dexterity,
            vitality,
            magic,
            spirit,
            luck,
            weapon,
            skill_type,
            skill_1,
            skill_2,
            skill_3,
            skill_4,
            skill_5
        ) 
        VALUES (
            NULL,
            {discordid},
            '{stat_dict['name']}',
            {stat_dict['level']},
            {stat_dict['exp']},
            {stat_dict['hp']},
            {stat_dict['mp']},
            {stat_dict['strength']},
            {stat_dict['dexterity']},
            {stat_dict['vitality']},
            {stat_dict['magic']},
            {stat_dict['spirit']},
            {stat_dict['luck']},
            '{stat_dict['weapon']}',
            '{stat_dict['skill_type']}',
            {skill_1},
            {skill_2},
            {skill_3},
            {skill_4},
            {skill_5}
        );
        """
        message = "Adventurer Successfully Created!"
    execute_query(query)
    return message


async def test_points(ctx):
    userID = ctx.message.author.id
    update_points(userID, int(1))

async def test_gold(ctx):
    userID = ctx.message.author.id
    update_gold(userID, int(1))
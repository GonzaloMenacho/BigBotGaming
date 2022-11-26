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

async def test_points(ctx):
    userID = ctx.message.author.id
    update_points(userID, int(1))

async def test_gold(ctx):
    userID = ctx.message.author.id
    update_gold(userID, int(1))
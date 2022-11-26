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

def update_points(userID, points_to_add):
    points_to_add = int(points_to_add)
    findUsers = """
    SELECT ID FROM UserStats;
    """
    knownUsers = read_query(findUsers)      # returns as nested list
    knownUsers = chain.from_iterable(knownUsers)
    if userID in knownUsers:
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
    gold_to_add = int(gold_to_add)
    findUsers = """
    SELECT ID FROM UserStats;
    """
    knownUsers = read_query(findUsers)      # returns as nested list
    knownUsers = chain.from_iterable(knownUsers)
    if userID in knownUsers:
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

async def view_stats(ctx):
    select_query = """
    SELECT * FROM UserStats;
    """
    
    results = read_query(select_query)

    for result in results:
        ID, points, gold = result
        member = await ctx.bot.fetch_user(ID)
        print(member.name)
        await ctx.send(f"{member.name}\nPoints: {points}\nGold: {gold}")

async def test_points(ctx):
    userID = ctx.message.author.id
    update_points(userID, int(1))

async def test_gold(ctx):
    userID = ctx.message.author.id
    update_gold(userID, int(1))
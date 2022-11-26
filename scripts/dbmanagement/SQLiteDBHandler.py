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

def update_points(ctx, points_to_add):
    points_to_add = int(points_to_add)
    user = str(ctx.message.author)
    print(user)
    findUsers = """
    SELECT User FROM UserStats;
    """
    knownUsers = read_query(findUsers)      # returns as nested list
    knownUsers = chain.from_iterable(knownUsers)
    print(knownUsers, user)
    if user in knownUsers:
        findPoints = f"""
        SELECT Points FROM UserStats
        WHERE User = '{user}';
        """
        currentPoints = read_query(findPoints)
        # grab value from nested list
        currentPoints = currentPoints[0][0]

        newPoints = currentPoints + points_to_add
        updateQuery = f"""
        UPDATE UserStats
        SET Points = {newPoints}
        WHERE User = '{user}';
        """
    else:
        updateQuery = f"""
        INSERT INTO UserStats VALUES
        ('{user}', {points_to_add}, 0);
        """
    execute_query(updateQuery)

def update_gold(ctx, gold_to_add):
    gold_to_add = int(gold_to_add)
    user = str(ctx.message.author)
    print(user)
    findUsers = """
    SELECT User FROM UserStats;
    """
    knownUsers = read_query(findUsers)      # returns as nested list
    knownUsers = chain.from_iterable(knownUsers)
    print(knownUsers, user)
    if user in knownUsers:
        findGold = f"""
        SELECT Gold FROM UserStats
        WHERE User = '{user}';
        """
        currentGold = read_query(findGold)
        # grab value from nested list
        currentGold = currentGold[0][0]

        newGold = currentGold + gold_to_add
        updateQuery = f"""
        UPDATE UserStats
        SET Gold = {newGold}
        WHERE User = '{user}';
        """
    else:
        updateQuery = f"""
        INSERT INTO UserStats VALUES
        ('{user}', 0, {gold_to_add});
        """
    execute_query(updateQuery)

def make_test_table():
    create_test_table = """
    CREATE TABLE Test (
      "User"	TEXT NOT NULL UNIQUE,
	  "Points"	INTEGER,
      "Gold"    INTEGER,
	  PRIMARY KEY("User")
      );
     """
    pop_test_table = """
    INSERT INTO Test VALUES
    ('Player 3', 3, 30),
    ('Player 2', 2, 20),
    ('Player 1', 1, 10);
    """

    execute_query(create_test_table) # execute our defined query
    execute_query(pop_test_table)

async def view_stats(ctx):
    select_query = """
    SELECT * FROM UserStats;
    """
    
    results = read_query(select_query)

    for result in results:
        name, points, gold = result
        await ctx.send(f"{name}\nPoints: {points}\nGold: {gold}")

async def test_points(ctx):
    update_points(ctx, int(1))

async def test_gold(ctx):
    update_gold(ctx, int(1))
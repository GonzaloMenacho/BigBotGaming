# Run the following commands to install the packages before importing:
# pip install pandas
# praw, discord, dotenv, sqlite3

import discord
import dotenv
import os
import pandas as pd
import sqlite3

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

def make_test_table():
    create_test_table = """
    CREATE TABLE UserStats (
      "User"	TEXT NOT NULL UNIQUE,
	  "Points"	INTEGER,
      "Gold"    INTEGER,
	  PRIMARY KEY("User")
      );
     """
    pop_test_table = """
    INSERT INTO UserStats VALUES
    ('Player 3', 3, 30),
    ('Player 2', 2, 20),
    ('Player 1', 1, 10);
    """

    execute_query(create_test_table) # execute our defined query
    execute_query(pop_test_table)


async def view_test_table(ctx):
    select_query = """
    SELECT * FROM UserStats;
    """
    
    results = read_query(select_query)

    for result in results:
        name, points, gold = result
        await ctx.send("{0}\nPoints: {1}\nGold: {2}".format(name, points, gold))

async def testdb(ctx):
    try:
        make_test_table()
        print("test table created")
        await view_test_table(ctx)
    except Exception as err:
        print(f"Error: '{err}'")
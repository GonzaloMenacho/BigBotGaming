# Resources used:
## https://www.freecodecamp.org/news/connect-python-with-sql/

# Run the following commands to install the packages before importing:
# pip install mysql-connector
# pip install pandas
# praw, discord, dotenv

import discord
import dotenv
import os
import mysql.connector
from mysql.connector import Error
import pandas as pd

DBPASSWORD = os.getenv('DBPASSWORD')

connection = None

# connect to a database within the server
def create_db_connection(host_name, user_name, user_password, db_name):
    # close any existing connections
    connection = None

    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password,
            database = db_name
        )
        print("MySQL Database connection successful")
    except Exception as err:
        print(f"Error: '{err}'")

    return connection

# for creating tables and inserting data
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Exception as err:
        print(f"Error: '{err}'")

# for viewing tables and data
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as err:
        print(f"Error: '{err}'")

def make_test_table(connection):
    create_test_table = """
    CREATE TABLE high_scores (
      username VARCHAR(40) PRIMARY KEY,
      points INT
      );
     """
    pop_test_table = """
    INSERT INTO high_scores VALUES
    ('Player 3', 3),
    ('Player 2', 2),
    ('Player 1', 1);
    """

    execute_query(connection, create_test_table) # execute our defined query
    execute_query(connection, pop_test_table)


async def view_test_table(ctx, connection):
    select_query = """
    SELECT * FROM high_scores;
    """
    
    results = read_query(connection, select_query)

    for result in results:
        await ctx.send(result)

async def testdb(ctx, db_name):
    # pw is the root password for the MySQL Server as a string.
    pw = DBPASSWORD
    db = db_name
    try:
        connection = create_db_connection("localhost", "root", pw, db)
        # await ctx.send(f"MySQL Database connection successful")
        make_test_table(connection)
        print("test table created")
        await view_test_table(ctx, connection)
    except Exception as err:
        print(f"Error: '{err}'")

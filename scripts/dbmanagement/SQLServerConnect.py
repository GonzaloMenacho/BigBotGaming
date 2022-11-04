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

def create_server_connection(host_name, user_name, user_password):
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
    except Error as err:
        print(f"Error: '{err}'")

    return connection

async def connect_to_DB(ctx):
    # pw is the root password for the MySQL Server as a string.
    pw = DBPASSWORD
    try:
        connection = create_db_connection("localhost", "root", pw, db)
        # await ctx.send(f"MySQL Database connection successful")
        make_test_table(connection)
        print("test table created")
        await view_test_table(ctx, connection)
    except Error as err:
        print(f"Error: '{err}'")
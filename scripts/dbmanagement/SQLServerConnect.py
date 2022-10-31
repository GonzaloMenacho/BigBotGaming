# Resources used:
## https://www.freecodecamp.org/news/connect-python-with-sql/

# Run the following commands to install the packages before importing:
# pip install mysql-connector-python
# pip install pandas

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
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

async def connect_to_DB(ctx):
    # pw is the root password for the MySQL Server as a string.
    pw = DBPASSWORD
    try:
        connection = create_server_connection("localhost", "root", pw)
        await ctx.send(f"MySQL Database connection successful")
    except Error as err:
        await ctx.send(f"Error: '{err}'")

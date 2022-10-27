# Resources used:
## https://www.freecodecamp.org/news/connect-python-with-sql/

# Run the following commands to install the packages before importing:
# pip install mysql-connector-python
# pip install pandas

import mysql.connector
from mysql.connector import Error
import pandas as pd

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


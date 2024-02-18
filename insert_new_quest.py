#!./venv/bin/python3.11

import psycopg2, os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get database connection parameters from environment variables
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)

# Create a cursor object to interact with the database
cur = conn.cursor()

# Get the current date and time
current_datetime = datetime.now()
current_datestamp = current_datetime.strftime("%Y-%m-%d")



# Read the content of the quest condition text file
with open("quest_condition.txt", "r") as file:
    quest_condition = file.read()

# Read the content of the function_template text file
with open("function_template.txt", "r") as file:
    function_template = file.read()

# Read the content of the unit_tests text file
with open("unit_tests.txt", "r") as file:
    unit_tests = file.read()

# Execute a query to get the PostgreSQL version
cur.execute("SELECT version();")

# Fetch the result of the query
version = cur.fetchone()[0]


# Print the PostgreSQL version
print("PostgreSQL version:", version)

# Define the SQL query with placeholders for parameters
# Define the parameters for the query
# params = ("PY-000001", 'Python', 'Novice Quests', 'Sum Numbers', 'Aleksandar Karastoyanov', current_datestamp, current_datestamp, str(quest_condition), str(function_template), str(unit_tests), '30')
print(type(unit_tests))
# print(type(sql))

# # Execute the query
# cur.execute(sql)

# Commit the transaction
conn.commit()
# Close the cursor and connection
cur.close()
conn.close()
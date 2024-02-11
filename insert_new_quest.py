#!./venv/bin/python3.11

import psycopg2, os
from dotenv import load_dotenv

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

# Execute a query to get the PostgreSQL version
cur.execute("SELECT version();")

# Fetch the result of the query
version = cur.fetchone()[0]


# Print the PostgreSQL version
print("PostgreSQL version:", version)

# Define the SQL query with placeholders for parameters
sql = """INSERT INTO coding_quests (language, difficulty, quest_name, quest_author, date_added, last_modified, condition, function_template, unit_tests, xp)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""


# Define the parameters for the query
params = ('Python', 'Novice Quests', 'Sum Numbers', 'Aleksandar Karastoyanov', '2024-02-10', '2024-02-10',
          'Write a function which returns the divison of two numbers', 
          "import unittest\n\ndef add_numbers(a, b):\n    '''\n    Function to add two numbers.\n    '''\n    \n    return a + b\n\nclass TestAddNumbers(unittest.TestCase):\n    def test_positive_numbers(self):\n        self.assertEqual(add_numbers(3, 5), 8)\n\n    def test_negative_numbers(self):\n        self.assertEqual(add_numbers(-3, -5), -8)\n\n    def test_mixed_numbers(self):\n        self.assertEqual(add_numbers(-3, 5), 2)\n\n    def test_zero(self):\n        self.assertEqual(add_numbers(0, 0), 0)\n\nif __name__ == '__main__':\n    unittest.main()",
          "class TestAddNumbers(unittest.TestCase):\n    def test_positive_numbers(self):\n        self.assertEqual(add_numbers(3, 5), 8)\n\n    def test_negative_numbers(self):\n        self.assertEqual(add_numbers(-3, -5), -8)\n\n    def test_mixed_numbers(self):\n        self.assertEqual(add_numbers(-3, 5), 2)\n\n    def test_zero(self):\n        self.assertEqual(add_numbers(0, 0), 0)\n\nif __name__ == '__main__':\n    unittest.main()",
          '30')

# Execute the query
cur.execute(sql, params)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
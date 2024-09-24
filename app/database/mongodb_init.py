from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()


# MongoDB connection Init
MONGO_HOSTNAME = os.getenv('MONGO_HOSTNAME')
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_AUTH_SOURCE = os.getenv('MONGO_AUTH_SOURCE')
MONGO_PRIMARY_PORT = int(os.getenv('MONGO_PRIMARY_PORT'))


# Load the env variables
mongo1_client = MongoClient(
    host=os.getenv('MONGO_DATABASE_URI_DEV'))


# Connect to the MongoDB with the provided URI(primary and secondary clients)
mongo1_db = mongo1_client[MONGO_DATABASE]
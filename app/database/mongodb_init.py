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
MONGO_SECONDARY_PORT = int(os.getenv('MONGO_SECONDARY_PORT'))
MONGO_SECONDARY_PORT_2 = int(os.getenv('MONGO_SECONDARY_PORT_2'))
MONGO_REPLICA_SET = os.getenv('MONGO_REPLICA_SET')

print(MONGO_HOSTNAME)
print(MONGO_USERNAME)
print(MONGO_PASSWORD)
print(MONGO_DATABASE)
print(MONGO_AUTH_SOURCE)
print(MONGO_PRIMARY_PORT)
print(MONGO_SECONDARY_PORT)
print(MONGO_SECONDARY_PORT_2)


# Load the env variables
mongo1_client = MongoClient(
    host=f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOSTNAME}:{MONGO_PRIMARY_PORT}/?'
         f'authSource={MONGO_DATABASE}&replicaSet={MONGO_REPLICA_SET}&directConnection=true')
mongo2_client = MongoClient(
    host=f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOSTNAME}:{MONGO_SECONDARY_PORT}/?'
         f'authSource={MONGO_DATABASE}&replicaSet={MONGO_REPLICA_SET}&directConnection=true')

# Connect to the MongoDB with the provided URI(primary and secondary clients)
mongo1_db = mongo1_client[MONGO_DATABASE]
mongo2_db = mongo2_client[MONGO_DATABASE]

# Get collections from database
user_logins_collection = mongo1_db['userLogins']


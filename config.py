import os
from dotenv import load_dotenv

# Load the env variables
load_dotenv()

class Config:
    SECRET_KEY = os.urandom(24).hex()
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_DEV')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIMEZONE = 'Europe/Sofia'

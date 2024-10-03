import os
from dotenv import load_dotenv
from datetime import timedelta
import urllib.parse

# Load the env variables
load_dotenv()

# Define the connection parameters as variables
USERNAME = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
ENCODED_PASSWORD = urllib.parse.quote_plus(PASSWORD)
DB_NAME = os.getenv('DB_NAME')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')

SQL_URI = f'postgresql://{USERNAME}:{ENCODED_PASSWORD}@{HOST}:{PORT}/{DB_NAME}'


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = SQL_URI
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_DOMAIN = False
    TIMEZONE = 'Europe/Sofia'
    PREFERRED_URL_SCHEME = 'https'
    REMEMBER_COOKIE_DURATION = timedelta(days=7)

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Ensure cookies are sent over HTTPS
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = False  # Ensure remember me cookie is sent over HTTPS

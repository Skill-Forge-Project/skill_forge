import os
from dotenv import load_dotenv
from datetime import timedelta

# Load the env variables
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_DEV')
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
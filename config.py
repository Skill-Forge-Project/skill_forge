import os
from dotenv import load_dotenv

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
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True
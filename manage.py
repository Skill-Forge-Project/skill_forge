from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
import app
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


################################### USE WITH CAUITON ##########################################
##################### UPDATE THE BELOW CONTENT BEFORE RUNNING A MIGRATION #####################
# flask db init
# flask db migrate -m "Migrate database <include migration message>"
# flask db upgrade

########## Write below the code to be migrated ##########
from flask import Blueprint

# Initialize main Blueprint
bp = Blueprint('main', __name__)

# Import routes from quest routes
from .quests_routes import bp_qst

# Import routes from user submited quests routes
from .user_submit_quest_routes import bp_usq

# Import routes from user routes
from .user_routes import bp_usr

# Import routes from user submited solutions routes
from .user_submited_solutions import bp_uss
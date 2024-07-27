import random, string, base64, json, os
from datetime import datetime
from flask import Blueprint, redirect, url_for, request, render_template, jsonify, flash, abort
from flask_login import login_required, current_user
# Import the forms and models
from app.models import Quest, ReportedQuest, User, SubmitedSolution, UserAchievement, Achievement, Comment
from app.forms import QuestForm, PublishCommentForm, EditQuestForm, EditReportedQuestForm
# Import code runners
from app.code_runners import run_python, run_javascript, run_java, run_csharp
# Import the database instance
from app.database.db_init import db
from sqlalchemy.orm import joinedload
# Import MongoDB transactions functions
from app.database.mongodb_transactions import mongo_transaction
# Import admin_required decorator
from app.user_permission import admin_required


bp_guild = Blueprint('guilds', __name__)

# Redirect to create new guild page
@bp_guild.route('/create_guild', methods=['GET'])
def open_create_guild():
    return render_template('guild_templates/create_guild.html')

# Create new guild
@bp_guild.route('/guilds/create', methods=['GET', 'POST'])
@login_required
def create_new_guild():
    pass
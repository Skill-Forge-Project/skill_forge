import random, string, base64, json, os
from datetime import datetime
from flask import Blueprint, redirect, url_for, request, render_template, jsonify, flash, abort
from flask_login import login_required, current_user
# Import the forms and models
from app.models import Quest, ReportedQuest, User, SubmitedSolution, UserAchievement, Achievement, Comment
from app.forms import QuestForm, PublishCommentForm, EditQuestForm, EditReportedQuestForm

ranklist = Blueprint('ranklist', __name__)

# Open the ranklist page
@ranklist.route('/ranklist')
def open_ranklist_board():
    # Get the first, second and third players from the database by XP points
    first_player = User.query.filter(User.user_role != 'Admin').order_by(User.xp.desc()).first()
    second_player = User.query.filter(User.user_role != 'Admin').order_by(User.xp.desc()).offset(1).first()
    third_player = User.query.filter(User.user_role != 'Admin').order_by(User.xp.desc()).offset(2).first()
    
    # Get the top users by XP points(4-10)
    top_users = User.query.filter(User.user_role != 'Admin')\
    .order_by(User.xp.desc())\
    .offset(3)\
    .limit(7)\
    .all()
    
    
    return render_template('ranklist_board/ranklist_board.html', 
                           first_player=first_player,
                           second_player=second_player,
                           third_player=third_player,
                           top_users=top_users)
    

@ranklist.route('/ranklist/top_three_players')
def top_three_players():
    pass
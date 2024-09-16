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
    # Get top 20 players by XP points
    top_players = User.query.order_by(User.xp.desc()).limit(20).all()
    return render_template('ranklist_board/ranklist_board.html', top_players=top_players)
    

@ranklist.route('/ranklist/top_three_players')
def top_three_players():
    pass
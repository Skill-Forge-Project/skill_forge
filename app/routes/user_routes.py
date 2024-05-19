import random, string, base64
from datetime import datetime
from flask import Blueprint, redirect, url_for, request, flash, render_template
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
# Import the database instance
from app.database.db_init import db
# Import the forms and models
from app.models import SubmitedSolution, User, UserAchievement, Quest, ReportedQuest, SubmitedQuest

bp_usr = Blueprint('usr', __name__)

#  Get the user's avatar, used in the comments section
@bp_usr.route('/get_avatar/<user_id>', methods=['GET'])
@login_required
def get_avatar(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    avatar = user.avatar
    return avatar

# Route to handle the user profile (self-open)
@bp_usr.route('/my_profile', methods=['POST', 'GET'])
@login_required
def open_user_profile():    
    # Get the User ID for the session
    user_id = current_user.user_id
    # Get the user's solved quests from the database
    user_solved_quests = SubmitedSolution.query.options(joinedload(SubmitedSolution.coding_quest)).all()
    # Get the user info from the database
    user = User.query.get(user_id)
    user.date_registered.strftime('%d-%m-%Y %H:%M:%S')
    # Get the user social media links
    user_facebook = User.query.get(user_id).facebook_profile
    user_instagram = User.query.get(user_id).instagram_profile
    user_github = User.query.get(user_id).github_profile
    user_discord = User.query.get(user_id).discord_id
    user_linked_in = User.query.get(user_id).linked_in
    # Get the user achievements
    user_achievements = UserAchievement.query.filter(UserAchievement.user_id==user_id).all()
    # Convert avatar binary data to Base64-encoded string
    avatar_base64 = base64.b64encode(user.avatar).decode('utf-8') if user.avatar else None
    # Get the last logged date
    user_status = User.query.filter(User.user_id == user_id).first().user_online_status
    last_logged_date = User.query.filter(User.user_id == user_id).first().last_status_update

    return render_template('user_profile.html', user=user, 
                           formatted_date=user.date_registered.strftime('%d-%m-%Y %H:%M:%S'), 
                           avatar=avatar_base64, 
                           user_solved_quests=user_solved_quests,
                           user_facebook=user_facebook,
                           user_instagram=user_instagram,
                           user_github=user_github,
                           user_discord=user_discord,
                           user_linked_in=user_linked_in,
                           user_achievements=user_achievements,
                           user_status=user_status,
                           last_logged_date=last_logged_date)

# Route to handle the user profile (self-open)
@bp_usr.route('/user_profile/<username>', methods=['POST', 'GET'])
@login_required
def open_user_profile_view(username):
    # Get the user info from the database
    user = User.query.filter_by(username=username).first()
    user_id = user.user_id
    if user_id == current_user.user_id:
        return redirect(url_for('usr.open_user_profile'))
    else:
        # Convert avatar binary data to Base64-encoded string
        avatar_base64 = base64.b64encode(user.avatar).decode('utf-8') if user.avatar else None
        # Get the last logged date
        user_status = User.query.filter(User.user_id == user_id).first().user_online_status
        last_logged_date = User.query.filter(User.user_id == user_id).first().last_status_update
        if user:
            return render_template('user_profile_view.html', 
                                user=user, 
                                avatar=avatar_base64,
                                user_status=user_status,
                                last_logged_date=last_logged_date)
        else:
            # Handle the case where the user is not found
            return "User not found", 404


# Change the User avatar route
@bp_usr.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    # Get user ID from session or request parameters
    user_id = current_user.user_id
    if user_id is None:
        # Handle case where user is not logged in
        return redirect(url_for('login'))
    
    # Check if the avatar file is provided in the request
    if 'avatar' not in request.files:
        # Handle case where no file is uploaded
        flash('No avatar file uploaded', 'error')
        return redirect(request.url)
    
    # Get the uploaded file data
    avatar_file = request.files['avatar']
    
    # Read the file data as bytes
    avatar_data = avatar_file.read()
    
    # Update the user's avatar in the database
    user = User.query.get(user_id)
    user.avatar = avatar_data
    db.session.commit()
    
    # Redirect to the user profile page or any other page
    return redirect(url_for('usr.open_user_profile'))


# Update User info route (Self-Update)
@bp_usr.route('/self_update', methods=['GET', 'POST'])
@login_required
def user_self_update():
    current_user_id = current_user.user_id
    new_first_name = request.form.get('change_first_name')
    new_last_name = request.form.get('change_last_name')
    new_email_address = request.form.get('change_email')
    fb_link = request.form.get('change_facebook')
    instagram_link = request.form.get('change_instagram')
    gh_link = request.form.get('change_github')
    discord_id = request.form.get('change_discord')
    linked_in_link = request.form.get('change_linkedin')
    user = User.query.get(current_user_id)
    user.first_name = new_first_name
    user.last_name = new_last_name
    user.email = new_email_address
    user.facebook_profile = fb_link
    user.instagram_profile = instagram_link
    user.github_profile = gh_link
    user.discord_id = discord_id
    user.linked_in = linked_in_link
    db.session.commit()
    return redirect(url_for('usr.open_user_profile'))


# Redirect to the Admin Panel (Admin Role in the database is needed)
@bp_usr.route('/admin_panel')
@login_required
def open_admin_panel():
    # Retrieve all quests from the database
    all_quests = Quest.query.all()
    all_submited_quests = SubmitedQuest.query.all()
    # Get the User ID for the session
    logged_user_id = current_user.user_id
    # Get the user object with the User ID from the session
    currently_logged_user = User.query.get(logged_user_id)
    # Get all reported quests
    all_reported_quests = ReportedQuest.query.all()
    # Get all users (this is needed so we can extract the name of the user who has reported a quest)
    all_users = User.query.all()
    # Get all admins (this is needed so we can create a dropdown menu in the `Check Reports` table)
    all_admins = User.query.filter_by(user_role='Admin').all()
    if currently_logged_user.user_role == "Admin":
        return render_template('admin_panel.html', 
        all_quests=all_quests, 
        all_submited_quests=all_submited_quests, 
        reported_quests=all_reported_quests,
        all_users=all_users,
        all_admins=all_admins)
    flash('You must be an admin to access this page.', 'error')
    return redirect(url_for('main.login'))
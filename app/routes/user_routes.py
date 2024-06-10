import base64, json, re
from datetime import datetime
from flask import Blueprint, redirect, url_for, request, flash, render_template
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
# Import the forms and models
from app.models import SubmitedSolution, User, UserAchievement, Quest, ReportedQuest, SubmitedQuest
from app.forms import QuestForm
# Import the database instance
from app.database.db_init import db
# Import MongoDB transactions functions
from app.database.mongodb_transactions import mongo_transaction

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
    # Get the xp points for the level rank
    with open('app/static/configs/levels.json', 'r') as file:
        levels_data = json.load(file)
    for i in levels_data:
        for rank, data in i.items():
            if rank== user.rank:
                max_xp = data['max_xp']
    xp_percentage = int((user.xp / max_xp) * 100)

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
                           last_logged_date=last_logged_date,
                           max_xp=max_xp,
                           xp_percentage=xp_percentage)

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
        # Get the xp points for the level rank
        with open('app/static/configs/levels.json', 'r') as file:
            levels_data = json.load(file)
        for i in levels_data:
            for rank, data in i.items():
                if rank== user.rank:
                    max_xp = data['max_xp']
        xp_percentage = int((user.xp / max_xp) * 100)
        if user:
            return render_template('user_profile_view.html', 
                                user=user, 
                                avatar=avatar_base64,
                                user_status=user_status,
                                last_logged_date=last_logged_date,
                                max_xp=max_xp,
                                xp_percentage=xp_percentage)
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
    mongo_transaction('user_avatar_change', 
                      action=f'User {user.username} changed avatar',
                      user_id=user_id, username=user.username, 
                      timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
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
    
    mongo_transaction('user_info_update',
                      action=f'User {user.username} updated its info',
                      user_id=current_user_id, 
                      username=user.username,
                      timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return redirect(url_for('usr.open_user_profile'))


# Redirect to the Admin Panel (Admin Role in the database is needed)
@bp_usr.route('/admin_panel')
@login_required
def open_admin_panel():
    create_quest_post = QuestForm()
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
        all_admins=all_admins,
        form=create_quest_post)
    flash('You must be an admin to access this page.', 'error')
    return redirect(url_for('main.login'))


# Open user for editing from the Admin Panel
@bp_usr.route('/edit_user/<user_id>')
@login_required
def open_edit_user(user_id):
    # Retrieve the specific user from the database, based on the user_id
    user = User.query.get(user_id)
    return render_template('edit_user.html', user=user)

# Handle user edit from the Admin Panel
@bp_usr.route('/edit_user_db', methods=['GET', 'POST'])
@login_required
def edit_user_db():
    user_id = request.form.get('user_id')
    user_role = request.form.get('user_role')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('user_email')

    user = User.query.get(user_id)

    # Updating information about the user
    user.user_role = user_role
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    db.session.commit()
    return redirect(url_for('usr.open_admin_panel'))


# Ban user route
@bp_usr.route('/ban_user/<user_id>')
@login_required
def ban_user(user_id, ban_reason='no reason'):
    # Retrieve the specific user from the database, based on the user_id
    user = User.query.get(user_id)
    request_arguments = dict(request.args) # This prints {'ban_reason': 'some_value'}
    # Set new values to these three fields in the database
    user.is_banned = True
    user.ban_date = datetime.now()
    user.ban_reason = request_arguments['ban_reason']
    db.session.commit()
    return redirect(url_for('usr.open_admin_panel'))

# Unban user route
@bp_usr.route('/unban_user/<user_id>')
@login_required
def unban_user(user_id):
    # Retrieve the specific user from the database, based on the user_id
    user = User.query.get(user_id)
    # Set new values to these three fields in the database
    user.is_banned = False
    user.ban_date = None
    user.ban_reason = ''
    db.session.commit()
    return redirect(url_for('usr.open_admin_panel'))
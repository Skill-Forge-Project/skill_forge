import random, string, base64, json
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
# Import the database instance
from app.database.db_init import db
# Import MongoDB transactions functions
from app.database.mongodb_transactions import mongo_transaction
# Import the forms and models
from app.models import SubmitedQuest, Quest, User, Achievement, UserAchievement
# Import the forms
from app.forms import QuestSubmissionForm, QuestApprovalForm
# Import admin_required decorator
from app.user_permission import admin_required
# Import the mail functions
from app.mailtrap import (send_quest_approved_email,
                          send_quest_rejected_email,
                          send_quest_changes_requested_email)

bp_usq = Blueprint('usq', __name__)

# Redirect to the user submit quest page
@bp_usq.route('/open_user_submit_quest')
@login_required
def open_user_submit_quest():
    form = QuestSubmissionForm()
    return render_template('user_submit_quest.html', form=form)


#  Open User Submited Quest for editing from the Admin Panel
@bp_usq.route('/open_submited_quest/<quest_id>', methods=['GET'])
@login_required
@admin_required
def open_submited_quest(quest_id):
    submited_quest = SubmitedQuest.query.filter_by(quest_id=quest_id).first()
    user_avatar = base64.b64encode(current_user.avatar).decode('utf-8')
    form = QuestApprovalForm()
    form.submited_quest_id.data = quest_id
    form.submited_quest_name.data = submited_quest.quest_name
    form.submited_quest_language.data = submited_quest.language
    form.submited_quest_difficulty.data = submited_quest.difficulty
    form.submited_quest_author.data = submited_quest.quest_author
    form.submited_quest_date_added.data = submited_quest.date_added
    form.submited_quest_condition.data = submited_quest.condition
    form.submited_function_template.data = submited_quest.function_template
    form.submited_quest_unitests.data = submited_quest.unit_tests
    form.submited_quest_inputs.data = submited_quest.test_inputs
    form.submited_quest_outputs.data = submited_quest.test_outputs
    
    
    return render_template('edit_submited_quest.html', 
                           submited_quest=submited_quest,
                           user_avatar=user_avatar,
                           form=form)

# Submit new quest as a regular user
@bp_usq.route('/user_submit_quest', methods=['GET', 'POST'])
@login_required
def user_submit_quest():
    form = QuestSubmissionForm()
    if form.validate_on_submit():
        
        # Generate random suffix
        suffix_length = 6
        suffix = ''.join(random.choices(string.digits, k=suffix_length))
        # Determine prefix based on language
        if request.form['quest_language'] == 'Python':
            prefix = 'PY-'
        elif request.form['quest_language'] == 'Java':
            prefix = 'JV-'
        elif request.form['quest_language'] == 'JavaScript':
            prefix = 'JS-'
        elif request.form['quest_language'] == 'C#':
            prefix = 'CS-'
        else:
            prefix = 'UNK-'  # Default prefix for unknown languages
        # Construct quest ID
        quest_id = f"{prefix}{suffix}"
        
        # Assing XP points based on difficulty
        xp = 0
        quest_type = ''
        if request.form['quest_difficulty'] == 'Novice Quests':
            xp = 30
            quest_type = 'Basic'
        elif request.form['quest_difficulty'] == 'Adventurous Challenges':
            xp = 60
            quest_type = 'Basic'
        elif request.form['quest_difficulty'] == 'Epic Campaigns':
            xp = 100
            quest_type = 'Basic'
        elif request.form['quest_difficulty'] == 'Abyssal Trials':
            quest_type = 'Advanced'
        
        # Get the current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        new_user_submitted_quest = SubmitedQuest(
            quest_id = quest_id,
            quest_name=form.quest_name.data,
            language=form.quest_language.data,
            difficulty=form.quest_difficulty.data,
            quest_author=current_user.username,
            quest_author_id=current_user.user_id,
            status = 'Pending',
            date_added=current_time,
            last_modified=current_time,
            condition=form.quest_condition.data,
            function_template=form.function_template.data,
            test_inputs=form.quest_inputs.data,
            test_outputs=form.quest_outputs.data,
            unit_tests=form.quest_unitests.data,
            type = quest_type,
            xp = str(xp),
        )
        
        # Increase the user's submited quest count
        current_user.total_submited_quests += 1
        
        db.session.add(new_user_submitted_quest)
        db.session.commit()
        mongo_transaction('user_submitted_quests', action = f'User {current_user.username} submitted a new quest with ID: {quest_id}',
                          user_id = current_user.user_id, username = current_user.username, timestamp = current_time)
        flash('Your quest has been submitted successfully!', 'success')
        return redirect(url_for('main.main_page'))
    else:
        flash('Quest submission failed! Check the fields and try again', 'danger')
        return render_template('user_submit_quest.html', form=form)

# Route to Approve the Submited Quest to the database class Quests
@bp_usq.route('/approve_quest/<quest_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def approve_submited_quest(quest_id):
    form = QuestApprovalForm()
    quest = SubmitedQuest.query.get_or_404(quest_id)
    quest_author = User.query.filter_by(username=form.submited_quest_author.data).first()
    
    if request.method == 'POST':
        action = ''
        if 'approve' in request.form:
            action = 'approve'
        elif 'request_changes' in request.form:
            action = 'request_changes'
        elif 'reject' in request.form:
            action = 'reject'
            
    if form.validate_on_submit():
        if action == 'approve':
            quest.status = 'Approved'
            # Assing XP points based on difficulty
            xp = 0
            type = ''
            if request.form['submited_quest_difficulty'] == 'Novice Quests':
                xp = 30
                type = 'Basic'
            elif request.form['submited_quest_difficulty'] == 'Adventurous Challenges':
                xp = 60
                type = 'Basic'
            elif request.form['submited_quest_difficulty'] == 'Epic Campaigns':
                xp = 100
                type = 'Basic'
        
            # Get the current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            approved_quest = Quest.query.filter_by(quest_id=form.submited_quest_id.data).first()
            if approved_quest:
                flash('Quest already exists in the database.', 'danger')
                return redirect(url_for('usq.open_submited_quest', quest_id=quest_id))
            new_quest = Quest(
                quest_id=form.submited_quest_id.data,
                language=form.submited_quest_language.data,
                difficulty=form.submited_quest_difficulty.data,
                quest_name=form.submited_quest_name.data,
                quest_author=quest_author.username,
                date_added=form.submited_quest_date_added.data,
                last_modified=current_time,
                condition=form.submited_quest_condition.data,
                function_template=form.submited_function_template.data,
                unit_tests=form.submited_quest_unitests.data,
                test_inputs=form.submited_quest_inputs.data,
                test_outputs=form.submited_quest_outputs.data,
                xp=str(xp),
                type=type
            )
            quest_author.total_approved_submited_quests += 1
            
            achievement = Achievement.query.filter(
                Achievement.achievement_name=="Skill Forge Contributor", 
                Achievement.quests_number_required==quest_author.total_approved_submited_quests).all()

            if achievement:
                achievement_id = Achievement.query.filter(Achievement.achievement_id == achievement[0].achievement_id).first().achievement_id
                # Generate random suffix
                suffix_length = 16
                suffix = ''.join(random.choices(string.digits, k=suffix_length))
                prefix = 'USR-ACHV-'
                user_achievement_id = f"{prefix}{suffix}"
                while UserAchievement.query.filter_by(user_achievement_id=user_achievement_id).first():
                    # If it exists, generate a new submission_id
                    suffix = ''.join(random.choices(string.digits, k=suffix_length))
                    user_achievement_id = f"{prefix}{suffix}"
                user_achievement = UserAchievement(user_achievement_id=user_achievement_id, 
                                                   user_id=quest_author.user_id,
                                                   username=quest_author.username,
                                                   achievement_id=achievement_id, 
                                                   earned_on=current_time)
                db.session.add(user_achievement)
            
            db.session.add(new_quest)
            send_quest_approved_email(quest_author.email, quest_author.username, quest.quest_name, quest.language, quest.quest_id)
            mongo_transaction('user_submited_approved_quests', action=f'Quest {quest.quest_name} has been approved by {current_user.username}', user_id=current_user.user_id, username=current_user.username, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            flash('Quest approved successfully.', 'success')
        elif action == 'reject':
            quest.status = 'Rejected'
            quest_author.total_rejected_submited_quests += 1
            send_quest_rejected_email(quest_author.email, quest_author.username, quest.quest_name, quest.language)
            mongo_transaction('user_submited_rejected_quests', 
                              action=f'Quest {quest.quest_name} has been rejected by {current_user.username}', 
                              user_id=current_user.user_id, username=current_user.username, 
                              timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            flash('Quest rejected.', 'danger')
        elif action == 'request_changes':
            print("I want changes!")
            quest.status = 'Pending'
            comments = form.request_changes_comment.data
            send_quest_changes_requested_email(quest_author.email, quest_author.username, quest.quest_name, quest.language, comments)
            mongo_transaction('user_submited_changes_requested', 
                              action=f'Changes requested for quest {quest.quest_name} by {current_user.username}', 
                              user_id=current_user.user_id, username=current_user.username, 
                              timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            flash('Changes requested for the quest.', 'warning')
        db.session.commit()
        return redirect(url_for('usr.open_admin_panel'))
    flash('ERROR!', 'error')
    print(f'Form Errors: {form.errors}')
    return redirect(url_for('usr.open_admin_panel'))

# Post new comment in comments sections
@bp_usq.route('/post_comment', methods=['POST'])
@login_required
def post_comment():
    submited_quest_id = request.form.get('submited_quest_id')
    all_comments = json.loads(request.form.get('submited_quest_comments'))
    comment = request.form.get('submited_quest_comment')
    user_id = current_user.user_id
    user_role = current_user.user_role
    username = current_user.username
    user_avatar = base64.b64encode(current_user.avatar).decode('utf-8')
    # Get the current time
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    created_at = current_time
    
    current_quest = SubmitedQuest.query.filter_by(quest_id=submited_quest_id).first()
    data = {
        'username': username, 
        'user_id': user_id, 
        'user_role': user_role, 
        'user_avatar': user_avatar, 
        'posted_at': created_at, 
        'comment': comment}
    
    all_comments.append(data)
    current_quest.comments = all_comments
    
    db.session.commit()
    
    return redirect(url_for('usq.open_submited_quest', 
                            quest_id=submited_quest_id,
                           submited_quest=current_quest, 
                           user_role=user_role, 
                           user_id=user_id))
    
# Route to open submited quest for editing as regular user
@bp_usq.route('/edit_submited_quest/<quest_id>', methods=['GET'])
@login_required
def open_submited_quest_as_user(quest_id):
    submited_quest = SubmitedQuest.query.filter_by(quest_id=quest_id).first_or_404()
    
    # Throw 404 error if the user is not the author of the quest OR the user is not an admin
    if current_user.username != submited_quest.quest_author and current_user.user_role != 'Admin':
        abort(404)
    
    form = QuestApprovalForm()
    
    try:
        if form.validate_on_submit():
            form.submited_quest_id.data = quest_id
            form.submited_quest_name.data = submited_quest.quest_name
            form.submited_quest_language.data = submited_quest.language
            form.submited_quest_difficulty.data = submited_quest.difficulty
            form.submited_quest_author.data = submited_quest.quest_author
            form.submited_quest_date_added.data = submited_quest.date_added
            form.submited_quest_condition.data = submited_quest.condition
            form.submited_function_template.data = submited_quest.function_template
            form.submited_quest_unitests.data = submited_quest.unit_tests
            form.submited_quest_inputs.data = submited_quest.test_inputs
            form.submited_quest_outputs.data = submited_quest.test_outputs
    except:
        flash('Quest update failed! Check the fields and try again', 'danger')
        return render_template('edit_submited_quest_as_user.html', 
                               submited_quest=submited_quest,
                               form=form)
    
    return render_template('edit_submited_quest_as_user.html', 
                           submited_quest=submited_quest,
                           form=form)
    
# Route to update the submited quest as regular user
@bp_usq.route('/update_submited_quest/<quest_id>', methods=['POST'])
def update_submited_quest(quest_id):
    form = QuestApprovalForm()
    quest_id = form.submited_quest_id.data
    submited_quest = SubmitedQuest.query.filter_by(quest_id=quest_id).first()
    
    # Check if the quest is pending
    if submited_quest.status != 'Pending':
        flash('You can only edit pending quests!', 'danger')
        return redirect(url_for('main.main_page'))
    
    try:
        if form.validate_on_submit():
            submited_quest.quest_name = form.submited_quest_name.data
            submited_quest.language = form.submited_quest_language.data
            submited_quest.difficulty = form.submited_quest_difficulty.data
            submited_quest.condition = form.submited_quest_condition.data
            submited_quest.function_template = form.submited_function_template.data
            submited_quest.unit_tests = form.submited_quest_unitests.data
            submited_quest.test_inputs = form.submited_quest_inputs.data
            submited_quest.test_outputs = form.submited_quest_outputs.data
            submited_quest.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            db.session.commit()
            flash('Quest updated successfully!', 'success')
            return redirect(url_for('usq.open_submited_quest_as_user', quest_id=quest_id))
    except:
        flash('Quest update failed! Check the fields and try again', 'danger')
        return render_template('edit_submited_quest_as_user.html', 
                               submited_quest=submited_quest,
                               form=form)
    else:
        flash('Quest update failed! Check the fields and try again', 'danger')
        return render_template('edit_submited_quest_as_user.html', 
                               submited_quest=submited_quest,
                               form=form)
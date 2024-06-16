import random, string, base64, json, os
from datetime import datetime
from flask import Blueprint, redirect, url_for, request, render_template, jsonify, flash, session
from flask_login import login_required, current_user
# Import the forms and models
from app.models import Quest, ReportedQuest, User, SubmitedSolution, UserAchievement, Achievement
from app.forms import QuestForm, PublishCommentForm, EditQuestForm
# Import code runners
from app.code_runners import run_python, run_javascript, run_java, run_csharp
# Import the database instance
from app.database.db_init import db
# Import MongoDB transactions functions
from app.database.mongodb_transactions import mongo_transaction

bp_qst = Blueprint('quests', __name__)

# Create a new quest as admin
@bp_qst.route('/submit_quest', methods=['GET', 'POST'])
@login_required
def submit_quest():
    create_quest_post = QuestForm()
    if create_quest_post.validate_on_submit():
        # Generate random suffix
        suffix_length = 6
        suffix = ''.join(random.choices(string.digits, k=suffix_length))
        # Determine prefix based on language
        prefix_mapping = {
            'Python': 'PY-',
            'Java': 'JV-',
            'JavaScript': 'JS-',
            'C#': 'CS-'
        }
        quest_language = create_quest_post.quest_language.data
        prefix = prefix_mapping.get(quest_language, 'UNK-')
        # Construct quest ID
        quest_id = f"{prefix}{suffix}"
        
        # Assign XP points based on difficulty
        selected_difficulty = create_quest_post.quest_difficulty.data
        xp_mapping = {
            'Novice Quests': 30,
            'Adventurous Challenges': 60,
            'Epic Campaigns': 100
        }
        xp = xp_mapping.get(selected_difficulty, 0)
        type = 'Basic'
        
        # Create a new Quest object
        new_quest = Quest(
            quest_id=quest_id,
            language=create_quest_post.quest_language.data,
            difficulty=create_quest_post.quest_difficulty.data,
            quest_name=create_quest_post.quest_name.data,
            quest_author=current_user.username,
            date_added=datetime.now(),
            last_modified=datetime.now(),
            condition=create_quest_post.quest_condition.data,
            function_template=create_quest_post.function_template.data,
            unit_tests=create_quest_post.quest_unitests.data,
            test_inputs=create_quest_post.quest_inputs.data,
            test_outputs=create_quest_post.quest_outputs.data,
            type=type,
            xp=str(xp)
        )

        # Add the new quest to the database session
        db.session.add(new_quest)
        db.session.commit()
        mongo_transaction('quests_created', 
                          action=f'User {current_user.username} created a new quest {quest_id}-{create_quest_post.quest_name}',                
                          user_id=current_user.user_id, 
                          username=current_user.username, 
                          timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        flash('Quest submitted successfully!', 'success')
        return redirect(url_for('usr.open_admin_panel'))

    flash('Quest submission unsuccessful!', 'error')
    return redirect(url_for('usr.open_admin_panel'))

# Post new comment in comments sections
@bp_qst.route('/quest_post_comment/<quest_id>', methods=['POST'])
@login_required
def quest_post_comment(quest_id):
    username = current_user.username
    user_id = current_user.user_id
    user_role = current_user.user_role
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get the quest from the database
    quest_post_form = PublishCommentForm()
    if quest_post_form.validate_on_submit():
        comment = quest_post_form.comment.data
        # Append the new comment to the quest's comments list
        data = {
            'username': username,
            'user_id': user_id,
            'user_role': user_role,
            'posted_at': current_time,
            'comment': comment
            }
        quest = Quest.query.filter_by(quest_id=quest_id).first()
        all_quest_comments = list(quest.quest_comments)
        all_quest_comments.append(data)
        quest.quest_comments = all_quest_comments
        # Commit the changes to the database
        db.session.commit()
        mongo_transaction('quests_comments',
                          action=f'User {username} posted a comment on quest {quest_id}',
                          user_id=user_id,
                          username=username,
                          timestamp=current_time)
        # Redirect to the quest page
        flash('Comment posted successfully!', 'success')
        return redirect(url_for('quests.open_curr_quest', 
                                quest_id=quest_id,
                                user_role=user_role,
                                user_id=user_id,
                                form=quest_post_form))
    else:
        quest_id = quest_post_form.quest_id.data
        user_role = current_user.user_role
        user_id = current_user.user_id
        flash('Comment posting unsuccessful!', 'error')
        return redirect(url_for('quests.open_curr_quest', 
                                quest_id=quest_id,
                                user_role=user_role,
                                user_id=user_id,
                                form=quest_post_form))

# Delete comment from the comments section (Admin role is required)
@bp_qst.route('/delete_comment', methods=['POST'])
@login_required
def delete_comment():
    quest_id = request.form.get('quest_id')
    comment_index = int(request.form.get('comment_index'))
    # Get the quest from the database
    quest = Quest.query.filter_by(quest_id=quest_id).first()
    quest_comment = quest.quest_comments[comment_index]
    reversed_comments = list(reversed(quest.quest_comments))
    if quest:
        if 0 <= comment_index < len(quest.quest_comments):
            reversed_comments.pop(comment_index)
            reversed_comments = list(reversed(reversed_comments))
            quest.quest_comments = reversed_comments
            db.session.commit()
            mongo_transaction('quest_comments',
                              action=f'User {current_user.username} deleted a comment on quest {quest_id}',
                              user_id=current_user.user_id,
                              username=current_user.username,
                              timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            return redirect(url_for('quests.open_curr_quest', quest_id=quest_id))
    else:
        print("Error: Comment could not be deleted."), 404


# Handle quest edit from the Admin Panel
@bp_qst.route('/edit_quest_db', methods=['GET', 'POST'])
def edit_quest_db():
    form = EditQuestForm()
    print("Calling the update quest function!")
    if request.method == 'POST':
        if form.validate_on_submit():
            quest_id = form.quest_id.data
            quest = Quest.query.get(quest_id)
            reported_quest = ReportedQuest.query.filter_by(quest_id=quest_id).first()

            if quest:
                quest.quest_name = form.quest_name.data
                quest.language = form.quest_language.data
                quest.difficulty = form.quest_difficulty.data
                quest.condition = form.quest_condition.data
                quest.function_template = form.function_template.data
                quest.unit_tests = form.quest_unitests.data
                quest.test_inputs = form.quest_test_inputs.data
                quest.test_outputs = form.quest_test_outputs.data

                # Change the XP points based on difficulty
                selected_difficulty = form.quest_difficulty.data
                xp_mapping = {
                    'Novice Quests': 30,
                    'Adventurous Challenges': 60,
                    'Epic Campaigns': 100
                }
                xp = xp_mapping.get(selected_difficulty, 0)
                quest.xp = str(xp)

                if form.progress_option.data:
                    report_progress = form.progress_option.data
                    reported_quest.report_status = report_progress
                    if report_progress == 'Resolved':
                        db.session.delete(reported_quest)
                        quest.is_active = True
                        mongo_transaction('quests_resolved',
                                          action=f'User {current_user.username} resolved quest {quest_id}',
                                          user_id=current_user.user_id,
                                          username=current_user.username,
                                          timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))                                         

                db.session.commit()
                mongo_transaction('quests_edited',
                                  action=f'User {current_user.username} edited quest {quest_id}',
                                  user_id=current_user.user_id,
                                  username=current_user.username,
                                  timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                return redirect(url_for('usr.open_admin_panel'))
            else:
                flash('Quest not found!', 'danger')
                return render_template('edit_quest.html', form=form), 404
        else:
            # If the form is not valid, print the errors for debugging
            print(form.errors)
            flash('Form validation failed!', 'danger')
    return render_template('edit_quest.html', form=form)



# Open Quest for editing from the Admin Panel
@login_required
@bp_qst.route('/edit_quest/<quest_id>', methods=['GET'])
def open_edit_quest(quest_id):
    edit_quest_form = EditQuestForm()
    # Retrieve the specific quest from the database, based on the quest_id
    quest = Quest.query.get(quest_id)
    if quest:
        edit_quest_form.quest_id.data = quest.quest_id
        edit_quest_form.quest_name.data = quest.quest_name
        edit_quest_form.quest_language.data = quest.language
        edit_quest_form.quest_difficulty.data = quest.difficulty
        edit_quest_form.quest_condition.data = quest.condition
        edit_quest_form.function_template.data = quest.function_template
        edit_quest_form.quest_test_inputs.data = quest.test_inputs
        edit_quest_form.quest_test_outputs.data = quest.test_outputs
        edit_quest_form.quest_unitests.data = quest.unit_tests
        return render_template('edit_quest.html', form=edit_quest_form)
    else:
        flash('Quest not found!', 'danger')
        return redirect(url_for('usr.open_admin_panel')), 404


# Open Reported Quest for editing from the Admin Panel
@login_required
@bp_qst.route('/edit_reported_quest/<report_id>')
def open_edit_reported_quest(report_id):
    reported_quest_form = EditQuestForm()
    reported_quest = ReportedQuest.query.filter_by(report_id=report_id).first()
    quest = Quest.query.get(reported_quest.quest_id)
    if quest:
        reported_quest_form.quest_id.data = quest.quest_id
        reported_quest_form.quest_name.data = quest.quest_name
        reported_quest_form.quest_language.data = quest.language
        reported_quest_form.quest_difficulty.data = quest.difficulty
        reported_quest_form.quest_condition.data = quest.condition
        reported_quest_form.function_template.data = quest.function_template
        reported_quest_form.quest_test_inputs.data = quest.test_inputs
        reported_quest_form.quest_test_outputs.data = quest.test_outputs
        reported_quest_form.quest_unitests.data = quest.unit_tests
        return render_template('edit_reported_quest.html', quest=quest, reported_quest=reported_quest, form=reported_quest_form)
    else:
        flash('Quest not found!', 'danger')
        return redirect(url_for('usr.open_admin_panel')), 404


# Route to handle `Report Quest` Button
@login_required
@bp_qst.route('/report_quest/<curr_quest_id>')
def report_quest(curr_quest_id, report_reason='no reason'):
    request_arguments = dict(request.args)  # This prints {'report_reason': 'some_value'}
    quest = Quest.query.get(curr_quest_id)
    
    # Generate random suffix
    suffix_length = 16
    suffix = ''.join(random.choices(string.digits, k=suffix_length))
    prefix = 'REP-'
    report_id = f"{prefix}{suffix}"
    # Construct quest ID
    while ReportedQuest.query.filter_by(report_id=report_id).first():
        # If it exists, generate a new submission_id
        suffix = ''.join(random.choices(string.digits, k=suffix_length))
        report_id = f"{prefix}{suffix}"
    
    # # Get the current time
    # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save the submission to the database
    new_reported_quest = ReportedQuest(
        quest_id=quest.quest_id,
        report_id=report_id,
        report_status = 'Not Resolved',
        report_user_id = current_user.user_id,
        report_reason = request_arguments['report_reason'],  # This needs to be changed
        admin_assigned = None  # This needs to be changed
    )

    quest.is_active = False

    # Add the new submission to the database session
    db.session.add(new_reported_quest)
    db.session.commit()
    mongo_transaction('quest_reported',
                      action=f'User {current_user.username} reported quest {curr_quest_id}',
                      user_id=current_user.user_id,
                      username=current_user.username,
                      timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return redirect(url_for('quests.open_curr_quest', quest_id=curr_quest_id))


# Redirect to the table with all tasks. Change from template to real page!!!! 
@bp_qst.route('/quests/<language>', methods=['GET'])
@login_required
def open_quests_table(language):
    user_id = current_user.user_id
    # Retrieve all quests from the database
    all_quests = Quest.query.filter(Quest.language == language).all()
    # Retrieve all users from the database
    all_users = User.query.all()
    # Retrieve the submitted solutions from the database
    solved_quests = SubmitedSolution.query.filter_by(user_id=user_id, quest_passed=True).all()
    # Create a set of solved quest IDs for quick lookup
    solved_quest_ids = {solved.quest_id for solved in solved_quests}
    # Annotate each quest with a 'solved' attribute
    for quest in all_quests:
        quest.solved = quest.quest_id in solved_quest_ids
    
    return render_template('quest_table.html', quests=all_quests, users=all_users, solved_quests=solved_quests, language=language) 

# Open Quest for submitting. Change from template to real page!!!!
@bp_qst.route('/quest/<quest_id>', methods=['GET'])
@login_required
def open_curr_quest(quest_id):
    quest_post_form = PublishCommentForm()
    # Retrieve the specific quest from the database, based on the quest_id
    quest = Quest.query.get(quest_id)
    quest_id = quest.quest_id
    user_avatar = base64.b64encode(current_user.avatar).decode('utf-8')
    user_role = current_user.user_role
    return render_template('open_quest.html', 
                           quest=quest,
                           quest_id=quest_id,
                           user_avatar=user_avatar,
                           user_role=user_role,
                           form=quest_post_form)

# Route to handle solution submission
@bp_qst.route('/submit-solution', methods=['POST'])
@login_required
def submit_solution():
    user_id = current_user.user_id
    username = current_user.username
    user_xp_points = current_user.xp
    current_quest_language = request.form.get('quest_language')
    current_quest_type = request.form.get('quest_type')
    current_quest_id = request.form.get('quest_id')
    current_quest_difficulty = request.form.get('quest_difficulty')
    # Handle the simple quests testing
    if current_quest_type == 'Basic':
        user_code = request.form.get('user_code')
        quest_inputs = [eval(x) for x in request.form.get('quest_inputs').split("\r\n")]
        quest_outputs = [eval(x) for x in request.form.get('quest_outputs').split("\r\n")]
        # Handle the code runner exection based on the Quest language
        if current_quest_language == 'Python':
            successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs  = run_python.run_code(user_code, quest_inputs, quest_outputs, user_id, username, current_quest_id)

        elif current_quest_language == 'JavaScript':
            successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs  = run_javascript.run_code(user_code, quest_inputs, quest_outputs, user_id, username, current_quest_id)
                    
        elif current_quest_language == 'Java':
            successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs  = run_java.run_code(user_code, quest_inputs, quest_outputs, user_id, username, current_quest_id)

        elif current_quest_language == 'C#':
            successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs  = run_csharp.run_code(user_code, quest_inputs, quest_outputs, user_id, username, current_quest_id)
        
        # Submit new solution to the database
        quest_id = request.form.get('quest_id')
        user_id = current_user.user_id
        user_code = request.form.get('user_code')
        successful_tests = successful_tests
        unsuccessful_tests = unsuccessful_tests
        quest_passed = True if unsuccessful_tests == 0 else False
        
        # Generate random suffix
        suffix_length = 16
        suffix = ''.join(random.choices(string.digits, k=suffix_length))
        prefix = 'SUB-'
        submission_id = f"{prefix}{suffix}"
        # Construct quest ID
        while SubmitedSolution.query.filter_by(submission_id=submission_id).first():
            # If it exists, generate a new submission_id
            suffix = ''.join(random.choices(string.digits, k=suffix_length))
            submission_id = f"{prefix}{suffix}"
                
        # Check if the user already solved the particular quest and IF NOT add XP points, count the quest and update users stats
        solution = SubmitedSolution.query.filter_by(user_id=user_id, quest_id=quest_id, quest_passed=True).first()
        update_user_stats = False
        if not solution or solution == None:
            update_user_stats = True

        # Save the submission to the database
        new_submission = SubmitedSolution(
            submission_id=submission_id,
            user_id=user_id,
            quest_id=quest_id,
            submission_date=datetime.now(),
            user_code=user_code,
            successful_tests=successful_tests,
            unsuccessful_tests=unsuccessful_tests,
            quest_passed=quest_passed
        )
            
        # Add the new submission to the database session
        db.session.add(new_submission)
        db.session.commit()
        mongo_transaction('quests_solutions',
                          action=f'User {username} submitted a solution for quest {quest_id}',
                          user_id=user_id,
                          username=username,
                          timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Handle the leveling of the user
        # Update succesfully solved quests
        if update_user_stats:
            # Update the quest solved counter if the solution is correct
            current_quest = Quest.query.filter_by(quest_id=quest_id).first()
            current_quest.solved_times += 1
        
            # Update the user stats if the solution is correct
            current_quest_number = 0
            if unsuccessful_tests == 0:
                current_user.total_solved_quests += 1
                if current_quest_language == "Python":
                    current_user.total_python_quests += 1
                    current_quest_number = current_user.total_python_quests
                elif current_quest_language == "JavaScript":
                    current_user.total_javascript_quests += 1
                    current_quest_number = current_user.total_javascript_quests
                elif current_quest_language == "Java":
                    current_user.total_java_quests += 1
                    current_quest_number = current_user.total_java_quests
                elif current_quest_language == "C#":
                    current_user.total_csharp_quests += 1
                    current_quest_number = current_user.total_csharp_quests
                
                # Update the user XP
                if current_quest_difficulty == "Novice Quests":
                    current_user.xp += 30
                elif current_quest_difficulty == "Adventurous Challenges":
                    current_user.xp += 60
                elif current_quest_difficulty == "Epic Campaigns":
                    current_user.xp += 100
            
                # Update the user XP level and rank
                with open(os.path.join('app/static/configs/levels.json'), 'r') as levels_file:
                    leveling_data = json.load(levels_file)
                for level in leveling_data:
                    for level_name, level_stats in level.items():
                        if int(level_stats['min_xp']) <= int(current_user.xp) <= int(level_stats['max_xp']):
                            current_user.level = level_stats['level']
                            current_user.rank = level_name
                            db.session.commit()        
                            break    

            
                # Generate achievement for the user    
                achievement = Achievement.query.filter(
                    Achievement.language == current_quest_language,
                    Achievement.quests_number_required == current_quest_number).all()
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
                        
                    user_achievement = UserAchievement(
                                        user_achievement_id=user_achievement_id,
                                        user_id=user_id,
                                        username=username,
                                        achievement_id=achievement_id,
                                        earned_on=datetime.now())
                    db.session.add(user_achievement)
                    mongo_transaction('user_achievements',
                                      action=f'User {username} earned an achievement {achievement_id}',
                                      user_id=user_id,
                                      username=username,
                                      timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            db.session.commit()

        
        # Return the results of the tests and the final message to the frontend
        return jsonify({
            'successful_tests': successful_tests,
            'unsuccessful_tests': unsuccessful_tests,
            'message': message,
            'zero_test_input': zero_tests[0],
            'zero_test_output': zero_tests[1],
            'zero_test_result': zero_tests_outputs[0],
            'zero_test_error': zero_tests_outputs[1]
        })
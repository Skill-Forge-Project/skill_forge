import os, requests, string, re, random
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, abort, request, flash
from flask_login import login_required, current_user
from app.forms import BossResponseForm
from app.models import Achievement, UserAchievement
# Import MongoDB transactions functions
from app.database.db_init import db
from app.database.mongodb_transactions import mongo_transaction


# Underworld Blueprint
undwrld_bp = Blueprint('undwrld_bp', __name__, template_folder='templates/underworld_realm', static_folder='static/css/underworld_realm')

# Underworld Realm
@undwrld_bp.route('/underworld', methods=['GET'])
@login_required
def open_underworld():
    underworld_status_url = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/"
    try:
        status_response = requests.get(underworld_status_url)
        
        if not status_response.ok:
            abort(404)
        else:
            # Attempt to retrieve bosses from the Underworld Realm service
            all_bosses_url = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/get_all_bosses"
            try:
                response = requests.get(all_bosses_url)
                if response.status_code == 200:
                    bosses = response.json()
                else:
                    bosses = []
                    print(f"Error fetching bosses: {response.status_code}")

            except requests.exceptions.RequestException as e:
                bosses = []
                print(f"Request failed: {e}")
                abort(404)

            return render_template('underworld_realm/underworld.html', title='Underworld Realm', bosses=bosses)

    except requests.exceptions.RequestException as e:
        # Handle any connection error and display the custom 404 page
        print(f"Underworld Realm is unreachable: {e}")
        abort(404)
    
# Update Boss Challenge Status
@undwrld_bp.route('/update_challenge_status', methods=['POST'])
@login_required
def update_challenge_status():
    update_status_url_failed = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/update_challenge_fail"
    data = request.get_json()
    challenge_id = data.get('challenge_id')
    status = data.get('status')
    
    try:
        if challenge_id and status == 'Failed':
            response = requests.post(update_status_url_failed, json={'challenge_id': challenge_id})
            if response.ok:
                flash('Reloading the page during challenge is not allowed!', 'error')
                return redirect(url_for('undwrld_bp.open_underworld'))
            else:
                print(f"Error updating challenge status: {response.status_code}")
                abort(404)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        abort(404)

# Reload the Underworld Realm if the challenge timer is over
@undwrld_bp.route('/challenge_timer_over', methods=['GET','POST'])
@login_required
def challenge_timer_over():
    update_status_url = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/update_challenge_fail"
    try:
        # Extract the challenge_id from the query string
        challenge_id = request.args.get('challenge_id')
        print(challenge_id)
        if not challenge_id:
            flash('Invalid challenge ID!', 'error')
            return redirect(url_for('undwrld_bp.open_underworld'))
        
        response = requests.post(update_status_url, json={'challenge_id': challenge_id})
        if response.ok:
            flash('Your time is over! You have failed the challenge!\nTrain you skills and try again!', 'error')
            return redirect(url_for('undwrld_bp.open_underworld'))
        else:
            print(f"Error updating challenge status: {response.status_code}")
            abort(404)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        abort(404)

# Challenge Boss
@undwrld_bp.route('/challenge_boss/<boss_id>', methods=['GET', 'POST'])
@login_required
def challenge_boss(boss_id):
    boss_details = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/get_boss" 
    
    try:
        # Check if user has already challenged the boss (today)
        check_if_challenge = requests.get(f"{os.getenv('UNDERWORLD_REALM_API_URL')}/check_active_challenge", json={'user_id': current_user.user_id, 'boss_id': boss_id})
        if check_if_challenge.ok:
            flash('You have already challenged this boss! Try again tommorow.', 'info')
            return redirect(url_for('undwrld_bp.open_underworld'))
        
        # Send a GET request to the microservice
        response = requests.get(boss_details, json={'boss_id': boss_id})
        # Check if the request was successful
        if response.ok:
            boss = response.json()
            # Generate new question from the Boss
            question = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/generate_new_question"
            form = BossResponseForm()
            question_request = requests.post(question, json={'boss_id': boss_id,
                                                             "boss_name": boss['boss_name'], 
                                                             "boss_language": boss['boss_language'], 
                                                             "boss_difficulty": boss['boss_difficulty'],
                                                             "boss_specialty": boss['boss_specialty'],
                                                             "boss_description": boss['boss_description'],
                                                             "user_id": current_user.user_id,
                                                             "user_name": current_user.username}).json()
            # Extract the challenge_id from the response
            challenge_id = question_request['challenge_id']
            # If AI generated question contains code, extract it and separate it from the question
            pattern = re.compile(r'```(?:javascript|java|python|csharp)?\s*([\s\S]*?)\s*```')
            try:
                question = question_request['question']
                question_code = pattern.search(question).group(1)
                question = question.replace(f'```python\n{question_code}\n```', '').replace(f'```java\n{question_code}\n```', '').replace(f'```javascript\n{question_code}\n```', '').replace(f'```csharp\n{question_code}\n```', '').strip()                
            except AttributeError:
                question = question_request['question']
                question_code = ''
            language = boss['boss_language']
            if language == 'Python':
                question_language = 'python'
            elif language == 'Java':
                question_language = 'java'
            elif language == 'JavaScript':
                question_language = 'javascript'
            elif language == 'C#':
                question_language = 'csharp'
                
            return render_template('underworld_realm/challenge_boss.html', 
                                   title='Challenge Boss', 
                                   boss=boss, 
                                   form=form, 
                                   question=question,
                                   question_code=question_code,
                                   question_language=question_language,
                                   challenge_id=challenge_id)
        else:
            boss = {}
            print(f"Error fetching boss details: {response.status_code}")
            abort(404)
        return boss
    except requests.exceptions.RequestException as e:
        boss = {}
        abort(404)

# Submit Challenge
@undwrld_bp.route('/submit_challenge', methods=['POST'])
@login_required
def submit_boss_challenge():
    form = BossResponseForm()    
    if form.validate_on_submit():
        # Get the form data
        question = request.form.get('question')
        user_answer = form.user_answer.data
        code_answer = form.code_answer.data
        challenge_id = request.form.get('challenge_id')
        boss_id = request.form.get('boss_id')
        boss_name = request.form.get('boss_name')
        boss_title = request.form.get('boss_title')
        boss_language = request.form.get('boss_language')
        boss_difficulty = request.form.get('boss_difficulty')
        boss_specialty = request.form.get('boss_specialty')
        boss_description = request.form.get('boss_description')
        # Submit the challenge to the Underworld Realm service
        submit_challenge_url = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/evaluate_user_answer"
        try:
            response = requests.post(submit_challenge_url, json={'boss_id': boss_id, 
                                                                 "boss_name": boss_name, 
                                                                 "challenge_id": challenge_id,
                                                                 "user_id": current_user.user_id,
                                                                 "user_name": current_user.username,
                                                                 "boss_language": boss_language, 
                                                                 "boss_difficulty": boss_difficulty,
                                                                 "boss_specialty": boss_specialty,
                                                                 "boss_description": boss_description,
                                                                 "boss_question": question,
                                                                 "user_answer": user_answer,
                                                                 "user_code_answer": code_answer})
            if response.ok:
                # evaluation = response.json()
                evaluation = response.json()

                # Update user's XP points
                current_user.xp_points += int(evaluation["xp_points"])
                            
                # Check if user has completed the Underworld Conqueror achievement
                if evaluation["underworld_achievement"] == True:
                    try:
                        # Generate a new unique achievement ID
                        achievement_id = Achievement.query.filter(Achievement.achievement_name == "Underworld Conqueror").first().achievement_id
                        suffix_length = 16
                        suffix = ''.join(random.choices(string.digits, k=suffix_length))
                        prefix = 'USR-ACHV-'
                        user_achievement_id = f"{prefix}{suffix}"
                        while UserAchievement.query.filter_by(user_achievement_id=user_achievement_id).first():
                        # If it exists, generate a new submission_id
                            suffix = ''.join(random.choices(string.digits, k=suffix_length))
                            user_achievement_id = f"{prefix}{suffix}"
                        # Give user's achievement
                        user_achievement = UserAchievement(
                                            user_achievement_id=user_achievement_id,
                                            user_id=current_user.user_id,
                                            username=current_user.username,
                                            achievement_id=achievement_id,
                                            earned_on=datetime.now())
                        db.session.add(user_achievement)
                        db.session.commit()
                    except Exception as e:
                        print(f"Error giving achievement: {e}.")
                
                # Check if user has completed the Underworld specific boss achievement
                if evaluation["boss_achievement"] == True:
                    try:
                        # Generate a new unique achievement ID
                        achievement_id = Achievement.query.filter(Achievement.achievement_description.like(f'%{boss_name}%')).first().achievement_id
                        suffix_length = 16
                        suffix = ''.join(random.choices(string.digits, k=suffix_length))
                        prefix = 'USR-ACHV-'
                        user_achievement_id = f"{prefix}{suffix}"
                        while UserAchievement.query.filter_by(user_achievement_id=user_achievement_id).first():
                        # If it exists, generate a new submission_id
                            suffix = ''.join(random.choices(string.digits, k=suffix_length))
                            user_achievement_id = f"{prefix}{suffix}"
                        # Give user's achievement
                        user_achievement = UserAchievement(
                                            user_achievement_id=user_achievement_id,
                                            user_id=current_user.user_id,
                                            username=current_user.username,
                                            achievement_id=achievement_id,
                                            earned_on=datetime.now())
                        db.session.add(user_achievement)
                        db.session.commit()
                    except Exception as e:
                        print(f"Error giving achievement: {e}.")
                
                return render_template('underworld_realm/challenge_grade.html', title='Challenge Result', 
                                        boss_name=boss_name, 
                                        boss_description=boss_description,
                                        boss_title=boss_title,
                                        boss_language=boss_language,
                                        boss_specialty=boss_specialty,
                                        boss_difficulty=boss_difficulty,
                                        evaluation=evaluation["evaluation"],
                                        feedback=evaluation["feedback"],
                                        xp_points=evaluation["xp_points"],)
            else:
                print(f"Error submitting challenge: {response.status_code} for challenge ID: {challenge_id}")
                abort(404)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Challenge ID: {challenge_id}")
            abort(404)
    return redirect(url_for('undwrld_bp.open_underworld'))
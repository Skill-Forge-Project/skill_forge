import os, requests
from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required
from app.forms import BossResponseForm
# Import MongoDB transactions functions
from app.database.mongodb_transactions import mongo_transaction


# Underworld Blueprint
undwrld_bp = Blueprint('undwrld_bp', __name__, template_folder='templates/underworld_realm', static_folder='static/css/underworld_realm')

# Underworld Realm
@undwrld_bp.route('/underworld')
@login_required
def open_underworld():
    underworld_status_url = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/"
    try:
        status_response = requests.get(underworld_status_url)
        
        if status_response.status_code != 200:
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
    


# Challenge Boss
@undwrld_bp.route('/challenge_boss/<boss_id>')
@login_required
def challenge_boss(boss_id):
    boss_details = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/get_boss" 
    try:
        # Send a GET request to the microservice
        response = requests.get(boss_details, json={'boss_id': boss_id})
        # Check if the request was successful
        if response.status_code == 200:
            boss = response.json()
            # Generate new question from the Boss
            question = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/generate_new_question"
            form = BossResponseForm()
            # question_response = requests.post(question, json={'boss_id': boss_id, 
            #                                                  "boss_name": boss['boss_name'], 
            #                                                  "boss_language": boss['boss_language'], 
            #                                                  "boss_difficulty": boss['boss_difficulty'],
            #                                                  "boss_specialty": boss['boss_specialty'],
            #                                                  "boss_description": boss['boss_description']}).json()
            # question=question_response['question']
            return render_template('underworld_realm/challenge_boss.html', title='Challenge Boss', boss=boss, form=form)
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
        boss_id = form.boss_id.data
        boss_name = form.boss_name.data
        boss_language = form.boss_language.data
        boss_difficulty = form.boss_difficulty.data
        boss_specialty = form.boss_specialty.data
        boss_description = form.boss_description.data
        question = form.question.data
        answer = form.answer.data
        user_answer = form.user_answer.data
        # Submit the challenge to the Underworld Realm service
        submit_challenge_url = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/submit_challenge"
        try:
            response = requests.post(submit_challenge_url, json={'boss_id': boss_id, 
                                                                 "boss_name": boss_name, 
                                                                 "boss_language": boss_language, 
                                                                 "boss_difficulty": boss_difficulty,
                                                                 "boss_specialty": boss_specialty,
                                                                 "boss_description": boss_description,
                                                                 "question": question,
                                                                 "answer": answer,
                                                                 "user_answer": user_answer})
            if response.status_code == 200:
                result = response.json()
                return render_template('underworld_realm/challenge_result.html', title='Challenge Result', result=result)
            else:
                print(f"Error submitting challenge: {response.status_code}")
                abort(404)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            abort(404)
    return redirect(url_for('undwrld_bp.open_underworld'))
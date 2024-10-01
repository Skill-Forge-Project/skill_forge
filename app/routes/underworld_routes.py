import os, requests
from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required
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
    print(f"Boss details URL: {boss_details}")
    try:
        # Send a GET request to the microservice
        response = requests.get(boss_details, json={'boss_id': boss_id})
        # Check if the request was successful
        if response.status_code == 200:
            boss = response.json()
            # Generate new question from the Boss
            question = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/generate_new_question"
            question_response = requests.post(question, json={'boss_id': boss_id, 
                                                             "boss_name": boss['boss_name'], 
                                                             "boss_language": boss['boss_language'], 
                                                             "boss_difficulty": boss['boss_difficulty'],
                                                             "boss_specialty": boss['boss_specialty'],
                                                             "boss_description": boss['boss_description']}).json()
            return render_template('underworld_realm/challenge_boss.html', title='Challenge Boss', boss=boss, question=question_response['question'])
        else:
            boss = {}
            print(f"Error fetching boss details: {response.status_code}")
            abort(404)
        return boss
    except requests.exceptions.RequestException as e:
        boss = {}
        abort(404)
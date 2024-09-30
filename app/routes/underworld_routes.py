import os, requests
from flask import Blueprint, render_template
from flask_login import login_required
# Import MongoDB transactions functions
from app.database.mongodb_transactions import mongo_transaction


# Underworld Blueprint
undwrld_bp = Blueprint('undwrld_bp', __name__, template_folder='templates/underworld_realm', static_folder='static/css/underworld_realm')

# Underworld Realm
@undwrld_bp.route('/underworld')
@login_required
def open_underworld():
    all_boses = f"{os.getenv('UNDERWORLD_REALM_API_URL')}/get_all_bosses"
    try:
        # Send a GET request to the microservice
        response = requests.get(all_boses)
        # Check if the request was successful
        if response.status_code == 200:
            bosses = response.json()  # Parse JSON response
        else:
            bosses = []  # Handle error or empty case
            print(f"Error fetching bosses: {response.status_code}")
    except requests.exceptions.RequestException as e:
        bosses = []  # Handle exception case
        print(f"Request failed: {e}")
    
    return render_template('underworld_realm/underworld.html', title='Underworld Realm', bosses=bosses)
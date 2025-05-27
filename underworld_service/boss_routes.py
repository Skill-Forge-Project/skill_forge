import io
from flask import Blueprint, request, jsonify, send_file
from extensions import db
from services import token_required
from sqlalchemy import text
from models import Boss
from genai_client import generate_underworld_challenge

boss_routes = Blueprint('boss_routes', __name__)

# Get all bosses
@boss_routes.route('/bosses', methods=['GET'])
@token_required
def get_bosses():
    """
    Get all bosses from the database.
    
    Returns:
        JSON response with the list of bosses.
    """
    query = text("SELECT * FROM bosses")
    result = db.session.execute(query).mappings().all()
    bosses = [dict(row) for row in result]
    return jsonify(bosses), 200

# Get a specific boss by ID
@boss_routes.route('/bosses/<string:boss_id>', methods=['GET'])
@token_required
def get_boss(boss_id):
    """
    Get a specific boss by ID.
    
    Args:
        boss_id (str): The ID of the boss to retrieve.
    
    Returns:
        JSON response with the boss details or an error message if not found.
    """
    query = text("SELECT * FROM bosses WHERE id = :boss_id")
    result = db.session.execute(query, {'boss_id': boss_id})
    boss = result.fetchone()

    if boss is None:
        return jsonify({"error": "Boss not found"}), 404
    
    return jsonify(
        {
            "boss_id": boss.id,
            "boss_name": boss.boss_name,
            "boss_title": boss.boss_title,
            "boss_language": boss.boss_language,
            "boss_difficulty": boss.boss_difficulty,
            "boss_specialty": boss.boss_specialty,
            "boss_description": boss.boss_description,
        }), 200

# Create a new boss
@boss_routes.route('/bosses', methods=['POST'])
@token_required
def create_boss():
    """
    Create a new boss in the database.
    
    Returns:
        JSON response with the created boss details or an error message.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    try:
        new_boss = Boss(
            boss_name=data['boss_name'],
            boss_title=data['boss_title'],
            boss_language=data['boss_language'],
            boss_difficulty=data['boss_difficulty'],
            boss_specialty=data['boss_specialty'],
            boss_description=data.get('boss_description')
        )
        
        db.session.add(new_boss)
        db.session.commit()
        
        return jsonify({"message": "Boss created successfully", "boss_id": new_boss.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Generate Underworld challenge for a specific boss
@boss_routes.route('/bosses/<string:boss_id>/challenge', methods=['POST'])
@token_required
def generate_challenge(boss_id):
    """
    Generate an Underworld challenge for a specific boss.
    
    Args:
        boss_id (str): The ID of the boss for which to generate the challenge.
    
    Returns:
        JSON response with the generated challenge or an error message.
    """
    
    if boss_id is None:
        return jsonify({"error": "Boss not found"}), 404
    
    challenge = generate_underworld_challenge(boss_id)
    
    return jsonify(challenge), 200
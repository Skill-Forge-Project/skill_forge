import os
from flask import Blueprint, request, jsonify, send_file
from extensions import db
from services import internal_only
from sqlalchemy import text

users_progress = Blueprint("progress", __name__)

@users_progress.route("/users/<user_id>/xp", methods=["PUT"])
@internal_only
def update_user_xp(user_id):
    """Update user XP points by user id.
    
    return: json object with updated user XP points
    """
    
    data = request.get_json()
    xp_points = data.get("xp_points")

    if xp_points is None:
        return jsonify({"error": "xp_points is required"}), 400

    query = text("""
        UPDATE users 
        SET xp_points = xp_points + :xp_points 
        WHERE id = :user_id
    """)
    
    db.session.execute(query, {"xp_points": xp_points, "user_id": user_id})
    db.session.commit()

    return jsonify({"message": "User XP points updated successfully"}), 200

@users_progress.route("/users/<user_id>/quests", methods=["PUT"])
@internal_only
def update_user_quests(user_id):
    """Update user solved quests by user id.
    
    return: json object with updated user quests
    """
    
    data = request.get_json()
    completed_quests = data.get("completed_quests")

    if not completed_quests:
        return jsonify({"error": "completed_quests is required"}), 400

    query = text("""
        UPDATE users 
        SET completed_quests = :completed_quests 
        WHERE id = :user_id
    """)
    
    db.session.execute(query, {"completed_quests": completed_quests, "user_id": user_id})
    db.session.commit()

    return jsonify({"message": "User quests updated successfully"}), 200
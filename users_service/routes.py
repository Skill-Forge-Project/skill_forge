import io
from flask import Blueprint, request, jsonify, send_file
from extensions import db
from services import token_required
from sqlalchemy import text

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["GET"])
@token_required
def get_all_users():
    """Get all users from database with their attributes.
    
    return: json object with all users and their attributes
    """

    query = text("""
        SELECT 
            id, 
            user_role, 
            username, 
            first_name,
            last_name,
            email, 
            user_online_status,
            last_seen_date,
            xp_points, 
            level ,
            rank
        FROM users
    """)
    result = db.session.execute(query).fetchall()

    users = []
    for row in result:
        user_dict = dict(row._mapping)
        users.append(user_dict)

    return jsonify(users)

@users_bp.route("/users/<user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    """Get user by id from database with their attributes.
    
    return: json object with user and their attributes
    """

    query = text("""
        SELECT 
            id, 
            user_role, 
            username, 
            first_name,
            last_name,
            email, 
            about_me,
            user_online_status,
            registration_date,
            last_seen_date,
            xp_points, 
            level ,
            rank,
            facebook_profile,
            instagram_profile,
            github_profile,
            discord_id,
            linked_in
            total_solved_quests,
            total_python_quests,
            total_java_quests,
            total_javascript_quests,
            total_csharp_quests,
            total_submited_quests,
            total_approved_submited_quests,
            total_rejected_submited_quests
        FROM users
        WHERE id = :user_id
    """)
    result = db.session.execute(query, {"user_id": user_id}).fetchone()

    if result is None:
        return jsonify({"error": "User not found"}), 404

    user_dict = dict(result._mapping)

    return jsonify(user_dict)

@users_bp.route("/users/<user_id>/avatar", methods=["GET"])
@token_required
def get_user_avatar(user_id):
    """Get user avatar by id from database.

    Args:
        user_id (str): The ID of the user whose avatar is to be retrieved.

    Returns:
        json: json object with user avatar
    """
    user = db.session.execute(
        text("SELECT avatar FROM users WHERE id = :user_id"),
        {"user_id": user_id}
    ).mappings().fetchone()

    if user is None or user["avatar"] is None:
        return jsonify({"message": "Avatar not found"}), 404

    return send_file(
        io.BytesIO(user["avatar"]),
        mimetype="image/png",
    )


@users_bp.route("/ban_user/<user_id>", methods=["PUT"])
@token_required
def ban_user():
    """Ban user by id from database.

    Args:
        user_id (str): The ID of the user to be banned.

    Returns:
        json: json object with user ban status
    """
    user_id = request.args.get("user_id, ban_reason")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    query = text("""
        UPDATE users
        SET is_banned = TRUE
        SET ban_reson: reason
        WHERE id = :user_id
    """)
    db.session.execute(query, {"user_id": user_id})
    db.session.commit()

    return jsonify({"message": "User banned successfully"}), 204

@users_bp.route("/unban_user/<user_id>", methods=["PUT"])
@token_required
def unban_user():
    """Unban user by id from database.

    Args:
        user_id (str): The ID of the user to be unbanned.

    Returns:
        json: json object with user unban status
    """
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    query = text("""
        UPDATE users
        SET is_banned = FALSE
        SET ban_reason = ""
        WHERE id = :user_id
    """)
    db.session.execute(query, {"user_id": user_id})
    db.session.commit()

    return jsonify({"message": "User unbanned successfully"}), 204

@users_bp.route("/update_user/<user_id>", methods=["PUT"])
@token_required
def update_user(user_id):
    """Update user by id from database."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    query = text("""
        UPDATE users
        SET first_name = :first_name,
            last_name = :last_name,
            email = :email,
            about_me = :about_me,
            facebook_profile = :facebook_profile,
            instagram_profile = :instagram_profile,
            github_profile = :github_profile,
            discord_id = :discord_id,
            linked_in = :linked_in
        WHERE id = :user_id
    """)
    db.session.execute(query, {**data, "user_id": user_id})
    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200

@users_bp.route("/update_user/<user_id>/avatar", methods=["PUT"])
@token_required
def update_user_avatar(user_id):
    """Update user avatar by id from database."""
    if "avatar" not in request.files:
        return jsonify({"error": "No selected file"}), 400

    file = request.files["avatar"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    avatar = file.read()

    query = text("""
        UPDATE users
        SET avatar = :avatar
        WHERE id = :user_id
    """)
    db.session.execute(query, {"avatar": avatar, "user_id": user_id})
    db.session.commit()

    return jsonify({"message": "Avatar updated successfully"}), 200
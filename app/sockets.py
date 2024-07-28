from flask_socketio import emit, disconnect
from flask_login import current_user
from flask import request
from datetime import datetime
from app.models import User
from app.database.db_init import db
from app import socketio as socketio

# Define the function to update the user status
def update_user_status(user_id, status):
    user = User.query.filter(User.user_id == user_id).first()
    if user:
        user.user_online_status = status
        user.last_status_update = datetime.now()
        db.session.commit()
 
# Define the event handlers               
@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        user_id = current_user.user_id
        update_user_status(user_id, 'Online')
        emit('status_update', {'status': 'Online', 'user': current_user.username}, broadcast=True)
    else:
        disconnect()

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        user_id = current_user.user_id
        update_user_status(user_id, 'Offline')
        emit('status_update', {'status': 'Offline', 'user': current_user.username}, broadcast=True)
  
# Define the event handler for the status update request        
@socketio.on('status_update_request')
def handle_status_update_request(data):
    if current_user.is_authenticated:
        status = data.get('status', 'Offline')
        update_user_status(current_user.user_id, status)
        emit('status_update', {'status': status, 'user': current_user.username}, broadcast=True)
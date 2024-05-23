from flask_socketio import emit
from flask_login import current_user
from flask import request
from datetime import datetime
from app.models import User
from app.database.db_init import db
from app import socketio as socketio

def update_user_status(user_id, status):
    user = User.query.filter(User.user_id == user_id).first()
    current_time = datetime.now()
    if user:
        user.user_online_status = status
        user.last_status_update = current_time
        db.session.commit()

@socketio.on('connect')
def handle_connect(auth):
    if current_user.is_authenticated:
        user_id = current_user.user_id
        update_user_status(user_id, 'Online')
        emit('status_update', {'user_id': user_id, 'status': 'Online'}, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    print('User disconnected')
    if current_user.is_authenticated:
        user_id = current_user.user_id
        update_user_status(user_id, 'Offline')
        emit('status_update', {'user_id': user_id, 'status': 'Offline'}, broadcast=True)

@socketio.on('heartbeat')
def handle_heartbeat(data):
    user_id = data.get('user_id')
    if user_id and current_user.is_authenticated:
        update_user_status(user_id, 'Online')
        emit('status_update', {'user_id': user_id, 'status': 'Online'}, broadcast=True)

@socketio.on('request_user_status')
def handle_request_user_status(data):
    user_id = data.get('user_id')
    user = User.query.filter(User.user_id == user_id).first()
    if user:
        emit('current_user_status', {'status': user.user_online_status}, room=request.sid)
# Import connection to primary MongoDB node
from app.database.mongodb_init import mongo1_db, mongo1_client
# Import connection to secondary MongoDB node
from app.database.mongodb_init import mongo2_db, mongo2_client

# Create a transaction for inserting a log entry in the userLogins or userLoggouts collection
def session_transaction(collection, user_id, username, timestamp):
    user_logins_collection = mongo1_db[f'{collection}']
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            user_logins_collection.insert_one({'user_id': user_id, 'username': username, 'timestamp': timestamp}, session=session)
            session.commit_transaction()
        except Exception as e:
            print(f'Error while inserting log entry in userLogin collection for user: {username}, Error: {e}')
            session.abort_transaction()
            return False


# Create a transaction for inserting a log entry in the userRegister collection
def user_register_transaction(collection, user_id, username, timestamp):
    user_register_collection = mongo2_db[f'{collection}']
    session = mongo2_client.start_session()
    with session.start_transaction():
        try:
            user_register_collection.insert_one({'user_id': user_id, 'username': username, 'timestamp': timestamp}, session=session)
            session.commit_transaction()
        except Exception as e:
            print(f'Error while inserting log entry in userRegister collection for user: {username}, Error: {e}')
            session.abort_transaction()
            return False
        

# Create a transaction for inserting a log entry in questCreate collection
def new_quest_transaction(collection, user_id, username, quest_id, quest_name, quest_author, timestamp):
    new_quest_collection = mongo1_db[f'{collection}']
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            new_quest_collection.insert_one({'user_id': user_id, 
                                             'username': username, 
                                             'quest_id': quest_id, 
                                             'quest_name': quest_name,
                                             'quest_author': quest_author,
                                             'timestamp': timestamp}, 
                                            session=session)
            session.commit_transaction()
        except Exception as e:
            print(f'Error while inserting log entry in newQuest collection for quest: {quest_id}-{quest_name}, Error: {e}')
            session.abort_transaction()
            return False
# Import connection to primary MongoDB node
from app.database.mongodb_init import mongo1_db, mongo1_client
# Import connection to secondary MongoDB node
from app.database.mongodb_init import mongo2_db, mongo2_client

# Create a transaction for inserting a log entry in the userLogins or userLoggouts collection
def mongo_transaction(collection_name, **kwargs):
    collection = mongo1_db[collection_name]
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            collection.insert_one(
                {
                    'action': kwargs['action'],
                    'user_id': kwargs['user_id'], 
                    'username': kwargs['username'], 
                    'timestamp': kwargs['timestamp'],
                }, 
                session=session)
            session.commit_transaction()
            session.end_session()
        except Exception as e:
            print(f'Error while inserting log entry in {collection} collection for user: {kwargs["username"]}, Error: {e}')
            session.abort_transaction()
            return False
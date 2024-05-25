# Import connection to primary MongoDB node
from app.database.mongodb_init import mongo1_db, mongo1_client
# Import connection to secondary MongoDB node
from app.database.mongodb_init import mongo2_db, mongo2_client

# Create a transaction for inserting a log entry in the userLogins or userLoggouts collection
def mongo_transaction(*args):
    collection = mongo1_db[args[0]]
    print(collection)
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            collection.insert_one(
                {
                    'action': args[1],
                    'user_id': args[2], 
                    'username': args[3], 
                    'timestamp': args[4]
                }, 
                session=session)
            session.commit_transaction()
            session.end_session()
        except Exception as e:
            print(f'Error while inserting log entry in {collection} collection for user: {args[3]}, Error: {e}')
            session.abort_transaction()
            return False
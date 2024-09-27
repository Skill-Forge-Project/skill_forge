# Import connection to primary MongoDB node
from app.database.mongodb_init import mongo1_db, mongo1_client


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
        

# Create a transaction for inserting a submission in the submissions collection
def mongo_submission_transaction(collection_name, **kwargs):
    collection = mongo1_db[collection_name]
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            collection.insert_one(
                {
                    'user_id': kwargs['user_id'], 
                    'username': kwargs['username'], 
                    'quest_id': kwargs['quest_id'],
                    'submission_id': kwargs['submission_id'],
                    'timestamp': kwargs['timestamp'],
                    'code': kwargs['code'],
                    'result': kwargs['all_results'],
                    'successful_tests': kwargs['successful_tests'],
                    'unsuccessful_tests': kwargs['unsuccessful_tests'],
                    'zero_tests': kwargs['zero_tests'],
                    'zero_tests_outputs': kwargs['zero_tests_outputs'],
                    'message': kwargs['message'],
                }, 
                session=session)
            session.commit_transaction()
            session.end_session()
        except Exception as e:
            print(f'Error while inserting submission in {collection} collection for user: {kwargs["username"]}, Error: {e}')
            session.abort_transaction()
            return False

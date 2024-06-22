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
        
# Create a transaction for inserting a compilation error for Java code runner
def java_compliation_error_transaction(collection_name, **kwargs):
    collection = mongo1_db[collection_name]
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            collection.insert_one(
                {
                    'user_id': kwargs['user_id'], 
                    'username': kwargs['username'], 
                    'quest_id': kwargs['quest_id'],
                    'java_code': kwargs['java_code'],
                    'error': kwargs['stderr_str'],
                    'timestamp': kwargs['timestamp'],
                }, 
                session=session)
            session.commit_transaction()
            session.end_session()
        except Exception as e:
            print(f'Error while inserting compilation error in {collection} collection for user: {kwargs["username"]}, Error: {e}')
            session.abort_transaction()
            return False
        
# Create a transaction for inserting a successful code execution for Java code runner
def java_code_runner_transaction(collection_name, **kwargs):
    collection = mongo1_db[collection_name]
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            collection.insert_one(
                {
                    'user_id': kwargs['user_id'], 
                    'username': kwargs['username'], 
                    'quest_id': kwargs['quest_id'],
                    'java_code': kwargs['java_code'],
                    'inputs': kwargs['inputs'],
                    'outputs': kwargs['outputs'],
                    'message': kwargs['message'],
                    'successful_tests': kwargs['successful_tests'],
                    'unsuccessful_tests': kwargs['unsuccessful_tests'],
                    'zero_tests': kwargs['zero_tests'],
                    'zero_tests_outputs': kwargs['zero_tests_outputs'],
                    'timestamp': kwargs['timestamp'],
                }, 
                session=session)
            session.commit_transaction()
            session.end_session()
        except Exception as e:
            print(f'Error while inserting code runner transaction in {collection} collection for user: {kwargs["username"]}, Error: {e}')
            session.abort_transaction()
            return False
        

# Create a transaction for inserting a compilation error for C# code runner
def csharp_compliation_error_transaction(collection_name, **kwargs):
    collection = mongo1_db[collection_name]
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            collection.insert_one(
                {
                    'user_id': kwargs['user_id'], 
                    'username': kwargs['username'], 
                    'quest_id': kwargs['quest_id'],
                    'java_code': kwargs['csharp_code'],
                    'error': kwargs['stderr_str'],
                    'timestamp': kwargs['timestamp'],
                }, 
                session=session)
            session.commit_transaction()
            session.end_session()
        except Exception as e:
            print(f'Error while inserting compilation error in {collection} collection for user: {kwargs["username"]}, Error: {e}')
            session.abort_transaction()
            return False

# Create a transaction for inserting a successful code execution for Java code runner
def csharp_code_runner_transaction(collection_name, **kwargs):
    collection = mongo1_db[collection_name]
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            collection.insert_one(
                {
                    'user_id': kwargs['user_id'], 
                    'username': kwargs['username'], 
                    'quest_id': kwargs['quest_id'],
                    'csharp_code': kwargs['csharp_code'],
                    'inputs': kwargs['inputs'],
                    'outputs': kwargs['outputs'],
                    'message': kwargs['message'],
                    'successful_tests': kwargs['successful_tests'],
                    'unsuccessful_tests': kwargs['unsuccessful_tests'],
                    'zero_tests': kwargs['zero_tests'],
                    'zero_tests_outputs': kwargs['zero_tests_outputs'],
                    'timestamp': kwargs['timestamp'],
                }, 
                session=session)
            session.commit_transaction()
            session.end_session()
        except Exception as e:
            print(f'Error while inserting code runner transaction in {collection} collection for user: {kwargs["username"]}, Error: {e}')
            session.abort_transaction()
            return False
        
# Create a transaction for inserting a compilation error for JavaScript code runner
def javascript_compliation_error_transaction(collection_name, **kwargs):
    collection = mongo1_db[collection_name]
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            collection.insert_one(
                {
                    'user_id': kwargs['user_id'], 
                    'username': kwargs['username'], 
                    'quest_id': kwargs['quest_id'],
                    'javascript_code': kwargs['javascript_code'],
                    'error': kwargs['stderr_str'],
                    'timestamp': kwargs['timestamp'],
                }, 
                session=session)
            session.commit_transaction()
            session.end_session()
        except Exception as e:
            print(f'Error while inserting compilation error in {collection} collection for user: {kwargs["username"]}, Error: {e}')
            session.abort_transaction()
            return False

# Create a transaction for inserting a successful code execution for JavaScript code runner
def javascript_code_runner_transaction(collection_name, **kwargs):
    collection = mongo1_db[collection_name]
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            collection.insert_one(
                {
                    'user_id': kwargs['user_id'], 
                    'username': kwargs['username'], 
                    'quest_id': kwargs['quest_id'],
                    'javascript_code': kwargs['javascript_code'],
                    'inputs': kwargs['inputs'],
                    'outputs': kwargs['outputs'],
                    'message': kwargs['message'],
                    'successful_tests': kwargs['successful_tests'],
                    'unsuccessful_tests': kwargs['unsuccessful_tests'],
                    'zero_tests': kwargs['zero_tests'],
                    'zero_tests_outputs': kwargs['zero_tests_outputs'],
                    'timestamp': kwargs['timestamp'],
                }, 
                session=session)
            session.commit_transaction()
            session.end_session()
        except Exception as e:
            print(f'Error while inserting code runner transaction in {collection} collection for user: {kwargs["username"]}, Error: {e}')
            session.abort_transaction()
            return False

# Create a transaction for inserting a compilation error for Python code runner
def python_compliation_error_transaction(collection_name, **kwargs):
    collection = mongo1_db[collection_name]
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            collection.insert_one(
                {
                    'user_id': kwargs['user_id'], 
                    'username': kwargs['username'], 
                    'quest_id': kwargs['quest_id'],
                    'python_code': kwargs['python_code'],
                    'error': kwargs['stderr_str'],
                    'timestamp': kwargs['timestamp'],
                }, 
                session=session)
            session.commit_transaction()
            session.end_session()
        except Exception as e:
            print(f'Error while inserting compilation error in {collection} collection for user: {kwargs["username"]}, Error: {e}')
            session.abort_transaction()
            return False
        
# Create a transaction for inserting a successful code execution for Python code runner
def python_code_runner_transaction(collection_name, **kwargs):
    collection = mongo1_db[collection_name]
    session = mongo1_client.start_session()
    with session.start_transaction():
        try:
            collection.insert_one(
                {
                    'user_id': kwargs['user_id'], 
                    'username': kwargs['username'], 
                    'quest_id': kwargs['quest_id'],
                    'python_code': kwargs['python_code'],
                    'inputs': kwargs['inputs'],
                    'outputs': kwargs['outputs'],
                    'message': kwargs['message'],
                    'successful_tests': kwargs['successful_tests'],
                    'unsuccessful_tests': kwargs['unsuccessful_tests'],
                    'zero_tests': kwargs['zero_tests'],
                    'zero_tests_outputs': kwargs['zero_tests_outputs'],
                    'timestamp': kwargs['timestamp'],
                }, 
                session=session)
            session.commit_transaction()
            session.end_session()
        except Exception as e:
            print(f'Error while inserting code runner transaction in {collection} collection for user: {kwargs["username"]}, Error: {e}')
            session.abort_transaction()
            return False
import requests, json, uuid, os, re, subprocess
from flask import jsonify
from dotenv import load_dotenv

# Load the env variables
load_dotenv()

def run_code(code, inputs, outputs, user_id, username, quest_id, language):
    tests_count = len(inputs)
    successful_tests = 0
    unsuccessful_tests = 0
    zero_tests = [] # Hold the first example test input and putput
    zero_tests_outputs = [] # Hold the first example after executing the user code (stdout & stderr)
    execution_id = str(uuid.uuid4())
    # Hold all the results of the tests
    all_results = {}
    
    for i in range(len(inputs)):
        flattened_values = [str(value) for sublist in inputs[i] for value in sublist]
        result = "\n".join(flattened_values)
        print(f"The inputs will be:\n{result}")
            
        data = {
            "language": f"{language}",
            "version": "3.12",
            "files": [
                {
                    "name": f"{language}_{execution_id}_{quest_id}.{language}",
                    "content": code
                }
            ],
            "stdin": result,
            "args": [],
            "compile_timeout": 10000,
            "run_timeout": 3000,
            "compile_memory_limit": -1,
            "run_memory_limit": -1
        }
        
        exec_url = os.getenv('PISTON_API_URL') + '/api/v2/execute'
        response = requests.post(exec_url, json=data)
        
        if response.status_code == 200:
            current_output = response.json()['run']['stdout'].strip()
            current_error = response.json()['run']['stderr'].strip()
            print(f"The output is: {current_output}")
            print(f"The expected output is: {outputs[i][0]}")
            if str(current_output) == str(outputs[i][0]):
                successful_tests += 1
                print("Test passed!")
            else:
                unsuccessful_tests += 1
                print("Test failed!")
            
            if i == 0:
                zero_tests.append(result)
                zero_tests.append(outputs[i][0])
                zero_tests_outputs.append(current_output)
                zero_tests_outputs.append(current_error)
        
        # If Piston API returns an error
        else:
            message = 'Runtime Error! Try again!'
            logs_message = response.json()
            successful_tests = 0
            unsuccessful_tests = len(inputs)
            zero_tests.append("")
            zero_tests.append("")
            zero_tests_outputs.append("")
            zero_tests_outputs.append("")
            return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs
        
        
    if unsuccessful_tests == 0:
        message = 'Congratulations! Your solution is correct!'
    elif successful_tests > 0 and unsuccessful_tests > 0:
        message = 'Your solution is partially correct! Try again!'
    else:
        message = 'Your solution is incorrect! Try again!'
    return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs
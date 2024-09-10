import subprocess, os, re, uuid, shutil
from datetime import datetime
# Import MongoDB transactions functions
from app.database.mongodb_transactions import (java_compliation_error_transaction, 
                                               java_code_runner_transaction)

def run_code(java_code, inputs, outputs, unit_tests, user_id, username, quest_id):
    tests_count = len(inputs)
    successful_tests = 0
    unsuccessful_tests = 0
    zero_tests = [] # Hold the first example test input and putput
    zero_tests_outputs = [] # Hold the first example after executing the user code (stdout & stderr)
    execution_id = str(uuid.uuid4())
    workdir = f"/tmp/{execution_id}"
    # Hold all the results of the tests
    all_results = {}
    os.makedirs(workdir, exist_ok=True)
    
    # Generate a unique dir and file name for the Java code
    java_file_path = os.path.join(workdir, "Main.java")
    
    # Replace the user's solution in the unit tests with the Java code
    submission_code = unit_tests.replace("// Your solution", java_code)
    # Save the Java code to a file
    with open(java_file_path, "w") as java_file:
        java_file.write(submission_code)

    # Compile the Java code using firejail
    compile_command = ['firejail', '--quiet', '--noprofile', '--net=none', '--private', '--private-tmp', f'--whitelist={workdir}',
                        '--timeout=00:00:01', 'javac', java_file_path]        
    compile_process = subprocess.Popen(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = compile_process.communicate()
    stdout_str = stdout.decode('utf-8').strip()
    stderr_str = stderr.decode('utf-8').strip()
    
    # If compilation failed
    if stderr_str:
        stderr_str = re.findall(r"(?<=java:\d:)\s.*", stderr_str)
        zero_tests_outputs.append(stdout_str)
        zero_tests_outputs.append(stderr_str)
        current_input = str(inputs[0])
        correct_output = str(outputs[0])
        zero_tests.append(current_input)
        zero_tests.append(correct_output)
        unsuccessful_tests = tests_count
        message = 'Your solution is incorrect! Try again!'
        # Insert the compilation error transaction into the MongoDB log database
        java_compliation_error_transaction('java_compliation_errors', 
                                        user_id=user_id, 
                                        username=username, 
                                        quest_id=quest_id, 
                                        java_code=submission_code,
                                        stderr_str=stderr_str,
                                        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs

    # If compilation was successful, run and check the code
    else:
        for i in range(tests_count):        
            current_input = ' '.join([str(element) for element in inputs[i]])
            correct_output = str(outputs[i][0])
            
            # Execute the compiled Java code using firejail
            execute_command = [
                'firejail', '--quiet', '--noprofile', '--net=none', '--private', '--private-tmp', f'--whitelist={workdir}',
                '--timeout=00:00:01', 'java', '-cp', workdir, 'Main'] + current_input.split()
            execute_process = subprocess.Popen(execute_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = execute_process.communicate()
            stdout_str = stdout.decode('utf-8').strip()
            stderr_str = stderr.decode('utf-8').strip()
            
            all_results.update({f"Test {i+1}": {"input": current_input, "output": stdout_str, "expected_output": correct_output, "error": stderr_str}})


            # Check if output matches expected output
            if str(stdout_str) == str(correct_output):
                successful_tests += 1
            else:
                unsuccessful_tests += 1

            # Handle the zero test case
            if i == 0:
                zero_tests.append(current_input)
                zero_tests.append(correct_output)
                zero_tests_outputs.append(stdout_str)
                zero_tests_outputs.append(stderr_str)

    # Determine message based on test results
    if unsuccessful_tests == 0:
        message = 'Congratulations! Your solution is correct!'
    elif successful_tests > 0 and unsuccessful_tests > 0:
        message = 'Your solution is partially correct! Try again!'
    else:
        message = 'Your solution is incorrect! Try again!'

    # Cleanup the directory
    shutil.rmtree(workdir)
    # Insert the code runner transaction into the MongoDB log database
    java_code_runner_transaction('java_code_runner', 
                                user_id=user_id, 
                                username=username, 
                                quest_id=quest_id, 
                                java_code=submission_code, 
                                inputs=inputs, 
                                outputs=outputs,
                                message=message, 
                                successful_tests=successful_tests,
                                unsuccessful_tests=unsuccessful_tests,
                                zero_tests=zero_tests, 
                                zero_tests_outputs=zero_tests_outputs,
                                all_results=all_results,
                                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs
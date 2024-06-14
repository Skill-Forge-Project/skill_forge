import subprocess, os, re, uuid, shutil
from datetime import datetime
# Import MongoDB transactions functions
from app.database.mongodb_transactions import (javascript_compliation_error_transaction,
                                               javascript_code_runner_transaction)

def run_code(js_code, inputs, outputs, user_id, username, quest_id):
    tests_count = len(inputs)
    successful_tests = 0
    unsuccessful_tests = 0
    zero_tests = [] # Hold the first example test input and putput
    zero_tests_outputs = [] # Hold the first example after executing the user code (stdout & stderr)
    execution_id = str(uuid.uuid4())
    workdir = f"/tmp/{execution_id}"
    os.makedirs(workdir, exist_ok=True)
    
    # Create new Python file in /tmp directory
    code_filename = f'user_code_{execution_id}.js'
    function_name = re.findall(r"(?<=function ).*(?=\()", js_code)
    
    for i in range(tests_count):
        current_input = [f'"{element}"' if isinstance(element, str) else str(element) for element in inputs[i]]
        current_input = ', '.join(current_input)
        correct_output = str(outputs[i][0])
        

        if current_input.isalpha():
            current_execute = js_code + '\n\n' + f'console.log({function_name[0]}("{current_input}"))'
        else:
            current_execute = js_code + '\n\n' + f'console.log({function_name[0]}({current_input}))'
        
        # Write Python code to file
        with open(os.path.join(workdir, code_filename), 'w') as f:
            f.write(current_execute)
        
        # Execute JavaScript code with Firejail
        execute_command = ['firejail', '--quiet', '--noprofile', '--net=none', '--private', '--private-tmp', f'--whitelist={workdir}',
                           '--timeout=00:00:01', 'node', os.path.join(workdir, code_filename)]
        process = subprocess.Popen(execute_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
            
        
        # Decode output from bytes to string
        stdout_str = stdout.decode('utf-8').replace('\n', '').replace('undefined', '') # handle undefined output as well
        stderr_str = stderr.decode('utf-8')
        
        if stderr_str:
            # Insert the compilation error transaction into the MongoDB log database
            javascript_compliation_error_transaction('javascript_compliation_errors', 
                                                user_id=user_id, 
                                                username=username, 
                                                quest_id=quest_id, 
                                                javascript_code=js_code,
                                                stderr_str=stderr_str,
                                                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs
        
        # Handle the zero test case
        if i == 0:
            zero_tests.append(current_input)
            zero_tests.append(correct_output)
            zero_tests_outputs.append(stdout_str)
            zero_tests_outputs.append(stderr_str)
        
        if correct_output == stdout_str:
            successful_tests += 1
        else:
            unsuccessful_tests += 1
        
        if unsuccessful_tests == 0:
            message = 'Congratulations! Your solution is correct!'
        elif successful_tests > 0 and unsuccessful_tests > 0:
            message = 'Your solution is partially correct! Try again!'
        elif successful_tests == 0 and unsuccessful_tests > 0:
            message = 'Your solution is incorrect! Try again!'
            
    # Cleanup the directory
    shutil.rmtree(workdir)
    # Insert the code runner transaction into the MongoDB log database
    javascript_code_runner_transaction('javascript_code_runner', 
                                    user_id=user_id, 
                                    username=username, 
                                    quest_id=quest_id, 
                                    javascript_code=js_code,
                                    inputs=inputs,
                                    outputs=outputs,
                                    message=message,
                                    successful_tests=successful_tests,
                                    unsuccessful_tests=unsuccessful_tests,
                                    zero_tests=zero_tests,
                                    zero_tests_outputs=zero_tests_outputs,
                                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs
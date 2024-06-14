import subprocess, os, re, uuid, shutil
import subprocess, os, re, uuid, shutil
from datetime import datetime
# Import MongoDB transactions functions
from app.database.mongodb_transactions import (python_compliation_error_transaction,
                                               python_code_runner_transaction)

def run_code(python_code, inputs, outputs, user_id, username, quest_id):
    tests_count = len(inputs)
    successful_tests = 0
    unsuccessful_tests = 0
    zero_tests = [] # Hold the first example test input and putput
    zero_tests_outputs = [] # Hold the first example after executing the user code (stdout & stderr)
    execution_id = str(uuid.uuid4())
    workdir = f"/tmp/{execution_id}"
    os.makedirs(workdir, exist_ok=True)
    
    # Create new Python file in /tmp directory
    code_filename = f'user_code_{execution_id}.py'
    # Get the function name
    function_name = re.findall(r"(?<=def ).*(?=\()", python_code)
    
    for i in range(tests_count):
        current_input = [f'"{element}"' if isinstance(element, str) else str(element) for element in inputs[i]]
        current_input = ', '.join(current_input)
        correct_output = str(outputs[i][0])
        
        # Concatenate the Python code with the function call
        current_execute = python_code + '\n\n' + f'print({function_name[0]}({current_input}))'

        # Write Python code to file
        with open(os.path.join(workdir, code_filename), 'w') as f:
            f.write(current_execute)

        # Execute the Python code
        run_command = ['firejail', '--quiet', '--noprofile', '--net=none', '--private', '--private-tmp', f'--whitelist={workdir}',
                       '--timeout=00:00:01', 'python3', os.path.join(workdir, code_filename)] + current_input.split()
        try:
            run_process = subprocess.run(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout_str = run_process.stdout.decode('utf-8').strip()
            stderr_str = run_process.stderr.decode('utf-8').strip()
            if stderr_str:
                # Insert the compilation error transaction into the MongoDB log database
                python_compliation_error_transaction('python_compliation_errors', 
                                                    user_id=user_id, 
                                                    username=username, 
                                                    quest_id=quest_id, 
                                                    python_code=python_code,
                                                    stderr_str=stderr_str,
                                                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs
        except subprocess.TimeoutExpired:
            stdout_str = ''
            stderr_str = 'Execution timed out.'
        
        if i == 0:
            zero_tests.append(current_input)
            zero_tests.append(correct_output)
            zero_tests_outputs.append(stdout_str)
            zero_tests_outputs.append(stderr_str)

        if stdout_str == correct_output:
            successful_tests += 1
        else:
            unsuccessful_tests += 1

    if unsuccessful_tests == 0:
        message = 'Congratulations! Your solution is correct!'
    elif successful_tests > 0 and unsuccessful_tests > 0:
        message = 'Your solution is partially correct! Try again!'
    else:
        message = 'Your solution is incorrect! Try again!'
    
    # Cleanup the directory
    shutil.rmtree(workdir)
    # Insert the transaction into the MongoDB log database
    python_code_runner_transaction('python_code_runner', 
                                    user_id=user_id, 
                                    username=username, 
                                    quest_id=quest_id, 
                                    python_code=python_code,
                                    inputs=inputs,
                                    outputs=outputs,
                                    message=message,
                                    successful_tests=successful_tests,
                                    unsuccessful_tests=unsuccessful_tests,
                                    zero_tests=zero_tests,
                                    zero_tests_outputs=zero_tests_outputs,
                                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs
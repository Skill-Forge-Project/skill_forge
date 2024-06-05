import subprocess, os, re, uuid

def run_code(python_code, inputs, outputs):
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
                       'python3', os.path.join(workdir, code_filename)] + current_input.split()
        run_process = subprocess.Popen(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = run_process.communicate()
        
        stdout_str = stdout.decode('utf-8').strip()
        stderr_str = stderr.decode('utf-8').strip()
        
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
    
    return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs

# Example Python code
# python_code = """
# print('Hello, world!')
# """

# # Execute Python code
# stdout, stderr = run_code(python_code)
# print("STDOUT:")
# print(stdout)
# print("STDERR:")
# print(stderr)
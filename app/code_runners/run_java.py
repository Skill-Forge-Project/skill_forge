import subprocess, os, re, uuid, shutil

def run_code(java_code, inputs, outputs, user_id, username, quest_id):
    tests_count = len(inputs)
    successful_tests = 0
    unsuccessful_tests = 0
    zero_tests = [] # Hold the first example test input and putput
    zero_tests_outputs = [] # Hold the first example after executing the user code (stdout & stderr)
    execution_id = str(uuid.uuid4())
    workdir = f"/tmp/{execution_id}"
    os.makedirs(workdir, exist_ok=True)
    
    # Generate a unique dir and file name for the Java code
    directory = f"{username}_{user_id}_{quest_id}"
    java_file_path = os.path.join(workdir, "Main.java")
    class_file_path = os.path.join(workdir, "Main.class")
    
    # Save the Java code to a file
    with open(java_file_path, "w") as java_file:
        java_file.write(java_code)

    # Compile the Java code using firejail
    compile_command = [
        'firejail', '--quiet', '--noprofile', '--net=none', '--private', '--private-tmp', f'--whitelist={workdir}',
        '--timeout=00:00:01', 'javac', java_file_path
    ]        
    compile_process = subprocess.Popen(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = compile_process.communicate()
    
    stdout_str = stdout.decode('utf-8').strip()
    stderr_str = stderr.decode('utf-8').strip()
    # If compilation failed
    if stderr_str:
        stderr_str = re.findall(r"(?<=java:\d:)\s.*", stderr_str)
        zero_tests_outputs.append(stdout_str)
        zero_tests_outputs.append(stderr_str)
        zero_tests.append(current_input)
        zero_tests.append(correct_output)
        unsuccessful_tests = tests_count
        message = 'Your solution is incorrect! Try again!'
        return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs

        # If compilation was successful, run and check the code
    else:
        for i in range(tests_count):        
            current_input = [f'"{element}"' if isinstance(element, str) else str(element) for element in inputs[i]]
            current_input = ' '.join(current_input)
            correct_output = str(outputs[i][0])

            # Execute the compiled Java code using firejail
            execute_command = [
                'firejail', '--quiet', '--noprofile', '--net=none', '--private', '--private-tmp', f'--whitelist={workdir}',
                '--rlimit-cpu=60', 'java', '-cp', workdir, 'Main'
            ] + current_input.split()
            execute_process = subprocess.Popen(execute_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = execute_process.communicate()
            stdout_str = stdout.decode('utf-8').strip()
            stderr_str = stderr.decode('utf-8').strip()

            # Check if output matches expected output
            if stdout_str == correct_output:
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
    return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs

# Example Java code
# java_code = """
# public class Main {
#     public static void main(String[] args) {
#         System.out.println("Hello, world!");
#     }
# }
# """


# Use for debuging porposes only
# Execute Java code
# stdout, stderr = run_code(java_code)
# print("STDOUT:")
# print(stdout)
# print("STDERR:")
# print(stderr)
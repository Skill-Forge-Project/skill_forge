import subprocess, os, re, uuid, shutil

def run_code(csharp_code, inputs, outputs, user_id, username, quest_id):
    tests_count = len(inputs)
    successful_tests = 0
    unsuccessful_tests = 0
    zero_tests = [] # Hold the first example test input and putput
    zero_tests_outputs = [] # Hold the first example after executing the user code (stdout & stderr)
    execution_id = str(uuid.uuid4())
    workdir = f"/tmp/{execution_id}"
    os.makedirs(workdir, exist_ok=True)
    
    # Generate a unique dir and file name for the Java code
    csharp_file_path = os.path.join(workdir, "Program.cs")
    executable_file_path = os.path.join(workdir, "Program")

    # Save the Csharp code to a file
    with open(csharp_file_path, "w") as java_file:
        java_file.write(csharp_code)

    # Compile the Csharp code using firejail
    compile_command = [
        'firejail', '--quiet', '--noprofile', '--net=none', '--private', '--private-tmp', f'--whitelist={workdir}',
        '--timeout=00:00:01', 'mono-scs', csharp_code
    ]
    compile_process = subprocess.Popen(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = compile_process.communicate()
    stdout_str = stdout.decode('utf-8').strip()
    stderr_str = stderr.decode('utf-8').strip()
    
    # Save the Java code to a file
    with open(csharp_file_path, "w") as cs_file:
        cs_file.write(csharp_code)

    # Compile & Execute the CS code
    compile_command = ['firejail', '--quiet', '--noprofile', '--net=none', '--private', '--private-tmp', f'--whitelist={workdir}',
                        '--timeout=00:00:01', 'mono-csc', csharp_file_path]
    compile_process = subprocess.Popen(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_str, stderr_str = compile_process.communicate()
    stdout_str = stdout_str.decode('utf-8')
    stderr = stderr_str.decode('utf-8')
    
    # If Compilation failed
    if stderr_str:
        stderr_str = re.findall(r"error CS.*", stderr)
        zero_tests_outputs.append(stdout_str)
        zero_tests_outputs.append(stderr_str)
        current_input = inputs[0]
        correct_output = outputs[0]
        zero_tests.append(current_input)
        zero_tests.append(correct_output)
        unsuccessful_tests = tests_count
        message = 'Your solution is incorrect! Try again!'
        return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs
    
    # If Compilation was successful run and check the code
    else:
        for i in range(tests_count):
            current_input = ' '.join([str(element) for element in inputs[i]])
            correct_output = outputs[i][0]
            # Execute the compiled Java code using firejail
            execute_command = ['firejail', '--quiet', '--noprofile', '--net=none', '--private', '--private-tmp', f'--whitelist={workdir}',
                                '--timeout=00:00:01', 'mono', f'{workdir}/Program.exe'] + current_input.split()
            execute_process = subprocess.Popen(execute_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout_str, stderr_str = execute_process.communicate()
            stdout_str = stdout_str.decode('utf-8').replace('\n', '')
            stderr_str = stderr_str.decode('utf-8').replace('\n', '')
    
            # Check if output matches expected output
            if stdout_str == str(correct_output):
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
    elif successful_tests == 0 and unsuccessful_tests > 0:
        message = 'Your solution is incorrect! Try again!'

    # Cleanup the directory
    shutil.rmtree(workdir)
    return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs
        
# Example C# code
csharp_code = """
using System;
class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello World!");
    }
}
"""

# Use for debuging porposes only
# Execute C# code
# stdout, stderr = run_code(csharp_code)
# print("STDOUT:")
# print(stdout)
# print("STDERR:")
# print(stderr)
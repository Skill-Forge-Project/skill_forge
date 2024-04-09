import subprocess
import os
import re

def run_code(csharp_code, inputs, outputs, user_id, username, quest_id):
    tests_count = len(inputs)
    successful_tests = 0
    unsuccessful_tests = 0
    zero_tests = [] # Hold the first example test input and putput
    zero_tests_outputs = [] # Hold the first example after executing the user code (stdout & stderr)

    # Generate a unique dir and file name for the Java code
    directory = f"{username}_{user_id}_{quest_id}"
    os.makedirs(os.path.join(f"test_runners/cs-files/{directory}"), exist_ok=True)
    os.chdir(os.path.join(f"test_runners/cs-files/{directory}"))
        
    for i in range(tests_count):
        current_input = [f'"{element}"' if isinstance(element, str) else str(element) for element in inputs[i]]
        current_input = ', '.join(current_input)
        correct_output = str(outputs[i][0])
        file_path = os.path.join(os.getcwd(), "Program.cs")
        class_path = os.path.join(os.getcwd(), "Program.exe")
        
        # Save the Java code to a file
        with open(file_path, "w") as cs_file:
            cs_file.write(csharp_code)


        # Compile & Execute the CS code
        compile_process = subprocess.Popen(['mono-csc', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_str, stderr_str = compile_process.communicate()
        stdout_str = stdout_str.decode('utf-8')
        stderr = stderr_str.decode('utf-8')
        
        # If Compilation failed
        if stderr_str:
            stderr_str = re.findall(r"error CS.*", stderr)
            zero_tests_outputs.append(stdout_str)
            zero_tests_outputs.append(stderr_str)
            current_input = ' '.join([str(element) for element in inputs[i]])
            correct_output = outputs[i][0]
            zero_tests.append(current_input)
            zero_tests.append(correct_output)
            zero_tests_outputs.append(stdout_str)
            zero_tests_outputs.append(stderr_str)
            unsuccessful_tests = tests_count
            message = 'Your solution is incorrect! Try again!'
            # Remove the Program.cs file
            os.remove("Program.cs")
            # Remove the directory
            os.chdir("../")
            os.rmdir(directory)
            os.chdir("../")
            return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs
        # If Compilation was successful run and check the code
        else:
            # Execute the CS code
            current_input = ' '.join([str(element) for element in inputs[i]])
            correct_output = outputs[i][0]
            execute_command = ['mono', 'Program.exe'] + current_input.split()
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
        
            # Remove the files
            os.remove("Program.cs")
            os.remove("Program.exe")
            
    # Remove the directory
    os.chdir("../")
    os.rmdir(directory)
    os.chdir("../../")

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
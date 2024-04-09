import subprocess
import os

def run_code(csharp_code, inputs, outputs, user_id, username, quest_id):
    tests_count = len(inputs)
    successful_tests = 0
    unsuccessful_tests = 0
    zero_tests = [] # Hold the first example test input and putput
    zero_tests_outputs = [] # Hold the first example after executing the user code (stdout & stderr)
    
    # Generate a unique dir and file name for the Java code
    directory = f"{username}_{user_id}_{quest_id}"
    os.makedirs(os.path.join("test_runners/cs-files", directory), exist_ok=True)
    os.chdir(os.path.join("test_runners/cs-files", directory))
    for i in range(tests_count):
        file_path = os.path.join(os.getcwd(), "Program.cs")
        class_path = os.path.join(os.getcwd(), "Program.exe")
        
        # Save the CS code to a file
        try:
            with open(file_path, "w") as cs_file:
                cs_file.write(csharp_code)
        except Exception as e:
            print("Error:", e)
            return 0, tests_count, "Error occurred while saving CS code to file."
        
        # Compile the CS code
        try:
            compile_process = subprocess.Popen(['mono-csc', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout_str, stderr_str = compile_process.communicate()
            if stderr_str:
                print("Compilation Error:", stderr_str.decode('utf-8'))
                return 0, tests_count, f"Compilation Error: {stderr_str.decode('utf-8')}"
        except Exception as e:
            print("Error:", e)
            return 0, tests_count, "Error occurred during Java code compilation."
        
        # Execute the CS code
        try:
            current_input = ' '.join([str(element) for element in inputs[i]])
            correct_output = outputs[i][0]
            execute_command = ['mono', 'Program.exe'] + current_input.split()
            execute_process = subprocess.Popen(execute_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout_str, stderr_str = execute_process.communicate()
            if stderr_str:
                print("Execution Error:", stderr_str.decode('utf-8'))
                return 0, tests_count, f"Execution Error: {stderr_str.decode('utf-8')}"
            else:
                # Check if output matches expected output
                if str(stdout_str.decode('utf-8').replace('\n', '')) == str(correct_output):
                    successful_tests += 1
                else:
                    unsuccessful_tests += 1
        except Exception as e:
            print("Error:", e)
            return 0, tests_count, "Error occurred during CS code execution."
        
        # Handle the zero test case
        if i == 0:
            zero_tests.append(current_input)
            zero_tests.append(correct_output)
            zero_tests_outputs.append(stdout_str.decode('utf-8'))
            zero_tests_outputs.append(stderr_str.decode('utf-8'))
            
        # Determine message based on test results
        if unsuccessful_tests == 0:
            message = 'Congratulations! Your solution is correct!'
        elif successful_tests > 0 and unsuccessful_tests > 0:
            message = 'Your solution is partially correct! Try again!'
        elif successful_tests == 0 and unsuccessful_tests > 0:
            message = 'Your solution is incorrect! Try again!'
        
    os.chdir("../../../")

    return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs
        

    # # Compile the C# code
    # compile_process = subprocess.Popen(['mono-csc', 'Program.cs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # compile_stdout, compile_stderr = compile_process.communicate()

    # # Execute the compiled C# program
    # if compile_process.returncode == 0:
    #     execution_process = subprocess.Popen(['mono', 'Program.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     execution_stdout, execution_stderr = execution_process.communicate()
    #     stdout_str = execution_stdout.decode('utf-8')
    #     stderr_str = execution_stderr.decode('utf-8')
    # else:
    #     stdout_str = ""
    #     stderr_str = compile_stderr.decode('utf-8')

    # # Delete the C# file
    # os.remove("Program.cs")
    # os.remove("Program.exe")
    # return stdout_str, stderr_str

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